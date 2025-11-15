# Marketing Analytics Data Pipeline

A high-performance marketing analytics pipeline built in Go that processes clickstream and conversion data in real-time.

## Features

- **Real-time Data Processing**: Handles click and conversion events concurrently
- **Campaign Analytics**: Tracks clicks, conversions, revenue, and conversion rates
- **Web Dashboard**: Beautiful real-time dashboard with charts and metrics
- **REST API**: Full API for integrating with other systems
- **Concurrent Processing**: Efficiently handles high-volume data

## Tech Stack

- **Go**: Backend data processing and API
- **Concurrency**: Goroutines and mutexes for safe data handling
- **REST API**: HTTP endpoints for data ingestion and querying
- **Chart.js**: Real-time data visualization

## 🚀 Quick Start

**Prerequisites**

* Go 1.21+ installed on your system
* Git for cloning the repository

**Installation & Running**

1. Initialize and download dependencies:

```bash
go mod init marketing-analytics-pipeline
go mod tidy
```

2. Run the application:

```bash
go run main.go
```

3. Open your browser to:

```
http://localhost:8080
```

You should see the Marketing Analytics Dashboard with sample data already loaded!

## 📊 Using the Dashboard

**Viewing Analytics**

* The main dashboard shows real-time charts and metrics
* See total campaigns, clicks, conversions, and revenue at a glance
* Watch the charts update automatically every 5 seconds
* View conversion rates by campaign in the pie chart

**Testing with Sample Data**

The application comes with pre-loaded sample data showing:

* Three different marketing campaigns
* Click and conversion events
* Revenue tracking across different products

## 🔌 API Usage

**Record a Click Event**

```bash
curl -X POST http://localhost:8080/api/click \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "summer_sale",
    "user_id": "customer_123", 
    "source": "google",
    "ad_id": "banner_ad_456"
  }'
```

**Record a Conversion Event**

```bash
curl -X POST http://localhost:8080/api/conversion \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "summer_sale",
    "user_id": "customer_123",
    "amount": 99.99,
    "product": "premium_package"
  }'
```

**Get Analytics Data**

```bash
# Get all campaigns
curl http://localhost:8080/api/analytics

# Get specific campaign
curl http://localhost:8080/api/analytics?campaign_id=summer_sale
```

**Health Check**

```bash
curl http://localhost:8080/api/health
```

## 🎯 Example Marketing Use Cases

* **1. Track Facebook Ad Campaign**:
   · Campaign ID: fb_q1_promo
   · Source: facebook
   · Track clicks and purchases
* **2. Monitor Google Ads Performance**:
   · Campaign ID: google_search_spring
   · Source: google
   · Measure conversion rates
* **3. Compare Social Media Channels**:
   · Create campaigns for instagram, twitter, linkedin
   · Compare which platform drives most conversions

## 🛠️ Development

**Project Structure**

```
├── main.go                 # HTTP server and routes
├── config/config.go        # Configuration settings  
├── models/models.go        # Data structures
├── processor/              # Data processing logic
│   └── data_processor.go
└── data/
    └── sample_logs.txt     # Sample marketing data
```

**Adding New Features**

* Modify models/models.go to add new data fields
* Update processor/data_processor.go for new calculations
* Extend the dashboard in main.go serveDashboard function

## ❓ Troubleshooting

Port already in use?

```bash
# Use a different port
PORT=8081 go run main.go
```

Dependencies not found?

```bash
go mod tidy
```

No data showing?

* Check that data/sample_logs.txt exists
* Verify the file format matches the examples

## 📈 Next Steps

Once you have the basic pipeline running, you can:

* Connect it to real ad platforms using their APIs
* Add database storage (PostgreSQL, MongoDB)
* Implement user authentication
* Add more advanced analytics (ROI, customer lifetime value)
* Set up email/Slack notifications for high-performing campaigns
