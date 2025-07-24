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
        minRows: 5,
        minCols: 2,
        minSpareRows: 1,
        contextMenu: true,
        licenseKey: 'non-commercial-and-evaluation'
    });

    // Add row button functionality
    document.getElementById('addRow').addEventListener('click', function() {
        const currentData = hot.getData();
        const newRowIndex = currentData.length;
        hot.alter('insert_row', newRowIndex);
        hot.render(); // Force re-render
    });

    // Remove row button functionality
    document.getElementById('removeRow').addEventListener('click', function() {
        const currentData = hot.getData();
        if (currentData.length > 2) { // Keep at least header row and one data row
            hot.alter('remove_row', currentData.length - 1);
            hot.render();
        }
    });

    // Add column button functionality
    document.getElementById('addColumn').addEventListener('click', function() {
        const currentData = hot.getData();
        const newColIndex = currentData[0].length;
        hot.alter('insert_col', newColIndex);
        hot.render(); // Force re-render
        
        // Update column headers
        const headers = Array.from({length: hot.countCols()}, (_, i) => 
            String.fromCharCode(65 + i)); // A, B, C, etc.
        hot.updateSettings({
            colHeaders: headers
        });
    });

    // Remove column button functionality
    document.getElementById('removeColumn').addEventListener('click', function() {
        const currentData = hot.getData();
        if (currentData[0].length > 2) { // Keep at least X and Y columns
            hot.alter('remove_col', currentData[0].length - 1);
            hot.render();
            
            // Update column headers
            const headers = Array.from({length: hot.countCols()}, (_, i) => 
                String.fromCharCode(65 + i));
            hot.updateSettings({
                colHeaders: headers
            });
        }
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
