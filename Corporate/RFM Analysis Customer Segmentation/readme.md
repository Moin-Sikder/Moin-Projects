# Customer Segmentation Analysis using RFM

## Project Overview
This project demonstrates customer segmentation using RFM (Recency, Frequency, Monetary) analysis and K-means clustering in R. The analysis identifies distinct customer groups for targeted marketing strategies.

## Business Objective
Segment customers based on their purchasing behavior to enable personalized marketing campaigns and improve customer retention.

## Methodology
- **RFM Analysis**: Calculated Recency, Frequency, and Monetary metrics
- **K-means Clustering**: Grouped customers into 4 distinct segments
- **Data Visualization**: Created comprehensive plots to illustrate segments

## Key Features
- Synthetic customer data generation
- Data preprocessing and standardization
- Optimal cluster determination using elbow method
- Cluster profiling and interpretation
- Marketing strategy recommendations

## Customer Segments Identified
1. **High-Value Loyalists**: High frequency and spending
2. **At-Risk Customers**: High value but infrequent purchases  
3. **New/Low-Value Customers**: Low engagement and spending
4. **Regular Spenders**: Consistent moderate spending

## Files
- `customer_segmentation.R`: Main R script
- `customer_segmentation_results.csv`: Output data with cluster assignments
- `readme.md`: Project documentation

## Technologies Used
- R
- tidyverse, cluster, factorextra packages

## How to Run
1. Open `customer_segmentation.R` in RStudio
2. Install required packages if missing
3. Run the entire script
4. View generated plots and analysis results
