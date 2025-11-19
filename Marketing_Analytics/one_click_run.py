# Marketing Analytics Project - Complete Implementation
# Run this entire code in Google Colab

# Install required packages
!pip install sqlalchemy pandas numpy matplotlib seaborn plotly scikit-learn faker

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
from faker import Faker
import warnings
warnings.filterwarnings('ignore')

print("🚀 Marketing Analytics Project - Starting Setup...")

# =============================================================================
# CONFIGURATION CLASS
# =============================================================================

class ProjectConfig:
    # Project Settings
    PROJECT_NAME = "Marketing Analytics Dashboard"
    RANDOM_SEED = 42
    
    # Analysis Period (Dynamic Variables)
    START_DATE = '2023-01-01'
    END_DATE = '2024-01-01'
    ANALYSIS_DAYS = 365
    
    # Customer Segmentation Thresholds
    RFM_THRESHOLDS = {
        'recency_days': [30, 90, 180],
        'frequency_bins': [1, 3, 10],
        'monetary_bins': [100, 500, 2000]
    }
    
    # Campaign Performance Metrics
    MIN_CONVERSION_RATE = 0.01
    MAX_COST_PER_ACQUISITION = 100
    
    # Privacy Settings
    ANONYMIZE_IDS = True
    ADD_NOISE_TO_SENSITIVE = True
    NOISE_LEVEL = 0.05
    
    # Database Configuration
    DB_PATH = '/content/marketing_analytics.db'
    
    def update_period(self, start_date, end_date):
        """Update analysis period dynamically"""
        self.START_DATE = start_date
        self.END_DATE = end_date
        
    def update_rfm_thresholds(self, recency, frequency, monetary):
        """Update RFM segmentation thresholds"""
        self.RFM_THRESHOLDS = {
            'recency_days': recency,
            'frequency_bins': frequency,
            'monetary_bins': monetary
        }

# =============================================================================
# PRIVACY MANAGER
# =============================================================================

class PrivacyManager:
    def __init__(self, noise_level=0.05):
        self.fake = Faker()
        self.noise_level = noise_level
        self.customer_mapping = {}
        
    def anonymize_customer_id(self, customer_id):
        """Anonymize customer IDs using hash function"""
        if customer_id not in self.customer_mapping:
            hashed_id = hashlib.sha256(str(customer_id).encode()).hexdigest()[:16]
            self.customer_mapping[customer_id] = f"CUST_{hashed_id}"
        return self.customer_mapping[customer_id]
    
    def add_noise_to_sensitive_data(self, series):
        """Add random noise to sensitive numerical data"""
        noise = np.random.normal(0, self.noise_level * series.std(), len(series))
        return series * (1 + noise)

# =============================================================================
# DATA PROCESSOR
# =============================================================================

class DataProcessor:
    def __init__(self, config):
        self.config = config
        
    def calculate_rfm_scores(self, df):
        """Calculate RFM scores for customer segmentation"""
        # Calculate recency, frequency, monetary values
        customer_summary = df.groupby('customer_id').agg({
            'purchase_date': 'max',
            'purchase_amount': ['count', 'sum']
        }).reset_index()
        
        customer_summary.columns = ['customer_id', 'last_purchase_date', 'frequency', 'monetary']
        
        # Calculate recency
        customer_summary['recency'] = (pd.to_datetime(self.config.END_DATE) - 
                                     pd.to_datetime(customer_summary['last_purchase_date'])).dt.days
        
        return customer_summary
    
    def segment_customers(self, df):
        """Segment customers using RFM analysis"""
        thresholds = self.config.RFM_THRESHOLDS
        
        # RFM Scoring
        df['r_score'] = pd.cut(df['recency'], 
                              bins=[0] + thresholds['recency_days'] + [np.inf],
                              labels=[3, 2, 1], right=False)
        
        df['f_score'] = pd.cut(df['frequency'],
                              bins=[0] + thresholds['frequency_bins'] + [np.inf],
                              labels=[1, 2, 3], right=False)
        
        df['m_score'] = pd.cut(df['monetary'],
                              bins=[0] + thresholds['monetary_bins'] + [np.inf],
                              labels=[1, 2, 3], right=False)
        
        df['rfm_score'] = df['r_score'].astype(str) + df['f_score'].astype(str) + df['m_score'].astype(str)
        
        # Customer Segments
        segment_map = {
            '333': 'Champions', '323': 'Champions', '313': 'Champions',
            '233': 'Loyal Customers', '223': 'Loyal Customers',
            '133': 'At Risk', '123': 'At Risk',
            '111': 'Lost Customers', '112': 'Lost Customers'
        }
        
        df['segment'] = df['rfm_score'].map(segment_map).fillna('Need Attention')
        
        return df
    
    def calculate_campaign_metrics(self, df_transactions, df_campaigns):
        """Calculate marketing campaign performance metrics"""
        campaign_stats = df_transactions.groupby('campaign_id').agg({
            'customer_id': 'nunique',
            'purchase_amount': 'sum',
            'converted': 'sum'
        }).reset_index()
        
        campaign_stats = campaign_stats.merge(df_campaigns, on='campaign_id')
        campaign_stats.rename(columns={'customer_id': 'reach'}, inplace=True)
        campaign_stats['conversion_rate'] = campaign_stats['converted'] / campaign_stats['reach']
        campaign_stats['roi'] = (campaign_stats['purchase_amount'] - campaign_stats['cost']) / campaign_stats['cost']
        campaign_stats['cpa'] = campaign_stats['cost'] / campaign_stats['converted']
        
        return campaign_stats

