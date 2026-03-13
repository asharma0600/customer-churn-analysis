"""
Customer Churn Analysis — Step 1: EDA & Data Cleaning
Company: StreamLine (fictional B2B SaaS)
Author: Alisha Sharma

This script:
1. Loads the raw messy dataset
2. Performs exploratory data analysis (EDA)
3. Cleans and prepares the data for SQL analysis
4. Saves a clean CSV ready for Power BI / SQL
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ============================================================
# STEP 1 — LOAD DATA
# ============================================================
print("=" * 60)
print("STEP 1: LOADING RAW DATA")
print("=" * 60)

df = pd.read_csv('data/raw_churn_data.csv')
print(f"Raw dataset shape: {df.shape}")
print(f"\nColumn data types:\n{df.dtypes}")

# ============================================================
# STEP 2 — EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# Basic stats
print(f"\nBasic Statistics:")
print(df.describe().round(2))

# Missing values
print(f"\nMissing Values:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
print(missing_df[missing_df['Missing Count'] > 0])

# Duplicates
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# Churn distribution
print(f"\nChurn Distribution:")
print(df['churned'].value_counts())
print(f"Churn Rate: {df['churned'].mean()*100:.1f}%")

# Categorical columns - check for inconsistencies
print(f"\nPlan Type unique values: {df['plan_type'].unique()}")
print(f"Payment Method unique values: {df['payment_method'].unique()}")
print(f"Contract Type unique values: {df['contract_type'].unique()}")

# Outlier check
print(f"\nMonthly Charges - Min: {df['monthly_charges'].min()}, Max: {df['monthly_charges'].max()}")
print(f"Tenure Months - Min: {df['tenure_months'].min()}, Max: {df['tenure_months'].max()}")

# ============================================================
# STEP 3 — DATA CLEANING
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: DATA CLEANING")
print("=" * 60)

df_clean = df.copy()
original_rows = len(df_clean)

# 1. Remove duplicates
df_clean = df_clean.drop_duplicates()
print(f"Removed duplicates: {original_rows - len(df_clean)} rows removed")

# 2. Fix inconsistent casing
df_clean['plan_type'] = df_clean['plan_type'].str.strip().str.title()
df_clean['payment_method'] = df_clean['payment_method'].str.strip().str.title()
df_clean['contract_type'] = df_clean['contract_type'].str.strip().str.title()
df_clean['industry'] = df_clean['industry'].str.strip().str.title()
df_clean['region'] = df_clean['region'].str.strip().str.title()
print(f"Fixed casing inconsistencies in categorical columns")

# 3. Remove outliers in monthly_charges (negative or > 1000)
outlier_mask = (df_clean['monthly_charges'] < 0) | (df_clean['monthly_charges'] > 1000)
df_clean = df_clean[~outlier_mask]
print(f"Removed monthly_charges outliers: {outlier_mask.sum()} rows removed")

# 4. Remove negative tenure
neg_tenure = df_clean['tenure_months'] < 0
df_clean = df_clean[~neg_tenure]
print(f"Removed negative tenure rows: {neg_tenure.sum()} rows removed")

# 5. Fill missing values
df_clean['monthly_charges'] = df_clean['monthly_charges'].fillna(df_clean.groupby('plan_type')['monthly_charges'].transform('median'))
df_clean['tenure_months'] = df_clean['tenure_months'].fillna(df_clean['tenure_months'].median())
df_clean['support_tickets'] = df_clean['support_tickets'].fillna(0)
df_clean['last_login_days'] = df_clean['last_login_days'].fillna(df_clean['last_login_days'].median())
print(f"Filled missing values using median/group imputation")

# 6. Standardize date format
df_clean['signup_date'] = pd.to_datetime(df_clean['signup_date'])
df_clean['signup_year'] = df_clean['signup_date'].dt.year
df_clean['signup_month'] = df_clean['signup_date'].dt.month
print(f"Standardized signup_date format and extracted year/month")

# 7. Add derived columns useful for analysis
df_clean['annual_revenue'] = (df_clean['monthly_charges'] * 12).round(2)
df_clean['revenue_per_user'] = (df_clean['monthly_charges'] / df_clean['num_users']).round(2)
df_clean['high_support'] = (df_clean['support_tickets'] >= 5).astype(int)
df_clean['inactive_user'] = (df_clean['last_login_days'] >= 30).astype(int)
df_clean['churn_risk_segment'] = np.where(
    (df_clean['tenure_months'] < 6) & (df_clean['support_tickets'] >= 3), 'High Risk',
    np.where(df_clean['tenure_months'] < 12, 'Medium Risk', 'Low Risk')
)
print(f"Added derived columns: annual_revenue, revenue_per_user, high_support, inactive_user, churn_risk_segment")

# Final shape
print(f"\nCleaning Summary:")
print(f"Original rows: {original_rows}")
print(f"Clean rows: {len(df_clean)}")
print(f"Rows removed: {original_rows - len(df_clean)}")
print(f"Missing values remaining: {df_clean.isnull().sum().sum()}")

# ============================================================
# STEP 4 — KEY INSIGHTS FROM EDA
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: KEY BUSINESS INSIGHTS")
print("=" * 60)

churn_by_plan = df_clean.groupby('plan_type')['churned'].mean().round(3) * 100
print(f"\nChurn Rate by Plan Type:\n{churn_by_plan}")

churn_by_contract = df_clean.groupby('contract_type')['churned'].mean().round(3) * 100
print(f"\nChurn Rate by Contract Type:\n{churn_by_contract}")

churn_by_region = df_clean.groupby('region')['churned'].mean().round(3) * 100
print(f"\nChurn Rate by Region:\n{churn_by_region}")

avg_tenure_churn = df_clean.groupby('churned')['tenure_months'].mean().round(1)
print(f"\nAverage Tenure (Churned vs Retained):\n{avg_tenure_churn}")

avg_tickets_churn = df_clean.groupby('churned')['support_tickets'].mean().round(1)
print(f"\nAverage Support Tickets (Churned vs Retained):\n{avg_tickets_churn}")

revenue_at_risk = df_clean[df_clean['churned'] == 1]['annual_revenue'].sum()
print(f"\nTotal Annual Revenue Lost to Churn: ${revenue_at_risk:,.0f}")

# ============================================================
# STEP 5 — VISUALIZATIONS
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: GENERATING VISUALIZATIONS")
print("=" * 60)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('StreamLine SaaS — Customer Churn Analysis', fontsize=16, fontweight='bold', y=1.02)
colors = ['#2ecc71', '#e74c3c']

# 1. Churn rate by plan type
ax1 = axes[0, 0]
churn_by_plan.plot(kind='bar', ax=ax1, color=['#3498db', '#e67e22', '#9b59b6'], edgecolor='white')
ax1.set_title('Churn Rate by Plan Type (%)', fontweight='bold')
ax1.set_xlabel('')
ax1.set_ylabel('Churn Rate (%)')
ax1.tick_params(axis='x', rotation=0)

# 2. Churn rate by contract type
ax2 = axes[0, 1]
churn_by_contract.plot(kind='bar', ax=ax2, color=['#1abc9c', '#e74c3c', '#3498db'], edgecolor='white')
ax2.set_title('Churn Rate by Contract Type (%)', fontweight='bold')
ax2.set_xlabel('')
ax2.set_ylabel('Churn Rate (%)')
ax2.tick_params(axis='x', rotation=15)

# 3. Tenure distribution
ax3 = axes[0, 2]
churned = df_clean[df_clean['churned'] == 1]['tenure_months']
retained = df_clean[df_clean['churned'] == 0]['tenure_months']
ax3.hist(retained, bins=20, alpha=0.6, color='#2ecc71', label='Retained')
ax3.hist(churned, bins=20, alpha=0.6, color='#e74c3c', label='Churned')
ax3.set_title('Tenure Distribution: Churned vs Retained', fontweight='bold')
ax3.set_xlabel('Tenure (Months)')
ax3.set_ylabel('Count')
ax3.legend()

# 4. Support tickets vs churn
ax4 = axes[1, 0]
avg_tickets = df_clean.groupby('churned')['support_tickets'].mean()
bars = ax4.bar(['Retained', 'Churned'], avg_tickets.values, color=['#2ecc71', '#e74c3c'], edgecolor='white')
ax4.set_title('Avg Support Tickets: Churned vs Retained', fontweight='bold')
ax4.set_ylabel('Avg Support Tickets')
for bar, val in zip(bars, avg_tickets.values):
    ax4.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05, f'{val:.1f}', ha='center', fontweight='bold')

# 5. Churn by risk segment
ax5 = axes[1, 1]
risk_churn = df_clean.groupby('churn_risk_segment')['churned'].mean() * 100
risk_churn.plot(kind='bar', ax=ax5, color=['#e74c3c', '#3498db', '#2ecc71'], edgecolor='white')
ax5.set_title('Churn Rate by Risk Segment (%)', fontweight='bold')
ax5.set_xlabel('')
ax5.set_ylabel('Churn Rate (%)')
ax5.tick_params(axis='x', rotation=0)

# 6. Monthly charges distribution
ax6 = axes[1, 2]
df_clean.boxplot(column='monthly_charges', by='plan_type', ax=ax6,
                 boxprops=dict(color='#2c3e50'),
                 medianprops=dict(color='#e74c3c', linewidth=2))
ax6.set_title('Monthly Charges by Plan Type', fontweight='bold')
ax6.set_xlabel('Plan Type')
ax6.set_ylabel('Monthly Charges ($)')
plt.suptitle('')

plt.tight_layout()
plt.savefig('outputs/churn_analysis_charts.png', dpi=150, bbox_inches='tight')
print("Saved visualizations to outputs/churn_analysis_charts.png")

# ============================================================
# STEP 6 — SAVE CLEAN DATA
# ============================================================
df_clean.to_csv('data/clean_churn_data.csv', index=False)
print(f"\nClean data saved to data/clean_churn_data.csv")
print(f"Final dataset: {len(df_clean)} rows, {df_clean.shape[1]} columns")
print("\n✅ EDA & Cleaning complete! Ready for SQL analysis.")
