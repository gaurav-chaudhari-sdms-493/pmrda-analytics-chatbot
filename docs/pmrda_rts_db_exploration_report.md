# PMRDA RTS Database (`PMRDA-RTS`) Table & Schema Utility Report

> [!NOTE]
> **Database Host**: `10.9.53.38:5432`  
> **Database Name**: `PMRDA-RTS`  
> **Database Engine**: PostgreSQL 16.15 (Ubuntu 24.04)  
> **Primary Schema**: `public`  
> **Assessment Date**: September 23, 2026  

---

## 1. Executive Summary

A comprehensive structural and volumetric audit was performed on the **PMRDA Right to Services (RTS)** production database (`PMRDA-RTS`). The database contains **253 total table structures** in the `public` schema.

* **185 Useful / Active Tables (73.1%)**: Tables populated with live operational data, historical workflow logs, payment transactions, citizen applications, generated certificates, user access control profiles, system backups, and master configurations. Total record volume across all active tables is **351,469 records**.
* **68 Empty / Unused Tables (26.9%)**: Tables containing **0 records**. These represent unlaunched sub-modules (e.g., Slum Management, PMC Care Gardens, Swachh Survekshan, CFC Counter Scrolls), unconfigured payment features (e.g., i18n localization, recurring subscriptions, refunds), or legacy sequence placeholders.

### Key Metrics Summary

| Metric Category | Count / Value | Percentage |
| :--- | :--- | :--- |
| **Total Database Objects (Tables)** | **253** | 100.0% |
| **Active / Useful Tables (> 0 rows)** | **185** | **73.1%** |
| **Empty Tables (0 rows)** | **68** | **26.9%** |
| **Total Database Records (Across Active Tables)** | **351,469** | — |
| **Database Schemas Detected** | **1 (`public`)** | — |

---

## 2. Table Distribution & Domain Topology

```mermaid
pie title Database Table Utilization (253 Total Tables)
    "Backup & Staging Tables (89)" : 89
    "Migration & Legacy Mapping (22)" : 22
    "Audit, Logs & Notifications (16)" : 16
    "Payment & Fee Engine (15)" : 15
    "User Auth & RBAC (10)" : 10
    "Services & SLA Config (8)" : 8
    "Workflow & Approval Engine (7)" : 7
    "Document Gen & E-Sign (6)" : 6
    "RTS Applications (5)" : 5
    "Master & Geo Data (4)" : 4
    "Form Builder (3)" : 3
    "Empty / Unused Tables (68)" : 68
```

---

## 3. Useful Tables Breakdown (185 Active Tables)

The **185 active tables** are categorized into 11 core functional domains:

### 3.1. RTS Core Applications & Citizen Services (5 Tables | 41,736 Rows)
Holds core application instances submitted by citizens and officer evaluation records.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `rts_citizen_application_files` | **25,096** | 25 | Uploaded citizen document files, attachments, and binary storage references. |
| `rts_application_document_reviews` | **11,715** | 17 | Document review notes, approval statuses, and officer verification remarks. |
| `rts_citizen_applications` | **4,276** | 43 | **Core Entity**: Primary citizen service application records submitted to PMRDA. |
| `rts_application_sla_notification_log` | **606** | 5 | SLA violation and warning notification events for pending applications. |
| `rts_citizen_application_appeals` | **43** | 21 | Citizen appeals lodged against rejected or delayed service applications. |

---

### 3.2. Workflow & Approval Engine (`sdk_aw_*`) (7 Tables | 35,843 Rows)
Powers state machine transitions, officer task queues, and stage approvals.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `sdk_aw_workflow_audit_logs` | **12,472** | 14 | Audit history of state changes, reassignments, and stage completions. |
| `sdk_aw_application_noc_conditions` | **8,014** | 20 | NOC (No Objection Certificate) stipulations attached to workflow decisions. |
| `sdk_aw_workflow_tasks` | **7,855** | 25 | **Core Entity**: Active and completed officer action tasks across all departments. |
| `sdk_aw_workflow_instances` | **4,525** | 26 | Workflow instance execution tracking per application. |
| `sdk_aw_task_comments` | **2,637** | 9 | Detailed comments and note logs added by reviewing officers. |
| `sdk_aw_workflow_stages` | **281** | 22 | Stage definitions for multi-level approval workflows. |
| `sdk_aw_workflow_definitions` | **59** | 16 | Master workflow templates defined per service. |

