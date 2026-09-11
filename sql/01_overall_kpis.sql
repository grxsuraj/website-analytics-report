-- ==============================================================================
-- 01_overall_kpis.sql
-- Business Question: What are the overall website KPIs across the 24-month period?
-- Metrics: Total Sessions, Total Conversions, Conversion Rate, Bounce Rate, Avg Duration
-- ==============================================================================

SELECT 
    COUNT(session_id) AS total_sessions,
    SUM(CASE WHEN converted = TRUE THEN 1 ELSE 0 END) AS total_conversions,
    ROUND(SUM(CASE WHEN converted = TRUE THEN 1.0 ELSE 0.0 END) / COUNT(session_id) * 100, 2) AS conversion_rate_pct,
    ROUND(AVG(CASE WHEN bounced = TRUE THEN 1.0 ELSE 0.0 END) * 100, 1) AS bounce_rate_pct,
    ROUND(AVG(session_duration_s) / 60.0, 1) AS avg_duration_minutes
FROM website_sessions;
