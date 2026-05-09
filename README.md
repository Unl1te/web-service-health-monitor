# Web Service Health Monitor

A complete monitoring and alerting system for a Flask web application.
It exposes health metrics, collects them with Prometheus, visualizes them in Grafana, and sends Telegram alerts via Alertmanager when the service goes down.
Includes a CI pipeline with GitHub Actions.

---

## Team

* Artem Ulianov
* Mikhail Tikhonov
* Ziad Mohamed

---

## Features

* Flask app with `/`, `/health`, `/error` endpoints
* Prometheus metrics (`/metrics`) on it's address
* Nginx as reverse proxy
* Grafana dashboards (auto-provisioned)
* Alertmanager + Telegram notifications
* GitHub Actions CI (build, start, test root/metrics, Prometheus targets)

---

## Requirements

* Docker & Docker Compose
* Ports:

  * `80` (Nginx)
  * `3000` (Grafana)
  * `9090` (Prometheus)
  * `9093` (Alertmanager)
* Telegram bot token and chat ID (see setup below)

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-repo/web-service-health-monitor.git
cd web-service-health-monitor
```

### 2. Edit a `.env` file

Replace `your_token_here` and `your_chat_id_here` with your real Telegram bot token and chat ID.

### 3. Start the stack

```bash
docker compose up -d --build
```

### 4. Verify services

* Website: http://localhost
* Prometheus: http://localhost:9090
* Grafana: http://localhost:3000 (default login: `admin / admin`)
* Alertmanager: http://localhost:9093

---

## Endpoints

| Endpoint   | Description                                                     |
| ---------- | --------------------------------------------------------------- |
| `/`        | HTML page + JSON (depending on Accept header or `?format=json`) |
| `/health`  | Same as `/` (alias)                                             |
| `/error`   | Returns `{"status":"error"}` with HTTP 500                      |

---

## Testing Alerts

### Stop the Flask container

```bash
docker compose stop app
```

Wait ~1 minute – you’ll receive a Telegram alert **“FIRING”**.

### Restart the container

```bash
docker compose start app
```

After ~30 seconds you’ll receive a **“RESOLVED”** notification.

---

## Grafana Dashboards

* Dashboards are provisioned automatically from:

  ```
  grafana/dashboards/web-health-monitor.json
  ```
* Prometheus data source is also provisioned:

  ```
  grafana/provisioning/datasources/datasource.yml
  ```
* Default credentials: `admin / admin`

---

## CI Pipeline (GitHub Actions)

The workflow (`.github/workflows/ci.yml`) runs on every push to `main` and on pull requests. It:

1. Creates a dummy `.env` file (to avoid missing secrets)
2. Builds and starts containers:

   ```bash
   docker compose up -d --build
   ```
3. Waits 10 seconds for services to become ready
4. Tests:

   * Root endpoint `/`
   * Metrics endpoint `/metrics`
   * Prometheus targets API
5. Shows logs on failure

No real Telegram token is required for CI — dummy values are used.

---

## Project Structure

```text
.
├── .github/workflows/ci.yml
├── alertmanager/
│   └── alertmanager.yml.template
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── grafana/
│   ├── dashboards/
│   │   └── web-health-monitor.json
│   └── provisioning/
│       ├── dashboards/default.yml
│       └── datasources/datasource.yml
├── nginx/
│   └── nginx.conf
├── prometheus/
│   ├── alerts.yml
│   └── prometheus.yml
├── templates/
│   └── telegram.tmpl
├── .env
├── alertmanager.Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Environment Variables

The following variables must be defined in `.env`:

| Variable           | Description                     |
| ------------------ | ------------------------------- |
| TELEGRAM_BOT_TOKEN | Your Telegram bot token         |
| TELEGRAM_CHAT_ID   | Your Telegram chat ID (numeric) |

Alertmanager reads these variables and substitutes them into `alertmanager.yml.template` at runtime using `envsubst`.

---

## License

This project is created for educational purposes as part of a System and Network Administration course.