---

### 3.3. Payment Gateway & Fee Engine (15 Tables | 143,010 Rows)
Handles fee calculation rules, online payment transactions, and budget head allocation.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `sdk_svc_fee_evaluation_log` | **104,192** | 8 | Step-by-step fee computation logs per application evaluation. |
| `rts_legacy_payment_recon` | **19,553** | 13 | Payment reconciliation records imported from the legacy system. |
| `rts_migration_payment_errors` | **9,694** | 13 | Payment reconciliation error tracking from data migration. |
| `sdk_pg_transactions` | **5,327** | 47 | **Core Entity**: Payment gateway transaction master records (MahaOnline/SBI/etc). |
| `sdk_pg_audit_log` | **1,557** | 12 | Gateway request/response audit trail logs. |
| `sdk_pg_transaction_line_items` | **1,303** | 9 | Itemized breakdown of fees per transaction line. |
| `xw_payment_old_to_new` | **1,047** | 10 | Legacy-to-new payment transaction ID mapping. |
| `sdk_pg_budget_codes` | **84** | 9 | Government treasury budget head code definitions. |
| `sdk_svc_fee_rule` | **68** | 18 | Configured fee rules for services. |
| `sdk_svc_fee_rule_formula` | **63** | 3 | Mathematical formula strings for fee logic. |
| `sdk_svc_fee_reference_data` | **54** | 12 | Standard rate lookup tables for area/type calculations. |
| `rts_hoarding_challan_reminder_log` | **48** | 9 | Challan payment reminder notifications log. |
| `sdk_svc_service_fees` | **18** | 24 | Service-level base fee schedules. |
| `sdk_svc_payment_auto_reject_config` | **1** | 7 | System configuration for automatic payment timeouts/rejections. |
| `xw_payment_precedence_policy` | **1** | 8 | Policy config for payment priority resolution. |

---

### 3.4. User Management & Auth (`sdk_rbac_*`) (10 Tables | 41,212 Rows)
Role-Based Access Control (RBAC) governing citizen accounts, departmental officers, and permissions.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `sdk_rbac_audit_logs` | **20,609** | 17 | Access control and authorization audit event log. |
| `sdk_rbac_user_sessions` | **16,675** | 16 | User login session tokens and connection metadata. |
| `sdk_rbac_users` | **2,053** | 43 | **Core Entity**: User accounts (citizens, officers, superadmins). |
| `sdk_rbac_role_permissions` | **1,524** | 6 | Permission-to-role mappings. |
| `sdk_rbac_user_roles` | **174** | 10 | User-to-role assignments. |
| `sdk_rbac_permissions` | **58** | 11 | Master permission keys defined in the system. |
| `sdk_rbac_user_service_allotments` | **46** | 12 | Service-level approval authority allotments per officer. |
| `sdk_rbac_user_profiles` | **38** | 12 | Officer profile metadata and designation details. |
| `sdk_rbac_roles` | **34** | 18 | Master system roles (e.g., Clerk, Town Planner, Collector). |
| `sdk_rbac_tenants` | **1** | 14 | System tenant configuration (PMRDA). |

---

### 3.5. Services & SLA Configuration (`sdk_svc_*`) (8 Tables | 331 Rows)
Defines PMRDA RTS service catalog, turnaround times (SLA), and department mappings.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `sdk_svc_service_workflows` | **85** | 15 | Mapping of services to specific workflow definitions. |
| `sdk_svc_service_documents` | **73** | 20 | Mandatory and optional document requirements per service. |
| `sdk_svc_noc_condition_templates` | **36** | 21 | Standard NOC condition clause templates. |
| `sdk_svc_services` | **36** | 37 | **Core Entity**: Master list of RTS services provided by PMRDA. |
| `sdk_svc_holidays` | **34** | 12 | PMRDA official holiday calendar used for working-day SLA calculation. |
| `sdk_svc_departments` | **28** | 15 | **Core Entity**: PMRDA departments (Town Planning, Building, Fire, etc.). |
| `sdk_svc_department_officers` | **23** | 6 | Mapping officers to primary/secondary departments. |
| `sdk_svc_service_sla` | **16** | 15 | Statutory timeline limits (in days) per service type. |

