document.getElementById('analyzeBtn').addEventListener('click', function() {
    const url = document.getElementById('urlInput').value.trim();
    if (url === '') {
        showError('Please enter a URL.');
        return;
    }

    // Hide previous result/error
    document.getElementById('result').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');

    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
        } else {
            displayResult(data);
        }
    })
    .catch(err => {
        showError('An error occurred. Please try again.');
        console.error(err);
    });
});

function displayResult(data) {
    document.getElementById('urlDisplay').textContent = data.url;
    document.getElementById('score').textContent = data.score;
    document.getElementById('classification').textContent = data.classification;

    // Build details list
    const details = data.details;
    let html = '<ul>';
    html += `<li>URL length > 50: ${details.length_gt_50 ? 'Yes (+1)' : 'No'}</li>`;
    html += `<li>Uses HTTP (not HTTPS): ${details.uses_http ? 'Yes (+1)' : 'No'}</li>`;
    html += `<li>Contains '@' symbol: ${details.contains_at ? 'Yes (+2)' : 'No'}</li>`;
    html += `<li>Hostname is an IP address: ${details.has_ip ? 'Yes (+3)' : 'No'}</li>`;
    html += `<li>Number of dots in domain: ${details.dot_count} (${details.dot_count > 3 ? '>3 → +1' : ''} ${details.dot_count > 5 ? '+1' : ''})</li>`;
    html += '</ul>';
    document.getElementById('details').innerHTML = html;

    document.getElementById('result').classList.remove('hidden');
}

function showError(message) {
    document.getElementById('error').textContent = message;
    document.getElementById('error').classList.remove('hidden');
}
// After setting the classification text
const resultDiv = document.getElementById('result');
resultDiv.classList.remove('safe', 'suspicious', 'phishing');
if (data.classification === 'Safe Website') {
    resultDiv.classList.add('safe');
} else if (data.classification === 'Suspicious') {
    resultDiv.classList.add('suspicious');
} else if (data.classification === 'Phishing Website') {
    resultDiv.classList.add('phishing');
}