"""
Single file database logger for pmrda_metadata_db.
Encapsulates all database operations for storing chat sessions, messages,
SQL query logs, phase timings, developer info, and unmatched scope queries using distinct columns.
"""

import os
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import psycopg2
import psycopg2.extras

logger = logging.getLogger("pmrda_chatbot.metadata_logger")


class PmrdaMetadataLogger:
    """Standalone database manager for pmrda_metadata_db with dedicated columns for Developer Info & Phase Timing metrics."""

    def __init__(self, connection_string: Optional[str] = None):
        raw_url = (
            connection_string
            or os.getenv("METADATA_DATABASE_URL")
            or "postgresql://postgres:postgres_password@localhost:5433/pmrda_metadata_db"
        )
        self.connection_string = raw_url.replace("postgresql+asyncpg://", "postgresql://", 1)
        self._ensure_database_exists()
        self._ensure_tables_exist()

    def _ensure_database_exists(self):
        try:
            conn = psycopg2.connect(self.connection_string)
            conn.close()
        except psycopg2.OperationalError as e:
            if "does not exist" in str(e):
                try:
                    from urllib.parse import urlparse
                    parsed = urlparse(self.connection_string)
                    dbname = parsed.path.lstrip('/')
                    user_pass = f"{parsed.username}:{parsed.password}@" if parsed.username else ""
                    port = f":{parsed.port}" if parsed.port else ""
                    default_dsn = f"postgresql://{user_pass}{parsed.hostname}{port}/postgres"
                    conn = psycopg2.connect(default_dsn)
                    conn.autocommit = True
                    with conn.cursor() as cur:
                        cur.execute(f'CREATE DATABASE "{dbname}";')
                    conn.close()
                    logger.info(f"Successfully created metadata database: {dbname}")
                except Exception as ex:
                    logger.warning(f"Auto-creating metadata database failed: {ex}")

    def _ensure_tables_exist(self):
        try:
            conn = psycopg2.connect(self.connection_string)
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS chat_sessions (
                        id VARCHAR(255) PRIMARY KEY,
                        title TEXT,
                        mode VARCHAR(50) DEFAULT 'agent',
                        user_id TEXT,
                        user_email TEXT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS chat_messages (
                        id SERIAL PRIMARY KEY,
                        session_id VARCHAR(255) NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
                        request_id TEXT,
                        sender VARCHAR(50) NOT NULL,
                        content TEXT,
                        sql_used TEXT,
                        execution_time_ms DOUBLE PRECISION,
                        total_records BIGINT,
                        llm_model TEXT,
                        nitro_routing BOOLEAN DEFAULT FALSE,
                        prompt_tokens INT,
                        completion_tokens INT,
                        total_tokens INT,
                        estimated_cost_usd DOUBLE PRECISION,
                        total_latency_ms DOUBLE PRECISION,
                        phase1_rag_ms DOUBLE PRECISION,
                        phase2_schema_prompt_ms DOUBLE PRECISION,
                        phase3_llm_reasoning_ms DOUBLE PRECISION,
                        phase4_sql_execution_ms DOUBLE PRECISION,
                        phase5_ui_overhead_ms DOUBLE PRECISION,
                        llm_and_framework_ms DOUBLE PRECISION,
                        status VARCHAR(50) DEFAULT 'SUCCESS',
                        error_message TEXT,
                        output_file TEXT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS query_execution_log (
                        id SERIAL PRIMARY KEY,
                        session_id VARCHAR(255),
                        query_text TEXT NOT NULL,
                        template_id TEXT,
                        template_version INT,
                        bound_parameters TEXT,
                        result_row_count BIGINT,
                        execution_time_ms DOUBLE PRECISION,
                        status VARCHAR(50) DEFAULT 'SUCCESS',
                        error_message TEXT,
                        executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS unmatched_scope_queries (
                        id SERIAL PRIMARY KEY,
                        query_text TEXT NOT NULL,
                        reason TEXT,
                        candidate_template_ids TEXT,
                        session_id VARCHAR(255),
                        logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );

                    ALTER TABLE chat_sessions ADD COLUMN IF NOT EXISTS user_id TEXT;
                    ALTER TABLE chat_sessions ADD COLUMN IF NOT EXISTS user_email TEXT;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS request_id TEXT;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS total_records BIGINT;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS llm_model TEXT;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS nitro_routing BOOLEAN DEFAULT FALSE;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS prompt_tokens INT;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS completion_tokens INT;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS total_tokens INT;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS estimated_cost_usd DOUBLE PRECISION;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS total_latency_ms DOUBLE PRECISION;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS phase1_rag_ms DOUBLE PRECISION;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS phase2_schema_prompt_ms DOUBLE PRECISION;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS phase3_llm_reasoning_ms DOUBLE PRECISION;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS phase4_sql_execution_ms DOUBLE PRECISION;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS phase5_ui_overhead_ms DOUBLE PRECISION;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS llm_and_framework_ms DOUBLE PRECISION;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'SUCCESS';
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS error_message TEXT;
                    ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS output_file TEXT;
                """)
                conn.commit()
            conn.close()
            logger.info("Successfully ensured metadata database tables exist.")
        except Exception as e:
            logger.warning(f"Ensuring metadata database tables failed: {e}")

    def _get_connection(self):
        return psycopg2.connect(self.connection_string)

    def ensure_chat_session(
        self,
        session_id: str,
        title: Optional[str] = None,
        mode: str = "agent",
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
    ) -> str:
        """Create or update a chat session in chat_sessions table."""
        if not session_id:
            return ""
        now = datetime.utcnow()
        session_title = (title[:50] if title else "New Chat Session").strip()
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO chat_sessions (id, title, mode, user_id, user_email, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET 
                        updated_at = %s, 
                        title = COALESCE(EXCLUDED.title, chat_sessions.title),
                        user_id = COALESCE(EXCLUDED.user_id, chat_sessions.user_id),
                        user_email = COALESCE(EXCLUDED.user_email, chat_sessions.user_email);
                    """,
                    (session_id, session_title, mode, user_id, user_email, now, now, now),
                )
                conn.commit()
                return session_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Error ensuring chat session {session_id}: {e}")
            return session_id
        finally:
            conn.close()

    def log_user_message(
        self,
        session_id: str,
        content: str,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
    ) -> Optional[int]:
        """Save a user question prompt to chat_messages table."""
        if not session_id or not content:
            return None
        self.ensure_chat_session(session_id, title=content[:50], user_id=user_id, user_email=user_email)
        now = datetime.utcnow()
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO chat_messages (session_id, sender, content, created_at)
                    VALUES (%s, 'user', %s, %s) RETURNING id;
                    """,
                    (session_id, content, now),
                )
                msg_id = cur.fetchone()[0]
                conn.commit()
                return msg_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Error logging user message for session {session_id}: {e}")
            return None
        finally:
            conn.close()

    def log_agent_message(
        self,
        session_id: str,
        content: str,
        request_id: Optional[str] = None,
        sql_used: Optional[str] = None,
        execution_time_ms: Optional[float] = None,
        total_records: Optional[int] = None,
        llm_model: Optional[str] = None,
        nitro_routing: bool = False,
        prompt_tokens: Optional[int] = None,
        completion_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        estimated_cost_usd: Optional[float] = None,
        total_latency_ms: Optional[float] = None,
        phase1_rag_ms: Optional[float] = None,
        phase2_schema_prompt_ms: Optional[float] = None,
        phase3_llm_reasoning_ms: Optional[float] = None,
        phase4_sql_execution_ms: Optional[float] = None,
        phase5_ui_overhead_ms: Optional[float] = None,
        llm_and_framework_ms: Optional[float] = None,
        status: str = "SUCCESS",
        error_message: Optional[str] = None,
        output_file: Optional[str] = None,
    ) -> Optional[int]:
        """Save an agent/LLM response directly into dedicated scalar columns in chat_messages table."""
        if not session_id:
            return None
        self.ensure_chat_session(session_id)
        now = datetime.utcnow()
        
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO chat_messages (
                        session_id, request_id, sender, content, sql_used, execution_time_ms, total_records,
                        llm_model, nitro_routing, prompt_tokens, completion_tokens, total_tokens, estimated_cost_usd,
                        total_latency_ms, phase1_rag_ms, phase2_schema_prompt_ms, phase3_llm_reasoning_ms, 
                        phase4_sql_execution_ms, phase5_ui_overhead_ms, llm_and_framework_ms, status, error_message, output_file, created_at
                    )
                    VALUES (%s, %s, 'agent', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    RETURNING id;
                    """,
                    (
                        session_id, request_id, content, sql_used, execution_time_ms, total_records,
                        llm_model, nitro_routing, prompt_tokens, completion_tokens, total_tokens, estimated_cost_usd,
                        total_latency_ms, phase1_rag_ms, phase2_schema_prompt_ms, phase3_llm_reasoning_ms,
                        phase4_sql_execution_ms, phase5_ui_overhead_ms, llm_and_framework_ms, status, error_message, output_file, now,
                    ),
                )
                msg_id = cur.fetchone()[0]
                
                # Update session timestamp
                cur.execute("UPDATE chat_sessions SET updated_at = %s WHERE id = %s;", (now, session_id))
                conn.commit()
                return msg_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Error logging agent message for session {session_id}: {e}")
            return None
        finally:
            conn.close()

    def log_query_execution(
        self,
        query_text: str,
        session_id: Optional[str] = None,
        status: str = "SUCCESS",
        execution_time_ms: Optional[float] = None,
        result_row_count: Optional[int] = None,
        error_message: Optional[str] = None,
        template_id: Optional[str] = None,
        template_version: Optional[int] = None,
        bound_parameters: Optional[Dict[str, Any]] = None,
    ) -> Optional[int]:
        """Log SQL query execution details into query_execution_log table."""
        if not query_text:
            return None
        now = datetime.utcnow()
        bound_json = json.dumps(bound_parameters) if bound_parameters else None
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO query_execution_log (
                        session_id, query_text, template_id, template_version, bound_parameters, 
                        result_row_count, execution_time_ms, status, error_message, executed_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
                    """,
                    (session_id, query_text, template_id, template_version, bound_json, result_row_count, execution_time_ms, status, error_message, now),
                )
                log_id = cur.fetchone()[0]
                conn.commit()
                return log_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Error logging query execution: {e}")
            return None
        finally:
            conn.close()

    def log_unmatched_query(
        self,
        query_text: str,
        reason: str = "OFF_TOPIC",
        session_id: Optional[str] = None,
        candidate_template_ids: Optional[List[str]] = None,
    ) -> Optional[int]:
        """Log rejected or unmatched queries into unmatched_scope_queries table."""
        if not query_text:
            return None
        now = datetime.utcnow()
        candidates_json = json.dumps(candidate_template_ids) if candidate_template_ids else None
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO unmatched_scope_queries (query_text, reason, candidate_template_ids, session_id, logged_at)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                    """,
                    (query_text, reason, candidates_json, session_id, now),
                )
                unmatched_id = cur.fetchone()[0]
                conn.commit()
                return unmatched_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Error logging unmatched query: {e}")
            return None
        finally:
            conn.close()

    def fetch_chat_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Fetch all messages for a session from chat_messages table."""
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, session_id, request_id, sender, content, sql_used, execution_time_ms, total_records,
                           llm_model, nitro_routing, prompt_tokens, completion_tokens, total_tokens, estimated_cost_usd,
                           total_latency_ms, phase1_rag_ms, phase2_schema_prompt_ms, phase3_llm_reasoning_ms, 
                           phase4_sql_execution_ms, phase5_ui_overhead_ms, llm_and_framework_ms, status, error_message, output_file, created_at
                    FROM chat_messages
                    WHERE session_id = %s
                    ORDER BY created_at ASC, id ASC;
                    """,
                    (session_id,),
                )
                return [dict(r) for r in cur.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching history for {session_id}: {e}")
            return []
        finally:
            conn.close()

    def fetch_developer_info(self, session_id: str) -> List[Dict[str, Any]]:
        """Fetch Developer Info & Phase Timing metrics for a given session using distinct columns."""
        history = self.fetch_chat_history(session_id)
        dev_info = []
        for msg in history:
            if msg["sender"] == "agent":
                dev_info.append({
                    "message_id": msg["id"],
                    "session_id": msg["session_id"],
                    "request_id": msg["request_id"],
                    "created_at": msg["created_at"],
                    "llm_model": msg.get("llm_model"),
                    "nitro_routing": msg.get("nitro_routing"),
                    "sql_used": msg.get("sql_used"),
                    "execution_time_ms": msg.get("execution_time_ms"),
                    "total_records": msg.get("total_records"),
                    "tokens": {
                        "prompt_tokens": msg.get("prompt_tokens"),
                        "completion_tokens": msg.get("completion_tokens"),
                        "total_tokens": msg.get("total_tokens"),
                    },
                    "estimated_cost_usd": msg.get("estimated_cost_usd"),
                    "phase_timing": {
                        "total_latency_ms": msg.get("total_latency_ms"),
                        "phase1_rag_ms": msg.get("phase1_rag_ms"),
                        "phase2_schema_prompt_ms": msg.get("phase2_schema_prompt_ms"),
                        "phase3_llm_reasoning_ms": msg.get("phase3_llm_reasoning_ms"),
                        "phase4_sql_execution_ms": msg.get("phase4_sql_execution_ms"),
                        "phase5_ui_overhead_ms": msg.get("phase5_ui_overhead_ms"),
                        "llm_and_framework_ms": msg.get("llm_and_framework_ms"),
                    },
                    "status": msg.get("status"),
                    "error_message": msg.get("error_message"),
                    "output_file": msg.get("output_file"),
                })
        return dev_info


# Backwards compatibility alias
PmcMetadataLogger = PmrdaMetadataLogger

# Singleton Global Metadata Logger Instance
_global_logger: Optional[PmrdaMetadataLogger] = None

def get_metadata_logger() -> PmrdaMetadataLogger:
    global _global_logger
    if _global_logger is None:
        _global_logger = PmrdaMetadataLogger()
    return _global_logger