---

### 3.6. Backup & Staging Tables (`bak_*`) (89 Tables | 14,541 Rows)
Contains snapshot tables created during system maintenance, task date updates, and officer reassignments.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `bak_tasks_pre_perofficer` | **7,200** | 25 | Task snapshot prior to officer reassignment. |
| `bak_dt_provnoc_tasks` | **3,025** | 25 | Backup of provisional NOC workflow tasks. |
| `bak_vivaran_exclude_meta` | **1,165** | 4 | Meta backup table for form exclusions. |
| `bak_dt_finalnoc_tasks` | **943** | 25 | Final NOC task backup snapshot. |
| `bak_dt2_prov_tasks` | **589** | 25 | Provisional task backup snapshot. |
| `bak_all_active_sla_snapshot_20260716` | **403** | 26 | SLA snapshot taken on July 16, 2026. |
| `bak_dt2_finalnoc_tasks` | **292** | 25 | Final NOC task secondary snapshot. |
| `bak_taskdates_ec_tasks` | **145** | 25 | Task dates snapshot for Environmental Clearance. |
| `bak_vivaranfb_provisional_fire_noc_application__new_re` | **114** | 30 | Fire NOC form field backup snapshot. |
| *(Plus 80 additional `bak_*` tables)* | — | — | *System maintenance and operational snapshot tables.* |

---

### 3.7. Document Generation & E-Sign (`sdk_dg_*`, `sdk_esign_*`) (6 Tables | 4,700 Rows)
Automated PDF certificate generation, Jinja templating, and digital signatures.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `sdk_dg_documents` | **2,033** | 28 | **Core Entity**: Generated output certificates, sanction letters, and NOC PDFs. |
| `sdk_esign_audit_log` | **1,085** | 15 | Audit trail of e-sign requests and responses. |
| `sdk_esign_transactions` | **604** | 28 | Active e-sign transaction sessions for approval sign-offs. |
| `sdk_dg_audit_log` | **552** | 8 | Document generator execution logs. |
| `sdk_dg_verification_log` | **382** | 8 | Public QR-code certificate verification access logs. |
| `sdk_dg_templates` | **44** | 22 | Certificate HTML/Jinja design templates. |

---

### 3.8. Dynamic Form Builder (`sdk_fb_*`) (3 Tables | 740 Rows)
Renders dynamic application web forms.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `sdk_fb_form_fields` | **489** | 30 | Field UI components, validation rules, and labels. |
| `sdk_fb_form_versions` | **233** | 12 | Version control history of form schemas. |
| `sdk_fb_forms` | **18** | 20 | Form containers mapped to RTS services. |

---

### 3.9. Master Data & Geographics (4 Tables | 2,815 Rows)
Geographic administrative boundaries and master license references.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `license_master` | **1,400** | 12 | Master catalog of technical person / architect licenses. |
| `sdk_core_villages` | **1,390** | 19 | Villages under PMRDA jurisdiction. |
| `sdk_core_talukas` | **22** | 15 | Talukas under PMRDA. |
| `sdk_core_app_config` | **3** | 5 | Platform system-level dynamic flags. |

---

