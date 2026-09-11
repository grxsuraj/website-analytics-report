-- ==============================================================================
-- 04_monthly_trends.sql
-- Business Question: How do traffic volumes and booking conversions evolve over time?
-- Metrics: Monthly Sessions, Conversions, Conversion Rate, Bounce Rate
-- ==============================================================================

SELECT 
    year_month,
    COUNT(session_id) AS total_sessions,
    SUM(CASE WHEN converted = TRUE THEN 1 ELSE 0 END) AS total_conversions,
    ROUND(SUM(CASE WHEN converted = TRUE THEN 1.0 ELSE 0.0 END) / COUNT(session_id) * 100, 2) AS conversion_rate_pct,
    ROUND(AVG(CASE WHEN bounced = TRUE THEN 1.0 ELSE 0.0 END) * 100, 1) AS bounce_rate_pct
FROM website_sessions
GROUP BY year_month
ORDER BY year_month ASC;
