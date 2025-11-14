# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

# --- 1. Data Simulation ---
print("--- 1. Generating Simulated Sales Data ---")
# Define the date range (e.g., 3 years of daily data)
date_range = pd.date_range(start='2022-01-01', periods=1095, freq='D')
n_days = len(date_range)

# Simulate sales data: Base + Trend + Seasonality + Noise
base_sales = 500
trend = np.linspace(0, 50, n_days)
# Weekly Seasonality (higher sales on weekends)
weekly_seasonality = 10 * np.sin(2 * np.pi * np.arange(n_days) / 7)
# Yearly Seasonality (peak around holidays/Q4)
yearly_seasonality = 50 * np.sin(2 * np.pi * np.arange(n_days) / 365)
noise = np.random.normal(0, 15, n_days)

# Total Sales
simulated_sales = (base_sales + trend + weekly_seasonality + yearly_seasonality + noise).astype(int)
simulated_sales[simulated_sales < 0] = 0 # Ensure no negative sales

# Create the DataFrame
df = pd.DataFrame({'Date': date_range, 'Sales': simulated_sales})
df = df.set_index('Date')
print(f"Data Generated: {len(df)} records from {df.index.min().date()} to {df.index.max().date()}")

# --- 2. Sales Forecasting (ARIMA Model) ---
print("\n--- 2. Performing ARIMA Forecasting ---")

# Define the split point for training/testing (last 90 days)
split_date = df.index[-90] 
train_data = df[:split_date]

# FIX: Use .copy() to avoid SettingWithCopyWarning
test_data = df[split_date:].copy()

# Flag to check if ARIMA succeeded
arima_success = True

# Fit ARIMA model
try:
    # Setting enforce_stationarity/invertibility=False for simulated data robustness
    model = ARIMA(train_data['Sales'], order=(5, 1, 0), enforce_stationarity=False, enforce_invertibility=False)
    model_fit = model.fit()
    print("ARIMA Model Fitted Successfully.")
except Exception as e:
    print(f"Error fitting ARIMA: {e}. Using last actual sales as a simple naive forecast.")
    # Fallback forecast
    test_data['Forecast'] = train_data['Sales'].iloc[-1]
    arima_success = False
else:
    # Forecast the test period
    forecast_steps = len(test_data)
    forecast = model_fit.get_forecast(steps=forecast_steps)
    
    # CRITICAL FIX: Use .values to avoid index misalignment and NaN errors
    test_data['Forecast'] = forecast.predicted_mean.values

    # Calculate Next Quarter (90 days) Forecast for Management Insight
    next_quarter_start = test_data.index[-1] + pd.Timedelta(days=1)
    next_quarter_dates = pd.date_range(start=next_quarter_start, periods=90, freq='D')
    
    # CRITICAL FIX: Used 'next_quarter_dates' for steps (resolved NameError)
    next_quarter_forecast = model_fit.get_forecast(steps=len(next_quarter_dates))
    
    next_quarter_df = pd.DataFrame({
        'Date': next_quarter_dates,
        'Forecasted Sales': next_quarter_forecast.predicted_mean.values.astype(int)
    }).set_index('Date')
    print(f"Forecasted next 90 days starting: {next_quarter_df.index.min().date()}")


# --- 3. Error Metrics & Safety Stock Calculation ---
print("\n--- 3. Error Metrics and Safety Stock ---")

# Calculate Mean Squared Error (MSE) and Root Mean Squared Error (RMSE)
mse = mean_squared_error(test_data['Sales'], test_data['Forecast'])
rmse = np.sqrt(mse)

# Calculate Mean Absolute Deviation (MAD) of the residuals for Safety Stock
residuals = test_data['Sales'] - test_data['Forecast']
mad = np.mean(np.abs(residuals))

# --- Management Insight: Suggested Safety Stock ---
# Safety Stock = Z-score * MAD * sqrt(Lead Time in days)
# Using Z-score for 95% service level (1.645) and a lead time (LT) of 7 days
Z_score = 1.645
Lead_Time_Days = 7
Safety_Stock_Daily = Z_score * mad * np.sqrt(Lead_Time_Days)
Safety_Stock_Daily = int(np.ceil(Safety_Stock_Daily))

print(f"**Error Metrics (Test Period - {len(test_data)} days):**")
print(f"  > RMSE: {rmse:.2f}")
print(f"  > MAD: {mad:.2f}")

print("\n**Inventory Management Insight:**")
print(f"  > Suggested Daily Safety Stock (95% Service Level, 7-day LT): **{Safety_Stock_Daily} units**")
if arima_success:
    # Display suggested average demand for the next quarter
    avg_next_quarter_demand = next_quarter_df['Forecasted Sales'].mean().astype(int)
    print(f"  > Suggested Average Daily Demand (Next Quarter): **{avg_next_quarter_demand} units**")


# --- 4. Visualization (Dashboard Element) ---
print("\n--- 4. Generating Visualization (Actual vs. Forecast) ---")

plt.figure(figsize=(14, 7))
sns.set_style("whitegrid")

# Plot Actual Sales History
plt.plot(df.index, df['Sales'], label='Actual Sales (Full History)', color='grey', alpha=0.6)

# Highlight the Training and Test Periods Split
plt.axvline(x=split_date, color='red', linestyle='--', label='Forecast Start')

# Plot Test Actual Sales
plt.plot(test_data.index, test_data['Sales'], label='Actual Sales (Test Period)', color='blue')

# Plot Forecasted Sales
plt.plot(test_data.index, test_data['Forecast'], label='Forecasted Sales (Test Period)', color='orange', linestyle='--')

# Plot Next Quarter Forecast (if ARIMA succeeded)
if arima_success:
    plt.plot(next_quarter_df.index, next_quarter_df['Forecasted Sales'], label='Next Quarter Forecast', color='green', linestyle=':')

# Title and Labels
plt.title('Sales Forecasting & Inventory Optimization Dashboard', fontsize=16, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Sales Volume (Units)')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

# Final output for quick reference
print("\n--- Dashboard Summary ---")
print(f"RMSE: {rmse:.2f} | Suggested Daily Safety Stock: {Safety_Stock_Daily} units")