### 3.10. Migration & Legacy Crosswalk Mappings (22 Tables | 24,826 Rows)
Stores crosswalk translation maps used during legacy data ETL into the current system.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `rts_legacy_workflow_history` | **8,704** | 19 | Historical workflow logs imported from legacy portal. |
| `rts_migration_application_id_map` | **3,666** | 7 | Old application ID to new system UUID mapping. |
| `rts_legacy_application_refs` | **3,631** | 9 | Old application tracking numbers. |
| `xw_citizen_old_to_new` | **2,059** | 7 | Old citizen ID to new user ID crosswalk. |
| `rts_legacy_license_detail` | **1,605** | 9 | Legacy architect/engineer license details. |
| `xw_location_old_to_new` | **1,428** | 8 | Legacy location ID to new village ID mapping. |
| `rts_migration_application_errors` | **1,098** | 11 | Application data migration validation error log. |
| `xw_payload_old_to_new_field` | **624** | 17 | Field-level JSON payload transformation rules. |
| `rts_migration_batch_audit` | **621** | 12 | ETL batch run execution audit logs. |
| `rts_legacy_service_extension_json` | **445** | 2 | Raw JSON legacy extension payloads. |
| `rts_legacy_field_config` | **244** | 8 | Legacy form field mapping configurations. |
| `xw_service_pam_to_service_uuid` | **189** | 7 | Legacy PAM service codes to new service UUID map. |
| `rts_migration_phase_checkpoints` | **146** | 7 | Checkpoint tracking for multi-stage ETL runs. |
| `xw_user_old_to_new` | **107** | 8 | Legacy officer user ID map. |
| `xw_document_old_to_new_field` | **78** | 11 | Legacy document field map. |
| `xw_budget_head_old_to_new` | **73** | 7 | Legacy budget head map. |
| `rts_migration_etl_runs` | **34** | 8 | High-level migration job execution logs. |
| `rts_migration_fk_errors` | **24** | 8 | Foreign key violation audit during data migration. |
| `xw_status_value_map` | **11** | 8 | Legacy status text to new status enum mapping. |
| `xw_flag_value_map` | **4** | 8 | Legacy boolean/flag mappings. |
| `xw_service_pam_to_service_uuid_bak_pam268` | **1** | 7 | Specific service code migration backup map. |
| `xw_payment_precedence_policy` | **1** | 8 | Policy config for payment priority resolution. |

---

### 3.11. Notifications, Support & System Integrations (16 Tables | 41,715 Rows)
System alerting, support tickets, and external integration tokens.

| Table Name | Row Count | Columns | Description & Business Purpose |
| :--- | :---: | :---: | :--- |
| `notif_in_app` | **41,201** | 16 | Citizen & officer web dashboard notifications. |
| `sdk_migrations` | **320** | 3 | Database schema migration version tracking (`flyway`/`alembic`). |
| `_bak_prod_testdel_tasks` | **68** | 25 | Staging test deletion tasks log. |
| `_bak_prod_testdel_apps` | **23** | 43 | Staging test deletion applications log. |
| `notif_template_versions` | **14** | 11 | SMS/Email/In-App notification template version history. |
| `notif_templates` | **14** | 14 | SMS/Email master templates. |
| `rts_integration_service_mappings` | **14** | 7 | External portal API service integration routes. |
| `rts_integration_services` | **14** | 10 | Registered external integration services. |
| `rts_inspection_reports` | **13** | 18 | Site inspection officer reports. |
| `rts_support_ticket_activities` | **12** | 9 | Helpdesk ticket comment/action history. |
| `rts_support_tickets` | **10** | 20 | Citizen helpdesk support tickets. |
| `mst_financial_year` | **4** | 5 | Master financial year reference records (e.g. 2023-24, 2024-25, 2025-26). |
| `rts_integration_temp_tokens` | **4** | 5 | API authentication bearer tokens for external gateways. |
| `rts_integration_users` | **2** | 9 | Service account API credentials for external integrations. |
| `rts_external_reference_map` | **1** | 7 | Map table for third-party reference numbers. |
| `rts_integrations` | **1** | 12 | Master integration endpoint configuration. |

---

## 4. Breakdown of Empty Tables (68 Unused Tables)

The **68 empty tables** (0 records) represent optional, unlaunched, or unpopulated modules:

### 4.1. Unlaunched Sub-Modules
* **Slum Management System (8 Tables)**:  
  `rts_slum_applicant_snapshots`, `rts_slum_banks`, `rts_slum_branches`, `rts_slum_legacy_applicants`, `rts_slum_legacy_transactions`, `rts_slum_payment_instruments`, `rts_slum_payments`, `rts_slum_receipts`.
