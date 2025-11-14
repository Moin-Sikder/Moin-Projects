!pip install pandas numpy plotly
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. SIMULATE THE DATASET ---
np.random.seed(42)
N_CUSTOMERS = 1000

# Calculate Churn_Risk and Churned arrays before defining the dictionary
churn_risk_array = np.random.beta(a=1.5, b=5, size=N_CUSTOMERS) * 0.9 + (np.random.rand(N_CUSTOMERS) * 0.1)
# Churn decision uses the calculated risk array
churned_array = (np.random.rand(N_CUSTOMERS) < (np.clip(churn_risk_array * 1.5, 0, 1) * 0.2)).astype(int)

data = {
    'Customer_ID': range(1000, 1000 + N_CUSTOMERS),
    'Age': np.random.randint(25, 70, N_CUSTOMERS),
    'Account_Type': np.random.choice(['Standard', 'Premium', 'Gold'], N_CUSTOMERS, p=[0.55, 0.3, 0.15]),
    'Branch_Location': np.random.choice(['Urban', 'Suburban', 'Rural'], N_CUSTOMERS, p=[0.45, 0.4, 0.15]),
    'CLV': np.random.lognormal(mean=7.5, sigma=0.8, size=N_CUSTOMERS).round(2),

    # Use the pre-calculated arrays
    'Churn_Risk': churn_risk_array,
    'Churned': churned_array,

    # Top 3 features driving churn (simulated impact)
    'Failed_Logins_Last_Month': np.random.randint(0, 10, N_CUSTOMERS),
    'Deposit_Decrease_Pct': np.random.uniform(0, 0.8, N_CUSTOMERS),
}

df = pd.DataFrame(data)

# Scale Churn_Risk for better visualization (0 to 100)
df['Churn_Risk_Score'] = (df['Churn_Risk'] * 100).round(1)

# --- 2. CALCULATE KEY METRICS ---
overall_churn_rate = df['Churned'].mean()

# --- 3. CREATE THE DASHBOARD VISUALIZATIONS ---

# Set up the dashboard figure with subplots
fig = make_subplots(
    rows=3, cols=2,
    specs=[
        [{"colspan": 2}, None],
        [{}, {}],
        [{}, {}]
    ],
    column_widths=[0.5, 0.5],
    row_heights=[0.35, 0.35, 0.3],
    subplot_titles=(
        f"1. Customer Lifetime Value (CLV) vs. Churn Risk Score (Overall Churn: {overall_churn_rate:.2%})",
        "2. Churn Rate by Account Type",
        "3. Top Feature Importance for Churn Prediction (Simulated)",
        "4. Simulated Retention Campaign ROI",
        "5. Churn Rate by Branch Location"
    )
)

# --- VIZ 1: CLV vs. Churn Risk Quadrant Chart (Row 1, Col 1-2) ---
fig_quadrant = px.scatter(
    df, x='CLV', y='Churn_Risk_Score', color='Churned',
    color_continuous_scale=px.colors.sequential.Plasma,
    hover_data={'Customer_ID': True, 'Churn_Risk_Score': True, 'CLV': True, 'Churned': True},
)

# Define Quadrant thresholds (simulated)
clv_threshold = df['CLV'].quantile(0.65)
risk_threshold = df['Churn_Risk_Score'].quantile(0.65)

# Add quadrant lines and annotation
fig_quadrant.add_shape(
    type="line", x0=clv_threshold, y0=0, x1=clv_threshold, y1=100,
    line=dict(color="Red", width=1, dash="dash")
)
fig_quadrant.add_shape(
    type="line", x0=0, y0=risk_threshold, x1=df['CLV'].max(), y1=risk_threshold,
    line=dict(color="Red", width=1, dash="dash")
)

# Identify the High-Value, High-Risk Quadrant (Target Segment)
fig_quadrant.add_annotation(
    x=df['CLV'].max() * 0.95, y=risk_threshold * 1.1,
    text="Target Segment: High Value, High Risk",
    showarrow=False,
    font=dict(color="Red", size=10),
    bgcolor="rgba(255, 0, 0, 0.1)"
)

# Add the trace to the subplot
for trace in fig_quadrant.data:
    fig.add_trace(trace, row=1, col=1)

# Update layout for the scatter plot within the subplot
fig.update_xaxes(title_text="Customer Lifetime Value (CLV)", row=1, col=1)
fig.update_yaxes(title_text="Churn Risk Score (0-100)", row=1, col=1)

