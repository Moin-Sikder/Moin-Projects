import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import plotly.graph_objects as go

# --- 1. Simulate the Dataset ---
np.random.seed(42)
n_samples = 2000

# Features:
data = {
    'Annual_Income': np.random.randint(30000, 150000, n_samples),
    'Credit_Score': np.random.randint(550, 850, n_samples),
    'Loan_Amount': np.random.randint(500, 50000, n_samples),
    'Loan_Term_Months': np.random.choice([12, 24, 36, 60], n_samples),
    'Employment_Status': np.random.choice(['Employed', 'Self-Employed', 'Unemployed'], n_samples, p=[0.7, 0.2, 0.1])
}
df = pd.DataFrame(data)

# Target (Default): Create a low base default rate (~8%)
df['Default'] = np.random.choice([0, 1], n_samples, p=[0.92, 0.08])

# Introduce correlation with key features (lower income/score -> higher default)
df.loc[df['Credit_Score'] < 650, 'Default'] = np.random.choice([0, 1], len(df[df['Credit_Score'] < 650]), p=[0.75, 0.25])
df.loc[df['Annual_Income'] < 50000, 'Default'] = np.random.choice([0, 1], len(df[df['Annual_Income'] < 50000]), p=[0.8, 0.2])

# Introduce an 'Application_Decision' for the approval rate chart
df['Application_Decision'] = np.where(df['Credit_Score'] > 620, 'Approved', 'Rejected')


# --- 2. Predictive Modeling (Logistic Regression) ---
print("--- Training Model ---")

# Prepare data
X = df[['Annual_Income', 'Credit_Score', 'Loan_Amount', 'Loan_Term_Months']]
y = df['Default']

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Handle Imbalanced Data using SMOTE (Synthetic Minority Over-sampling Technique)
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42)

# Train Logistic Regression Model
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# Calculate AUC on test set (a key model performance metric)
y_pred_proba = model.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, y_pred_proba)

print(f"Model AUC Score: {auc_score:.4f}")
print("--- Training Complete ---")


# --- 3. Dashboard Data Preparation ---

# A. Approval vs. Rejection Rates
approval_rates = df['Application_Decision'].value_counts(normalize=True).mul(100).round(2).reset_index()
approval_rates.columns = ['Decision', 'Percentage']

# B. Expected Loss Ratio by Risk Segment (simulated based on Credit Score)
df['Risk_Segment'] = pd.cut(df['Credit_Score'], 
                            bins=[0, 620, 720, 850], 
                            labels=['High Risk', 'Medium Risk', 'Low Risk'],
                            right=False)

# Simulate Expected Loss Ratio (Higher risk -> higher loss)
loss_map = {'High Risk': 0.15, 'Medium Risk': 0.05, 'Low Risk': 0.01}
loss_data = df.groupby('Risk_Segment')['Default'].mean().reset_index()
loss_data['Expected_Loss_Ratio'] = loss_data['Risk_Segment'].map(loss_map)

# C. Feature Importance (from Logistic Regression coefficients)
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    # Coefficients indicate feature weight/importance in LogReg
    'Importance': np.abs(model.coef_[0])
}).sort_values(by='Importance', ascending=False)


# --- 4. Interactive Dashboard Visualizations (Plotly Express) ---
print("\n--- Generating Dashboard Visuals ---")

# --- VISUAL 1: Approval vs. Rejection Rates (Pie Chart) ---
fig1 = px.pie(approval_rates, values='Percentage', names='Decision', 
              title='📊 Application Decision Rates',
              color='Decision',
              color_discrete_map={'Approved':'#2ECC71', 'Rejected':'#E74C3C'})
fig1.update_traces(textinfo='percent+label')
fig1.show()
print("Approval Rate: ", approval_rates.loc[approval_rates['Decision'] == 'Approved', 'Percentage'].values[0], "%")

# --- VISUAL 2: Expected Loss Ratio by Risk Segment (Bar Chart) ---
fig2 = px.bar(loss_data, x='Risk_Segment', y='Expected_Loss_Ratio',
              title='📉 Expected Portfolio Loss Ratio by Risk Segment',
              color='Risk_Segment',
              color_discrete_map={'High Risk': '#E74C3C', 'Medium Risk': '#F39C12', 'Low Risk': '#2ECC71'},
              labels={'Expected_Loss_Ratio': 'Expected Loss Ratio (Simulated)', 'Risk_Segment': 'Credit Risk Segment'},
              text=loss_data['Expected_Loss_Ratio'].apply(lambda x: f'{x:.2%}'))
fig2.update_traces(textposition='outside')
fig2.show()
print("Insight: To maximize profitability, management must focus on optimizing lending to the **Medium Risk** segment.")

# --- VISUAL 3: Feature Importance (Bar Chart) ---
fig3 = px.bar(feature_importance.head(5), x='Importance', y='Feature', 
              title='⭐ Predictive Feature Importance (Logistic Regression Coeff.)',
              orientation='h',
              color='Feature',
              color_discrete_sequence=px.colors.qualitative.Vivid)
fig3.update_layout(yaxis={'categoryorder':'total ascending'})
fig3.show()
print("Key Insight: Features with higher importance (longer bars) have the greatest impact on predicting **Default**.")

print("\n--- Dashboard Generation Complete ---")
