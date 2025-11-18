# =============================================================================
# COMPLETE MARKETING ANALYSIS WITH FILE UPLOAD - GOOGLE COLAB
# =============================================================================

# STEP 1: INSTALL REQUIRED PACKAGES
cat("📦 STEP 1: Installing packages...\n")
install.packages(c("tidyverse", "plotly", "caret", "forecast", "tseries", "corrplot", "DT", "lubridate"))
library(tidyverse)
library(lubridate)
library(plotly)
cat("✅ Packages installed successfully!\n\n")

# STEP 2: FILE UPLOAD FUNCTION
upload_mart_csv <- function() {
  cat("📂 STEP 2: File Upload\n")
  cat("=====================\n")
  
  df <- NULL
  
  # Method 1: Try file.choose() for local files
  if(interactive()) {
    cat("Method 1: Please select your mart.csv file...\n")
    tryCatch({
      file_path <- file.choose()
      df <- read.csv(file_path)
      cat("✅ File uploaded successfully!\n")
    }, error = function(e) {
      cat("❌ File selection cancelled or failed.\n")
    })
  }
  
  # Method 2: If file.choose fails, use sample data
  if(is.null(df)) {
    cat("\nMethod 2: Using sample data for demonstration...\n")
    cat("Please upload your actual mart.csv file to Colab storage for real analysis.\n")
    
    # Create realistic sample data
    set.seed(123)
    dates <- seq(as.Date("2025-01-01"), by = "week", length.out = 12)
    
    df <- data.frame(
      Store = rep(c(10, 3, 25, 42), each = 12),
      Date = rep(dates, 4),
      Weekly_Sales = round(c(
        # Store 10
        rnorm(12, 1600000, 200000),
        # Store 3
        rnorm(12, 450000, 80000),
        # Store 25
        rnorm(12, 800000, 150000),
        # Store 42
        rnorm(12, 700000, 100000)
      ), 2),
      Holiday_Flag = rep(c(0,0,0,1,0,0,0,0,0,1,0,0), 4),
      Temperature = round(runif(48, 20, 80), 2),
      Fuel_Price = round(seq(3.2, 2.9, length.out = 48), 3),
      Marketing_Spend_Online = round(runif(48, 3000, 15000), 2),
      Product_Category = sample(c("Grocery", "Electronics", "Apparel"), 48, replace = TRUE),
      Customer_Segment = sample(c("Family", "Premium", "Value"), 48, replace = TRUE)
    )
    
    cat("⚠️  Sample data loaded. To use your own file:\n")
    cat("1. Click the folder icon 📁 in left sidebar\n")
    cat("2. Upload your mart.csv file\n")
    cat("3. Use this code: df <- read.csv('mart.csv')\n\n")
  }
  
  # Convert date column
  df$Date <- as.Date(df$Date)
  
  cat("📊 Data Summary:\n")
  cat("Rows:", nrow(df), "| Columns:", ncol(df), "\n")
  cat("Date range:", as.character(min(df$Date)), "to", as.character(max(df$Date)), "\n")
  cat("Stores:", paste(unique(df$Store), collapse = ", "), "\n\n")
  
  return(df)
}

# STEP 3: LOAD YOUR DATA
cat("🔄 Loading your data...\n")
df <- upload_mart_csv()
cat("✅ Data loaded successfully!\n\n")

# STEP 4: PROJECT 1 - MARKETING PERFORMANCE DASHBOARD
project1_dashboard <- function(df) {
  cat("🎯 PROJECT 1: MARKETING PERFORMANCE DASHBOARD\n")
  cat("============================================\n")
  
  # 1. Basic Metrics
  metrics <- df %>%
    summarise(
      Total_Sales = sum(Weekly_Sales),
      Total_Marketing_Spend = sum(Marketing_Spend_Online),
      Overall_ROI = round(Total_Sales / Total_Marketing_Spend, 2),
      Avg_Weekly_Sales = mean(Weekly_Sales),
      Number_of_Stores = n_distinct(Store),
      Date_Range = paste(min(Date), "to", max(Date))
    )
  
  cat("📈 KEY PERFORMANCE INDICATORS:\n")
  cat("Total Sales: $", format(metrics$Total_Sales, big.mark = ","), "\n")
  cat("Total Marketing Spend: $", format(metrics$Total_Marketing_Spend, big.mark = ","), "\n")
  cat("Overall ROI: ", metrics$Overall_ROI, "\n")
  cat("Average Weekly Sales: $", format(round(metrics$Avg_Weekly_Sales), big.mark = ","), "\n")
  cat("Number of Stores: ", metrics$Number_of_Stores, "\n\n")
  
  # 2. ROI by Category
  roi_by_category <- df %>%
    group_by(Product_Category) %>%
    summarise(
      Total_Sales = sum(Weekly_Sales),
      Marketing_Spend = sum(Marketing_Spend_Online),
      ROI = round(Total_Sales / Marketing_Spend, 2),
      .groups = 'drop'
    ) %>%
    arrange(desc(ROI))
  
  cat("📊 ROI BY PRODUCT CATEGORY:\n")
  print(roi_by_category)
  cat("\n")
  
  # 3. Visualization
  p1 <- ggplot(roi_by_category, aes(x = reorder(Product_Category, ROI), y = ROI, fill = Product_Category)) +
    geom_col() +
    coord_flip() +
    labs(title = "Marketing ROI by Product Category",
         x = "Product Category", y = "Return on Investment (ROI)") +
    theme_minimal() +
    scale_fill_brewer(palette = "Set2")
  
  print(p1)
  
  cat("✅ Project 1 Completed!\n\n")
}

