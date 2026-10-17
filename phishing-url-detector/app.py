import re
import ipaddress
from urllib.parse import urlparse
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def has_ip_address(url):
    """Check if the hostname is an IP address (IPv4 or IPv6)."""
    try:
        hostname = urlparse(url).hostname
        if hostname is None:
            return False
        # ipaddress module accepts both IPv4 and IPv6
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False

def count_dots_in_domain(url):
    """Count the number of dots in the domain part of the URL."""
    hostname = urlparse(url).hostname
    if hostname is None:
        return 0
    return hostname.count('.')

def analyze_url(url):
    """
    Apply rule‑based checks and return a risk score and classification.
    Rules:
      - URL length > 50                     → +1
      - Uses HTTP (not HTTPS)                → +1
      - Contains '@' symbol                   → +2
      - Hostname is an IP address             → +3
      - Number of dots in domain:
          > 3  → +1
          > 5  → +2 (additional point)
    """
    score = 0

    # Rule 1: URL length
    if len(url) > 50:
        score += 1

    # Rule 2: HTTP vs HTTPS
    if urlparse(url).scheme == 'http':
        score += 1

    # Rule 3: Presence of '@'
    if '@' in url:
        score += 2

    # Rule 4: IP address as hostname
    if has_ip_address(url):
        score += 3

    # Rule 5: Number of dots in domain
    dots = count_dots_in_domain(url)
    if dots > 3:
        score += 1
    if dots > 5:
        score += 1   # extra point for many dots

    # Classification based on total score
    if score <= 1:
        classification = 'Safe Website'
    elif score <= 3:
        classification = 'Suspicious'
    else:
        classification = 'Phishing Website'

    return {
        'url': url,
        'score': score,
        'classification': classification,
        'details': {
            'length_gt_50': len(url) > 50,
            'uses_http': urlparse(url).scheme == 'http',
            'contains_at': '@' in url,
            'has_ip': has_ip_address(url),
            'dot_count': count_dots_in_domain(url)
        }
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Basic validation: ensure it's a plausible URL (starting with http:// or https://)
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url   # default to http for analysis

    result = analyze_url(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)