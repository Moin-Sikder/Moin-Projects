!pip install altair pandas vega_datasets

import pandas as pd
import numpy as np
import altair as alt
import random

# --- 2. Simulated Data Generation ---
def generate_simulated_data(n_days=60):
    """Generates a DataFrame with simulated task management data."""
    tasks = ['Coding/Development', 'Meetings', 'Documentation/Planning', 'Email/Admin', 'Learning/Training']
    statuses = ['Completed', 'In Progress', 'Blocked']
    priorities = ['High', 'Medium', 'Low']
    
    # Create dates ending today's date (simulated)
    dates = pd.to_datetime(pd.date_range(end='2025-11-15', periods=n_days, freq='D'))
    
    data = []
    for date in dates:
        num_tasks = np.random.randint(5, 12)
        for _ in range(num_tasks):
            time_spent = np.random.uniform(0.5, 4.0)
            status = random.choice(statuses)
            
            data.append({
                'Date': date,
                'Task Category': random.choice(tasks),
                'Time Spent (Hours)': round(time_spent, 1),
                'Status': status,
                'Priority': random.choice(priorities),
                'Completed': 1 if status == 'Completed' else 0
            })
            
    df = pd.DataFrame(data)
    return df

df = generate_simulated_data(n_days=60)

# --- 3. Dashboard Visualizations (Altair) ---

print("--- 🎯 Personalized Task Management Dashboard ---")

# --- Metric 1: Time Allocation by Category (Donut Chart) ---
time_by_category = df.groupby('Task Category', as_index=False)['Time Spent (Hours)'].sum()
time_by_category['Percentage'] = (time_by_category['Time Spent (Hours)'] / time_by_category['Time Spent (Hours)'].sum())

base = alt.Chart(time_by_category).encode(
    theta=alt.Theta("Time Spent (Hours)", stack=True)
)

pie = base.mark_arc(outerRadius=120, innerRadius=80).encode(
    color=alt.Color("Task Category"),
    order=alt.Order("Time Spent (Hours)", sort="descending"),
    tooltip=["Task Category", "Time Spent (Hours)", alt.Tooltip("Percentage", format=".1%")]
)

text = base.mark_text(radius=140).encode(
    text=alt.Text("Percentage", format=".1%"),
    order=alt.Order("Time Spent (Hours)", sort="descending"),
    color=alt.value("black") 
)

chart1 = (pie + text).properties(
    title='Time Allocation by Task Category',
    height=300,
    width=400
)

# --- Metric 2: Daily Completion Trend (Line Chart) ---
daily_completion = df.groupby('Date').agg(
    Completed_Tasks=('Completed', 'sum'),
    Total_Tasks=('Completed', 'count')
).reset_index()
daily_completion['Completion Rate'] = (daily_completion['Completed_Tasks'] / daily_completion['Total_Tasks'])

chart2 = alt.Chart(daily_completion).mark_line(point=True).encode(
    x=alt.X('Date', axis=alt.Axis(title='Day')),
    y=alt.Y('Completion Rate', axis=alt.Axis(format='.0%', title='Completion Rate')),
    tooltip=['Date', alt.Tooltip('Completion Rate', format='.1%')]
).properties(
    title='Daily Task Completion Rate Trend',
    height=300,
    width=500
)

# --- Metric 3: Completion by Priority (Bar Chart) ---
priority_metrics = df.groupby('Priority', as_index=False).agg(
    Total_Tasks=('Status', 'count'),
    Completed_Tasks=('Completed', 'sum')
)

chart3_base = alt.Chart(priority_metrics).encode(
    x=alt.X('Total_Tasks', title='Count')
)

# Layer 1: Total Tasks
total_bar = chart3_base.mark_bar(color='skyblue').encode(
    y=alt.Y('Priority', sort='-x', title='Task Priority'),
    tooltip=['Priority', 'Total_Tasks']
).properties(title='Task Volume by Priority')

# Layer 2: Completed Tasks (using a different color and encoding)
completed_bar = alt.Chart(priority_metrics).mark_bar(color='lightcoral').encode(
    y=alt.Y('Priority', sort='-x'),
    x='Completed_Tasks',
    tooltip=['Priority', 'Completed_Tasks']
)

chart3 = (total_bar + completed_bar).resolve_scale(
    x='shared'
).properties(
    title='Task Volume (Blue) vs. Completed (Red) by Priority',
    height=200,
    width=500
)


# Combine the charts for the final dashboard display
# Use '|' to display side-by-side or '&' for layered
final_dashboard = (chart1 | (chart2 & chart3)).properties(
    title="Personalized Task Performance Dashboard"
).configure_title(
    fontSize=20,
    anchor='start',
    color='gray'
)

# Display the dashboard in Colab
final_dashboard
