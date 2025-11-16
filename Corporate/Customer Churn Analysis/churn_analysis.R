# Customer Churn Analysis for Marketing
# Author: [Your Name]
# Date: [Current Date]

# Load required libraries
library(dplyr)
library(ggplot2)
library(caret)
library(randomForest)
library(corrplot)

# Set random seed for reproducibility
set.seed(123)

# Create sample customer data (in real scenario, you would load your own CSV)
create_sample_data <- function() {
  n <- 1000
  customer_data <- data.frame(
    customer_id = 1:n,
    tenure_months = sample(1:60, n, replace = TRUE),
    monthly_charges = round(runif(n, 20, 120), 2),
    total_charges = round(runif(n, 50, 5000), 2),
    contract_type = sample(c("Month-to-month", "One year", "Two year"), n, replace = TRUE, prob = c(0.6, 0.3, 0.1)),
    payment_method = sample(c("Electronic check", "Credit card", "Bank transfer"), n, replace = TRUE),
    monthly_usage_gb = round(rnorm(n, 200, 50)),
    support_calls = sample(0:10, n, replace = TRUE),
    churn_status = sample(0:1, n, replace = TRUE, prob = c(0.7, 0.3))
  )
  
  # Calculate total charges based on tenure and monthly charges
  customer_data$total_charges <- customer_data$tenure_months * customer_data$monthly_charges * runif(n, 0.8, 1.2)
  
  return(customer_data)
}

# Load or create data
customer_data <- create_sample_data()

# Save sample data to CSV
write.csv(customer_data, "data/sample_customer_data.csv", row.names = FALSE)

# Display basic information
cat("=== CUSTOMER CHURN ANALYSIS ===\n")
cat("Dataset Dimensions:", dim(customer_data), "\n")
cat("Churn Rate:", round(mean(customer_data$churn_status) * 100, 2), "%\n")

# Exploratory Data Analysis
cat("\n=== EXPLORATORY DATA ANALYSIS ===\n")

# Summary statistics
summary(customer_data)

# Churn by contract type
churn_by_contract <- customer_data %>%
  group_by(contract_type) %>%
  summarise(
    total_customers = n(),
    churn_rate = mean(churn_status) * 100,
    avg_tenure = mean(tenure_months)
  )

print(churn_by_contract)

# Visualizations
# 1. Churn distribution
p1 <- ggplot(customer_data, aes(x = factor(churn_status, labels = c("Active", "Churned")))) +
  geom_bar(fill = c("steelblue", "coral2"), alpha = 0.8) +
  labs(title = "Customer Churn Distribution", 
       x = "Customer Status", 
       y = "Count") +
  theme_minimal()

# 2. Churn by contract type
p2 <- ggplot(customer_data, aes(x = contract_type, fill = factor(churn_status))) +
  geom_bar(position = "fill") +
  scale_fill_manual(values = c("steelblue", "coral2"), 
                    name = "Status",
                    labels = c("Active", "Churned")) +
  labs(title = "Churn Rate by Contract Type",
       x = "Contract Type",
       y = "Proportion") +
  theme_minimal()

# 3. Monthly charges vs tenure by churn status
p3 <- ggplot(customer_data, aes(x = tenure_months, y = monthly_charges, color = factor(churn_status))) +
  geom_point(alpha = 0.6) +
  scale_color_manual(values = c("steelblue", "coral2"),
                     name = "Status",
                     labels = c("Active", "Churned")) +
  labs(title = "Monthly Charges vs Tenure",
       x = "Tenure (Months)",
       y = "Monthly Charges ($)") +
  theme_minimal()

# Display plots
print(p1)
print(p2)
print(p3)

# Statistical Analysis
cat("\n=== STATISTICAL ANALYSIS ===\n")

# T-test for monthly charges
t_test_result <- t.test(monthly_charges ~ churn_status, data = customer_data)
cat("T-test for Monthly Charges:\n")
print(t_test_result)

# Correlation analysis
numeric_data <- customer_data %>% 
  select(tenure_months, monthly_charges, total_charges, monthly_usage_gb, support_calls, churn_status)

correlation_matrix <- cor(numeric_data)
print("Correlation Matrix:")
print(correlation_matrix)

# Predictive Modeling
cat("\n=== PREDICTIVE MODELING ===\n")

# Prepare data for modeling
model_data <- customer_data %>%
  select(-customer_id) %>%
  mutate(
    churn_status = as.factor(churn_status),
    contract_type = as.factor(contract_type),
    payment_method = as.factor(payment_method)
  )

# Split data into training and testing sets
train_index <- createDataPartition(model_data$churn_status, p = 0.8, list = FALSE)
train_data <- model_data[train_index, ]
test_data <- model_data[-train_index, ]

# Train Random Forest model
cat("Training Random Forest Model...\n")
rf_model <- randomForest(churn_status ~ ., data = train_data, ntree = 100, importance = TRUE)

# Make predictions
predictions <- predict(rf_model, test_data)

# Model evaluation
confusion_matrix <- confusionMatrix(predictions, test_data$churn_status)
print(confusion_matrix)

# Feature importance
importance <- importance(rf_model)
var_importance <- data.frame(
  feature = rownames(importance),
  importance = importance[, "MeanDecreaseGini"]
) %>%
  arrange(desc(importance))

print("Feature Importance:")
print(var_importance)

# Visualize feature importance
p4 <- ggplot(var_importance, aes(x = reorder(feature, importance), y = importance)) +
  geom_col(fill = "steelblue", alpha = 0.8) +
  coord_flip() +
  labs(title = "Feature Importance for Churn Prediction",
       x = "Features",
       y = "Importance (Mean Decrease Gini)") +
  theme_minimal()

print(p4)

# Business Insights and Recommendations
cat("\n=== MARKETING INSIGHTS & RECOMMENDATIONS ===\n")

# Key insights
cat("1. CONTRACT INSIGHTS:\n")
cat("   - Month-to-month contracts have", round(filter(churn_by_contract, contract_type == "Month-to-month")$churn_rate, 1), "% churn rate\n")
cat("   - Two-year contracts have", round(filter(churn_by_contract, contract_type == "Two year")$churn_rate, 1), "% churn rate\n")
cat("   → RECOMMENDATION: Promote long-term contract incentives\n\n")

cat("2. PRICING INSIGHTS:\n")
cat("   - Churned customers pay $", round(mean(customer_data$monthly_charges[customer_data$churn_status == 1]), 2), " on average\n")
cat("   - Active customers pay $", round(mean(customer_data$monthly_charges[customer_data$churn_status == 0]), 2), " on average\n")
cat("   → RECOMMENDATION: Review pricing strategy for high-risk segments\n\n")

cat("3. TENURE INSIGHTS:\n")
cat("   - Average tenure for churned customers:", round(mean(customer_data$tenure_months[customer_data$churn_status == 1]), 1), "months\n")
cat("   - Average tenure for active customers:", round(mean(customer_data$tenure_months[customer_data$churn_status == 0]), 1), "months\n")
cat("   → RECOMMENDATION: Focus retention efforts on customers < 12 months tenure\n")

# Save workspace and results
save.image("churn_analysis_results.RData")
cat("\nAnalysis complete. Results saved to churn_analysis_results.RData\n")