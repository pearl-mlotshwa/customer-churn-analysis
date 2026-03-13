-- ============================================================
-- Customer Churn Risk Modelling - SQL Analysis
-- Author: Phumelele Pearl Mlotshwa
-- Tools: SQLite | Python | Power BI
-- ============================================================

-- ── 1. OVERVIEW: Churn rate by contract type ──────────────────
SELECT
    contract_type,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(100.0 * SUM(churned) / COUNT(*), 1) AS churn_rate_pct,
    ROUND(AVG(monthly_spend), 2) AS avg_monthly_spend
FROM customers
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;

-- ── 2. RISK SCORING: Rule-based churn risk framework ─────────
SELECT
    customer_id,
    tenure_months,
    contract_type,
    monthly_spend,
    num_support_calls,
    payment_delays,
    churned,
    CASE
        WHEN contract_type = 'Month-to-Month' AND tenure_months < 12
             AND num_support_calls > 5 THEN 'Critical'
        WHEN contract_type = 'Month-to-Month' AND payment_delays > 2 THEN 'High'
        WHEN num_support_calls > 5 OR payment_delays > 2 THEN 'Medium'
        ELSE 'Low'
    END AS risk_tier,
    ROUND(monthly_spend * tenure_months, 2) AS lifetime_value
FROM customers
ORDER BY risk_tier, monthly_spend DESC;

-- ── 3. REVENUE AT RISK: By risk tier ─────────────────────────
WITH risk_scored AS (
    SELECT *,
        CASE
            WHEN contract_type = 'Month-to-Month' AND tenure_months < 12
                 AND num_support_calls > 5 THEN 'Critical'
            WHEN contract_type = 'Month-to-Month' AND payment_delays > 2 THEN 'High'
            WHEN num_support_calls > 5 OR payment_delays > 2 THEN 'Medium'
            ELSE 'Low'
        END AS risk_tier
    FROM customers
)
SELECT
    risk_tier,
    COUNT(*) AS customers,
    SUM(churned) AS actual_churned,
    ROUND(SUM(monthly_spend), 2) AS monthly_revenue_at_risk,
    ROUND(AVG(monthly_spend), 2) AS avg_spend
FROM risk_scored
GROUP BY risk_tier
ORDER BY CASE risk_tier WHEN 'Critical' THEN 1 WHEN 'High' THEN 2
                         WHEN 'Medium' THEN 3 ELSE 4 END;

-- ── 4. SEGMENTATION: Tenure bands ─────────────────────────────
SELECT
    CASE
        WHEN tenure_months < 6  THEN '0-6 months'
        WHEN tenure_months < 12 THEN '6-12 months'
        WHEN tenure_months < 24 THEN '1-2 years'
        ELSE '2+ years'
    END AS tenure_band,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(churned) / COUNT(*), 1) AS churn_rate_pct,
    ROUND(AVG(monthly_spend), 2) AS avg_spend
FROM customers
GROUP BY tenure_band
ORDER BY churn_rate_pct DESC;

-- ── 5. REGIONAL ANALYSIS ──────────────────────────────────────
SELECT
    region,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned,
    ROUND(100.0 * SUM(churned) / COUNT(*), 1) AS churn_rate_pct,
    ROUND(SUM(monthly_spend), 2) AS total_monthly_revenue,
    RANK() OVER (ORDER BY SUM(churned) DESC) AS churn_rank
FROM customers
GROUP BY region
ORDER BY churn_rate_pct DESC;
