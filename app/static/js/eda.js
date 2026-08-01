// PredictiBetes - EDA & Correlation Explorer Script

document.addEventListener('DOMContentLoaded', () => {
    loadEDAData();
});

async function loadEDAData() {
    try {
        const response = await fetch('/api/eda');
        if (!response.ok) throw new Error('Failed to load EDA analytics.');

        const data = await response.json();
        const stats = data.stats;
        const charts = data.charts;

        const plotlyConfig = {
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            toImageButtonOptions: {
                format: 'png',
                filename: 'predictibetes_correlation_heatmap',
                height: 600,
                width: 800,
                scale: 2
            }
        };

        // Render Correlation Heatmap
        if (charts.heatmap_chart) {
            const heatmapObj = JSON.parse(charts.heatmap_chart);
            Plotly.newPlot('chart-heatmap', heatmapObj.data, heatmapObj.layout, plotlyConfig);
        }

        // Plain English Insights
        const insightsContainer = document.getElementById('insights-container');
        insightsContainer.innerHTML = '';
        stats.explanations.forEach(text => {
            const card = document.createElement('div');
            card.className = 'p-3 bg-dark bg-opacity-40 rounded-3 border-start border-3 border-emerald';
            card.innerHTML = `<p class="small text-secondary mb-0">${text}</p>`;
            insightsContainer.appendChild(card);
        });

        // Top Positive Correlations List
        const posList = document.getElementById('positive-corr-list');
        posList.innerHTML = '';
        stats.top_positive.forEach(item => {
            const li = document.createElement('li');
            li.className = 'list-group-item bg-transparent text-secondary border-secondary border-opacity-10 d-flex justify-content-between align-items-center py-2';
            li.innerHTML = `<span>${item.feature}</span> <span class="badge bg-success bg-opacity-20 text-success fw-bold">+${item.correlation}</span>`;
            posList.appendChild(li);
        });

        // Populate Statistical Summary Table
        const tbody = document.getElementById('eda-stats-tbody');
        tbody.innerHTML = '';

        const summary = stats.summary_stats;
        const skew = stats.skewness;
        const kurt = stats.kurtosis;
        const zeros = stats.zero_counts;

        const features = Object.keys(summary.mean);
        features.forEach(feat => {
            if (feat === 'Outcome') return;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="fw-bold text-white">${feat}</td>
                <td>${summary.mean[feat]}</td>
                <td>${summary.std[feat]}</td>
                <td>${summary.min[feat]}</td>
                <td>${summary['50%'][feat]}</td>
                <td>${summary.max[feat]}</td>
                <td><span class="badge bg-secondary">${skew[feat]}</span></td>
                <td><span class="badge bg-secondary">${kurt[feat]}</span></td>
                <td>${zeros[feat] !== undefined ? `<span class="badge bg-warning bg-opacity-20 text-warning">${zeros[feat]} (0 values)</span>` : '<span class="text-secondary">-</span>'}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        showToast(err.message, 'error');
    }
}
