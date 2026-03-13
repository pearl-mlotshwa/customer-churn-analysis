import pandas as pd
import numpy as np
import sqlite3
import os

np.random.seed(42)
n = 1000

df = pd.DataFrame({
    'customer_id': [f'CUST{str(i).zfill(4)}' for i in range(1, n+1)],
    'tenure_months': np.random.randint(1, 72, n),
    'contract_type': np.random.choice(['Month-to-Month', '1-Year', '2-Year'], n, p=[0.5, 0.3, 0.2]),
    'monthly_spend': np.round(np.random.uniform(20, 200, n), 2),
    'num_support_calls': np.random.randint(0, 15, n),
    'payment_delays': np.random.randint(0, 6, n),
    'product_count': np.random.randint(1, 6, n),
    'region': np.random.choice(['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Mpumalanga', 'Limpopo'], n),
    'age_group': np.random.choice(['18-25', '26-35', '36-50', '51+'], n),
})

# Derive churn probability based on realistic rules
churn_score = (
    (df['contract_type'] == 'Month-to-Month').astype(int) * 0.3 +
    (df['tenure_months'] < 12).astype(int) * 0.2 +
    (df['num_support_calls'] > 5).astype(int) * 0.25 +
    (df['payment_delays'] > 2).astype(int) * 0.25
)
df['churned'] = (churn_score + np.random.uniform(0, 0.2, n) > 0.45).astype(int)
df['total_revenue'] = df['monthly_spend'] * df['tenure_months']

os.makedirs('data', exist_ok=True)
df.to_csv('data/customers.csv', index=False)

# Write to SQLite
conn = sqlite3.connect('data/churn.db')
df.to_sql('customers', conn, if_exists='replace', index=False)
conn.close()

print(f"Generated {n} customer records")
print(f"Churn rate: {df['churned'].mean():.1%}")
print("Saved to data/customers.csv and data/churn.db")
