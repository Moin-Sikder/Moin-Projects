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
├── app.py
├── data_analyzer.py
├── requirements.txt
├── readme.md
└── sample_data/
    └── marketing_data.csv
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
   · Data Overview
   · Campaign Performance
   · Customer Segmentation
   · Full Report
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


### 5. sample_data/marketing_data.csv
```csv
Campaign,Date,Spend,Clicks,Conversions,Revenue,Age,Income
Campaign_A,2024-01-01,1000,5000,250,5000,35,55000
Campaign_B,2024-01-01,800,4000,180,4000,42,68000
Campaign_C,2024-01-02,1200,6000,300,6500,28,45000
Campaign_A,2024-01-02,1100,5200,260,5200,35,55000
Campaign_B,2024-01-03,850,4200,190,4100,42,68000
Campaign_C,2024-01-03,1300,5800,320,6800,28,45000
Campaign_A,2024-01-04,1050,5100,255,5100,35,55000
Campaign_B,2024-01-04,820,4100,185,4050,42,68000
Campaign_D,2024-01-05,900,3500,150,3000,39,60000
Campaign_D,2024-01-06,950,3600,160,3200,39,60000
```