# --- VIZ 2: Churn Rate by Account Type (Row 2, Col 1) ---
churn_by_account = df.groupby('Account_Type')['Churned'].mean().reset_index().rename(columns={'Churned': 'Churn_Rate'})
fig_account = px.bar(churn_by_account, x='Account_Type', y='Churn_Rate', text='Churn_Rate', color='Account_Type')
fig_account.update_traces(texttemplate='%{y:.2%}', textposition='outside')
fig_account.update_layout(xaxis_title='Account Type', yaxis_title='Churn Rate', showlegend=False)

for trace in fig_account.data:
    fig.add_trace(trace, row=2, col=1)

fig.update_yaxes(tickformat=".0%", row=2, col=1)

# --- VIZ 3: Top Feature Importance (Simulated) (Row 2, Col 2) ---
# Simulating a model's feature importance output
feature_importance = pd.DataFrame({
    'Feature': ['Decrease in Deposit Balance', 'Failed Login Attempts', 'No Recent Loan Inquiry', 'Age < 30'],
    'Importance': [0.45, 0.30, 0.15, 0.10]
}).sort_values('Importance', ascending=True)

fig_features = px.bar(
    feature_importance, y='Feature', x='Importance', orientation='h',
    color='Importance', color_continuous_scale='Sunsetdark'
)
fig_features.update_traces(texttemplate='%{x:.2f}', textposition='outside')
fig_features.update_layout(xaxis_title='Impact Score (SHAP/Gini)', yaxis_title='')

for trace in fig_features.data:
    fig.add_trace(trace, row=2, col=2)

fig.update_xaxes(row=2, col=2)

# --- VIZ 4: Simulated Retention Campaign ROI (Row 3, Col 1) ---
# Based on the "Target Segment: High Value, High Risk"
initial_churn_rate_target = 0.25 # Simulated high initial rate for the target segment
cost_per_offer = 50              # Personalized high-interest offer cost
clv_gained = 3000                # Avg CLV of a retained customer

# Scenario: 200 high-risk customers targeted
targeted_customers = 200
total_campaign_cost = targeted_customers * cost_per_offer
expected_churners = targeted_customers * initial_churn_rate_target

# Simulate a 30% reduction in churn for those targeted
churn_reduction_pct = 0.30
retained_customers = expected_churners * churn_reduction_pct
value_retained = retained_customers * clv_gained
roi = (value_retained - total_campaign_cost) / total_campaign_cost

roi_data = pd.DataFrame({
    'Metric': ['Value Retained (CLV)', 'Campaign Cost', 'ROI'],
    'Value': [value_retained, total_campaign_cost, roi]
})

fig_roi = go.Figure(data=[
    go.Bar(
        x=roi_data['Metric'],
        y=roi_data['Value'],
        marker_color=['green', 'red', 'blue']
    )
])
fig_roi.update_layout(yaxis_title='Amount ($)', xaxis_title='')
fig_roi.update_traces(
    text=[f'${value:,.0f}' for value in roi_data['Value'][:-1]] + [f'{roi_data["Value"].iloc[-1]:.1%}'],
    textposition='outside'
)

for trace in fig_roi.data:
    fig.add_trace(trace, row=3, col=1)

# --- VIZ 5: Churn Rate by Branch Location (Row 3, Col 2) ---
churn_by_branch = df.groupby('Branch_Location')['Churned'].mean().reset_index().rename(columns={'Churned': 'Churn_Rate'})
fig_branch = px.bar(churn_by_branch, x='Branch_Location', y='Churn_Rate', text='Churn_Rate', color='Branch_Location')
fig_branch.update_traces(texttemplate='%{y:.2%}', textposition='outside')
fig_branch.update_layout(xaxis_title='Branch Location', yaxis_title='Churn Rate', showlegend=False)

for trace in fig_branch.data:
    fig.add_trace(trace, row=3, col=2)

fig.update_yaxes(tickformat=".0%", row=3, col=2)

# --- FINAL LAYOUT AND DISPLAY ---
fig.update_layout(
    height=1200,
    title_text="🏦 Customer Churn Prediction & Retention Marketing Dashboard (Simulated Data)",
    showlegend=False,
    template="plotly_white",
    hovermode='closest'
)

fig.show()
