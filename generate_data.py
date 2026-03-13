import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)
N = 2000

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

customer_ids = [f'CUST-{str(i).zfill(5)}' for i in range(1, N+1)]
plan_types = np.random.choice(['Basic', 'Professional', 'Enterprise'], N, p=[0.4, 0.4, 0.2])
tenure = np.random.exponential(scale=24, size=N).clip(1, 72).astype(int)
monthly_charges = np.where(
    plan_types == 'Basic', np.random.normal(29, 5, N),
    np.where(plan_types == 'Professional', np.random.normal(79, 10, N),
             np.random.normal(199, 25, N))
).clip(10, 500).round(2)

churn_prob = (
    0.05 +
    0.15 * (plan_types == 'Basic') +
    0.10 * (tenure < 6) +
    0.12 * (np.random.randint(0, 10, N) > 7) +
    -0.08 * (plan_types == 'Enterprise')
).clip(0, 1)
churned = np.random.random(N) < churn_prob

start_date = datetime(2021, 1, 1)
end_date = datetime(2023, 12, 31)
signup_dates = [random_date(start_date, end_date).strftime('%Y-%m-%d') for _ in range(N)]
support_tickets = np.random.poisson(lam=np.where(churned, 4, 1.5), size=N)
last_login_days = np.where(churned, np.random.randint(30, 180, N), np.random.randint(1, 30, N))
num_users = np.random.randint(1, 50, N)
payment_method = np.random.choice(['Credit Card', 'Bank Transfer', 'PayPal', 'Invoice'], N, p=[0.5, 0.25, 0.15, 0.1])
contract_type = np.random.choice(['Month-to-Month', 'Annual', 'Two-Year'], N, p=[0.5, 0.35, 0.15])
industry = np.random.choice(['Technology', 'Healthcare', 'Retail', 'Finance', 'Education', 'Other'], N)
nps_score = np.where(churned, np.random.randint(0, 6, N), np.random.randint(5, 11, N))
region = np.random.choice(['North America', 'Europe', 'Asia Pacific', 'Latin America'], N, p=[0.5, 0.25, 0.15, 0.1])

df = pd.DataFrame({
    'customer_id': customer_ids,
    'signup_date': signup_dates,
    'plan_type': plan_types,
    'contract_type': contract_type,
    'tenure_months': tenure,
    'monthly_charges': monthly_charges,
    'num_users': num_users,
    'support_tickets': support_tickets,
    'last_login_days': last_login_days,
    'nps_score': nps_score,
    'payment_method': payment_method,
    'industry': industry,
    'region': region,
    'churned': churned.astype(int)
})

# Introduce mess
df_messy = df.copy()
for col in ['monthly_charges', 'tenure_months', 'support_tickets', 'last_login_days']:
    mask = np.random.random(len(df_messy)) < 0.04
    df_messy.loc[mask, col] = np.nan

idx1 = np.random.choice(len(df_messy), 80, replace=False)
df_messy.iloc[idx1, df_messy.columns.get_loc('plan_type')] = df_messy.iloc[idx1]['plan_type'].str.upper().values
idx2 = np.random.choice(len(df_messy), 60, replace=False)
df_messy.iloc[idx2, df_messy.columns.get_loc('payment_method')] = df_messy.iloc[idx2]['payment_method'].str.lower().values

dupes = df_messy.sample(30)
df_messy = pd.concat([df_messy, dupes], ignore_index=True)

idx4 = np.random.choice(len(df_messy), 10, replace=False)
df_messy.iloc[idx4, df_messy.columns.get_loc('monthly_charges')] = np.random.choice([9999, -50, 0], 10)
idx5 = np.random.choice(len(df_messy), 5, replace=False)
df_messy.iloc[idx5, df_messy.columns.get_loc('tenure_months')] = -1

df_messy = df_messy.sample(frac=1).reset_index(drop=True)
df_messy.to_csv('raw_churn_data.csv', index=False)
print(f"Generated {len(df_messy)} rows")
print(f"Missing values: {df_messy.isnull().sum().sum()}")
print(f"Duplicates: {df_messy.duplicated().sum()}")
print(f"Churn rate: {(df['churned'].mean()*100):.1f}%")
