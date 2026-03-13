-- ============================================================
-- Customer Churn Analysis — SQL Transformation & Analysis
-- Company: StreamLine (fictional B2B SaaS)
-- Author: Alisha Sharma
-- Database: SQLite / PostgreSQL compatible
-- ============================================================

-- ============================================================
-- STEP 1: CREATE THE MAIN TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS customer_churn (
    customer_id         TEXT PRIMARY KEY,
    signup_date         DATE,
    signup_year         INTEGER,
    signup_month        INTEGER,
    plan_type           TEXT,
    contract_type       TEXT,
    tenure_months       REAL,
    monthly_charges     REAL,
    annual_revenue      REAL,
    revenue_per_user    REAL,
    num_users           INTEGER,
    support_tickets     REAL,
    last_login_days     REAL,
    nps_score           INTEGER,
    payment_method      TEXT,
    industry            TEXT,
    region              TEXT,
    high_support        INTEGER,
    inactive_user       INTEGER,
    churn_risk_segment  TEXT,
    churned             INTEGER
);

-- ============================================================
-- STEP 2: OVERALL CHURN SUMMARY
-- ============================================================

-- Overall churn rate and revenue impact
SELECT
    COUNT(*)                                            AS total_customers,
    SUM(churned)                                        AS churned_customers,
    COUNT(*) - SUM(churned)                             AS retained_customers,
    ROUND(AVG(churned) * 100, 1)                       AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churned = 1 THEN annual_revenue ELSE 0 END), 0) AS revenue_lost,
    ROUND(SUM(annual_revenue), 0)                       AS total_revenue,
    ROUND(SUM(CASE WHEN churned = 1 THEN annual_revenue ELSE 0 END) 
          / SUM(annual_revenue) * 100, 1)               AS revenue_churn_pct
FROM customer_churn;

-- ============================================================
-- STEP 3: CHURN BY PLAN TYPE
-- ============================================================

SELECT
    plan_type,
    COUNT(*)                                            AS total_customers,
    SUM(churned)                                        AS churned,
    ROUND(AVG(churned) * 100, 1)                       AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2)                     AS avg_monthly_charges,
    ROUND(SUM(CASE WHEN churned = 1 THEN annual_revenue ELSE 0 END), 0) AS revenue_lost
FROM customer_churn
GROUP BY plan_type
ORDER BY churn_rate_pct DESC;

-- ============================================================
-- STEP 4: CHURN BY CONTRACT TYPE
-- ============================================================

SELECT
    contract_type,
    COUNT(*)                                            AS total_customers,
    SUM(churned)                                        AS churned,
    ROUND(AVG(churned) * 100, 1)                       AS churn_rate_pct,
    ROUND(AVG(tenure_months), 1)                       AS avg_tenure_months
FROM customer_churn
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;

-- ============================================================
-- STEP 5: CHURN BY SUPPORT TICKET VOLUME
-- ============================================================

SELECT
    CASE
        WHEN support_tickets = 0 THEN '0 Tickets'
        WHEN support_tickets BETWEEN 1 AND 2 THEN '1-2 Tickets'
        WHEN support_tickets BETWEEN 3 AND 5 THEN '3-5 Tickets'
        ELSE '6+ Tickets'
    END                                                 AS support_bucket,
    COUNT(*)                                            AS total_customers,
    SUM(churned)                                        AS churned,
    ROUND(AVG(churned) * 100, 1)                       AS churn_rate_pct
FROM customer_churn
GROUP BY support_bucket
ORDER BY churn_rate_pct DESC;

-- ============================================================
-- STEP 6: CHURN BY TENURE COHORT
-- ============================================================

SELECT
    CASE
        WHEN tenure_months <= 3  THEN '0-3 Months'
        WHEN tenure_months <= 6  THEN '4-6 Months'
        WHEN tenure_months <= 12 THEN '7-12 Months'
        WHEN tenure_months <= 24 THEN '13-24 Months'
        ELSE '24+ Months'
    END                                                 AS tenure_cohort,
    COUNT(*)                                            AS total_customers,
    SUM(churned)                                        AS churned,
    ROUND(AVG(churned) * 100, 1)                       AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2)                     AS avg_monthly_charges
