// PredictiBetes - Prediction Form & Multi-Step Loader Logic

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    if (form) {
        form.addEventListener('submit', handleSinglePrediction);
    }

    const batchForm = document.getElementById('batch-form');
    if (batchForm) {
        batchForm.addEventListener('submit', handleBatchPrediction);
    }
});

async function handleSinglePrediction(e) {
    e.preventDefault();

    const form = e.target;
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }

    // Show Multi-step Loading Experience
    const overlay = document.getElementById('prediction-loading-overlay');
    const stepTitle = document.getElementById('loading-step-title');
    const progressBar = document.getElementById('loading-progress-bar');
    
    overlay.classList.remove('d-none');

    const steps = [
        { title: "Analyzing Clinical Data...", progress: "25%" },
        { title: "Evaluating Patient Features...", progress: "50%" },
        { title: "Running Machine Learning Models...", progress: "75%" },
        { title: "Generating Clinical Insights...", progress: "95%" }
    ];

    for (let i = 0; i < steps.length; i++) {
        stepTitle.textContent = steps[i].title;
        progressBar.style.width = steps[i].progress;
        await new Promise(r => setTimeout(r, 220));
    }

    const payload = {
        pregnancies: parseInt(document.getElementById('pregnancies').value),
        glucose: parseFloat(document.getElementById('glucose').value),
        blood_pressure: parseFloat(document.getElementById('blood_pressure').value),
        skin_thickness: parseFloat(document.getElementById('skin_thickness').value),
        insulin: parseFloat(document.getElementById('insulin').value),
        bmi: parseFloat(document.getElementById('bmi').value),
        dpf: parseFloat(document.getElementById('dpf').value),
        age: parseInt(document.getElementById('age').value)
    };

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Prediction failed.');
        }

        const data = await response.json();
        renderPredictionResult(data);
        showToast('Prediction generated successfully!', 'success');
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        overlay.classList.add('d-none');
    }
}

function renderPredictionResult(data) {
    const placeholder = document.getElementById('results-placeholder');
    const card = document.getElementById('results-card');

    placeholder.classList.add('d-none');
    card.classList.remove('d-none');

    const isDiabetic = data.prediction === 1;
    const badge = document.getElementById('result-badge');
    badge.className = `badge px-3 py-2 fs-6 rounded-pill mb-2 ${isDiabetic ? 'bg-danger text-white' : 'bg-success text-white'}`;
    badge.textContent = data.result_label;

    document.getElementById('result-title').textContent = isDiabetic ? 'High Diabetes Risk' : 'Low Diabetes Risk';
    document.getElementById('result-model-info').textContent = `Classifier Model: ${data.model_used}`;

    // Emergency Alert Banner
    const emergencyAlert = document.getElementById('emergency-alert');
    if (data.risk_level === 'High' || data.risk_level === 'Very High') {
        emergencyAlert.classList.remove('d-none');
    } else {
        emergencyAlert.classList.add('d-none');
    }

    // Confidence
    const confVal = document.getElementById('confidence-val');
    const confBar = document.getElementById('confidence-bar');
    confVal.textContent = `${data.confidence_percent}%`;
    confBar.style.width = `${data.confidence_percent}%`;
    confBar.className = `progress-bar ${isDiabetic ? 'bg-danger' : 'bg-success'}`;

    // Risk badge
    const riskBadge = document.getElementById('risk-level-badge');
    const riskMap = {
        'Low': 'badge-risk-low',
        'Moderate': 'badge-risk-moderate',
        'High': 'badge-risk-high',
        'Very High': 'badge-risk-veryhigh'
    };
    riskBadge.className = `badge px-3 py-1 fs-6 mt-1 ${riskMap[data.risk_level] || 'bg-secondary'}`;
    riskBadge.textContent = data.risk_level;

    // BMI Category
    document.getElementById('bmi-category-badge').textContent = data.bmi_category;

    // Model Explainability Section
    const explainList = document.getElementById('explainability-list');
    explainList.innerHTML = '';

    const pos = data.top_positive_factors || [];
    const neg = data.top_negative_factors || [];

    if (pos.length > 0) {
        const topPosNames = pos.slice(0, 3).map(p => `<strong class="text-white">${p.feature}</strong>`).join(', ');
        explainList.innerHTML += `<p class="mb-1"><i class="bi bi-arrow-up-right-circle text-danger me-1"></i> Key risk-driving metrics: ${topPosNames}</p>`;
    }
    if (neg.length > 0) {
        const topNegNames = neg.slice(0, 2).map(n => `<strong class="text-white">${n.feature}</strong>`).join(', ');
        explainList.innerHTML += `<p class="mb-0"><i class="bi bi-arrow-down-right-circle text-success me-1"></i> Key protective factors: ${topNegNames}</p>`;
    }

    // Tips List
    const tipsList = document.getElementById('tips-list');
    tipsList.innerHTML = '';

    const allTips = [
        ...(data.health_tips.diet || []),
        ...(data.health_tips.exercise || []),
        ...(data.health_tips.monitoring || []),
        ...(data.health_tips.general || [])
    ];

    allTips.forEach(tip => {
        const li = document.createElement('li');
        li.className = 'list-group-item bg-transparent text-secondary border-secondary border-opacity-10 px-0 py-2 d-flex align-items-start gap-2';
        li.innerHTML = `<i class="bi bi-check-circle-fill text-emerald mt-1"></i> <span>${tip}</span>`;
        tipsList.appendChild(li);
    });
}

async function handleBatchPrediction(e) {
    e.preventDefault();
    const fileInput = document.getElementById('batch-file');
    if (!fileInput.files.length) {
        showToast('Please select a CSV file first.', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/api/predict/batch', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Batch processing failed.');
        }

        const data = await response.json();
        document.getElementById('batch-results-container').classList.remove('d-none');
        document.getElementById('batch-total').textContent = data.total_rows;
        document.getElementById('batch-diabetic').textContent = data.diabetic_count;
        document.getElementById('batch-non-diabetic').textContent = data.non_diabetic_count;

        showToast(`Successfully processed ${data.total_rows} records!`, 'success');
    } catch (err) {
        showToast(err.message, 'error');
    }
}