# =============================================================================
# DATABASE CREATION
# =============================================================================

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
            purchase_amount = max(10, np.random.gamma(2, 50))  # Right-skewed amounts, min $10
            
            transaction = {
                'customer_id': cust_id,
                'campaign_id': campaign['campaign_id'],
                'purchase_amount': purchase_amount,
                'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                'converted': 1
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
    
    # Create SQLite database
    conn = sqlite3.connect(db_path)
    
    df_customers.to_sql('customers', conn, index=False, if_exists='replace')
    df_transactions.to_sql('transactions', conn, index=False, if_exists='replace')
    df_campaigns.to_sql('campaigns', conn, index=False, if_exists='replace')
    
    conn.close()
    
    print(f"✅ Database created with {len(df_customers)} customers and {len(df_transactions)} transactions")
    return df_customers, df_transactions, df_campaigns

# =============================================================================
# MAIN ANALYSIS EXECUTION
# =============================================================================

print("📊 Creating synthetic marketing database...")
config = ProjectConfig()
customers, transactions, campaigns = create_marketing_database(config.DB_PATH)

# Initialize components
privacy_manager = PrivacyManager()
data_processor = DataProcessor(config)

# Connect to database
engine = create_engine(f'sqlite:///{config.DB_PATH}')

# Dynamic SQL Queries
def run_dynamic_analysis(start_date=None, end_date=None, min_purchase=0):
    """Run analysis with dynamic parameters"""
    
    if start_date is None:
        start_date = config.START_DATE
    if end_date is None:
        end_date = config.END_DATE
    
    # SQL Query with dynamic parameters
    query = f"""
    SELECT 
        t.customer_id,
        t.campaign_id,
        t.purchase_amount,
        t.purchase_date,
        c.age_group,
        c.region,
        camp.name as campaign_name,
        camp.channel as campaign_channel,
        camp.cost as campaign_cost
    FROM transactions t
    JOIN customers c ON t.customer_id = c.customer_id
    JOIN campaigns camp ON t.campaign_id = camp.campaign_id
    WHERE t.purchase_date BETWEEN '{start_date}' AND '{end_date}'
        AND t.purchase_amount >= {min_purchase}
    """
    
    df = pd.read_sql(query, engine)
    print(f"📈 Analyzing {len(df)} transactions from {start_date} to {end_date}")
    
    return df

# Run initial analysis
print("\n" + "="*60)
print("🎯 INITIAL ANALYSIS WITH DEFAULT PARAMETERS")
print("="*60)

df = run_dynamic_analysis()

# Apply privacy protection
if config.ANONYMIZE_IDS:
    df['customer_id'] = df['customer_id'].apply(privacy_manager.anonymize_customer_id)

if config.ADD_NOISE_TO_SENSITIVE:
    df['purchase_amount'] = privacy_manager.add_noise_to_sensitive_data(df['purchase_amount'])

# Customer Segmentation Analysis
print("🎯 Performing Customer Segmentation...")
df_rfm = data_processor.calculate_rfm_scores(df)
df_segmented = data_processor.segment_customers(df_rfm)

# Campaign Performance Analysis
print("📊 Analyzing Campaign Performance...")
campaign_metrics = data_processor.calculate_campaign_metrics(transactions, campaigns)

# =============================================================================
# VISUALIZATIONS
# =============================================================================

def create_visualizations(df_segmented, campaign_metrics):
    """Create comprehensive visualizations"""
    
    print("\n📊 GENERATING VISUALIZATIONS...")
    
    # 1. Customer Segments
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    segment_counts = df_segmented['segment'].value_counts()
    plt.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Customer Segments Distribution')
    
    plt.subplot(1, 3, 2)
    sns.boxplot(data=df_segmented, x='segment', y='monetary')
    plt.title('Spending by Segment')
    plt.xticks(rotation=45)
    
    plt.subplot(1, 3, 3)
    channel_performance = df_segmented.groupby('campaign_channel')['monetary'].sum()
    channel_performance.plot(kind='bar', color='skyblue')
    plt.title('Revenue by Marketing Channel')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # 2. Campaign Performance Dashboard
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=campaign_metrics['campaign_id'],
        y=campaign_metrics['conversion_rate'],
        name='Conversion Rate',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Scatter(
        x=campaign_metrics['campaign_id'],
        y=campaign_metrics['roi'],
        name='ROI',
        yaxis='y2',
        marker=dict(color='red', size=8),
        line=dict(width=3)
    ))
    
    fig.update_layout(
        title='Campaign Performance: Conversion Rate vs ROI',
        xaxis_title='Campaign',
        yaxis=dict(title='Conversion Rate'),
        yaxis2=dict(title='ROI', overlaying='y', side='right'),
        template='plotly_white'
    )
    
    fig.show()
    
    # 3. RFM Scatter Plot
    fig = px.scatter(df_segmented, 
                    x='recency', 
                    y='monetary', 
                    color='segment',
                    size='frequency',
                    hover_data=['customer_id'],
                    title='RFM Analysis: Recency vs Monetary Value',
                    size_max=15)
    fig.show()

