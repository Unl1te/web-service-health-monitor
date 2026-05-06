import time
import random
from flask import Flask, jsonify, request, render_template_string
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Health Monitor App', version='1.0.0')

START_TIME = time.time()
request_count = 0

HEALTH_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Health Monitor</title>
    <style>
        body { font-family: sans-serif; max-width: 500px; margin: 60px auto; padding: 0 20px; }
        h1 { font-size: 1.4rem; }
        .badge { display: inline-block; padding: 4px 12px; border-radius: 4px; font-weight: bold; }
        .ok { background: #d4edda; color: #155724; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        td { padding: 8px 12px; border: 1px solid #dee2e6; }
        td:first-child { font-weight: bold; width: 50%; }
    </style>
</head>
<body>
    <h1>Web Health Monitor</h1>
    <p>Status: <span class="badge ok">{{ status }}</span></p>
    <table>
        <tr><td>Uptime</td><td>{{ uptime }}</td></tr>
        <tr><td>Total requests</td><td>{{ request_count }}</td></tr>
        <tr><td>Response time (last)</td><td>{{ response_time_ms }} ms</td></tr>
    </table>
</body>
</html>
"""

@app.route('/')
@app.route('/health')
def health():
    global request_count
    request_count += 1

    delay = random.uniform(0, 0.2)
    time.sleep(delay)

    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"

    data = {
        "status": "ok",
        "service": "web-health-monitor",
        "uptime": uptime_str,
        "request_count": request_count,
        "response_time_ms": round(delay * 1000, 1)
    }

    best = request.accept_mimetypes.best_match(["application/json", "text/html"])
    if best == "application/json" or request.args.get("format") == "json":
        return jsonify(data)
    else:
        return render_template_string(HEALTH_HTML, **data)

@app.route('/error')
def error():
    return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)