#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Trap signals to cleanly terminate both processes on Ctrl+C / SIGTERM
cleanup() {
    echo ""
    echo "Stopping all Vanna services..."
    kill $(jobs -p) 2>/dev/null || true
}
trap cleanup INT TERM

# 1. Determine Python binary
if [ -f "$SCRIPT_DIR/venv/bin/python" ]; then
    PYTHON_BIN="$SCRIPT_DIR/venv/bin/python"
else
    PYTHON_BIN="python3"
fi

# Get local network IP address
LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP="127.0.0.1"
fi

echo "=================================================="
echo "⚡ Starting Vanna Agent Stack (Backend & Frontend)"
echo "=================================================="

# 0. Close existing running services on ports 8001 & 5174 (for this project only)
echo "Closing existing running services if any..."
if command -v fuser >/dev/null 2>&1; then
    fuser -k 8001/tcp 2>/dev/null || true
    fuser -k 5174/tcp 2>/dev/null || true
fi
if command -v lsof >/dev/null 2>&1; then
    PIDS=$(lsof -t -i:8001 -i:5174 2>/dev/null || true)
    if [ -n "$PIDS" ]; then
        kill -9 $PIDS 2>/dev/null || true
    fi
fi
pkill -f "$SCRIPT_DIR/main.py" 2>/dev/null || true
pkill -f "$SCRIPT_DIR/frontends/webcomponent" 2>/dev/null || true
sleep 1

# 2. Start FastAPI Backend (Port 8001)
echo "[1/2] Starting FastAPI Backend on http://0.0.0.0:8001..."
PORT=${PORT:-8001} "$PYTHON_BIN" main.py &
BACKEND_PID=$!

# Wait briefly for backend initialization
sleep 2

# 3. Start Web Components Frontend (Port 5174)
if [ -d "$SCRIPT_DIR/frontends/webcomponent" ]; then
    echo "[2/2] Starting Vite Frontend on http://0.0.0.0:5174..."
    cd "$SCRIPT_DIR/frontends/webcomponent"
    npm run dev -- --host --port 5174 &
    FRONTEND_PID=$!
fi

echo "=================================================="
echo "✅ Services Started!"
echo "👉 Local Access:      http://localhost:5174/"
echo "👉 Phone/Network IP:  http://${LOCAL_IP}:5174/"
echo "👉 FastAPI Backend:   http://${LOCAL_IP}:8001"
echo "Press Ctrl+C to stop all services."
echo "=================================================="

# Wait for background jobs
wait
