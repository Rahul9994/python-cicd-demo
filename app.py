import os
from datetime import datetime
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python CI/CD Pipeline Demo</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 50%, #020617 100%);
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.1);
            --accent-glow: rgba(99, 102, 241, 0.25);
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --emerald: #10b981;
            --emerald-glow: rgba(16, 185, 129, 0.3);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem 1rem;
            overflow-x: hidden;
            position: relative;
        }

        /* Ambient Glow Background elements */
        .ambient-glow {
            position: absolute;
            width: 500px;
            height: 500px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.15), transparent 70%);
            top: 10%;
            left: 20%;
            filter: blur(80px);
            z-index: 0;
            pointer-events: none;
        }

        .ambient-glow-2 {
            position: absolute;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(16, 185, 129, 0.12), transparent 70%);
            bottom: 10%;
            right: 20%;
            filter: blur(80px);
            z-index: 0;
            pointer-events: none;
        }

        .container {
            width: 100%;
            max-width: 860px;
            z-index: 1;
        }

        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 3rem 2.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 40px var(--accent-glow);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }

        .glass-card:hover {
            border-color: rgba(99, 102, 241, 0.3);
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 9999px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 1.5rem;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 0 0 var(--emerald-glow);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
            }
        }

        h1 {
            font-size: clamp(2.2rem, 5vw, 3.4rem);
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 70%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            font-size: 1.15rem;
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 2.5rem;
            max-width: 680px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2.5rem;
        }

        .stat-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 1.25rem 1rem;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 6px;
        }

        .stat-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }

        .stat-value {
            font-size: 1.25rem;
            font-weight: 700;
            color: #f1f5f9;
        }

        .stat-badge {
            font-size: 0.75rem;
            font-weight: 600;
            color: #34d399;
            background: rgba(16, 185, 129, 0.12);
            padding: 2px 8px;
            border-radius: 6px;
        }

        /* Pipeline Steps Visualizer */
        .pipeline-bar {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }

        .pipeline-title {
            font-size: 0.85rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .pipeline-steps {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            overflow-x: auto;
            padding-bottom: 4px;
        }

        .step-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            color: #cbd5e1;
            white-space: nowrap;
        }

        .step-icon {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 700;
        }

        .step-arrow {
            color: #475569;
            font-size: 0.8rem;
        }

        /* Actions */
        .action-group {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            align-items: center;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.95rem;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s ease;
            border: none;
            font-family: inherit;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
        }

        .btn-primary:hover {
            background: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.07);
            color: #f1f5f9;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.12);
            transform: translateY(-2px);
        }

        .json-preview {
            display: none;
            margin-top: 1.5rem;
            background: #020617;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 1rem 1.25rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #38bdf8;
            overflow-x: auto;
            text-align: left;
        }

        footer {
            margin-top: 2rem;
            text-align: center;
            color: #64748b;
            font-size: 0.85rem;
        }

        footer a {
            color: #818cf8;
            text-decoration: none;
        }

        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="ambient-glow"></div>
    <div class="ambient-glow-2"></div>

    <div class="container">
        <div class="glass-card">
            <div class="status-pill">
                <span class="pulse-dot"></span>
                CI/CD Pipeline Active & Healthy
            </div>

            <!-- Keep 'Hello World!' in text for pytest assertion -->
            <h1>Hello World! 🚀</h1>
            <p class="subtitle">
                Welcome to the modernized <strong>Python CI/CD Pipeline Demo</strong>! Every push automatically triggers continuous integration, tests, and verification on GitHub Actions.
            </p>

            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-label">Application Status</span>
                    <span class="stat-value">200 OK</span>
                    <span class="stat-badge">Healthy</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Environment</span>
                    <span class="stat-value">Production</span>
                    <span class="stat-badge">Live</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Python Version</span>
                    <span class="stat-value">{{ python_version }}</span>
                    <span class="stat-badge">Fast & Async</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Server Timestamp</span>
                    <span class="stat-value" style="font-size: 1rem;">{{ current_time }}</span>
                    <span class="stat-badge">Auto Synced</span>
                </div>
            </div>

            <div class="pipeline-bar">
                <div class="pipeline-title">
                    <span>GitHub Actions Workflow Stages</span>
                    <span style="color: #34d399; font-weight: 600;">All Checks Passing</span>
                </div>
                <div class="pipeline-steps">
                    <div class="step-item">
                        <span class="step-icon">✓</span> Checkout
                    </div>
                    <span class="step-arrow">→</span>
                    <div class="step-item">
                        <span class="step-icon">✓</span> Setup Python 3.11
                    </div>
                    <span class="step-arrow">→</span>
                    <div class="step-item">
                        <span class="step-icon">✓</span> Dependencies
                    </div>
                    <span class="step-arrow">→</span>
                    <div class="step-item">
                        <span class="step-icon">✓</span> Pytest Suite
                    </div>
                    <span class="step-arrow">→</span>
                    <div class="step-item">
                        <span class="step-icon">✓</span> Deploy
                    </div>
                </div>
            </div>

            <div class="action-group">
                <button class="btn btn-primary" onclick="testHealth()">
                    ⚡ Test Health API
                </button>
                <a class="btn btn-secondary" href="https://github.com/Rahul9994/python-cicd-demo" target="_blank" rel="noopener">
                    🐙 GitHub Repository
                </a>
            </div>

            <pre id="jsonPreview" class="json-preview"></pre>
        </div>

        <footer>
            Automated CI/CD Pipeline &bull; Maintained by <a href="https://github.com/Rahul9994" target="_blank">Rahul9994</a>
        </footer>
    </div>

    <script>
        function testHealth() {
            const preview = document.getElementById('jsonPreview');
            preview.style.display = 'block';
            preview.innerText = 'Calling /api/health...';
            fetch('/api/health')
                .then(res => res.json())
                .then(data => {
                    preview.innerText = JSON.stringify(data, null, 2);
                })
                .catch(err => {
                    preview.innerText = 'Error calling health API: ' + err;
                });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    """Main dashboard route"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    import sys
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    return render_template_string(HTML_TEMPLATE, current_time=now, python_version=py_ver), 200

@app.route("/api/health")
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "python-cicd-demo",
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "web_server": "ok",
            "tests": "passing"
        }
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
