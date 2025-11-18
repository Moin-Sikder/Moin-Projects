# --- 1. Load Necessary Packages ---

# Install and load required packages
if(!requireNamespace("dplyr", quietly = TRUE)) install.packages("dplyr")
if(!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
library(dplyr)
library(ggplot2)

# --- 2. Load the Dataset ---

# IMPORTANT: Ensure 'mart.csv' is uploaded to your Colab session storage.
data <- read.csv("mart.csv", header = TRUE)

print("Initial Data Head:")
print(head(data))
print("---")

# --- 3. Data Preparation (Type Conversion) ---

# Convert Date column to Date format
data$Date <- as.Date(data$Date, format = "%Y-%m-%d")

# Convert categorical variables to factor type for proper regression analysis
data <- data %>%
  mutate(
    Store = as.factor(Store),
    Holiday_Flag = as.factor(Holiday_Flag), # 0 = No Holiday, 1 = Holiday
    Product_Category = as.factor(Product_Category),
    Customer_Segment = as.factor(Customer_Segment)
  )

print("Data Structure after conversion:")
print(str(data))
print("---")


# --- 4. Multiple Linear Regression Model ---

# Model to predict Weekly_Sales based on marketing, economic, and segmentation factors.
model_sales <- lm(
  Weekly_Sales ~ Markdown1 + Markdown2 + Marketing_Spend_Online +
                 Holiday_Flag + Temperature + Fuel_Price +
                 CPI + Unemployment + Product_Category + Customer_Segment,
  data = data
)

# --- 5. Review Model Results and Interpretation ---

print("--- Model Summary (Promotional Effectiveness) ---")
# Print the full summary of the linear model
summary(model_sales)
