// Models evaluation matrix script

document.addEventListener('DOMContentLoaded', () => {
    loadModelMetrics();

    const retrainBtn = document.getElementById('retrain-btn');
    if (retrainBtn) {
        retrainBtn.addEventListener('click', handleRetrainModels);
    }
});

async function loadModelMetrics() {
    try {
        const response = await fetch('/api/metrics');
        if (!response.ok) throw new Error('Failed to load model metrics.');

        const data = await response.json();
        renderMetrics(data);
    } catch (err) {
        showToast(err.message, 'error');
    }
}

function renderMetrics(data) {
    document.getElementById('best-model-name-text').textContent = data.best_model_name || 'Logistic Regression';
    document.getElementById('trained-at-text').textContent = `Trained At: ${data.trained_at || 'Just now'}`;

    const tbody = document.getElementById('models-table-body');
    tbody.innerHTML = '';

    const models = data.models || {};
    const bestName = data.best_model_name;

    const rocTraces = [];
    const prTraces = [];
    const colors = ['#10B981', '#6366F1', '#06B6D4', '#F59E0B', '#8B5CF6', '#EC4899'];
    let idx = 0;

    for (const [name, m] of Object.entries(models)) {
        const isBest = name === bestName;
        const tr = document.createElement('tr');
        if (isBest) tr.className = 'table-active';

        tr.innerHTML = `
            <td class="fw-bold">${name} ${isBest ? '<span class="badge bg-success ms-2">Best Model</span>' : ''}</td>
            <td><span class="fw-bold text-emerald">${(m.accuracy * 100).toFixed(2)}%</span></td>
            <td>${(m.precision * 100).toFixed(2)}%</td>
            <td>${(m.recall * 100).toFixed(2)}%</td>
            <td>${m.f1_score.toFixed(4)}</td>
            <td><span class="badge bg-indigo">${m.roc_auc.toFixed(4)}</span></td>
            <td>${m.train_time_ms} ms</td>
            <td>${m.inference_time_ms} ms</td>
        `;
        tbody.appendChild(tr);

        // Prepare ROC Curve Trace
        if (m.roc_curve) {
            rocTraces.push({
                x: m.roc_curve.fpr,
                y: m.roc_curve.tpr,
                mode: 'lines',
                name: `${name} (AUC: ${m.roc_auc})`,
                line: { color: colors[idx % colors.length], width: isBest ? 3 : 1.5 }
            });
        }

        // Prepare PR Curve Trace
        if (m.pr_curve) {
            prTraces.push({
                x: m.pr_curve.recall,
                y: m.pr_curve.precision,
                mode: 'lines',
                name: `${name}`,
                line: { color: colors[idx % colors.length], width: isBest ? 3 : 1.5 }
            });
        }
        idx++;
    }

    // Render ROC Curves Chart
    const rocLayout = {
        title: 'ROC Curves Comparison',
        xaxis: { title: 'False Positive Rate (FPR)' },
        yaxis: { title: 'True Positive Rate (TPR)' },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#94A3B8', family: 'Inter, sans-serif' }
    };
    Plotly.newPlot('chart-roc-curves', rocTraces, rocLayout, {responsive: true});

    // Render PR Curves Chart
    const prLayout = {
        title: 'Precision-Recall Curves',
        xaxis: { title: 'Recall' },
        yaxis: { title: 'Precision' },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#94A3B8', family: 'Inter, sans-serif' }
    };
    Plotly.newPlot('chart-pr-curves', prTraces, prLayout, {responsive: true});
}

async function handleRetrainModels() {
    const btnText = document.getElementById('retrain-text');
    const btnSpinner = document.getElementById('retrain-spinner');
    const btn = document.getElementById('retrain-btn');

    btnText.classList.add('d-none');
    btnSpinner.classList.remove('d-none');
    btn.disabled = true;

    try {
        const response = await fetch('/api/retrain', { method: 'POST' });
        if (!response.ok) throw new Error('Retraining failed.');

        const data = await response.json();
        renderMetrics(data.metrics);
        showToast(`Retrained successfully! Best Model: ${data.best_model_name}`, 'success');
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        btnText.classList.remove('d-none');
        btnSpinner.classList.add('d-none');
        btn.disabled = false;
    }
}
