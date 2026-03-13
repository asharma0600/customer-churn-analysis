# 📉 Customer Churn Analysis — StreamLine SaaS

**Full-stack data analytics project:** Raw data → Python cleaning → SQL transformation → Power BI executive dashboard

---

## 1. Executive Summary

**Business Problem:** StreamLine, a B2B SaaS company, is losing 14.3% of its customers annually — costing $172,874 in lost annual revenue. Leadership needs to understand *why* customers churn and *which* customers are at highest risk.

**Solution:** Built an end-to-end analytics pipeline that cleans raw operational data, transforms it using SQL, and surfaces actionable churn insights through an executive Power BI dashboard.

**Impact:**
- Identified Basic plan customers as the highest-risk segment (24.8% churn rate — 3x the Enterprise rate)
- Found that customers with 5+ support tickets churn at 3x the rate of low-ticket customers
- Flagged $172,874 in annual revenue lost to churn with a clear recovery roadmap
- Isolated top 10 highest-revenue customers at imminent churn risk for immediate intervention

**Next Steps:** Implement 90-day onboarding program, proactive outreach at support ticket threshold, and annual contract incentive for month-to-month customers.

---

## 2. Business Problem

StreamLine's leadership has identified customer retention as a critical growth lever. Despite strong acquisition numbers, churn is eroding revenue and increasing CAC payback period. Key questions to answer:

- Which customer segments are churning at the highest rate?
- What behavioral signals predict churn before it happens?
- How much revenue is at risk and which customers need immediate intervention?
- What actions can reduce churn by 20% within 6 months?

---

## 3. Methodology

```
Raw Messy CSV (2,030 records)
        │
        ▼
🐍 Python — EDA & Data Cleaning
   • Removed 29 duplicate rows
   • Fixed inconsistent casing (BASIC → Basic)
   • Removed outliers (monthly charges of $9,999, negative tenure)
   • Imputed missing values using median/group imputation
   • Engineered 7 new features (annual_revenue, churn_risk_segment, etc.)
        │
        ▼
🗄️ SQL — Transformation & Aggregation
   • 11 analytical queries covering churn by segment, revenue impact,
     tenure cohorts, support buckets, and at-risk customer identification
        │
        ▼
📊 Power BI — Executive Dashboard
   • 4-page interactive dashboard with slicers for Plan, Region, Industry
   • KPI cards, bar charts, scatter plots, and recommendation page
        │
        ▼
💡 Business Recommendations
```

---

## 4. Skills Demonstrated

**Data Cleaning & EDA (Python)**
- Duplicate detection and removal
- Outlier identification using IQR and domain logic
- Missing value imputation (median, group median)
- Data type standardization and feature engineering
- Visualization with Matplotlib

**Data Transformation (SQL)**
- CTEs and aggregations
- CASE WHEN segmentation
- Window-style cohort analysis
- Multi-table KPI summary queries
- Revenue impact calculations

**Data Visualization (Power BI)**
- DAX measures for KPIs
- Interactive slicers and cross-filtering
- Executive dashboard design
- Business recommendation storytelling

---

## 5. Key Results & Business Insights

| Finding | Insight | Recommended Action |
|---|---|---|
| Basic plan churn: **24.8%** | 3x higher than Enterprise | Proactive outreach + upgrade incentive |
| 5+ support tickets → **3x churn** | Poor experience = exit signal | CS check-in after 3rd ticket |
| 0-6 month tenure: highest churn | Onboarding failure | 90-day onboarding program |
| Month-to-month: **15.2% churn** | No commitment = no retention | Annual contract incentive at month 3 |
| **$172,874** annual revenue lost | Preventable with early intervention | Target top 10 at-risk accounts |

---

## 6. Next Steps

**If given more time / data:**
- Build a predictive churn model (logistic regression) to score each customer
- Integrate with CRM data to automate at-risk alerts for the CS team
- A/B test the recommended interventions and measure lift
- Expand dataset to include product usage metrics (feature adoption, login frequency by feature)

**Data Limitations:**
- Dataset is synthetic — real-world data would include product usage logs, support ticket content, and billing history
- NPS scores are self-reported and may have response bias

---

## 7. Project Structure

```
customer-churn-analysis/
├── data/
│   ├── generate_data.py          # Generates realistic messy dataset
│   ├── raw_churn_data.csv        # Raw messy input data (2,030 rows)
│   └── clean_churn_data.csv      # Cleaned output ready for SQL/Power BI
├── notebooks/
│   └── 01_eda_cleaning.py        # Full EDA + cleaning pipeline
├── sql/
│   └── churn_analysis.sql        # 11 analytical SQL queries
├── outputs/
│   └── churn_analysis_charts.png # EDA visualizations
├── powerbi_guide.md              # Step-by-step Power BI dashboard guide
└── README.md
```

---

## 8. Tech Stack

| Tool | Purpose |
|---|---|
| Python (Pandas, NumPy, Matplotlib) | EDA, data cleaning, feature engineering |
| SQL (SQLite compatible) | Data transformation & aggregation |
| Power BI Desktop | Executive dashboard & visualization |

---

## 9. How to Run

```bash
# 1. Generate the raw dataset
python data/generate_data.py

# 2. Run EDA and cleaning
python notebooks/01_eda_cleaning.py

# 3. Run SQL queries
# Import clean_churn_data.csv into DB Browser for SQLite or any SQL client
# Run queries from sql/churn_analysis.sql

# 4. Build Power BI dashboard
# Follow instructions in powerbi_guide.md
```

---

*Built by Alisha Sharma | MS Marketing Analytics, Illinois Institute of Technology*