# STEP 5: PROJECT 2 - MARKETING MIX MODELING
project2_marketing_mix <- function(df) {
  cat("🔍 PROJECT 2: MARKETING MIX MODELING\n")
  cat("===================================\n")
  
  # 1. Correlation Analysis
  numeric_cols <- df %>% select(where(is.numeric))
  
  if(ncol(numeric_cols) > 1) {
    cor_matrix <- cor(numeric_cols, use = "complete.obs")
    
    cat("📈 CORRELATION MATRIX:\n")
    print(round(cor_matrix, 3))
    cat("\n")
    
    # 2. Marketing Effectiveness Model
    if("Weekly_Sales" %in% colnames(df) && "Marketing_Spend_Online" %in% colnames(df)) {
      model <- lm(Weekly_Sales ~ Marketing_Spend_Online + Holiday_Flag + Temperature, data = df)
      
      cat("📊 MARKETING EFFECTIVENESS MODEL:\n")
      print(summary(model))
      
      # 3. Key Insights
      marketing_effect <- coef(model)["Marketing_Spend_Online"]
      cat("💡 KEY INSIGHT: Each $1 in marketing generates $", round(marketing_effect, 2), " in sales\n")
    }
  }
  
  cat("✅ Project 2 Completed!\n\n")
}

# STEP 6: PROJECT 3 - CUSTOMER SEGMENT ANALYSIS
project3_customer_analysis <- function(df) {
  cat("👥 PROJECT 3: CUSTOMER SEGMENT ANALYSIS\n")
  cat("======================================\n")
  
  if("Customer_Segment" %in% colnames(df)) {
    # 1. Segment Performance
    segment_analysis <- df %>%
      group_by(Customer_Segment) %>%
      summarise(
        Total_Sales = sum(Weekly_Sales),
        Avg_Sales = mean(Weekly_Sales),
        Total_Marketing = sum(Marketing_Spend_Online),
        ROI = round(Total_Sales / Total_Marketing, 2),
        Transaction_Count = n(),
        .groups = 'drop'
      ) %>%
      arrange(desc(ROI))
    
    cat("🎯 CUSTOMER SEGMENT PERFORMANCE:\n")
    print(segment_analysis)
    cat("\n")
    
    # 2. Visualization
    p_segment <- ggplot(segment_analysis, aes(x = reorder(Customer_Segment, ROI), y = ROI, fill = Customer_Segment)) +
      geom_col() +
      coord_flip() +
      labs(title = "Marketing ROI by Customer Segment",
           x = "Customer Segment", y = "ROI") +
      theme_minimal() +
      scale_fill_brewer(palette = "Set1")
    
    print(p_segment)
    
    # 3. Best Performing Segment
    best_segment <- segment_analysis[1, ]
    cat("🏆 BEST PERFORMING SEGMENT: ", best_segment$Customer_Segment, 
        " (ROI: ", best_segment$ROI, ")\n", sep = "")
  } else {
    cat("⚠️  Customer_Segment column not found in data.\n")
  }
  
  cat("✅ Project 3 Completed!\n\n")
}

# STEP 7: MAIN MENU
run_analysis <- function() {
  cat("
🎯 R MARKETING ANALYSIS - MAIN MENU
===================================

Choose your analysis:

1. 📊 Marketing Performance Dashboard
2. 🔍 Marketing Mix Modeling  
3. 👥 Customer Segment Analysis
4. 📈 All Projects Together
5. 🔄 Reload Data

")
  
  choice <- readline(prompt = "Enter your choice (1-5): ")
  
  cat("\n" + strrep("=", 50) + "\n")
  
  switch(choice,
         "1" = project1_dashboard(df),
         "2" = project2_marketing_mix(df),
         "3" = project3_customer_analysis(df),
         "4" = {
           project1_dashboard(df)
           project2_marketing_mix(df)
           project3_customer_analysis(df)
         },
         "5" = {
           cat("🔄 Reloading data...\n")
           df <<- upload_mart_csv()
         },
         {
           cat("❌ Invalid choice. Please enter 1-5.\n")
         }
  )
  
  cat(strrep("=", 50) + "\n\n")
}

# STEP 8: RUN THE ANALYSIS
cat("🚀 STARTING MARKETING ANALYSIS...\n")
cat("=================================\n\n")

# Run the main menu
run_analysis()

# Option to run again
while(TRUE) {
  continue <- readline(prompt = "Run another analysis? (y/n): ")
  if(tolower(continue) %in% c("y", "yes")) {
    run_analysis()
  } else {
    cat("🎉 Analysis complete! Thank you for using R Marketing Analytics!\n")
    break
  }
}
