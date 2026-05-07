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

