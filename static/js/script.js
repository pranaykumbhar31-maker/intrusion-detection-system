/**
 * ==============================================================================
 * Intrusion Detection System (IDS) - Frontend JavaScript (script.js)
 * Handles preset loading, form submission, real-time prediction AJAX calls,
 * and Chart.js visualizations.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {

    // --------------------------------------------------------------------------
    // 1. Intrusion Detection Form & Presets Logic
    // --------------------------------------------------------------------------
    const form = document.getElementById('detectionForm');
    const btnPresetNormal = document.getElementById('btnPresetNormal');
    const btnPresetAttack = document.getElementById('btnPresetAttack');
    const btnPresetProbe = document.getElementById('btnPresetProbe');
    const btnResetForm = document.getElementById('btnResetForm');

    const presetDescBox = document.getElementById('presetDescBox');
    const presetDescTitle = document.getElementById('presetDescTitle');
    const presetDescText = document.getElementById('presetDescText');

    const idleState = document.getElementById('idleState');
    const loadingState = document.getElementById('loadingState');
    const activeResultState = document.getElementById('activeResultState');
    const errorState = document.getElementById('errorState');
    const errorMessage = document.getElementById('errorMessage');

    const resultBanner = document.getElementById('resultBanner');
    const resultIcon = document.getElementById('resultIcon');
    const resultLabel = document.getElementById('resultLabel');
    const resultSubtext = document.getElementById('resultSubtext');
    const resultConfidence = document.getElementById('resultConfidence');
    const resultRiskLevel = document.getElementById('resultRiskLevel');
    const resultExplanation = document.getElementById('resultExplanation');
    const inferenceStatusBadge = document.getElementById('inferenceStatusBadge');

    const probNormalBar = document.getElementById('probNormalBar');
    const probIntrusionBar = document.getElementById('probIntrusionBar');
    const probNormalText = document.getElementById('probNormalText');
    const probIntrusionText = document.getElementById('probIntrusionText');

    const btnPredict = document.getElementById('btnPredict');
    const predictBtnSpinner = document.getElementById('predictBtnSpinner');
    const predictBtnIcon = document.getElementById('predictBtnIcon');

    // Helper: Populate form fields from dictionary
    function populateForm(data, title, description) {
        if (!data) return;
        for (const [key, val] of Object.entries(data)) {
            const input = document.getElementById(key);
            if (input) {
                input.value = val;
                // Add a brief subtle glow to show it updated
                input.classList.add('border-info');
                setTimeout(() => input.classList.remove('border-info'), 600);
            }
        }
        if (presetDescBox && title) {
            presetDescBox.classList.remove('d-none');
            presetDescTitle.textContent = title;
            presetDescText.textContent = description;
        }
    }

    // Attach Preset Listeners
    if (btnPresetNormal) {
        btnPresetNormal.addEventListener('click', () => {
            const samples = window.PRESET_SAMPLES || {};
            if (samples.normal) {
                populateForm(samples.normal.features, samples.normal.title, samples.normal.description);
            }
        });
    }

    if (btnPresetAttack) {
        btnPresetAttack.addEventListener('click', () => {
            const samples = window.PRESET_SAMPLES || {};
            if (samples.attack) {
                populateForm(samples.attack.features, samples.attack.title, samples.attack.description);
            }
        });
    }

    if (btnPresetProbe) {
        btnPresetProbe.addEventListener('click', () => {
            const samples = window.PRESET_SAMPLES || {};
            if (samples.probe) {
                populateForm(samples.probe.features, samples.probe.title, samples.probe.description);
            }
        });
    }

    if (btnResetForm && form) {
        btnResetForm.addEventListener('click', () => {
            form.reset();
            if (presetDescBox) presetDescBox.classList.add('d-none');
        });
    }

    // Handle Predict Activity Submission
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Extract form values
            const formData = new FormData(form);
            const payload = {};
            formData.forEach((value, key) => {
                payload[key] = value;
            });

            // UI Loading state
            if (idleState) idleState.classList.add('d-none');
            if (activeResultState) activeResultState.classList.add('d-none');
            if (errorState) errorState.classList.add('d-none');
            if (loadingState) loadingState.classList.remove('d-none');

            if (btnPredict) btnPredict.disabled = true;
            if (predictBtnSpinner) predictBtnSpinner.classList.remove('d-none');
            if (predictBtnIcon) predictBtnIcon.classList.add('d-none');
            if (inferenceStatusBadge) {
                inferenceStatusBadge.textContent = 'Processing...';
                inferenceStatusBadge.className = 'badge bg-warning-subtle text-warning small';
            }

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (loadingState) loadingState.classList.add('d-none');
                if (btnPredict) btnPredict.disabled = false;
                if (predictBtnSpinner) predictBtnSpinner.classList.add('d-none');
                if (predictBtnIcon) predictBtnIcon.classList.remove('d-none');

                if (!response.ok || data.status === 'error') {
                    throw new Error(data.message || 'Error occurred while predicting.');
                }

                // Render Result
                if (activeResultState) activeResultState.classList.remove('d-none');

                const isNormal = data.prediction === 'NORMAL';

                // Banner styling
                if (resultBanner) {
                    resultBanner.className = `result-banner p-4 rounded-3 text-center mb-4 ${isNormal ? 'normal' : 'intrusion'}`;
                }
                if (resultIcon) {
                    resultIcon.innerHTML = isNormal
                        ? '<i class="bi bi-shield-check text-success"></i>'
                        : '<i class="bi bi-exclamation-triangle-fill text-danger"></i>';
                }
                if (resultLabel) {
                    resultLabel.textContent = isNormal ? 'NORMAL ACTIVITY' : 'INTRUSION DETECTED';
                    resultLabel.className = `display-6 fw-extrabold text-uppercase letter-spacing-1 ${isNormal ? 'text-success' : 'text-danger'}`;
                }
                if (resultSubtext) {
                    resultSubtext.textContent = isNormal
                        ? 'Benign Network Session • No Malicious Signature Detected'
                        : 'Potential Security Violation • Anomalous Behavior Flagged';
                }

                if (resultConfidence) {
                    resultConfidence.textContent = `${data.confidence_percent}%`;
                }
                if (resultRiskLevel) {
                    resultRiskLevel.textContent = data.risk_level;
                    resultRiskLevel.className = `h3 fw-bold mb-0 mt-1 ${isNormal ? 'text-success' : 'text-danger'}`;
                }

                // Probabilities progress bar
                const pNorm = data.probabilities ? data.probabilities.normal : (isNormal ? data.confidence_percent : 100 - data.confidence_percent);
                const pIntr = data.probabilities ? data.probabilities.intrusion : (!isNormal ? data.confidence_percent : 100 - data.confidence_percent);

                if (probNormalBar) {
                    probNormalBar.style.width = `${pNorm}%`;
                    probNormalBar.setAttribute('aria-valuenow', pNorm);
                }
                if (probIntrusionBar) {
                    probIntrusionBar.style.width = `${pIntr}%`;
                    probIntrusionBar.setAttribute('aria-valuenow', pIntr);
                }
                if (probNormalText) probNormalText.textContent = `${pNorm}%`;
                if (probIntrusionText) probIntrusionText.textContent = `${pIntr}%`;

                // Explanation
                if (resultExplanation) {
                    resultExplanation.textContent = data.explanation;
                }

                // Status Badge
                if (inferenceStatusBadge) {
                    const now = new Date().toLocaleTimeString();
                    inferenceStatusBadge.textContent = `Done at ${now}`;
                    inferenceStatusBadge.className = isNormal
                        ? 'badge bg-success-subtle text-success small'
                        : 'badge bg-danger-subtle text-danger small';
                }

            } catch (err) {
                if (loadingState) loadingState.classList.add('d-none');
                if (btnPredict) btnPredict.disabled = false;
                if (predictBtnSpinner) predictBtnSpinner.classList.add('d-none');
                if (predictBtnIcon) predictBtnIcon.classList.remove('d-none');

                if (errorState) {
                    errorState.classList.remove('d-none');
                    if (errorMessage) errorMessage.textContent = err.message;
                }
                if (inferenceStatusBadge) {
                    inferenceStatusBadge.textContent = 'Error';
                    inferenceStatusBadge.className = 'badge bg-danger-subtle text-danger small';
                }
            }
        });
    }


    // --------------------------------------------------------------------------
    // 2. Dashboard Charts Logic (Chart.js)
    // --------------------------------------------------------------------------
    const trafficRatioCanvas = document.getElementById('trafficRatioChart');
    const featureImportanceCanvas = document.getElementById('featureImportanceChart');

    if (trafficRatioCanvas && typeof Chart !== 'undefined') {
        const stats = window.INITIAL_STATS || { normal_predictions: 0, intrusion_predictions: 0 };
        const normVal = stats.normal_predictions || 0;
        const intrVal = stats.intrusion_predictions || 0;

        // If no data yet, show default placeholder ratio
        const chartData = (normVal === 0 && intrVal === 0) ? [1, 1] : [normVal, intrVal];
        const isPlaceholder = (normVal === 0 && intrVal === 0);

        new Chart(trafficRatioCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Normal', 'Intrusion'],
                datasets: [{
                    data: chartData,
                    backgroundColor: isPlaceholder 
                        ? ['rgba(0, 230, 118, 0.4)', 'rgba(255, 42, 95, 0.4)']
                        : ['#00e676', '#ff2a5f'],
                    borderColor: '#152033',
                    borderWidth: 3,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                if (isPlaceholder) return 'No tests run yet';
                                return `${context.label}: ${context.raw} packets`;
                            }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }

    if (featureImportanceCanvas && typeof Chart !== 'undefined') {
        const metrics = window.SERVER_METRICS || {};
        const topFeatures = metrics.top_features || [
            { feature: 'src_bytes', importance: 13.6 },
            { feature: 'dst_bytes', importance: 12.9 },
            { feature: 'flag_SF', importance: 8.9 },
            { feature: 'same_srv_rate', importance: 7.7 },
            { feature: 'diff_srv_rate', importance: 7.3 },
            { feature: 'dst_host_same_srv', importance: 7.1 },
            { feature: 'dst_host_srv_cnt', importance: 7.0 },
            { feature: 'count', importance: 6.1 }
        ];

        const labels = topFeatures.map(f => f.feature);
        const dataValues = topFeatures.map(f => f.importance);

        new Chart(featureImportanceCanvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Feature Weight (%)',
                    data: dataValues,
                    backgroundColor: 'rgba(0, 210, 255, 0.75)',
                    hoverBackgroundColor: '#00d2ff',
                    borderColor: '#00b4d8',
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.08)' },
                        ticks: { color: '#94a3b8', font: { family: 'Inter' } }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: '#f1f5f9', font: { family: 'JetBrains Mono', size: 12 } }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Importance: ${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });
    }

});
