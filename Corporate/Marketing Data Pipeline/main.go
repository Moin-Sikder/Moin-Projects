package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "sync"
    "time"

    "marketing-analytics-pipeline/config"
    "marketing-analytics-pipeline/models"
    "marketing-analytics-pipeline/processor"
)

var (
    analyticsData = make(map[string]*models.CampaignStats)
    mutex         = &sync.RWMutex{}
)

func main() {
    // Load configuration
    cfg := config.LoadConfig()

    // Process sample data file
    fmt.Println("🚀 Starting Marketing Analytics Pipeline...")
    fmt.Printf("Processing data from: %s\n", cfg.DataFile)

    // Process historical data
    processor.ProcessFile(cfg.DataFile, analyticsData, mutex)

    // Start web server for real-time data
    startWebServer(cfg.Port)
}

func startWebServer(port string) {
    router := http.NewServeMux()

    // API endpoints
    router.HandleFunc("/api/click", handleClickEvent)
    router.HandleFunc("/api/conversion", handleConversionEvent)
    router.HandleFunc("/api/analytics", handleAnalyticsRequest)
    router.HandleFunc("/api/health", handleHealthCheck)

    // Serve dashboard
    router.HandleFunc("/", serveDashboard)

    fmt.Printf("📊 Analytics Dashboard running on http://localhost:%s\n", port)
    fmt.Printf("📈 API endpoints available at http://localhost:%s/api/analytics\n", port)

    log.Fatal(http.ListenAndServe(":"+port, router))
}

func handleClickEvent(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var click models.ClickEvent
    if err := json.NewDecoder(r.Body).Decode(&click); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    click.Timestamp = time.Now()
    
    mutex.Lock()
    processor.ProcessClick(click, analyticsData)
    mutex.Unlock()

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{
        "status":  "success",
        "message": "Click event recorded",
    })
}

func handleConversionEvent(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var conversion models.ConversionEvent
    if err := json.NewDecoder(r.Body).Decode(&conversion); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    conversion.Timestamp = time.Now()
    
    mutex.Lock()
    processor.ProcessConversion(conversion, analyticsData)
    mutex.Unlock()

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{
        "status":  "success",
        "message": "Conversion event recorded",
    })
}

func handleAnalyticsRequest(w http.ResponseWriter, r *http.Request) {
    campaignID := r.URL.Query().Get("campaign_id")

    mutex.RLock()
    defer mutex.RUnlock()

    w.Header().Set("Content-Type", "application/json")

    if campaignID != "" {
        if stats, exists := analyticsData[campaignID]; exists {
            json.NewEncoder(w).Encode(stats)
            return
        }
        http.Error(w, "Campaign not found", http.StatusNotFound)
        return
    }

    // Return all analytics
    json.NewEncoder(w).Encode(analyticsData)
}

func handleHealthCheck(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{
        "status":    "healthy",
        "timestamp": time.Now(),
        "data": map[string]interface{}{
            "total_campaigns": len(analyticsData),
            "uptime":          time.Since(startTime).String(),
        },
    })
}

func serveDashboard(w http.ResponseWriter, r *http.Request) {
    dashboardHTML := `
<!DOCTYPE html>
<html>
<head>
    <title>Marketing Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #007bff; }
        .chart-container { margin: 30px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Marketing Analytics Dashboard</h1>
        <p>Real-time campaign performance monitoring</p>
        
        <div class="stats-grid" id="statsGrid">
            <!-- Stats will be populated by JavaScript -->
        </div>
        
        <div class="chart-container">
            <canvas id="performanceChart" width="400" height="200"></canvas>
        </div>
        
        <div class="chart-container">
            <canvas id="conversionChart" width="400" height="200"></canvas>
        </div>
    </div>

    <script>
        async function loadAnalytics() {
            try {
                const response = await fetch('/api/analytics');
                const data = await response.json();
                updateDashboard(data);
            } catch (error) {
                console.error('Error loading analytics:', error);
            }
        }

        function updateDashboard(data) {
            const statsGrid = document.getElementById('statsGrid');
            const campaigns = Object.values(data);
            
            if (campaigns.length === 0) {
                statsGrid.innerHTML = '<p>No campaign data available. Send some events to see analytics.</p>';
                return;
            }

            // Calculate totals
            const totals = campaigns.reduce((acc, campaign) => {
                acc.clicks += campaign.TotalClicks;
                acc.conversions += campaign.TotalConversions;
                acc.revenue += campaign.TotalRevenue;
                return acc;
            }, { clicks: 0, conversions: 0, revenue: 0 });

            // Update stats grid
            statsGrid.innerHTML = \`
                <div class="stat-card">
                    <h3>Total Campaigns</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #007bff;">\${campaigns.length}</p>
                </div>
                <div class="stat-card">
                    <h3>Total Clicks</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #28a745;">\${totals.clicks}</p>
                </div>
                <div class="stat-card">
                    <h3>Total Conversions</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #dc3545;">\${totals.conversions}</p>
                </div>
                <div class="stat-card">
                    <h3>Total Revenue</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #ffc107;">$\${totals.revenue.toFixed(2)}</p>
                </div>
            \`;

            // Update charts
            updateCharts(campaigns);
        }

        function updateCharts(campaigns) {
            const ctx1 = document.getElementById('performanceChart').getContext('2d');
            const ctx2 = document.getElementById('conversionChart').getContext('2d');
            
            const campaignNames = campaigns.map(c => c.CampaignID);
            const clicks = campaigns.map(c => c.TotalClicks);
            const conversions = campaigns.map(c => c.TotalConversions);
            
            // Performance Chart
            new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: campaignNames,
                    datasets: [
                        {
                            label: 'Clicks',
                            data: clicks,
                            backgroundColor: '#007bff'
                        },
                        {
                            label: 'Conversions',
                            data: conversions,
                            backgroundColor: '#28a745'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Campaign Performance'
                        }
                    }
                }
            });

            // Conversion Rate Chart
            new Chart(ctx2, {
                type: 'pie',
                data: {
                    labels: campaignNames,
                    datasets: [{
                        data: campaigns.map(c => c.ConversionRate),
                        backgroundColor: ['#007bff', '#28a745', '#dc3545', '#ffc107', '#6f42c1']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Conversion Rate by Campaign (%)'
                        }
                    }
                }
            });
        }

        // Load analytics every 5 seconds
        loadAnalytics();
        setInterval(loadAnalytics, 5000);
    </script>
</body>
</html>
    `
    w.Header().Set("Content-Type", "text/html")
    w.Write([]byte(dashboardHTML))
}

var startTime = time.Now()
