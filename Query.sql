SELECT LOWER(a.status) AS status, COUNT(DISTINCT a.id) AS shown_on_admin
FROM public.rts_citizen_applications a
JOIN public.sdk_aw_workflow_instances i
ON i.entity_id = a.id::text
AND i.entity_type = 'SERVICE_APPLICATION'
AND i.deleted_at IS NULL
JOIN public.sdk_aw_workflow_tasks t
ON t.instance_id = i.id
AND t.deleted_at IS NULL
WHERE a.deleted_at IS NULL
AND LOWER(COALESCE(a.status, '')) NOT IN ('draft', 'started', 'in_progress', 'deleted')
AND (
t.status NOT IN ('PENDING', 'IN_PROGRESS')
OR t.stage_id = i.current_stage_id
)
AND (
i.metadata->>'activePaymentStageId' IS NULL
OR UPPER(COALESCE(i.payment_status, '')) IN ('COMPLETED', 'SKIPPED')
OR t.stage_id::text = i.metadata->>'activePaymentStageId'
OR t.status IN ('COMPLETED', 'SKIPPED', 'EXPIRED')
)
GROUP BY 1
ORDER BY 2 DESC;