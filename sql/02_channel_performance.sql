-- ==============================================================================
-- 02_channel_performance.sql
-- Business Question: Which traffic acquisition channels generate the most volume vs highest conversions?
-- Metrics: Volume, Conversions, Conversion Rate, Bounce Rate by Channel
-- ==============================================================================

SELECT 
    traffic_source,
    COUNT(session_id) AS total_sessions,
    SUM(CASE WHEN converted = TRUE THEN 1 ELSE 0 END) AS total_conversions,
    ROUND(SUM(CASE WHEN converted = TRUE THEN 1.0 ELSE 0.0 END) / COUNT(session_id) * 100, 2) AS conversion_rate_pct,
    ROUND(AVG(CASE WHEN bounced = TRUE THEN 1.0 ELSE 0.0 END) * 100, 1) AS bounce_rate_pct
FROM website_sessions
GROUP BY traffic_source
ORDER BY total_sessions DESC;
