document.addEventListener('DOMContentLoaded', function() {
    // Initialize the spreadsheet
    const container = document.getElementById('dataGrid');
    const hot = new Handsontable(container, {
        data: [
            ['X', 'Y'],
            [1, 2],
            [2, 4],
            [3, 5],
            [4, 4],
            [5, 5],
        ],
        rowHeaders: true,
        colHeaders: true,
        height: '300px',
        licenseKey: 'non-commercial-and-evaluation'
    });

    // Add row and column buttons functionality
    document.getElementById('addRow').addEventListener('click', function() {
        hot.alter('insert_row');
    });

    document.getElementById('addColumn').addEventListener('click', function() {
        hot.alter('insert_col');
    });

    // Initialize the chart
    const ctx = document.getElementById('regressionChart').getContext('2d');
    let chart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Data Points',
                data: [],
                backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }, {
                label: 'Regression Line',
                data: [],
                type: 'line',
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'X'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Y'
                    }
                }
            }
        }
    });

    // Calculate regression and update chart
    document.getElementById('calculateRegression').addEventListener('click', function() {
        const data = hot.getData();
        const points = data.slice(1).map(row => [row[0], row[1]]).filter(point => 
            point[0] !== null && point[1] !== null && 
            !isNaN(point[0]) && !isNaN(point[1])
        );

        // Calculate regression
        const result = regression.linear(points);

        // Update scatter plot data
        chart.data.datasets[0].data = points.map(point => ({
            x: point[0],
            y: point[1]
        }));

        // Generate regression line points
        const minX = Math.min(...points.map(p => p[0]));
        const maxX = Math.max(...points.map(p => p[0]));
        chart.data.datasets[1].data = [
            { x: minX, y: result.predict(minX)[1] },
            { x: maxX, y: result.predict(maxX)[1] }
        ];

        // Update chart title to show regression equation
        const equation = `y = ${result.equation[0].toFixed(2)}x + ${result.equation[1].toFixed(2)}`;
        chart.options.plugins.title = {
            display: true,
            text: `Regression Equation: ${equation} (R² = ${result.r2.toFixed(4)})`,
            padding: {
                top: 10,
                bottom: 30
            }
        };

        // Update chart
        chart.update();
    });
});
