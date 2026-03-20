# Customer Churn Risk Modelling & Retention Analytics

## Overview
Most businesses only notice when customers have already left. 
This project was built to change that. Using a dataset of 1,000+ 
customer records, I developed a system that identifies which customers 
are at risk of churning before they actually do, so the business can 
intervene early and protect its revenue.

## The Approach
I started by cleaning and preparing the data in Python, removing 
duplicates, handling null values, and standardising formats. From 
there I engineered new features from the raw data, grouping customers 
by tenure, flagging high risk contract types, and identifying spend 
patterns associated with churn behaviour.

Rather than building a black box machine learning model, I developed 
a transparent rule-based risk scoring framework. Every customer receives 
a score based on their behaviour and that score places them into a low, 
medium, or high risk category. This approach makes the output easy for 
business stakeholders to understand and act on.

I then segmented customers by their risk level and spend value to help 
the business prioritise its retention efforts. High risk, high value 
customers get personal outreach. High risk, low value customers get 
automated campaigns. Low risk customers get loyalty rewards.

The final output is an executive Power BI dashboard showing overall 
churn rate, revenue at risk, churn drivers by segment, and targeted 
retention recommendations.

## Tools Used
Python, Pandas, NumPy, SQL, Power BI, DAX

## Key Insight
Month-to-month contract customers are disproportionately high risk 
regardless of how much they spend. Contract type is the strongest 
single predictor of churn, which means incentivising customers to 
move to longer contracts early is the most effective retention strategy.

---
Built by Pearl Mlotshwa
github.com/pearl-mlotshwa

