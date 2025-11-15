class MarketingDashboard {
    constructor() {
        this.reviews = [];
        this.abTests = [];
        this.sentimentChart = null;
        this.abTestChart = null;
        
        this.init();
    }

    async init() {
        await this.loadSampleData();
        this.setupEventListeners();
        this.renderDashboard();
        this.initializeCharts();
    }

    async loadSampleData() {
        try {
            // In a real app, this would be an API call
            this.reviews = [
                {
                    id: 1,
                    author: "Sarah Johnson",
                    rating: 5,
                    text: "Absolutely love the new campaign! The messaging is clear and compelling.",
                    sentiment: "positive",
                    date: "2024-01-15"
                },
                {
                    id: 2,
                    author: "Mike Chen",
                    rating: 2,
                    text: "The website redesign is confusing. Hard to find what I need.",
                    sentiment: "negative",
                    date: "2024-01-14"
                },
                {
                    id: 3,
                    author: "Emily Davis",
                    rating: 4,
                    text: "Good overall experience, but the checkout process could be smoother.",
                    sentiment: "neutral",
                    date: "2024-01-14"
                },
                {
                    id: 4,
                    author: "Alex Rodriguez",
                    rating: 5,
                    text: "Best marketing emails I've ever received! Relevant and engaging.",
                    sentiment: "positive",
                    date: "2024-01-13"
                },
                {
                    id: 5,
                    author: "Taylor Kim",
                    rating: 1,
                    text: "Too many pop-ups. Very annoying user experience.",
                    sentiment: "negative",
                    date: "2024-01-12"
                }
            ];

            this.abTests = [
                {
                    id: 1,
                    name: "Homepage Hero Copy",
                    variantA: { name: "A: Save Time", conversions: 245 },
                    variantB: { name: "B: Boost Productivity", conversions: 312 },
                    status: "running"
                },
                {
                    id: 2,
                    name: "Email Subject Lines",
                    variantA: { name: "A: Weekly Update", conversions: 120 },
                    variantB: { name: "B: New Opportunities", conversions: 98 },
                    status: "completed"
                }
            ];

        } catch (error) {
            console.error('Error loading data:', error);
        }
    }

    setupEventListeners() {
        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.filterReviews(e.target.dataset.filter);
            });
        });

        // Control buttons
        document.getElementById('startTest').addEventListener('click', () => this.startNewTest());
        document.getElementById('simulateData').addEventListener('click', () => this.simulateNewData());
    }

    renderDashboard() {
        this.updateKPIs();
        this.renderReviews();
        this.renderABTests();
    }

    updateKPIs() {
        // Calculate satisfaction score
        const positiveReviews = this.reviews.filter(r => r.sentiment === 'positive').length;
        const satisfactionScore = ((positiveReviews / this.reviews.length) * 100).toFixed(1);
        
        document.getElementById('satisfactionScore').textContent = `${satisfactionScore}%`;
        document.getElementById('totalReviews').textContent = this.reviews.length;

        // Calculate A/B test performance
        const bestTest = this.abTests[0];
        const bestVariant = bestTest.variantB.conversions > bestTest.variantA.conversions ? 
            bestTest.variantB : bestTest.variantA;
        const improvement = ((bestVariant.conversions - Math.min(bestTest.variantA.conversions, bestTest.variantB.conversions)) / 
                           Math.min(bestTest.variantA.conversions, bestTest.variantB.conversions) * 100).toFixed(1);
        
        document.getElementById('testPerformance').textContent = `${improvement}% better`;
    }

    renderReviews() {
        const container = document.getElementById('reviewsContainer');
        container.innerHTML = this.reviews.map(review => `
            <div class="review-card ${review.sentiment}">
                <div class="review-header">
                    <span class="review-author">${review.author}</span>
                    <span class="review-rating">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</span>
                </div>
                <p class="review-text">${review.text}</p>
                <small>${review.date} • ${review.sentiment.toUpperCase()}</small>
            </div>
        `).join('');
    }

    renderABTests() {
        const container = document.getElementById('currentTests');
        container.innerHTML = this.abTests.map(test => `
            <div class="current-test">
                <h4>${test.name}</h4>
                <div class="test-stats">
                    <div class="stat-item">
                        <div class="stat-value">${test.variantA.conversions}</div>
                        <div class="stat-label">${test.variantA.name}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${test.variantB.conversions}</div>
                        <div class="stat-label">${test.variantB.name}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${this.calculateConfidence(test)}%</div>
                        <div class="stat-label">Confidence</div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    initializeCharts() {
        this.createSentimentChart();
        this.createABTestChart();
    }

    createSentimentChart() {
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        
        const sentimentCounts = {
            positive: this.reviews.filter(r => r.sentiment === 'positive').length,
            negative: this.reviews.filter(r => r.sentiment === 'negative').length,
            neutral: this.reviews.filter(r => r.sentiment === 'neutral').length
        };

        this.sentimentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Negative', 'Neutral'],
                datasets: [{
                    data: [sentimentCounts.positive, sentimentCounts.negative, sentimentCounts.neutral],
                    backgroundColor: ['#2ecc71', '#e74c3c', '#f39c12'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    createABTestChart() {
        const ctx = document.getElementById('abTestChart').getContext('2d');
        const test = this.abTests[0];

        this.abTestChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [test.variantA.name, test.variantB.name],
                datasets: [{
                    label: 'Conversions',
                    data: [test.variantA.conversions, test.variantB.conversions],
                    backgroundColor: ['#3498db', '#9b59b6'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    filterReviews(sentiment) {
        const filteredReviews = sentiment === 'all' 
            ? this.reviews 
            : this.reviews.filter(review => review.sentiment === sentiment);
        
        const container = document.getElementById('reviewsContainer');
        container.innerHTML = filteredReviews.map(review => `
            <div class="review-card ${review.sentiment}">
                <div class="review-header">
                    <span class="review-author">${review.author}</span>
                    <span class="review-rating">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</span>
                </div>
                <p class="review-text">${review.text}</p>
                <small>${review.date} • ${review.sentiment.toUpperCase()}</small>
            </div>
        `).join('');
    }

    calculateConfidence(test) {
        // Simplified confidence calculation
        const total = test.variantA.conversions + test.variantB.conversions;
        const diff = Math.abs(test.variantA.conversions - test.variantB.conversions);
        return Math.min(95, Math.round((diff / total) * 100 * 2));
    }

    startNewTest() {
        alert('Starting new A/B test... In a real application, this would open a test creation form.');
    }

    simulateNewData() {
        // Add a new random review
        const sentiments = ['positive', 'negative', 'neutral'];
        const newReview = {
            id: this.reviews.length + 1,
            author: `Customer ${this.reviews.length + 1}`,
            rating: Math.floor(Math.random() * 5) + 1,
            text: `This is simulated review data #${this.reviews.length + 1}`,
            sentiment: sentiments[Math.floor(Math.random() * sentiments.length)],
            date: new Date().toISOString().split('T')[0]
        };
        
        this.reviews.unshift(newReview);
        
        // Update a random A/B test
        const randomTest = this.abTests[Math.floor(Math.random() * this.abTests.length)];
        randomTest.variantA.conversions += Math.floor(Math.random() * 10);
        randomTest.variantB.conversions += Math.floor(Math.random() * 10);
        
        this.renderDashboard();
        this.updateCharts();
        
        alert('New simulated data added! Check the updated dashboard.');
    }

    updateCharts() {
        if (this.sentimentChart) {
            this.sentimentChart.destroy();
        }
        if (this.abTestChart) {
            this.abTestChart.destroy();
        }
        this.initializeCharts();
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MarketingDashboard();
});
