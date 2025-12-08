# Kubernetes Deployment Guide for Flight Ticket Booking

## Prerequisites

- Kubernetes cluster running (minikube, Docker Desktop K8s, EKS, GKE, AKS, etc.)
- `kubectl` installed and configured
- Docker image pushed to a registry (Docker Hub, ECR, GCR, etc.) or available locally

## Setup Instructions

### 1. Push Docker Image to Registry

```bash
# For Docker Hub
docker login
docker tag flight-app:latest <your-docker-username>/flight-app:latest
docker push <your-docker-username>/flight-app:latest

# For AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag flight-app:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/flight-app:latest
docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/flight-app:latest
```

### 2. Update Image Reference

Edit `k8s/deployment.yaml` and replace:
```yaml
image: flight-app:latest
```
with your registry image:
```yaml
image: <your-docker-username>/flight-app:latest
```

Or edit `k8s/kustomization.yaml`:
```yaml
images:
- name: flight-app
  newName: <your-docker-username>/flight-app
  newTag: "latest"
```

### 3. Update SECRET_KEY

Edit `k8s/deployment.yaml` and replace the SECRET_KEY with a strong, unique value:
```yaml
stringData:
  SECRET_KEY: "your-strong-secret-key-here"
```

### 4. Deploy to Kubernetes

**Option A: Using kubectl directly**

```bash
kubectl create namespace flight-app
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

**Option B: Using Kustomize (recommended)**

```bash
kubectl apply -k k8s/
```

### 5. Verify Deployment

```bash
# Check namespace
kubectl get namespace flight-app

# Check deployment
kubectl get deployments -n flight-app

# Check pods
kubectl get pods -n flight-app

# Check service
kubectl get svc -n flight-app

# View pod logs
kubectl logs -n flight-app -l app=flight-app --tail=100 -f

# Describe deployment
kubectl describe deployment flight-app -n flight-app
```

### 6. Access the Application

```bash
# Get the external IP (may take a few minutes)
kubectl get svc flight-app-service -n flight-app

# On minikube
minikube service flight-app-service -n flight-app

# On Docker Desktop
# Access via: http://localhost (after port-forward setup)

# Port forward for local testing
kubectl port-forward -n flight-app svc/flight-app-service 8000:80
# Then access: http://localhost:8000
```

## Key Features in the Deployment

- **Namespace Isolation**: Dedicated `flight-app` namespace
- **ConfigMap**: Environment-specific configuration
- **Secrets**: Secure storage of sensitive data (SECRET_KEY)
- **Liveness & Readiness Probes**: Health checks for pod management
- **Resource Limits**: CPU and memory constraints
- **Horizontal Pod Autoscaler (HPA)**: Auto-scales between 2-5 replicas based on CPU (70%) and memory (80%)
- **LoadBalancer Service**: Exposes the app externally
- **NetworkPolicy**: Restricts pod-to-pod communication

## Scaling

The deployment automatically scales based on CPU and memory usage. View HPA status:

```bash
kubectl get hpa -n flight-app
kubectl describe hpa flight-app-hpa -n flight-app
```

## Cleanup

```bash
# Delete all resources in the namespace
kubectl delete namespace flight-app

# Or delete specific resources
kubectl delete -k k8s/
```

## Production Considerations

1. **Image Registry**: Use a private Docker registry (Docker Hub private, ECR, GCR)
2. **Secrets Management**: Use Kubernetes Secrets or external secret management (Sealed Secrets, HashiCorp Vault)
3. **Ingress**: Replace LoadBalancer with Ingress for domain routing
4. **Storage**: For persistent data, add PersistentVolume/PersistentVolumeClaim
5. **Monitoring**: Add Prometheus/Grafana for metrics
6. **Logging**: Integrate ELK stack or CloudWatch for centralized logging
7. **HTTPS**: Use cert-manager with Let's Encrypt
8. **Database**: Consider managed database service (RDS, Cloud SQL, etc.) instead of SQLite
