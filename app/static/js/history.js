// History page script for search, filter, delete, and table rendering

document.addEventListener('DOMContentLoaded', () => {
    loadHistory();

    const searchInput = document.getElementById('history-search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(loadHistory, 300));
    }

    const riskFilter = document.getElementById('history-risk-filter');
    if (riskFilter) {
        riskFilter.addEventListener('change', loadHistory);
    }

    const clearAllBtn = document.getElementById('clear-all-btn');
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', handleClearAll);
    }
});

async function loadHistory() {
    const search = document.getElementById('history-search').value.trim();
    const risk = document.getElementById('history-risk-filter').value;

    let url = '/api/history?limit=100';
    if (search) url += `&search=${encodeURIComponent(search)}`;
    if (risk) url += `&risk_level=${encodeURIComponent(risk)}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch history.');

        const records = await response.json();
        renderHistoryTable(records);
    } catch (err) {
        showToast(err.message, 'error');
    }
}

function renderHistoryTable(records) {
    const tbody = document.getElementById('history-tbody');
    document.getElementById('history-count-badge').textContent = `${records.length} Records`;
    tbody.innerHTML = '';

    if (!records.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center text-secondary py-4">
                    <i class="bi bi-inbox fs-3 d-block mb-1"></i> No prediction records found.
                </td>
            </tr>
        `;
        return;
    }

    const riskBadgeMap = {
        'Low': 'badge-risk-low',
        'Moderate': 'badge-risk-moderate',
        'High': 'badge-risk-high',
        'Very High': 'badge-risk-veryhigh'
    };

    records.forEach(r => {
        const dateStr = new Date(r.created_at).toLocaleString();
        const isDiabetic = r.prediction === 1;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="small text-secondary">${dateStr}</td>
            <td>
                <span class="badge ${isDiabetic ? 'bg-danger' : 'bg-success'}">
                    ${isDiabetic ? 'Diabetic' : 'Non-Diabetic'}
                </span>
            </td>
            <td>${(r.probability * 100).toFixed(1)}%</td>
            <td><span class="badge ${riskBadgeMap[r.risk_level] || 'bg-secondary'}">${r.risk_level}</span></td>
            <td>${r.glucose} mg/dL</td>
            <td>${r.bmi}</td>
            <td>${r.age} yrs</td>
            <td class="small text-secondary">${r.model_used}</td>
            <td class="text-end">
                <button onclick="deleteRecord(${r.id})" class="btn btn-sm btn-outline-danger border-0 rounded-circle" title="Delete Record">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function deleteRecord(recordId) {
    if (!confirm(`Delete prediction record #${recordId}?`)) return;

    try {
        const response = await fetch(`/api/history/${recordId}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Delete failed.');

        showToast(`Record #${recordId} deleted.`, 'success');
        loadHistory();
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function handleClearAll() {
    if (!confirm('Are you sure you want to delete ALL prediction history records?')) return;

    try {
        const response = await fetch('/api/history', { method: 'DELETE' });
        if (!response.ok) throw new Error('Failed to clear history.');

        showToast('All prediction history cleared.', 'success');
        loadHistory();
    } catch (err) {
        showToast(err.message, 'error');
    }
}

function debounce(func, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}
