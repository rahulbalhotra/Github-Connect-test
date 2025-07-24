let priceChart = null;
let returnsChart = null;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts
    initializeCharts();
    
    // Form submission handler
    document.getElementById('strategyForm').addEventListener('submit', function(e) {
        e.preventDefault();
        analyzeStrategy();
    });
});

function initializeCharts() {
    const priceCtx = document.getElementById('priceChart').getContext('2d');
    const returnsCtx = document.getElementById('returnsChart').getContext('2d');
    
    // Price and Signals Chart
    priceChart = new Chart(priceCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Price',
                    data: [],
                    borderColor: '#2c3e50',
                    fill: false
                },
                {
                    label: 'Short MA',
                    data: [],
                    borderColor: '#3498db',
                    fill: false
                },
                {
                    label: 'Long MA',
                    data: [],
                    borderColor: '#e74c3c',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Price'
                    }
                }
            }
        }
    });
    
    // Returns Chart
    returnsChart = new Chart(returnsCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Strategy Returns',
                    data: [],
                    borderColor: '#27ae60',
                    fill: false
                },
                {
                    label: 'Buy & Hold Returns',
                    data: [],
                    borderColor: '#95a5a6',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Returns'
                    }
                }
            }
        }
    });
}

async function analyzeStrategy() {
    const symbol = document.getElementById('symbol').value;
    const days = document.getElementById('days').value;
    const shortWindow = document.getElementById('shortWindow').value;
    const longWindow = document.getElementById('longWindow').value;
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                symbol: symbol,
                days: days,
                shortWindow: shortWindow,
                longWindow: longWindow
            })
        });
        
        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }
        
        updateCharts(data);
        updatePerformanceMetrics(data);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to analyze strategy. Please try again.');
    }
}

function updateCharts(data) {
    // Update Price Chart
    priceChart.data.labels = data.dates;
    priceChart.data.datasets[0].data = data.price;
    priceChart.data.datasets[1].data = data.shortMA;
    priceChart.data.datasets[2].data = data.longMA;
    priceChart.update();
    
    // Update Returns Chart
    returnsChart.data.labels = data.dates;
    returnsChart.data.datasets[0].data = data.returns;
    returnsChart.data.datasets[1].data = data.buyHoldReturns;
    returnsChart.update();
}

function updatePerformanceMetrics(data) {
    const lastIndex = data.returns.length - 1;
    const totalReturn = ((data.returns[lastIndex] - 1) * 100).toFixed(2);
    const buyHoldReturn = ((data.buyHoldReturns[lastIndex] - 1) * 100).toFixed(2);
    
    const metrics = `
        <div class="metric-card">
            <div class="metric-label">Total Strategy Return</div>
            <div class="metric-value ${totalReturn >= 0 ? 'positive' : 'negative'}">
                ${totalReturn}%
            </div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Buy & Hold Return</div>
            <div class="metric-value ${buyHoldReturn >= 0 ? 'positive' : 'negative'}">
                ${buyHoldReturn}%
            </div>
        </div>
    `;
    
    document.getElementById('performanceMetrics').innerHTML = metrics;
}
