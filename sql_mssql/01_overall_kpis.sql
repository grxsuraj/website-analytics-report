-- Overall website KPIs across the analysis period.
SELECT
    COUNT(session_id) AS total_sessions,
    SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) AS total_conversions,
    ROUND(
        SUM(CASE WHEN converted = 1 THEN 1.0 ELSE 0.0 END)
        / NULLIF(COUNT(session_id), 0) * 100,
        2
    ) AS conversion_rate_pct,
    ROUND(
        AVG(CASE WHEN bounced = 1 THEN 1.0 ELSE 0.0 END) * 100,
        1
    ) AS bounce_rate_pct,
    ROUND(AVG(session_duration_s) / 60.0, 1) AS avg_duration_minutes
FROM dbo.website_sessions;
