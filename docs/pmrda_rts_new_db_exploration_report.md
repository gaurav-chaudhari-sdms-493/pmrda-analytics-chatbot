# PMRDA RTS New Database (`PMRDA-RTS`) Table & Schema Utility Report

> [!NOTE]
> **Database Host**: `10.9.53.38:5432`  
> **Database Name**: `PMRDA-RTS`  
> **Database Engine**: PostgreSQL 16.15 (Ubuntu 24.04)  
> **Primary Schema**: `public`  
> **Assessment Date**: September 23, 2026  
> **Comparison Reference**: [pmrdarts18_05_db_exploration_report.md](file:///home/stark/PycharmProjects/pmrda-analytics-chatbot/docs/pmrdarts18_05_db_exploration_report.md)

---

## 1. Executive Summary

A comprehensive structural and volumetric audit was performed on the new **PMRDA Right to Services (RTS)** production database (`PMRDA-RTS` on host `10.9.53.38`). 

Compared to the older `pmrdarts18_05` database (which had 159 tables), the new `PMRDA-RTS` database contains **253 total table structures** in the `public` schema.

* **185 Active / Useful Tables (73.1%)**: Tables populated with live operational data, workflow audits, payment transactions, citizen applications, generated documents, and system backups. Total record volume across all active tables reached **351,469 records** (+145% increase vs. old DB).
* **68 Empty / Unused Tables (26.9%)**: Exactly 68 tables contain **0 records**. These represent unlaunched sub-modules (Slum Management, PMC Care Gardens, Swachh Survekshan, CFC Counter Scrolls) and unconfigured payment features (refunds, subscriptions, settlements).

### Key Metrics & Comparison Summary

| Metric Category | Old DB (`pmrdarts18_05`) | New DB (`PMRDA-RTS`) | Change / Variance |
| :--- | :---: | :---: | :--- |
| **PostgreSQL Engine Version** | PostgreSQL 14.24 | **PostgreSQL 16.15** | Upgraded to PG16 |
| **Total Database Objects (Tables)** | **159** | **253** | **+94 tables** |
| **Active / Useful Tables (> 0 rows)** | **91 (57.2%)** | **185 (73.1%)** | **+94 active tables** |
| **Backup / Staging Tables (`bak_*`)** | 0 | **89** | +89 snapshot tables |
| **Empty / Unused Tables (0 rows)** | **68 (42.8%)** | **68 (26.9%)** | Unchanged (0 delta) |
| **Total Database Records** | **~143,450** | **351,469** | **+208,019 records (+145%)** |

---

## 2. Table Distribution & Topology

```mermaid
pie title New Database Table Breakdown (253 Total Tables)
    "Backup & Staging Tables (89)" : 89
    "Migration & Legacy Mapping (22)" : 22
    "Audit, Logs & Notifications (16)" : 16
    "Payment Gateway & Fee Engine (15)" : 15
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

## 3. Comparative Growth: Top Growing Entities (New vs. Old DB)

The table below highlights the key active entities in the new database and their data growth relative to `pmrdarts18_05`:

| Table Name | Old DB Rows | New DB Rows | Growth (Delta) | Key Functional Impact |
| :--- | :---: | :---: | :---: | :--- |
| `sdk_svc_fee_evaluation_log` | 27,450 | **104,192** | **+76,742** | Significant expansion in service fee evaluation logs. |
| `notif_in_app` | 18,016 | **41,201** | **+23,185** | High volume of citizen & officer dashboard notifications. |
| `sdk_rbac_audit_logs` | 4,392 | **20,609** | **+16,217** | Enhanced security auditing & permission check logs. |
| `sdk_rbac_user_sessions` | 3,723 | **16,675** | **+12,952** | Increased active user login & web session history. |
| `sdk_aw_workflow_audit_logs` | 3,667 | **12,472** | **+8,805** | Detailed tracking of approval workflow step transitions. |
| `sdk_aw_application_noc_conditions` | 52 | **8,014** | **+7,962** | NOC conditions attached to active technical applications. |
| `rts_legacy_payment_recon` | 14,329 | **19,553** | **+5,224** | Additional imported legacy payment reconciliations. |
| `rts_citizen_application_files` | 20,130 | **25,096** | **+4,966** | Uploaded applicant documents & blueprints. |
| `sdk_aw_task_comments` | 722 | **2,637** | **+1,915** | Officer review notes & approval remarks. |
| `sdk_dg_documents` | 159 | **2,033** | **+1,874** | **Certificates & NOC Documents Generated**. |
| `rts_citizen_applications` | 3,699 | **4,276** | **+577** | Total citizen RTS applications submitted. |
| `sdk_pg_transactions` | 4,628 | **5,327** | **+699** | Online fee payment gateway transactions. |
| `sdk_rbac_users` | 1,565 | **2,053** | **+488** | Registered users (citizens & PMRDA officers). |

---

## 4. Useful Tables Breakdown (185 Active Tables)

The active tables are grouped into **11 functional categories**:

### 4.1. RTS Core Applications & Citizen Services (5 Tables | 41,736 Rows)
* `rts_citizen_application_files` — **25,096 rows** (25 cols): Uploaded attachments & blueprints.
* `rts_application_document_reviews` — **11,715 rows** (17 cols): Officer document review remarks & verification states.
* `rts_citizen_applications` — **4,276 rows** (43 cols): **Primary Entity**: Active citizen service applications.
* `rts_application_sla_notification_log` — **606 rows** (5 cols): SLA breach & warning alerts.
* `rts_citizen_application_appeals` — **43 rows** (21 cols): Formal citizen appeals lodged against application decisions.

### 4.2. Workflow & Approval Engine (`sdk_aw_*`) (7 Tables | 35,843 Rows)
* `sdk_aw_workflow_audit_logs` — **12,472 rows** (14 cols): System audit trail of stage transitions.
* `sdk_aw_application_noc_conditions` — **8,014 rows** (20 cols): Specific NOC stipulations attached to applications.
* `sdk_aw_workflow_tasks` — **7,855 rows** (25 cols): **Primary Entity**: Officer action tasks across all departments.
* `sdk_aw_workflow_instances` — **4,525 rows** (26 cols): Active workflow instance runs.
* `sdk_aw_task_comments` — **2,637 rows** (9 cols): Officer review notes.
* `sdk_aw_workflow_stages` — **281 rows** (22 cols): Workflow approval stage definitions.
* `sdk_aw_workflow_definitions` — **59 rows** (16 cols): Service workflow master templates.

### 4.3. Payment Gateway & Fee Engine (15 Tables | 143,010 Rows)
* `sdk_svc_fee_evaluation_log` — **104,192 rows** (8 cols): Mathematical fee evaluation execution logs.
* `rts_legacy_payment_recon` — **19,553 rows** (13 cols): Legacy portal payment reconciliations.
* `rts_migration_payment_errors` — **9,694 rows** (13 cols): Payment ETL migration audit errors.
* `sdk_pg_transactions` — **5,327 rows** (47 cols): **Primary Entity**: Online payment gateway transactions.
* `sdk_pg_audit_log` — **1,557 rows** (12 cols): Gateway communication logs.
* `sdk_pg_transaction_line_items` — **1,303 rows** (9 cols): Itemized fee line items.
* `xw_payment_old_to_new` — **1,047 rows** (10 cols): Payment ID crosswalk mapping.
* `sdk_pg_budget_codes` — **84 rows** (9 cols): Treasury budget head account codes.
* `sdk_svc_fee_rule` & `sdk_svc_fee_rule_formula` — **68 & 63 rows**: Dynamic fee logic and math formulas.
* `sdk_svc_fee_reference_data` — **54 rows** (12 cols): Base rate schedules per zone/type.

### 4.4. User Management & Auth (`sdk_rbac_*`) (10 Tables | 41,212 Rows)
* `sdk_rbac_audit_logs` — **20,609 rows** (17 cols): RBAC security event logs.
* `sdk_rbac_user_sessions` — **16,675 rows** (16 cols): Active user web login sessions.
* `sdk_rbac_users` — **2,053 rows** (43 cols): **Primary Entity**: Officer & citizen user accounts.
* `sdk_rbac_role_permissions` — **1,524 rows** (6 cols): Role permission mapping matrix.
* `sdk_rbac_user_roles` — **174 rows** (10 cols): User role grants.
* `sdk_rbac_permissions` & `sdk_rbac_roles` — **58 & 34 rows**: Access permission keys & master roles.
* `sdk_rbac_user_service_allotments` — **46 rows** (12 cols): Service authorization allotments per officer.
* `sdk_rbac_user_profiles` — **38 rows** (12 cols): Officer designations & profiles.

### 4.5. Services & SLA Configuration (`sdk_svc_*`) (8 Tables | 331 Rows)
* `sdk_svc_service_workflows` — **85 rows**: Service to workflow linkages.
* `sdk_svc_service_documents` — **73 rows**: Document requirement checklists.
* `sdk_svc_noc_condition_templates` — **36 rows**: Standard NOC clause templates.
* `sdk_svc_services` — **36 rows**: Master RTS services catalog.
* `sdk_svc_holidays` — **34 rows**: Official holiday calendar for working-day SLA calculation.
* `sdk_svc_departments` — **28 rows**: PMRDA departments.
* `sdk_svc_department_officers` — **23 rows**: Department officer mappings.
* `sdk_svc_service_sla` — **16 rows**: Turnaround SLA targets (days).

### 4.6. Backup & Staging Tables (`bak_*`) (89 Tables | 14,541 Rows)
The new database contains 89 backup and staging snapshot tables created during system maintenance and task date corrections:
* `bak_tasks_pre_perofficer` — **7,200 rows**: Task snapshot prior to officer reassignment.
* `bak_dt_provnoc_tasks` — **3,025 rows**: Backup of provisional NOC workflow tasks.
* `bak_vivaran_exclude_meta` — **1,165 rows**: Meta backup table.
* `bak_dt_finalnoc_tasks` — **943 rows**: Final NOC task backups.
* `bak_dt2_prov_tasks` — **589 rows**: Provisional task backups.
* `bak_all_active_sla_snapshot_20260716` — **403 rows**: SLA snapshot dated July 16, 2026.
* *(Plus 83 additional `bak_*` tables holding maintenance snapshots).*

### 4.7. Document Generation & E-Sign (6 Tables | 4,700 Rows)
* `sdk_dg_documents` — **2,033 rows** (28 cols): **Generated Certificates, Sanction Letters & NOC PDFs**.
* `sdk_esign_audit_log` & `sdk_esign_transactions` — **1,085 & 604 rows**: Digital signature operations.
* `sdk_dg_audit_log` — **552 rows**: Document rendering engine logs.
* `sdk_dg_verification_log` — **382 rows**: Public QR-code verification checks.
* `sdk_dg_templates` — **44 rows**: Certificate HTML/Jinja design templates.

### 4.8. Form Builder (3 Tables | 740 Rows)
* `sdk_fb_form_fields` — **489 rows**: Form dynamic field definitions.
* `sdk_fb_form_versions` — **233 rows**: Version history of dynamic forms.
* `sdk_fb_forms` — **18 rows**: Active dynamic web forms.

### 4.9. Migration & Legacy Mapping (22 Tables | 24,826 Rows)
* `rts_legacy_workflow_history` — **8,704 rows**: Historical legacy workflow logs.
* `rts_migration_application_id_map` & `rts_legacy_application_refs` — **3,666 & 3,631 rows**: Old-to-new application ID maps.
* `xw_citizen_old_to_new` & `xw_location_old_to_new` — **2,059 & 1,428 rows**: Citizen and village crosswalks.
* `rts_legacy_license_detail` — **1,605 rows**: Legacy architect license records.
* `rts_migration_application_errors` — **1,098 rows**: Data migration error logs.

---

## 5. Breakdown of Empty Tables (68 Unused Tables)

The **68 empty tables** (0 records) remain identical between both databases:

1. **Slum Management System (8 Tables)**: `rts_slum_applicant_snapshots`, `rts_slum_banks`, `rts_slum_branches`, `rts_slum_legacy_applicants`, `rts_slum_legacy_transactions`, `rts_slum_payment_instruments`, `rts_slum_payments`, `rts_slum_receipts`.
2. **PMC Care & Gardens Module (4 Tables)**: `rts_pmc_care_bookings`, `rts_pmc_care_garden_rates`, `rts_pmc_care_garden_time_slots`, `rts_pmc_care_gardens`.
3. **Swachh Survekshan Module (3 Tables)**: `rts_swachh_survekshan_applications`, `rts_swachh_survekshan_officers`, `rts_swachh_survekshan_transactions`.
4. **CFC Scrolls & Cashier Tokens (4 Tables)**: `rts_cfc_challan_tokens`, `rts_cfc_financial_audit_log`, `rts_cfc_scroll_transactions`, `rts_cfc_scrolls`.
5. **Payment Refunds & Subscriptions (4 Tables)**: `sdk_pg_payment_links`, `sdk_pg_refunds`, `sdk_pg_settlements`, `sdk_pg_subscriptions`.
6. **i18n Localization (2 Tables)**: `sdk_i18n_locales`, `sdk_i18n_translations`.

---

## 6. Recommendations for Updating Chatbot / Analytics Integration

> [!IMPORTANT]
> **Database Connection Update**: To point the chatbot or analytics service to the new `PMRDA-RTS` database, update your `.env` file as follows:
> ```env
> DATABASE_URL=postgresql+asyncpg://postgres:root@10.9.53.38:5432/PMRDA-RTS
> ```

1. **Filtering Out Backup Tables (`bak_*`)**:
   * SQL queries generated by the chatbot **MUST** filter out tables starting with `bak_` or `_bak_` to prevent querying stale snapshot data.
2. **Primary Analytics Entities**:
   * Application queries: Join `rts_citizen_applications` (4,276 rows) with `sdk_svc_services` (36 rows) and `sdk_svc_departments` (28 rows).
   * Task / SLA performance: Query `sdk_aw_workflow_tasks` (7,855 rows) and `sdk_aw_workflow_instances` (4,525 rows).
   * Certificate / Document output: Query `sdk_dg_documents` (2,033 generated documents).
