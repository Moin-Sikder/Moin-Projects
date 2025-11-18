# Cell 2: Run the comprehensive marketing analytics
# mart_analytics.py - Google Colab Version

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class MartAnalytics:
    def __init__(self, file_path='mart.csv'):
        """Initialize the analytics class with data loading"""
        self.df = pd.read_csv(file_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        print(f"✅ Data loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        
    def project_1_marketing_roi_analysis(self):
        """Project 1: Marketing ROI Analysis"""
        print("\n" + "="*50)
        print("📊 PROJECT 1: MARKETING ROI ANALYSIS")
        print("="*50)
        
        # Calculate ROI metrics
        self.df['Marketing_ROI'] = self.df['Weekly_Sales'] / self.df['Marketing_Spend_Online']
        self.df['Total_Markdown'] = self.df['Markdown1'] + self.df['Markdown2']
        self.df['Markdown_ROI'] = self.df['Weekly_Sales'] / (self.df['Total_Markdown'] + 1)
        
        # ROI by different segments
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # ROI by Product Category
        roi_by_category = self.df.groupby('Product_Category')['Marketing_ROI'].mean().sort_values(ascending=False)
        axes[0,0].bar(roi_by_category.index, roi_by_category.values)
        axes[0,0].set_title('Marketing ROI by Product Category', fontweight='bold')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # ROI by Customer Segment
        roi_by_segment = self.df.groupby('Customer_Segment')['Marketing_ROI'].mean().sort_values(ascending=False)
        axes[0,1].bar(roi_by_segment.index, roi_by_segment.values)
        axes[0,1].set_title('Marketing ROI by Customer Segment', fontweight='bold')
        
        # ROI by Store
        roi_by_store = self.df.groupby('Store')['Marketing_ROI'].mean().sort_values(ascending=False)
        axes[0,2].bar([str(x) for x in roi_by_store.index], roi_by_store.values)
        axes[0,2].set_title('Marketing ROI by Store', fontweight='bold')
        
        # Marketing Spend vs Sales
        axes[1,0].scatter(self.df['Marketing_Spend_Online'], self.df['Weekly_Sales'], alpha=0.6)
        axes[1,0].set_xlabel('Marketing Spend Online')
        axes[1,0].set_ylabel('Weekly Sales')
        axes[1,0].set_title('Marketing Spend vs Sales', fontweight='bold')
        
        # Markdown ROI by Category
        markdown_roi = self.df.groupby('Product_Category')['Markdown_ROI'].mean().sort_values(ascending=False)
        axes[1,1].bar(markdown_roi.index, markdown_roi.values)
        axes[1,1].set_title('Markdown ROI by Product Category', fontweight='bold')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        # Holiday vs Non-Holiday ROI
        holiday_roi = self.df.groupby('Holiday_Flag')['Marketing_ROI'].mean()
        axes[1,2].bar(['Non-Holiday', 'Holiday'], holiday_roi.values)
        axes[1,2].set_title('Marketing ROI: Holiday vs Non-Holiday', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        # Print insights
        print("\n📈 ROI INSIGHTS:")
        print(f"Highest ROI Category: {roi_by_category.index[0]} (${roi_by_category.values[0]:.2f})")
        print(f"Highest ROI Segment: {roi_by_segment.index[0]} (${roi_by_segment.values[0]:.2f})")
        print(f"Most Efficient Store: Store {roi_by_store.index[0]} (${roi_by_store.values[0]:.2f})")
        
    def project_2_customer_segmentation_analysis(self):
        """Project 2: Customer Segmentation Analysis"""
        print("\n" + "="*50)
        print("🎯 PROJECT 2: CUSTOMER SEGMENTATION ANALYSIS")
        print("="*50)
        
        # Prepare data for clustering
        segment_data = self.df.groupby(['Customer_Segment', 'Product_Category']).agg({
            'Weekly_Sales': 'mean',
            'Marketing_Spend_Online': 'mean',
            'Marketing_ROI': 'mean'
        }).reset_index()
        
        # Create pivot table for heatmap
        pivot_sales = segment_data.pivot(index='Customer_Segment', 
                                       columns='Product_Category', 
                                       values='Weekly_Sales')
        
        pivot_roi = segment_data.pivot(index='Customer_Segment', 
                                     columns='Product_Category', 
                                     values='Marketing_ROI')
        
        # Visualizations
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Sales heatmap by segment and category
        sns.heatmap(pivot_sales, annot=True, fmt='.0f', cmap='YlOrRd', ax=axes[0,0])
        axes[0,0].set_title('Average Weekly Sales by Segment & Category', fontweight='bold')
        
        # ROI heatmap by segment and category
        sns.heatmap(pivot_roi, annot=True, fmt='.2f', cmap='YlGn', ax=axes[0,1])
        axes[0,1].set_title('Marketing ROI by Segment & Category', fontweight='bold')
        
        # Customer segment performance
        segment_performance = self.df.groupby('Customer_Segment').agg({
            'Weekly_Sales': ['mean', 'sum'],
            'Marketing_ROI': 'mean'
        }).round(2)
        
        segment_performance.columns = ['Avg_Sales', 'Total_Sales', 'Avg_ROI']
        segment_performance = segment_performance.sort_values('Avg_ROI', ascending=False)
        
        segment_performance[['Avg_Sales', 'Avg_ROI']].plot(kind='bar', ax=axes[1,0])
        axes[1,0].set_title('Customer Segment Performance', fontweight='bold')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Product category preference by segment
        cross_tab = pd.crosstab(self.df['Customer_Segment'], self.df['Product_Category'])
        cross_tab.plot(kind='bar', ax=axes[1,1])
        axes[1,1].set_title('Product Category Preference by Segment', fontweight='bold')
        axes[1,1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.show()
        
        print("\n🎯 SEGMENTATION INSIGHTS:")
        print(segment_performance)
        
    def project_3_sales_forecasting(self):
        """Project 3: Sales Forecasting Model"""
        print("\n" + "="*50)
        print("📈 PROJECT 3: SALES FORECASTING MODEL")
        print("="*50)
        
        # Prepare features for forecasting
        features = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 
                   'Marketing_Spend_Online', 'Markdown1', 'Markdown2', 'Holiday_Flag']
        
        # Create additional time-based features
        self.df['Week'] = self.df['Date'].dt.isocalendar().week
        self.df['Month'] = self.df['Date'].dt.month
        
        # Encode categorical variables
        df_encoded = pd.get_dummies(self.df, columns=['Product_Category', 'Customer_Segment'])
        
        # Prepare feature set
        feature_columns = features + ['Week', 'Month'] + \
                         [col for col in df_encoded.columns if 'Product_Category_' in col or 'Customer_Segment_' in col]
        
        X = df_encoded[feature_columns]
        y = df_encoded['Weekly_Sales']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train models
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        results = {}
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        for idx, (name, model) in enumerate(models.items()):
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            results[name] = {'MAE': mae, 'R2': r2}
            
            # Plot actual vs predicted
            axes[idx, 0].scatter(y_test, y_pred, alpha=0.6)
            axes[idx, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
            axes[idx, 0].set_xlabel('Actual Sales')
            axes[idx, 0].set_ylabel('Predicted Sales')
            axes[idx, 0].set_title(f'{name}: Actual vs Predicted\nR² = {r2:.3f}', fontweight='bold')
            
            # Plot feature importance for Random Forest
            if name == 'Random Forest':
                feature_importance = pd.DataFrame({
                    'feature': feature_columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False).head(10)
                
                axes[idx, 1].barh(feature_importance['feature'], feature_importance['importance'])
                axes[idx, 1].set_title('Top 10 Feature Importance (Random Forest)', fontweight='bold')
            else:
                axes[idx, 1].text(0.5, 0.5, 'Feature importance\nnot available\nfor Linear Regression', 
                                 ha='center', va='center', transform=axes[idx, 1].transAxes, fontsize=12)
                axes[idx, 1].set_title('Feature Importance', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        print("\n📈 FORECASTING RESULTS:")
        for model, metrics in results.items():
            print(f"{model}: MAE = ${metrics['MAE']:,.2f}, R² = {metrics['R2']:.3f}")
            
    def project_4_marketing_mix_modeling(self):
        """Project 4: Marketing Mix Modeling"""
        print("\n" + "="*50)
        print("🔍 PROJECT 4: MARKETING MIX MODELING")
        print("="*50)
        
        # Correlation analysis
        numeric_cols = ['Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment',
                       'Marketing_Spend_Online', 'Markdown1', 'Markdown2']
        
        correlation_matrix = self.df[numeric_cols].corr()
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Correlation heatmap
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[0,0])
        axes[0,0].set_title('Correlation Matrix: Sales vs External Factors', fontweight='bold')
        
        # Impact of external factors on sales
        factors = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
        
        for i, factor in enumerate(factors):
            row, col = (i // 2) + 1, i % 2
            axes[row, col].scatter(self.df[factor], self.df['Weekly_Sales'], alpha=0.6)
            axes[row, col].set_xlabel(factor)
            axes[row, col].set_ylabel('Weekly Sales')
            axes[row, col].set_title(f'Sales vs {factor}', fontweight='bold')
            
            # Add trend line
            z = np.polyfit(self.df[factor], self.df['Weekly_Sales'], 1)
            p = np.poly1d(z)
            axes[row, col].plot(self.df[factor], p(self.df[factor]), "r--", alpha=0.8)
        
        plt.tight_layout()
        plt.show()
        
        # Multiple regression to quantify impact
        X_mmm = self.df[['Marketing_Spend_Online', 'Markdown1', 'Markdown2', 
                         'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Holiday_Flag']]
        X_mmm = pd.get_dummies(X_mmm, columns=['Holiday_Flag'], drop_first=True)
        y_mmm = self.df['Weekly_Sales']
        
        model = LinearRegression()
        model.fit(X_mmm, y_mmm)
        
        coefficients = pd.DataFrame({
            'Feature': X_mmm.columns,
            'Coefficient': model.coef_,
            'Impact_Percentage': (model.coef_ / model.coef_.sum()) * 100
        }).sort_values('Impact_Percentage', key=abs, ascending=False)
        
        print("\n🔍 MARKETING MIX INSIGHTS:")
        print("Factor Impact on Sales:")
        print(coefficients.round(4))
        
    def project_5_product_category_analysis(self):
        """Project 5: Product Category Performance"""
        print("\n" + "="*50)
        print("🏷️ PROJECT 5: PRODUCT CATEGORY PERFORMANCE")
        print("="*50)
        
        category_analysis = self.df.groupby('Product_Category').agg({
            'Weekly_Sales': ['mean', 'sum', 'std'],
            'Marketing_Spend_Online': 'mean',
            'Marketing_ROI': 'mean',
            'Store': 'nunique'
        }).round(2)
        
        category_analysis.columns = ['Avg_Sales', 'Total_Sales', 'Sales_Std', 
                                   'Avg_Marketing_Spend', 'Avg_ROI', 'Stores_Count']
        
        category_analysis = category_analysis.sort_values('Avg_ROI', ascending=False)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Average Sales by Category
        axes[0,0].bar(category_analysis.index, category_analysis['Avg_Sales'])
        axes[0,0].set_title('Average Weekly Sales by Category', fontweight='bold')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Marketing ROI by Category
        axes[0,1].bar(category_analysis.index, category_analysis['Avg_ROI'])
        axes[0,1].set_title('Marketing ROI by Category', fontweight='bold')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Marketing Spend vs Sales
        axes[1,0].scatter(category_analysis['Avg_Marketing_Spend'], 
                         category_analysis['Avg_Sales'], s=100)
        
        for i, category in enumerate(category_analysis.index):
            axes[1,0].annotate(category, 
                             (category_analysis['Avg_Marketing_Spend'].iloc[i], 
                              category_analysis['Avg_Sales'].iloc[i]),
                             xytext=(5, 5), textcoords='offset points')
            
        axes[1,0].set_xlabel('Average Marketing Spend')
        axes[1,0].set_ylabel('Average Sales')
        axes[1,0].set_title('Marketing Spend vs Sales by Category', fontweight='bold')
        
        # Sales distribution by category
        category_sales_data = [self.df[self.df['Product_Category'] == cat]['Weekly_Sales'] 
                             for cat in self.df['Product_Category'].unique()]
        
        axes[1,1].boxplot(category_sales_data, labels=self.df['Product_Category'].unique())
        axes[1,1].set_title('Sales Distribution by Category', fontweight='bold')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
        
        print("\n🏷️ PRODUCT CATEGORY INSIGHTS:")
        print(category_analysis)
        
    def project_6_promotional_effectiveness(self):
        """Project 6: Promotional Effectiveness Analysis"""
        print("\n" + "="*50)
        print("💰 PROJECT 6: PROMOTIONAL EFFECTIVENESS ANALYSIS")
        print("="*50)
        
        # Create promotional flags
        self.df['Has_Markdown'] = (self.df['Markdown1'] > 0) | (self.df['Markdown2'] > 0)
        self.df['Promotion_Type'] = 'No Promotion'
        self.df.loc[self.df['Holiday_Flag'] == 1, 'Promotion_Type'] = 'Holiday'
        self.df.loc[self.df['Has_Markdown'] & (self.df['Holiday_Flag'] == 0), 'Promotion_Type'] = 'Markdown'
        self.df.loc[self.df['Has_Markdown'] & (self.df['Holiday_Flag'] == 1), 'Promotion_Type'] = 'Holiday + Markdown'
        
        promotion_analysis = self.df.groupby('Promotion_Type').agg({
            'Weekly_Sales': ['mean', 'count'],
            'Marketing_ROI': 'mean',
            'Total_Markdown': 'mean'
        }).round(2)
        
        promotion_analysis.columns = ['Avg_Sales', 'Weeks_Count', 'Avg_ROI', 'Avg_Markdown']
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        # Average Sales by Promotion Type
        axes[0].bar(promotion_analysis.index, promotion_analysis['Avg_Sales'])
        axes[0].set_title('Average Sales by Promotion Type', fontweight='bold')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Marketing ROI by Promotion Type
        axes[1].bar(promotion_analysis.index, promotion_analysis['Avg_ROI'])
        axes[1].set_title('Marketing ROI by Promotion Type', fontweight='bold')
        axes[1].tick_params(axis='x', rotation=45)
        
        # Promotion frequency
        axes[2].pie(promotion_analysis['Weeks_Count'], labels=promotion_analysis.index, autopct='%1.1f%%')
        axes[2].set_title('Promotion Type Distribution', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        # Markdown effectiveness by product category
        markdown_effectiveness = self.df.groupby(['Product_Category', 'Has_Markdown']).agg({
            'Weekly_Sales': 'mean',
            'Marketing_ROI': 'mean'
        }).unstack().round(2)
        
        print("\n💰 PROMOTIONAL EFFECTIVENESS:")
        print(promotion_analysis)
        print("\n📊 MARKDOWN EFFECTIVENESS BY CATEGORY:")
        print(markdown_effectiveness)
        
    def project_7_holiday_impact_analysis(self):
        """Project 7: Holiday Season Impact Analysis"""
        print("\n" + "="*50)
        print("🎄 PROJECT 7: HOLIDAY IMPACT ANALYSIS")
        print("="*50)
        
        holiday_analysis = self.df.groupby(['Holiday_Flag', 'Product_Category']).agg({
            'Weekly_Sales': 'mean',
            'Marketing_Spend_Online': 'mean',
            'Marketing_ROI': 'mean',
            'Total_Markdown': 'mean'
        }).unstack().round(2)
        
        # Calculate percentage increase during holidays
        sales_comparison = self.df.groupby(['Holiday_Flag', 'Product_Category'])['Weekly_Sales'].mean().unstack()
        sales_increase = ((sales_comparison.loc[1] - sales_comparison.loc[0]) / sales_comparison.loc[0] * 100).round(2)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        
        # Sales comparison: Holiday vs Non-Holiday
        sales_comparison.T.plot(kind='bar', ax=axes[0,0])
        axes[0,0].set_title('Sales: Holiday vs Non-Holiday', fontweight='bold')
        axes[0,0].legend(['Non-Holiday', 'Holiday'])
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Sales increase percentage during holidays
        axes[0,1].bar(sales_increase.index, sales_increase.values)
        axes[0,1].set_title('Sales Increase During Holidays (%)', fontweight='bold')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Marketing ROI comparison
        roi_comparison = self.df.groupby(['Holiday_Flag', 'Product_Category'])['Marketing_ROI'].mean().unstack()
        roi_comparison.T.plot(kind='bar', ax=axes[1,0])
        axes[1,0].set_title('Marketing ROI: Holiday vs Non-Holiday', fontweight='bold')
        axes[1,0].legend(['Non-Holiday', 'Holiday'])
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Marketing spend comparison
        spend_comparison = self.df.groupby(['Holiday_Flag', 'Product_Category'])['Marketing_Spend_Online'].mean().unstack()
        spend_comparison.T.plot(kind='bar', ax=axes[1,1])
        axes[1,1].set_title('Marketing Spend: Holiday vs Non-Holiday', fontweight='bold')
        axes[1,1].legend(['Non-Holiday', 'Holiday'])
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
        
        print("\n🎄 HOLIDAY IMPACT INSIGHTS:")
        print("Sales Increase During Holidays by Category:")
        for category, increase in sales_increase.items():
            print(f"  {category}: {increase}%")
            
    def project_8_external_factors_analysis(self):
        """Project 8: External Factors Impact Analysis"""
        print("\n" + "="*50)
        print("🌡️ PROJECT 8: EXTERNAL FACTORS IMPACT ANALYSIS")
        print("="*50)
        
        # Create bins for continuous variables
        self.df['Temp_Bin'] = pd.cut(self.df['Temperature'], bins=5)
        self.df['CPI_Bin'] = pd.cut(self.df['CPI'], bins=5)
        self.df['Unemployment_Bin'] = pd.cut(self.df['Unemployment'], bins=5)
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        
        # Temperature impact
        temp_impact = self.df.groupby('Temp_Bin')['Weekly_Sales'].mean()
        axes[0,0].bar(range(len(temp_impact)), temp_impact.values)
        axes[0,0].set_title('Sales by Temperature Range', fontweight='bold')
        axes[0,0].set_xticks(range(len(temp_impact)))
        axes[0,0].set_xticklabels([str(x) for x in temp_impact.index], rotation=45)
        
        # CPI impact
        cpi_impact = self.df.groupby('CPI_Bin')['Weekly_Sales'].mean()
        axes[0,1].bar(range(len(cpi_impact)), cpi_impact.values)
        axes[0,1].set_title('Sales by CPI Range', fontweight='bold')
        axes[0,1].set_xticks(range(len(cpi_impact)))
        axes[0,1].set_xticklabels([str(x) for x in cpi_impact.index], rotation=45)
        
        # Unemployment impact
        unemp_impact = self.df.groupby('Unemployment_Bin')['Weekly_Sales'].mean()
        axes[0,2].bar(range(len(unemp_impact)), unemp_impact.values)
        axes[0,2].set_title('Sales by Unemployment Range', fontweight='bold')
        axes[0,2].set_xticks(range(len(unemp_impact)))
        axes[0,2].set_xticklabels([str(x) for x in unemp_impact.index], rotation=45)
        
        # Fuel Price impact
        fuel_impact = self.df.groupby(pd.cut(self.df['Fuel_Price'], bins=5))['Weekly_Sales'].mean()
        axes[1,0].bar(range(len(fuel_impact)), fuel_impact.values)
        axes[1,0].set_title('Sales by Fuel Price Range', fontweight='bold')
        axes[1,0].set_xticks(range(len(fuel_impact)))
        axes[1,0].set_xticklabels([str(x) for x in fuel_impact.index], rotation=45)
        
        # Multiple regression for external factors
        X_external = self.df[['Temperature', 'Fuel_Price', 'CPI', 'Unemployment']]
        y_external = self.df['Weekly_Sales']
        
        model = LinearRegression()
        model.fit(X_external, y_external)
        
        external_coef = pd.DataFrame({
            'Factor': X_external.columns,
            'Coefficient': model.coef_,
            'Absolute_Impact': np.abs(model.coef_)
        }).sort_values('Absolute_Impact', ascending=False)
        
        axes[1,1].bar(external_coef['Factor'], external_coef['Absolute_Impact'])
        axes[1,1].set_title('Relative Impact of External Factors', fontweight='bold')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        # R-squared value
        r2_external = model.score(X_external, y_external)
        axes[1,2].text(0.5, 0.5, f'External Factors Model\nR² = {r2_external:.3f}', 
                      ha='center', va='center', transform=axes[1,2].transAxes, fontsize=14)
        axes[1,2].set_title('Model Performance', fontweight='bold')
        axes[1,2].set_xticks([])
        axes[1,2].set_yticks([])
        
        plt.tight_layout()
        plt.show()
        
        print("\n🌡️ EXTERNAL FACTORS INSIGHTS:")
        print("Relative Impact on Sales:")
        print(external_coef[['Factor', 'Coefficient']].round(4))
        
    def project_9_store_performance_comparison(self):
        """Project 9: Store Performance Comparison"""
        print("\n" + "="*50)
        print("🏪 PROJECT 9: STORE PERFORMANCE COMPARISON")
        print("="*50)
        
        store_analysis = self.df.groupby('Store').agg({
            'Weekly_Sales': ['mean', 'std', 'sum'],
            'Marketing_Spend_Online': 'mean',
            'Marketing_ROI': 'mean',
            'Date': 'nunique'
        }).round(2)
        
        store_analysis.columns = ['Avg_Sales', 'Sales_Std', 'Total_Sales', 
                                'Avg_Marketing_Spend', 'Avg_ROI', 'Weeks_Count']
        
        store_analysis = store_analysis.sort_values('Avg_ROI', ascending=False)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Average Sales by Store
        axes[0,0].bar(store_analysis.index.astype(str), store_analysis['Avg_Sales'])
        axes[0,0].set_title('Average Weekly Sales by Store', fontweight='bold')
        axes[0,0].set_xlabel('Store')
        axes[0,0].set_ylabel('Average Sales')
        
        # Marketing ROI by Store
        axes[0,1].bar(store_analysis.index.astype(str), store_analysis['Avg_ROI'])
        axes[0,1].set_title('Marketing ROI by Store', fontweight='bold')
        axes[0,1].set_xlabel('Store')
        axes[0,1].set_ylabel('ROI')
        
        # Sales variability by Store
        axes[1,0].bar(store_analysis.index.astype(str), store_analysis['Sales_Std'])
        axes[1,0].set_title('Sales Variability (Std Dev) by Store', fontweight='bold')
        axes[1,0].set_xlabel('Store')
        axes[1,0].set_ylabel('Standard Deviation')
        
        # Marketing Spend vs ROI by Store
        scatter = axes[1,1].scatter(store_analysis['Avg_Marketing_Spend'], 
                                  store_analysis['Avg_ROI'], 
                                  s=store_analysis['Avg_Sales']/10000, alpha=0.6)
        
        # Add store labels
        for i, store in enumerate(store_analysis.index):
            axes[1,1].annotate(f'Store {store}', 
                             (store_analysis['Avg_Marketing_Spend'].iloc[i], 
                              store_analysis['Avg_ROI'].iloc[i]),
                             xytext=(5, 5), textcoords='offset points', fontsize=8)
            
        axes[1,1].set_xlabel('Average Marketing Spend')
        axes[1,1].set_ylabel('Average ROI')
        axes[1,1].set_title('Marketing Efficiency by Store\n(Bubble size = Average Sales)', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        print("\n🏪 STORE PERFORMANCE RANKINGS:")
        print("Top 3 Stores by ROI:")
        print(store_analysis.head(3))
        
    def project_10_marketing_budget_optimization(self):
        """Project 10: Marketing Budget Optimization"""
        print("\n" + "="*50)
        print("💰 PROJECT 10: MARKETING BUDGET OPTIMIZATION")
        print("="*50)
        
        # Current allocation analysis
        current_allocation = self.df.groupby(['Product_Category', 'Customer_Segment']).agg({
            'Marketing_Spend_Online': 'sum',
            'Weekly_Sales': 'sum',
            'Marketing_ROI': 'mean'
        }).round(2)
        
        current_allocation['Current_Spend_Pct'] = (
            current_allocation['Marketing_Spend_Online'] / 
            current_allocation['Marketing_Spend_Online'].sum() * 100
        ).round(2)
        
        # Optimal allocation based on ROI
        roi_weights = self.df.groupby(['Product_Category', 'Customer_Segment'])['Marketing_ROI'].mean()
        total_roi_weight = roi_weights.sum()
        optimal_allocation_pct = (roi_weights / total_roi_weight * 100).round(2)
        
        # Create comparison
        allocation_comparison = pd.DataFrame({
            'Current_Allocation_Pct': current_allocation['Current_Spend_Pct'],
            'Optimal_Allocation_Pct': optimal_allocation_pct,
            'ROI': current_allocation['Marketing_ROI']
        }).dropna()
        
        allocation_comparison['Adjustment'] = (
            allocation_comparison['Optimal_Allocation_Pct'] - 
            allocation_comparison['Current_Allocation_Pct']
        ).round(2)
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Current vs Optimal allocation
        x_pos = np.arange(len(allocation_comparison))
        width = 0.35
        
        axes[0].bar(x_pos - width/2, allocation_comparison['Current_Allocation_Pct'], 
                   width, label='Current', alpha=0.7)
        axes[0].bar(x_pos + width/2, allocation_comparison['Optimal_Allocation_Pct'], 
                   width, label='Optimal', alpha=0.7)
        
        axes[0].set_xlabel('Category - Segment')
        axes[0].set_ylabel('Allocation Percentage')
        axes[0].set_title('Current vs Optimal Budget Allocation', fontweight='bold')
        axes[0].set_xticks(x_pos)
        axes[0].set_xticklabels([f"{idx[0]}-{idx[1]}" for idx in allocation_comparison.index], 
                               rotation=45, ha='right')
        axes[0].legend()
        
        # ROI vs Current Allocation
        scatter = axes[1].scatter(allocation_comparison['Current_Allocation_Pct'],
                                allocation_comparison['ROI'],
                                s=100, alpha=0.6)
        
        # Add labels
        for idx, row in allocation_comparison.iterrows():
            axes[1].annotate(f"{idx[0]}-{idx[1]}", 
                           (row['Current_Allocation_Pct'], row['ROI']),
                           xytext=(5, 5), textcoords='offset points', fontsize=8)
            
        axes[1].set_xlabel('Current Allocation Percentage')
        axes[1].set_ylabel('Marketing ROI')
        axes[1].set_title('ROI vs Current Budget Allocation', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        print("\n💰 BUDGET OPTIMIZATION RECOMMENDATIONS:")
        print("Recommended Budget Reallocation:")
        for idx, row in allocation_comparison.iterrows():
            if row['Adjustment'] > 5:
                action = "INCREASE"
            elif row['Adjustment'] < -5:
                action = "DECREASE"
            else:
                action = "MAINTAIN"
                
            if action != "MAINTAIN":
                print(f"  {action} budget for {idx[0]} - {idx[1]}: {abs(row['Adjustment']):.1f}%")
                
    def run_all_analyses(self):
        """Run all marketing analytics projects"""
        print("🚀 STARTING COMPREHENSIVE MARKETING ANALYTICS")
        print("="*60)
        
        analyses = [
            self.project_1_marketing_roi_analysis,
            self.project_2_customer_segmentation_analysis,
            self.project_3_sales_forecasting,
            self.project_4_marketing_mix_modeling,
            self.project_5_product_category_analysis,
            self.project_6_promotional_effectiveness,
            self.project_7_holiday_impact_analysis,
            self.project_8_external_factors_analysis,
            self.project_9_store_performance_comparison,
            self.project_10_marketing_budget_optimization
        ]
        
        for analysis in analyses:
            try:
                analysis()
            except Exception as e:
                print(f"❌ Error in {analysis.__name__}: {e}")
                continue
                
        print("\n" + "="*60)
        print("✅ ALL ANALYSES COMPLETED!")
        print("💡 Key insights have been printed above")

# Initialize and run all analyses
print("🔧 Initializing Marketing Analytics...")
analytics = MartAnalytics('mart.csv')
analytics.run_all_analyses()