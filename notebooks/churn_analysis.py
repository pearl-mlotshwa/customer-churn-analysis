#!/usr/bin/env python3
"""
Customer Churn Risk Modelling & Retention Analytics
Author: Phumelele Pearl Mlotshwa
Tools: Python (Pandas, NumPy, Matplotlib, Seaborn), SQLite
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Setup ──────────────────────────────────────────────────────
os.makedirs('outputs', exist_ok=True)
sns.set_theme(style='whitegrid', palette='muted')

# ── 1. Load Data ───────────────────────────────────────────────
conn = sqlite3.connect('data/churn.db')
df = pd.read_sql('SELECT * FROM customers', conn)
conn.close()

print("=" * 55)
print("  Customer Churn Risk Modelling – Summary Report")
print("=" * 55)
print(f"\nTotal customers : {len(df):,}")
print(f"Churned         : {df['churned'].sum():,}  ({df['churned'].mean():.1%})")
print(f"Total monthly revenue : R{df['monthly_spend'].sum():,.0f}")

# ── 2. Risk Scoring ────────────────────────────────────────────
def assign_risk(row):
    if row['contract_type'] == 'Month-to-Month' and row['tenure_months'] < 12 and row['num_support_calls'] > 5:
        return 'Critical'
    elif row['contract_type'] == 'Month-to-Month' and row['payment_delays'] > 2:
        return 'High'
    elif row['num_support_calls'] > 5 or row['payment_delays'] > 2:
        return 'Medium'
    return 'Low'

df['risk_tier'] = df.apply(assign_risk, axis=1)
df['lifetime_value'] = df['monthly_spend'] * df['tenure_months']

# ── 3. Revenue at Risk ─────────────────────────────────────────
risk_summary = (
    df.groupby('risk_tier')
      .agg(customers=('customer_id', 'count'),
           churned=('churned', 'sum'),
           revenue_at_risk=('monthly_spend', 'sum'))
      .reindex(['Critical', 'High', 'Medium', 'Low'])
      .reset_index()
)
risk_summary['churn_rate'] = (risk_summary['churned'] / risk_summary['customers']).round(3)
print("\nRisk Tier Breakdown:")
print(risk_summary.to_string(index=False))

# ── 4. Visualisations ──────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Customer Churn Risk Analysis Dashboard', fontsize=15, fontweight='bold')

# 4a. Churn rate by contract type
ct = df.groupby('contract_type')['churned'].mean().sort_values(ascending=False)
ct.plot(kind='bar', ax=axes[0, 0], color=['#e74c3c', '#e67e22', '#2ecc71'], edgecolor='white')
axes[0, 0].set_title('Churn Rate by Contract Type')
axes[0, 0].set_ylabel('Churn Rate')
axes[0, 0].yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
axes[0, 0].tick_params(axis='x', rotation=15)

# 4b. Revenue at risk by tier
colors = ['#c0392b', '#e74c3c', '#e67e22', '#27ae60']
axes[0, 1].bar(risk_summary['risk_tier'], risk_summary['revenue_at_risk'], color=colors, edgecolor='white')
axes[0, 1].set_title('Monthly Revenue at Risk by Tier')
axes[0, 1].set_ylabel('Revenue (R)')
axes[0, 1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R{x:,.0f}'))

# 4c. Churn by tenure band
df['tenure_band'] = pd.cut(df['tenure_months'], bins=[0, 6, 12, 24, 72],
                           labels=['0-6 mo', '6-12 mo', '1-2 yr', '2+ yr'])
tb = df.groupby('tenure_band', observed=True)['churned'].mean()
tb.plot(kind='bar', ax=axes[1, 0], color='#3498db', edgecolor='white')
axes[1, 0].set_title('Churn Rate by Customer Tenure')
axes[1, 0].set_ylabel('Churn Rate')
axes[1, 0].yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
axes[1, 0].tick_params(axis='x', rotation=15)

# 4d. Regional churn
reg = df.groupby('region')['churned'].mean().sort_values(ascending=True)
reg.plot(kind='barh', ax=axes[1, 1], color='#9b59b6', edgecolor='white')
axes[1, 1].set_title('Churn Rate by Region')
axes[1, 1].xaxis.set_major_formatter(mticker.PercentFormatter(1.0))

plt.tight_layout()
plt.savefig('outputs/churn_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nDashboard saved to outputs/churn_dashboard.png")

# ── 5. Export enriched data for Power BI ──────────────────────
df.to_csv('outputs/churn_risk_scored.csv', index=False)
print("Risk-scored data exported to outputs/churn_risk_scored.csv")

# ── 6. Retention Recommendations ──────────────────────────────
print("\nRetention Strategy Recommendations:")
print("-" * 45)
critical = df[df['risk_tier'] == 'Critical']
high = df[df['risk_tier'] == 'High']
print(f"  Critical ({len(critical)} customers): Immediate outreach + loyalty discount")
print(f"  High     ({len(high)} customers): Proactive check-in + contract upgrade offer")
print(f"  Medium   : Automated re-engagement email sequence")
print(f"  Low      : Standard retention programme")
print("\nAnalysis complete.")
