package config

import (
    "os"
    "strconv"
)

type Config struct {
    Port     string
    DataFile string
}

func LoadConfig() *Config {
    port := getEnv("PORT", "8080")
    dataFile := getEnv("DATA_FILE", "./data/sample_logs.txt")

    return &Config{
        Port:     port,
        DataFile: dataFile,
    }
}

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
    if value := os.Getenv(key); value != "" {
        if intValue, err := strconv.Atoi(value); err == nil {
            return intValue
        }
    }
    return defaultValue
}
