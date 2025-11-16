# 🎯 AI Marketing Data Analyst

A Python-based marketing analytics tool that provides comprehensive analysis of marketing campaigns, customer segmentation, and performance metrics.

## Features

- **Campaign Performance Analysis**: ROI, CPA, Conversion rates
- **Customer Segmentation**: K-means clustering for customer groups
- **Interactive Dashboard**: Streamlit web interface
- **Automated Reporting**: Comprehensive marketing insights
- **Data Visualization**: Interactive charts and graphs


## Project Structure:

```
'Marketing Data Analysis'/
├── sample_data/
│   └── marketing_data.csv
├── app.py
├── data_analyzer.py
├── readme.md 
└── requirements.txt
```

## Installation 

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the Application:**

```bash
streamlit run app.py
```

## Usage

1. Upload your marketing data CSV file
2. Explore different analysis modes:
   * Data Overview
   * Campaign Performance
   * Customer Segmentation
   * Full Report
3. Download insights and reports

## Sample Data Format

Your CSV should include columns like:

* Campaign: Campaign names
* Spend: Advertising spend
* Revenue: Generated revenue
* Clicks: Number of clicks
* Conversions: Number of conversions
* Date: Date of activity

## Technologies Used

* Python
* Pandas, NumPy
* Scikit-learn
* Plotly, Matplotlib
* Streamlit

## Contributing

Feel free to submit issues and enhancement requests!