create_visualizations(df_segmented, campaign_metrics)

# =============================================================================
# KEY METRICS SUMMARY
# =============================================================================

def print_summary_metrics(df_segmented, campaign_metrics):
    """Print key marketing metrics"""
    
    print("\n" + "="*60)
    print("📊 MARKETING ANALYTICS SUMMARY")
    print("="*60)
    
    total_revenue = df_segmented['monetary'].sum()
    total_customers = df_segmented['customer_id'].nunique()
    avg_customer_value = total_revenue / total_customers
    
    print(f"💰 Total Revenue: ${total_revenue:,.2f}")
    print(f"👥 Total Customers: {total_customers}")
    print(f"📈 Average Customer Value: ${avg_customer_value:,.2f}")
    print(f"🎯 Customer Segments: {df_segmented['segment'].nunique()}")
    
    best_campaign = campaign_metrics.loc[campaign_metrics['roi'].idxmax()]
    worst_campaign = campaign_metrics.loc[campaign_metrics['roi'].idxmin()]
    
    print(f"\n🏆 Best Performing Campaign: {best_campaign['name']}")
    print(f"   ROI: {best_campaign['roi']:.2%}")
    print(f"   Conversion Rate: {best_campaign['conversion_rate']:.2%}")
    
    print(f"\n⚠️  Campaign Needing Attention: {worst_campaign['name']}")
    print(f"   ROI: {worst_campaign['roi']:.2%}")
    print(f"   Conversion Rate: {worst_campaign['conversion_rate']:.2%}")

print_summary_metrics(df_segmented, campaign_metrics)

# =============================================================================
# DYNAMIC ANALYSIS EXAMPLE
# =============================================================================

print("\n" + "="*60)
print("🔄 RUNNING DYNAMIC ANALYSIS WITH UPDATED PARAMETERS")
print("="*60)

# Update configuration dynamically
config.update_period('2023-06-01', '2023-12-31')
config.update_rfm_thresholds([45, 120, 240], [2, 5, 15], [150, 750, 3000])

# Rerun analysis with new parameters
df_dynamic = run_dynamic_analysis(config.START_DATE, config.END_DATE, min_purchase=50)
df_rfm_dynamic = data_processor.calculate_rfm_scores(df_dynamic)
df_segmented_dynamic = data_processor.segment_customers(df_rfm_dynamic)

print(f"🔄 New analysis period: {config.START_DATE} to {config.END_DATE}")
print(f"🔄 Updated RFM thresholds applied")
print(f"🔄 Segments in new analysis: {df_segmented_dynamic['segment'].nunique()}")

# =============================================================================
# EXPORT RESULTS FOR GITHUB
# =============================================================================

def export_results_for_github(df_segmented, campaign_metrics):
    """Export anonymized results for GitHub publication"""
    
    # Remove sensitive columns
    export_df = df_segmented.drop(columns=['customer_id'], errors='ignore')
    
    # Aggregate data for public sharing
    segment_summary = export_df.groupby(['segment']).agg({
        'monetary': ['count', 'sum', 'mean'],
        'recency': 'mean',
        'frequency': 'mean'
    }).round(2)
    
    # Flatten column names
    segment_summary.columns = ['_'.join(col).strip() for col in segment_summary.columns.values]
    segment_summary.reset_index(inplace=True)
    
    # Save to CSV
    segment_summary.to_csv('/content/customer_segments_summary.csv', index=False)
    campaign_metrics.to_csv('/content/campaign_performance.csv', index=False)
    
    print("\n📁 Results exported for GitHub:")
    print("   - customer_segments_summary.csv")
    print("   - campaign_performance.csv")
    
    # Display sample of exported data
    print("\n📋 Sample of Customer Segments Summary:")
    print(segment_summary.head())
    
    print("\n📋 Sample of Campaign Performance:")
    print(campaign_metrics[['name', 'channel', 'conversion_rate', 'roi']].head())

export_results_for_github(df_segmented, campaign_metrics)

print("\n" + "="*60)
print("✅ PROJECT EXECUTION COMPLETED SUCCESSFULLY!")
print("="*60)
print("\n🎉 Your marketing analytics project is ready!")
print("📊 Check the visualizations and summary metrics above")
print("📁 Files for GitHub have been exported")
print("\nYou can now modify the dynamic variables and rerun sections as needed!")