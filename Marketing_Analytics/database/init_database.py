# database/init_database.py

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_marketing_database(db_path, num_customers=1000, num_campaigns=8):
    """Create synthetic marketing database with realistic data"""
    
    np.random.seed(42)
    
    # Generate customer data
    customer_ids = [f"CUST_{i:04d}" for i in range(1, num_customers + 1)]
    
    # Campaign data
    campaigns = [
        {'campaign_id': 'CAMP_001', 'name': 'Summer Sale', 'channel': 'Email', 'cost': 5000},
        {'campaign_id': 'CAMP_002', 'name': 'Black Friday', 'channel': 'Social Media', 'cost': 8000},
        {'campaign_id': 'CAMP_003', 'name': 'Winter Clearance', 'channel': 'Paid Search', 'cost': 6000},
        {'campaign_id': 'CAMP_004', 'name': 'New Product Launch', 'channel': 'Influencer', 'cost': 10000},
        {'campaign_id': 'CAMP_005', 'name': 'Loyalty Program', 'channel': 'Email', 'cost': 3000},
        {'campaign_id': 'CAMP_006', 'name': 'Holiday Special', 'channel': 'Social Media', 'cost': 7000},
        {'campaign_id': 'CAMP_007', 'name': 'Spring Collection', 'channel': 'Paid Search', 'cost': 5500},
        {'campaign_id': 'CAMP_008', 'name': 'Referral Program', 'channel': 'Organic', 'cost': 2000},
    ]
    
    # Generate transactions
    transactions = []
    start_date = datetime(2023, 1, 1)
    
    for cust_id in customer_ids:
        n_purchases = np.random.poisson(3)  # Average 3 purchases per customer
        
        for _ in range(max(1, n_purchases)):
            campaign = np.random.choice(campaigns)
            purchase_date = start_date + timedelta(days=np.random.randint(0, 365))
            
            transaction = {
                'customer_id': cust_id,
                'campaign_id': campaign['campaign_id'],
                'purchase_amount': np.random.gamma(2, 50),  # Right-skewed purchase amounts
                'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                'converted': 1,
                'campaign_cost': campaign['cost']
            }
            transactions.append(transaction)
    
    # Create DataFrames
    df_customers = pd.DataFrame({
        'customer_id': customer_ids,
        'age_group': np.random.choice(['18-25', '26-35', '36-45', '46-55', '55+'], num_customers),
        'region': np.random.choice(['North', 'South', 'East', 'West'], num_customers),
        'signup_date': pd.date_range('2022-01-01', periods=num_customers, freq='D').strftime('%Y-%m-%d')
    })
    
    df_transactions = pd.DataFrame(transactions)
    df_campaigns = pd.DataFrame(campaigns)
    
    # Calculate last purchase date for each customer
    last_purchase = df_transactions.groupby('customer_id')['purchase_date'].max().reset_index()
    df_customers = df_customers.merge(last_purchase, on='customer_id', how='left')
    df_customers.rename(columns={'purchase_date': 'last_purchase_date'}, inplace=True)
    
    # Fill missing last purchase dates with signup date
    df_customers['last_purchase_date'] = df_customers['last_purchase_date'].fillna(df_customers['signup_date'])
    
    # Create SQLite database
    conn = sqlite3.connect(db_path)
    
    df_customers.to_sql('customers', conn, index=False, if_exists='replace')
    df_transactions.to_sql('transactions', conn, index=False, if_exists='replace')
    df_campaigns.to_sql('campaigns', conn, index=False, if_exists='replace')
    
    conn.close()
    
    print(f"Database created with {len(df_customers)} customers and {len(df_transactions)} transactions")
    return df_customers, df_transactions, df_campaigns

# Usage in Colab:
# from database.init_database import create_marketing_database
# customers, transactions, campaigns = create_marketing_database('/content/marketing_analytics.db')