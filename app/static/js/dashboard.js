// PredictiBetes - Dashboard Plotly Initializer with Chart Download Enabled

document.addEventListener('DOMContentLoaded', () => {
    loadDashboardAnalytics();
});

async function loadDashboardAnalytics() {
    try {
        const response = await fetch('/api/eda');
        if (!response.ok) throw new Error('Failed to load EDA analytics.');

        const data = await response.json();
        const stats = data.stats;
        const charts = data.charts;

        // Update KPI Summary Cards
        document.getElementById('dash-total-records').textContent = stats.total_records;
        document.getElementById('dash-diabetic-count').textContent = `${stats.diabetic_count} (${stats.diabetic_percent}%)`;
        document.getElementById('dash-nondiabetic-count').textContent = `${stats.non_diabetic_count} (${(100 - stats.diabetic_percent).toFixed(1)}%)`;

        const plotlyConfig = {
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            toImageButtonOptions: {
                format: 'png',
                filename: 'predictibetes_dashboard_chart',
                height: 500,
                width: 700,
                scale: 2
            }
        };

        // Render Plotly Charts
        if (charts.outcome_chart) {
            const outcomeObj = JSON.parse(charts.outcome_chart);
            Plotly.newPlot('chart-outcome', outcomeObj.data, outcomeObj.layout, plotlyConfig);
        }

        if (charts.histogram_chart) {
            const histObj = JSON.parse(charts.histogram_chart);
            Plotly.newPlot('chart-histogram', histObj.data, histObj.layout, plotlyConfig);
        }

        if (charts.scatter_chart) {
            const scatterObj = JSON.parse(charts.scatter_chart);
            Plotly.newPlot('chart-scatter', scatterObj.data, scatterObj.layout, plotlyConfig);
        }
    } catch (err) {
        showToast(err.message, 'error');
    }
}
