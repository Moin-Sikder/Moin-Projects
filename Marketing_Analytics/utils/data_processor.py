# utils/data_processor.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataProcessor:
    def __init__(self, config):
        self.config = config
        
    def calculate_rfm_scores(self, df):
        """Calculate RFM scores for customer segmentation"""
        # Recency: Days since last purchase
        df['recency'] = (pd.to_datetime(self.config.END_DATE) - pd.to_datetime(df['last_purchase_date'])).dt.days
        
        # Frequency: Number of purchases
        frequency = df.groupby('customer_id').size().reset_index(name='frequency')
        df = df.merge(frequency, on='customer_id')
        
        # Monetary: Total spending
        monetary = df.groupby('customer_id')['purchase_amount'].sum().reset_index(name='monetary')
        df = df.merge(monetary, on='customer_id')
        
        return df
    
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
    
    def calculate_campaign_metrics(self, df):
        """Calculate marketing campaign performance metrics"""
        campaign_metrics = df.groupby('campaign_id').agg({
            'customer_id': 'count',
            'purchase_amount': 'sum',
            'converted': 'sum',
            'campaign_cost': 'first'
        }).reset_index()
        
        campaign_metrics.rename(columns={'customer_id': 'reach'}, inplace=True)
        campaign_metrics['conversion_rate'] = campaign_metrics['converted'] / campaign_metrics['reach']
        campaign_metrics['roi'] = (campaign_metrics['purchase_amount'] - campaign_metrics['campaign_cost']) / campaign_metrics['campaign_cost']
        campaign_metrics['cpa'] = campaign_metrics['campaign_cost'] / campaign_metrics['converted']
        
        return campaign_metrics