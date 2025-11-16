import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class MarketingDataAnalyzer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.cleaned_data = None
        
    def explore_data(self):
        print("=== MARKETING DATA OVERVIEW ===")
        print(f"Dataset Shape: {self.data.shape}")
        print("\nFirst 5 rows:")
        print(self.data.head())
        print("\nDataset Info:")
        print(self.data.info())
        print("\nBasic Statistics:")
        print(self.data.describe())
        print("\nMissing Values:")
        print(self.data.isnull().sum())
        
        return self.data.shape, self.data.isnull().sum().sum()
    
    def clean_data(self):
        df = self.data.copy()
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Create additional marketing metrics
        if 'Revenue' in df.columns and 'Spend' in df.columns:
            df['ROI'] = (df['Revenue'] - df['Spend']) / df['Spend'] * 100
        if 'Clicks' in df.columns and 'Spend' in df.columns:
            df['CPC'] = df['Spend'] / df['Clicks']
        if 'Conversions' in df.columns and 'Clicks' in df.columns:
            df['Conversion_Rate'] = (df['Conversions'] / df['Clicks']) * 100
            
        self.cleaned_data = df
        print("✅ Data cleaning completed!")
        return df
    
    def campaign_performance_analysis(self):
        if self.cleaned_data is None:
            self.clean_data()
            
        df = self.cleaned_data
        results = {}
        
        # Campaign performance metrics
        if 'Campaign' in df.columns:
            campaign_stats = df.groupby('Campaign').agg({
                'Spend': 'sum',
                'Revenue': 'sum',
                'Conversions': 'sum',
                'Clicks': 'sum'
            }).reset_index()
            
            campaign_stats['ROI'] = (campaign_stats['Revenue'] - campaign_stats['Spend']) / campaign_stats['Spend'] * 100
            campaign_stats['CPA'] = campaign_stats['Spend'] / campaign_stats['Conversions']
            campaign_stats['Conversion_Rate'] = (campaign_stats['Conversions'] / campaign_stats['Clicks']) * 100
            
            results['campaign_performance'] = campaign_stats
            
        return results
    
    def customer_segmentation(self, features=None):
        if self.cleaned_data is None:
            self.clean_data()
            
        df = self.cleaned_data
        
        # Default features for segmentation
        if features is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            features = list(numeric_cols[:4])  # Use first 4 numeric features
            
        # Prepare data for clustering
        X = df[features].fillna(df[features].median())
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Find optimal clusters using elbow method
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            wcss.append(kmeans.inertia_)
        
        # Apply K-means clustering
        optimal_clusters = 4
        kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
        df['Segment'] = kmeans.fit_predict(X_scaled)
        
        # Analyze segments
        segment_analysis = df.groupby('Segment')[features].mean()
        
        return {
            'segmented_data': df,
            'segment_analysis': segment_analysis,
            'cluster_centers': kmeans.cluster_centers_,
            'wcss': wcss
        }
    
    def generate_visualizations(self):
        if self.cleaned_data is None:
            self.clean_data()
            
        df = self.cleaned_data
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('ROI by Campaign', 'Customer Segments', 
                          'Conversion Funnel', 'Spend vs Revenue'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "funnel"}, {"type": "scatter"}]]
        )
        
        # Plot 1: ROI by Campaign
        if 'Campaign' in df.columns and 'ROI' in df.columns:
            campaign_roi = df.groupby('Campaign')['ROI'].mean().reset_index()
            fig.add_trace(
                go.Bar(x=campaign_roi['Campaign'], y=campaign_roi['ROI'], name="ROI"),
                row=1, col=1
            )
        
        # Plot 2: Customer Segments
        if 'Segment' in df.columns:
            segment_counts = df['Segment'].value_counts()
            fig.add_trace(
                go.Scatter(x=segment_counts.index.astype(str), 
                          y=segment_counts.values, 
                          mode='lines+markers', name="Segments"),
                row=1, col=2
            )
        
        # Plot 3: Conversion Funnel
        if all(col in df.columns for col in ['Clicks', 'Conversions', 'Revenue']):
            funnel_data = {
                'Stage': ['Clicks', 'Conversions', 'Revenue'],
                'Value': [df['Clicks'].sum(), df['Conversions'].sum(), df['Revenue'].sum()/100]
            }
            fig.add_trace(
                go.Funnel(y=funnel_data['Stage'], x=funnel_data['Value'], name="Funnel"),
                row=2, col=1
            )
        
        # Plot 4: Spend vs Revenue
        if all(col in df.columns for col in ['Spend', 'Revenue']):
            fig.add_trace(
                go.Scatter(x=df['Spend'], y=df['Revenue'], 
                          mode='markers', name="Spend vs Revenue"),
                row=2, col=2
            )
        
        fig.update_layout(height=800, title_text="Marketing Dashboard", showlegend=False)
        return fig
    
    def generate_report(self):
        analysis_results = {}
        
        # Data exploration
        analysis_results['data_shape'] = self.explore_data()
        
        # Data cleaning
        analysis_results['cleaned_data'] = self.clean_data()
        
        # Campaign performance
        analysis_results['campaign_analysis'] = self.campaign_performance_analysis()
        
        # Customer segmentation
        analysis_results['segmentation'] = self.customer_segmentation()
        
        # Key metrics summary
        df = self.cleaned_data
        summary = {}
        
        if 'Revenue' in df.columns and 'Spend' in df.columns:
            summary['total_revenue'] = df['Revenue'].sum()
            summary['total_spend'] = df['Spend'].sum()
            summary['overall_roi'] = (summary['total_revenue'] - summary['total_spend']) / summary['total_spend'] * 100
        
        if 'Conversions' in df.columns and 'Clicks' in df.columns:
            summary['total_conversions'] = df['Conversions'].sum()
            summary['total_clicks'] = df['Clicks'].sum()
            summary['overall_conversion_rate'] = (summary['total_conversions'] / summary['total_clicks']) * 100
        
        analysis_results['summary'] = summary
        
        return analysis_results