package processor

import (
    "bufio"
    "fmt"
    "os"
    "strings"
    "sync"
    "time"

    "marketing-analytics-pipeline/models"
)

func ProcessFile(filename string, analyticsData map[string]*models.CampaignStats, mutex *sync.RWMutex) {
    file, err := os.Open(filename)
    if err != nil {
        fmt.Printf("Warning: Could not open data file: %v\n", err)
        return
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    linesProcessed := 0

    for scanner.Scan() {
        line := scanner.Text()
        processLine(line, analyticsData, mutex)
        linesProcessed++
    }

    fmt.Printf("✅ Processed %d lines from historical data\n", linesProcessed)
}

func processLine(line string, analyticsData map[string]*models.CampaignStats, mutex *sync.RWMutex) {
    parts := strings.Split(line, "|")
    if len(parts) < 3 {
        return
    }

    eventType := parts[0]
    campaignID := parts[1]
    
    mutex.Lock()
    defer mutex.Unlock()

    if _, exists := analyticsData[campaignID]; !exists {
        analyticsData[campaignID] = &models.CampaignStats{
            CampaignID:  campaignID,
            UniqueUsers: make(map[string]bool),
            LastUpdated: time.Now(),
        }
    }

    stats := analyticsData[campaignID]

    switch eventType {
    case "CLICK":
        if len(parts) >= 4 {
            userID := parts[2]
            stats.TotalClicks++
            stats.UniqueUsers[userID] = true
        }
    case "CONVERSION":
        if len(parts) >= 5 {
            userID := parts[2]
            // amount := parts[3] // You could parse amount if needed
            stats.TotalConversions++
            stats.UniqueUsers[userID] = true
            
            // Calculate conversion rate
            if stats.TotalClicks > 0 {
                stats.ConversionRate = float64(stats.TotalConversions) / float64(stats.TotalClicks) * 100
            }
        }
    }

    stats.LastUpdated = time.Now()
}

func ProcessClick(click models.ClickEvent, analyticsData map[string]*models.CampaignStats) {
    campaignID := click.CampaignID

    if _, exists := analyticsData[campaignID]; !exists {
        analyticsData[campaignID] = &models.CampaignStats{
            CampaignID:  campaignID,
            UniqueUsers: make(map[string]bool),
            LastUpdated: time.Now(),
        }
    }

    stats := analyticsData[campaignID]
    stats.TotalClicks++
    stats.UniqueUsers[click.UserID] = true
    
    // Recalculate conversion rate
    if stats.TotalClicks > 0 {
        stats.ConversionRate = float64(stats.TotalConversions) / float64(stats.TotalClicks) * 100
    }
    
    stats.LastUpdated = time.Now()
}

func ProcessConversion(conversion models.ConversionEvent, analyticsData map[string]*models.CampaignStats) {
    campaignID := conversion.CampaignID

    if _, exists := analyticsData[campaignID]; !exists {
        analyticsData[campaignID] = &models.CampaignStats{
            CampaignID:  campaignID,
            UniqueUsers: make(map[string]bool),
            LastUpdated: time.Now(),
        }
    }

    stats := analyticsData[campaignID]
    stats.TotalConversions++
    stats.TotalRevenue += conversion.Amount
    stats.UniqueUsers[conversion.UserID] = true
    
    // Recalculate conversion rate
    if stats.TotalClicks > 0 {
        stats.ConversionRate = float64(stats.TotalConversions) / float64(stats.TotalClicks) * 100
    }
    
    stats.LastUpdated = time.Now()
}