* **PMC Care & Gardens Module (4 Tables)**:  
  `rts_pmc_care_bookings`, `rts_pmc_care_garden_rates`, `rts_pmc_care_garden_time_slots`, `rts_pmc_care_gardens`.
* **Swachh Survekshan Module (3 Tables)**:  
  `rts_swachh_survekshan_applications`, `rts_swachh_survekshan_officers`, `rts_swachh_survekshan_transactions`.
* **CFC Counter Scroll & Cashier Tokens (4 Tables)**:  
  `rts_cfc_challan_tokens`, `rts_cfc_financial_audit_log`, `rts_cfc_scroll_transactions`, `rts_cfc_scrolls`.

### 4.2. Unused Payment Gateway Features
* **Refunds, Subscriptions & Settlements (4 Tables)**:  
  `sdk_pg_payment_links`, `sdk_pg_refunds`, `sdk_pg_settlements`, `sdk_pg_subscriptions`.
* **Budget Split & Fee Slabs (3 Tables)**:  
  `sdk_pg_service_budget_mapping`, `sdk_pg_service_fee_breakdown`, `sdk_svc_service_budget_split`.

### 4.3. Platform Extensions & Unpopulated Lookups
* **i18n Multi-language Localization (2 Tables)**:  
  `sdk_i18n_locales`, `sdk_i18n_translations`.
* **Workflow Escalations & Attachments (3 Tables)**:  
  `sdk_aw_task_attachments`, `sdk_aw_workflow_escalations`, `xw_escalation_to_aw_stage`.
* **Batch PDF Processing & Fonts (4 Tables)**:  
  `sdk_dg_batch_jobs`, `sdk_dg_categories`, `sdk_dg_fonts`, `sdk_dg_placeholders`.
* **Organization Hierarchy Extensions (2 Tables)**:  
  `sdk_rbac_organizations`, `sdk_rbac_organization_units`.
* **OPD & Specialized Licenses (5 Tables)**:  
  `license_running_sequence`, `license_transactions`, `nursing_license_sequence`, `rts_opd_budget_head_mappings`, `rts_opd_metadata`, `rts_opd_transactions`.

---

## 5. Key Recommendations for Analytics & Chatbot Integration

> [!IMPORTANT]
> **Primary Analytics Core**: When querying application counts, processing times, officer workloads, or revenue performance, queries **MUST** focus exclusively on the **Primary Active Entities** listed below.

```mermaid
graph TD
    A[Citizen Applications<br/>rts_citizen_applications] --> B[Workflow Execution<br/>sdk_aw_workflow_tasks]
    A --> C[Payment Gateway<br/>sdk_pg_transactions]
    A --> D[Services & SLAs<br/>sdk_svc_services / sdk_svc_service_sla]
    B --> E[User & Roles<br/>sdk_rbac_users / sdk_svc_departments]
    C --> F[Fee Evaluations<br/>sdk_svc_fee_evaluation_log]
```

1. **For Application & SLA Analytics**:
   * Join `rts_citizen_applications` (4,276 rows) with `sdk_svc_services` (36 rows), `sdk_svc_departments` (28 rows), and `sdk_svc_service_sla` (16 rows).
2. **For Officer & Departmental Performance**:
   * Query `sdk_aw_workflow_tasks` (7,855 rows) and `sdk_aw_workflow_instances` (4,525 rows) linked to `sdk_rbac_users` (2,053 rows) and `sdk_svc_departments`.
3. **For Revenue & Fee Collection Analytics**:
   * Query `sdk_pg_transactions` (5,327 rows) and `sdk_pg_transaction_line_items` (1,303 rows).
4. **For Certificates & Issued Documents**:
   * Query `sdk_dg_documents` (2,033 rows).
5. **Tables to Exclude**:
   * **Exclude `bak_*` backup tables** (89 snapshot tables) from SQL query routing.
   * Exclude the 68 empty tables (`rts_slum_*`, `rts_pmc_care_*`, `sdk_pg_refunds`, etc.).
