# Monitoring Setup: Prometheus & Grafana

## Deploy Prometheus
kubectl apply -f prometheus-configmap.yaml
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f prometheus-service.yaml

## Deploy Grafana
kubectl apply -f grafana-deployment.yaml
kubectl apply -f grafana-service.yaml

## Access Services
- Prometheus: http://<NodeIP>:32001
- Grafana: http://<NodeIP>:32000 (login: admin/admin)

## Configure Grafana
1. Add Prometheus as a data source (URL: http://prometheus:9090)
2. Import dashboards or create your own to visualize Django metrics

## Prometheus Scrape Target
- The config scrapes metrics from your Django service at `/metrics`.
- Ensure your Django service is named `django-service` and exposes port 8000.

## Example Dashboard
- Use the Prometheus data source in Grafana to create graphs for request count, latency, etc.
