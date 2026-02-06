# Customer Churn Analysis (Telecom)

## Project Overview
This project analyzes customer churn data for a telecom-style subscription business.  
The objective was to identify churn drivers, quantify risk across customer segments, and provide data-driven retention recommendations.

The project demonstrates end-to-end analytics skills using Python, SQL, and Power BI.

---

## Tools Used
- Python (Pandas, NumPy, Scikit-learn) – Data cleaning and exploratory analysis
- SQLite – SQL-based churn analysis
- Power BI – Interactive churn dashboard

---

## Dataset
Customer dataset containing:
- Customer demographics
- Contract type
- Tenure
- Payment methods
- Internet services
- Monthly and total charges
- Churn status

---

## Key Analysis (SQL)
- Overall churn rate
- Churn by contract type
- Churn by tenure bands
- Churn by payment method
- Churn by internet service

---

## Power BI Dashboard Features
- Total Customers KPI
- Churn Rate KPI
- Churn by Contract Type
- Churn by Tenure Band
- Interactive slicers:
  - Contract
  - Internet Service
  - Payment Method

---

## Key Insights
- Overall churn rate is **26.54%**, indicating significant customer attrition.
- Month-to-month customers exhibit extremely high churn (**42.7%**) compared to one-year (**11.3%**) and two-year (**2.8%**) contracts.
- New customers are most vulnerable, with **56% churn in the first 3 months**.
- Customers using **electronic check payment** have the highest churn (**45.3%**), while automatic payments show much lower churn.

---

## Recommendations
- Encourage month-to-month customers to migrate to longer-term contracts.
- Implement early onboarding and retention programs within the first 90 days.
- Incentivize customers to switch from electronic checks to automatic payment methods.
- Target high-risk segments with personalized retention offers.

---

## Project Structure
- `data/` – Cleaned dataset  
- `notebooks/` – Python EDA notebook  
- `sql/` – SQL analysis queries  
- `powerbi/` – Power BI dashboard  
- `visuals/` – Dashboard screenshots  

---

## Outcome
This project demonstrates:
- Data cleaning and preparation in Python
- SQL-based business analysis
- Feature engineering
- Dashboard design in Power BI
- Translating data into actionable business insights

---

## Author
Pearl Mlotshwa  
Aspiring Data Analyst
