import streamlit as st
import pandas as pd
import plotly.express as px
from data_analyzer import MarketingDataAnalyzer
import base64
import io

# Page configuration
st.set_page_config(
    page_title="Marketing Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🎯 AI Marketing Data Analyst</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose Analysis Mode", 
                                   ["Data Overview", "Campaign Performance", 
                                    "Customer Segmentation", "Full Report"])
    
    # File upload
    uploaded_file = st.sidebar.file_uploader("Upload Marketing Data (CSV)", type="csv")
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_data.csv", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        analyzer = MarketingDataAnalyzer("temp_data.csv")
        
        if app_mode == "Data Overview":
            show_data_overview(analyzer)
        elif app_mode == "Campaign Performance":
            show_campaign_performance(analyzer)
        elif app_mode == "Customer Segmentation":
            show_customer_segmentation(analyzer)
        elif app_mode == "Full Report":
            show_full_report(analyzer)
    else:
        st.info("👆 Please upload a CSV file to get started")
        st.markdown("""
        ### Sample Data Format:
        Your CSV should include columns like:
        - `Campaign`: Campaign names
        - `Spend`: Advertising spend
        - `Revenue`: Generated revenue
        - `Clicks`: Number of clicks
        - `Conversions`: Number of conversions
        - `Date`: Date of activity
        """)

def show_data_overview(analyzer):
    st.header("📈 Data Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Explore Data"):
            shape, missing = analyzer.explore_data()
            st.success(f"Data Shape: {shape}")
            st.warning(f"Missing Values: {missing}")
    
    with col2:
        if st.button("Clean Data"):
            cleaned_df = analyzer.clean_data()
            st.success("Data cleaned successfully!")
            st.dataframe(cleaned_df.head())
    
    # Show sample data
    st.subheader("Sample Data")
    sample_data = analyzer.data.head(10)
    st.dataframe(sample_data)

def show_campaign_performance(analyzer):
    st.header("🎯 Campaign Performance Analysis")
    
    analyzer.clean_data()
    results = analyzer.campaign_performance_analysis()
    
    if 'campaign_performance' in results:
        campaign_df = results['campaign_performance']
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_spend = campaign_df['Spend'].sum()
            st.metric("Total Spend", f"${total_spend:,.2f}")
        
        with col2:
            total_revenue = campaign_df['Revenue'].sum()
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
        
        with col3:
            avg_roi = campaign_df['ROI'].mean()
            st.metric("Average ROI", f"{avg_roi:.1f}%")
        
        with col4:
            total_conversions = campaign_df['Conversions'].sum()
            st.metric("Total Conversions", f"{total_conversions:,}")
        
        # Campaign performance table
        st.subheader("Campaign Performance Metrics")
        st.dataframe(campaign_df)
        
        # Visualization
        fig = px.bar(campaign_df, x='Campaign', y='ROI', 
                     title="ROI by Campaign", color='ROI',
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

def show_customer_segmentation(analyzer):
    st.header("👥 Customer Segmentation")
    
    analyzer.clean_data()
    segmentation_results = analyzer.customer_segmentation()
    
    segmented_df = segmentation_results['segmented_data']
    segment_analysis = segmentation_results['segment_analysis']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Segment Distribution")
        segment_counts = segmented_df['Segment'].value_counts()
        fig1 = px.pie(values=segment_counts.values, 
                      names=segment_counts.index.astype(str),
                      title="Customer Segments Distribution")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Segment Analysis")
        st.dataframe(segment_analysis)
    
    # Segment characteristics
    st.subheader("Segment Characteristics")
    
    # Allow user to select features for scatter plot
    numeric_cols = segmented_df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            x_feature = st.selectbox("X-Axis Feature", numeric_cols, index=0)
        with col2:
            y_feature = st.selectbox("Y-Axis Feature", numeric_cols, index=1)
        
        fig2 = px.scatter(segmented_df, x=x_feature, y=y_feature, 
                         color='Segment', title="Customer Segments Visualization",
                         hover_data=segmented_df.columns.tolist())
        st.plotly_chart(fig2, use_container_width=True)

def show_full_report(analyzer):
    st.header("📊 Comprehensive Marketing Report")
    
    with st.spinner("Generating comprehensive analysis..."):
        report = analyzer.generate_report()
        visualization = analyzer.generate_visualizations()
    
    # Summary metrics
    st.subheader("Executive Summary")
    
    if 'summary' in report:
        summary = report['summary']
        
        cols = st.columns(4)
        metric_keys = ['total_revenue', 'total_spend', 'overall_roi', 'overall_conversion_rate']
        metric_names = ['Total Revenue', 'Total Spend', 'Overall ROI', 'Conversion Rate']
        metric_formats = ['${:,.2f}', '${:,.2f}', '{:.1f}%', '{:.2f}%']
        
        for i, (col, key, name, fmt) in enumerate(zip(cols, metric_keys, metric_names, metric_formats)):
            if key in summary:
                with col:
                    st.metric(name, fmt.format(summary[key]))
    
    # Visualization
    st.subheader("Marketing Dashboard")
    st.plotly_chart(visualization, use_container_width=True)
    
    # Key insights
    st.subheader("🔍 Key Insights")
    
    insights = [
        "• Campaign performance varies significantly across different segments",
        "• ROI optimization opportunities identified in underperforming campaigns", 
        "• Customer segmentation reveals distinct behavioral patterns",
        "• Conversion funnel analysis shows potential improvement areas"
    ]
    
    for insight in insights:
        st.write(insight)
    
    # Download report
    st.subheader("Download Report")
    
    # Convert report to CSV for download
    if 'cleaned_data' in report:
        csv = report['cleaned_data'].to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="marketing_analysis_report.csv">📥 Download Analysis Report (CSV)</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()