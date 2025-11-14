!pip install pandas numpy scikit-learn plotly
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. SIMULATE ADVANCED CUSTOMER DATASET ---

np.random.seed(42)
n_customers = 500

data = {
    # Monetary Value: High, Medium, Low clusters
    'Monetary': np.concatenate([
        np.random.normal(500, 150, 150),
        np.random.normal(1500, 400, 200),
        np.random.normal(3500, 600, 150)
    ]).clip(min=100),

    # Frequency: High-Frequency, Low-Frequency
    'Frequency': np.concatenate([
        np.random.poisson(2, 150),
        np.random.poisson(6, 200),
        np.random.poisson(12, 150)
    ]).clip(min=1),

    # Recency (Days since last purchase): Recent, Less Recent
    'Recency': np.concatenate([
        np.random.randint(1, 30, 150),
        np.random.randint(30, 90, 200),
        np.random.randint(90, 180, 150)
    ]),

    # Engagement Score (e.g., website visits, email clicks)
    'Engagement_Score': np.concatenate([
        np.random.normal(2, 1.5, 150),
        np.random.normal(5, 2, 200),
        np.random.normal(8, 2.5, 150)
    ]).clip(min=0)
}

df = pd.DataFrame(data)

# --- 2. DATA PREPARATION (SCALING) ---

# Select the features for clustering
X = df[['Monetary', 'Frequency', 'Recency', 'Engagement_Score']]

# It is critical to scale features for K-Means
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- 3. K-MEANS CLUSTERING ---

# Determine the number of clusters (e.g., 4)
k = 4
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Convert cluster ID to categorical for better visualization labels
df['Cluster_ID'] = 'Segment ' + (df['Cluster'] + 1).astype(str)

# --- 4. CREATE THE VISUAL DASHBOARD ---

# Calculate the mean profile for each segment for the bar chart
segment_profiles = df.groupby('Cluster_ID')[['Monetary', 'Frequency', 'Recency', 'Engagement_Score']].mean().reset_index()
segment_profiles = segment_profiles.melt(id_vars='Cluster_ID', var_name='Metric', value_name='Mean_Value')


# Create Subplots for the "Dashboard"
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Segment Scatter Plot (Frequency vs. Monetary)", "Average Segment Profile"),
    # Set the widths for better layout
    column_widths=[0.6, 0.4]
)

# Plot 1: Scatter Plot (Relationship)
scatter_fig = px.scatter(
    df,
    x='Frequency',
    y='Monetary',
    color='Cluster_ID',
    hover_data=['Recency', 'Engagement_Score'],
    title='Customer Segments based on Key RFM Metrics',
    # Ensure the title is inside the main plot for clean layout
    template="plotly_white"
)

# Add the scatter plot trace to the subplot
for trace in scatter_fig.data:
    fig.add_trace(trace, row=1, col=1)

# Update layout for the scatter plot within the subplot
fig.update_xaxes(title_text="Frequency (Purchases/Time)", row=1, col=1)
fig.update_yaxes(title_text="Monetary Value ($)", row=1, col=1)

# Plot 2: Bar Chart (Profile)
bar_fig = px.bar(
    segment_profiles,
    x='Metric',
    y='Mean_Value',
    color='Cluster_ID',
    barmode='group',
    title='Mean Metric Value by Segment',
    template="plotly_white"
)

# Add the bar chart trace to the subplot
for trace in bar_fig.data:
    fig.add_trace(trace, row=1, col=2)

# Final Layout Adjustments
fig.update_layout(
    height=600,
    width=1200,
    title_text="**K-Means Customer Segmentation Dashboard**",
    legend_title="Customer Segment"
)

# Display the interactive dashboard
fig.show()

# --- 5. PRINT THE CLUSTER PROFILES (STRATEGIC INSIGHTS) ---

print("\n--- Segment Mean Profiles (for strategic insight) ---\n")
print(df.groupby('Cluster_ID')[['Monetary', 'Frequency', 'Recency', 'Engagement_Score']].mean().sort_values(by='Monetary', ascending=False).to_markdown(numalign="left", stralign="left", floatfmt=".2f"))