FROM customer_churn
GROUP BY tenure_cohort
ORDER BY churn_rate_pct DESC;

-- ============================================================
-- STEP 7: REVENUE AT RISK BY SEGMENT
-- ============================================================

SELECT
    churn_risk_segment,
    COUNT(*)                                            AS total_customers,
    SUM(churned)                                        AS already_churned,
    ROUND(AVG(churned) * 100, 1)                       AS churn_rate_pct,
    ROUND(SUM(annual_revenue), 0)                       AS segment_revenue,
    ROUND(SUM(CASE WHEN churned = 0 THEN annual_revenue ELSE 0 END), 0) AS revenue_at_risk
FROM customer_churn
GROUP BY churn_risk_segment
ORDER BY churn_rate_pct DESC;

-- ============================================================
-- STEP 8: TOP 10 CUSTOMERS BY REVENUE AT RISK
-- (High risk segment, not yet churned, highest revenue)
-- ============================================================

SELECT
    customer_id,
    plan_type,
    contract_type,
    ROUND(tenure_months, 0)                             AS tenure_months,
    ROUND(monthly_charges, 2)                          AS monthly_charges,
    ROUND(annual_revenue, 2)                           AS annual_revenue,
    support_tickets,
    last_login_days,
    nps_score,
    churn_risk_segment
FROM customer_churn
WHERE churned = 0
  AND churn_risk_segment = 'High Risk'
ORDER BY annual_revenue DESC
LIMIT 10;

-- ============================================================
-- STEP 9: MONTHLY CHURN TREND
-- ============================================================

SELECT
    signup_year,
    signup_month,
    COUNT(*)                                            AS total_customers,
    SUM(churned)                                        AS churned,
    ROUND(AVG(churned) * 100, 1)                       AS churn_rate_pct
FROM customer_churn
GROUP BY signup_year, signup_month
ORDER BY signup_year, signup_month;

-- ============================================================
-- STEP 10: INDUSTRY ANALYSIS
-- ============================================================

SELECT
    industry,
    COUNT(*)                                            AS total_customers,
    SUM(churned)                                        AS churned,
    ROUND(AVG(churned) * 100, 1)                       AS churn_rate_pct,
    ROUND(AVG(nps_score), 1)                           AS avg_nps_score,
    ROUND(AVG(monthly_charges), 2)                     AS avg_monthly_charges
FROM customer_churn
GROUP BY industry
ORDER BY churn_rate_pct DESC;

-- ============================================================
-- STEP 11: FINAL KPI SUMMARY TABLE (for Power BI)
-- ============================================================

SELECT
    'Total Customers'       AS metric, CAST(COUNT(*) AS TEXT)                          AS value FROM customer_churn
UNION ALL SELECT
    'Churn Rate'            AS metric, CAST(ROUND(AVG(churned)*100,1) AS TEXT) || '%'  AS value FROM customer_churn
UNION ALL SELECT
    'Revenue Lost'          AS metric, '$' || CAST(ROUND(SUM(CASE WHEN churned=1 THEN annual_revenue ELSE 0 END),0) AS TEXT) AS value FROM customer_churn
UNION ALL SELECT
    'Avg Tenure (Churned)'  AS metric, CAST(ROUND(AVG(CASE WHEN churned=1 THEN tenure_months END),1) AS TEXT) || ' months' AS value FROM customer_churn
UNION ALL SELECT
    'Avg Support Tickets (Churned)' AS metric, CAST(ROUND(AVG(CASE WHEN churned=1 THEN support_tickets END),1) AS TEXT) AS value FROM customer_churn
UNION ALL SELECT
    'High Risk Customers'   AS metric, CAST(COUNT(*) AS TEXT) AS value FROM customer_churn WHERE churn_risk_segment = 'High Risk' AND churned = 0;
