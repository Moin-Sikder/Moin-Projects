# Customer Segmentation Analysis using RFM
# Marketing Analytics Project

# Load required libraries
library(tidyverse)
library(cluster)
library(factoextra)
library(gridExtra)
library(scales)

# Set seed for reproducibility
set.seed(123)

# Generate synthetic customer data
n_customers <- 500

customer_data <- data.frame(
  CustomerID = 1:n_customers,
  Recency = sample(1:365, n_customers, replace = TRUE), # Days since last purchase
  Frequency = sample(1:50, n_customers, replace = TRUE), # Number of purchases
  Monetary = round(runif(n_customers, 10, 2000), 2) # Total spending
)

# Display first few rows
head(customer_data)

# Basic data summary
summary(customer_data)

# Data Visualization - Initial Exploration
p1 <- ggplot(customer_data, aes(x = Recency)) +
  geom_histogram(bins = 30, fill = "steelblue", alpha = 0.7) +
  labs(title = "Distribution of Recency",
       x = "Days Since Last Purchase",
       y = "Count") +
  theme_minimal()

p2 <- ggplot(customer_data, aes(x = Frequency)) +
  geom_histogram(bins = 30, fill = "darkorange", alpha = 0.7) +
  labs(title = "Distribution of Frequency",
       x = "Number of Purchases",
       y = "Count") +
  theme_minimal()

p3 <- ggplot(customer_data, aes(x = Monetary)) +
  geom_histogram(bins = 30, fill = "darkgreen", alpha = 0.7) +
  labs(title = "Distribution of Monetary Value",
       x = "Total Spending ($)",
       y = "Count") +
  theme_minimal()

# Arrange plots in grid
grid.arrange(p1, p2, p3, ncol = 3)

# Data Preprocessing - Standardize the RFM values
rfm_data <- customer_data %>%
  select(Recency, Frequency, Monetary) %>%
  scale() %>%
  as.data.frame()

# Reverse Recency (so higher value means more recent purchase)
rfm_data$Recency <- -rfm_data$Recency

colnames(rfm_data) <- c("Recency_Score", "Frequency_Score", "Monetary_Score")

# Determine optimal number of clusters using elbow method
wss <- map_dbl(1:10, function(k) {
  kmeans(rfm_data, centers = k, nstart = 25)$tot.withinss
})

# Elbow plot
elbow_plot <- data.frame(k = 1:10, wss = wss)

ggplot(elbow_plot, aes(x = k, y = wss)) +
  geom_line(color = "steelblue", size = 1.2) +
  geom_point(color = "steelblue", size = 3) +
  labs(title = "Elbow Method for Optimal K",
       x = "Number of Clusters (K)",
       y = "Total Within-Cluster Sum of Squares") +
  scale_x_continuous(breaks = 1:10) +
  theme_minimal()

# Perform K-means clustering with 4 clusters
k <- 4
kmeans_result <- kmeans(rfm_data, centers = k, nstart = 25)

# Add cluster assignments to original data
customer_data$Cluster <- as.factor(kmeans_result$cluster)

# Cluster Visualization
# PCA for dimensionality reduction
pca_result <- prcomp(rfm_data, scale. = TRUE)
pca_df <- as.data.frame(pca_result$x[, 1:2])
pca_df$Cluster <- customer_data$Cluster

# PCA plot
ggplot(pca_df, aes(x = PC1, y = PC2, color = Cluster)) +
  geom_point(alpha = 0.7, size = 2) +
  stat_ellipse(level = 0.8) +
  labs(title = "Customer Segments - PCA Visualization",
       x = "Principal Component 1",
       y = "Principal Component 2") +
  theme_minimal() +
  scale_color_viridis_d()

# Cluster profiles
cluster_profiles <- customer_data %>%
  group_by(Cluster) %>%
  summarise(
    Count = n(),
    Percentage = n() / nrow(customer_data) * 100,
    Avg_Recency = mean(Recency),
    Avg_Frequency = mean(Frequency),
    Avg_Monetary = mean(Monetary),
    Total_Revenue = sum(Monetary)
  ) %>%
  arrange(desc(Avg_Monetary))

print(cluster_profiles)

# RFM Distribution by Cluster
p4 <- ggplot(customer_data, aes(x = Cluster, y = Recency, fill = Cluster)) +
  geom_boxplot(alpha = 0.7) +
  labs(title = "Recency by Cluster",
       y = "Days Since Last Purchase") +
  theme_minimal() +
  scale_fill_viridis_d()

p5 <- ggplot(customer_data, aes(x = Cluster, y = Frequency, fill = Cluster)) +
  geom_boxplot(alpha = 0.7) +
  labs(title = "Frequency by Cluster",
       y = "Number of Purchases") +
  theme_minimal() +
  scale_fill_viridis_d()

p6 <- ggplot(customer_data, aes(x = Cluster, y = Monetary, fill = Cluster)) +
  geom_boxplot(alpha = 0.7) +
  labs(title = "Monetary Value by Cluster",
       y = "Total Spending ($)") +
  theme_minimal() +
  scale_fill_viridis_d()

grid.arrange(p4, p5, p6, ncol = 3)

# Segment Interpretation and Marketing Recommendations
segment_descriptions <- data.frame(
  Cluster = 1:4,
  Segment_Name = c("High-Value Loyalists", "At-Risk Customers", 
                   "New/Low-Value Customers", "Regular Spenders"),
  Description = c(
    "High frequency and monetary value, recent purchases",
    "High monetary value but infrequent recent purchases", 
    "Low frequency and monetary value, potentially new customers",
    "Moderate frequency and spending, consistent customers"
  ),
  Marketing_Strategy = c(
    "Reward with exclusive offers and loyalty programs",
    "Win-back campaigns with special incentives",
    "Engage with welcome offers and education",
    "Upsell complementary products and encourage frequency"
  )
)

print(segment_descriptions)

# Revenue Analysis by Segment
revenue_plot <- ggplot(cluster_profiles, aes(x = reorder(Cluster, -Total_Revenue), y = Total_Revenue, fill = Cluster)) +
  geom_col(alpha = 0.7) +
  labs(title = "Total Revenue by Customer Segment",
       x = "Cluster",
       y = "Total Revenue ($)") +
  scale_y_continuous(labels = dollar) +
  theme_minimal() +
  scale_fill_viridis_d()

print(revenue_plot)

# Save the results
write.csv(customer_data, "customer_segmentation_results.csv", row.names = FALSE)

# Print summary insights
cat("\n=== PROJECT SUMMARY ===\n")
cat("Total Customers Analyzed:", n_customers, "\n")
cat("Number of Segments Identified:", k, "\n")
cat("Most Valuable Segment:", segment_descriptions$Segment_Name[1], "\n")
cat("Segment with Most Customers:", segment_descriptions$Segment_Name[which.max(cluster_profiles$Count)], "\n")

# Performance metrics
cat("\nClustering Performance:\n")
cat("Within-cluster sum of squares:", kmeans_result$tot.withinss, "\n")
cat("Between-cluster sum of squares:", kmeans_result$betweenss, "\n")
cat("Ratio (BSS/TSS):", round(kmeans_result$betweenss/kmeans_result$totss, 3), "\n")
