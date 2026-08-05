# Kubernetes Notes

This folder contains a practical Kubernetes version of the diabetes API project.

## Project

Main project path:

`Container_Orchestration/k8s-diabetes-api`

Important files:

- `api/app.py` - FastAPI application
- `api/Dockerfile` - API image build
- `k8s/database-deployment.yaml` - PostgreSQL deployment
- `k8s/database-service.yaml` - PostgreSQL service
- `k8s/api-deployment.yaml` - API deployment
- `k8s/api-service.yaml` - API service

## What Kubernetes Replaces

Docker Compose version:

- one API container
- one PostgreSQL container
- internal networking between containers

Kubernetes version:

- one deployment for the API
- one deployment for PostgreSQL
- one service for the API
- one service for PostgreSQL

## Build The API Image

From inside `Container_Orchestration/k8s-diabetes-api`:

```bash
docker build -f api/Dockerfile -t diabetes-api:local .
```

Use this command because the Dockerfile copies files from the project root context.

## Deploy In Order

```bash
kubectl apply -f k8s/database-deployment.yaml
kubectl apply -f k8s/database-service.yaml
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/api-service.yaml
```

Check status:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

## Database Setup

Get the database pod name:

```bash
kubectl get pods -l app=diabetes-db
```

Open PostgreSQL inside the pod:

```bash
kubectl exec -it <db-pod-name> -- psql -U postgres -d diabetes_db
```

Create the logging table:

```sql
CREATE TABLE IF NOT EXISTS prediction_logs (
	id SERIAL PRIMARY KEY,
	timestamp TIMESTAMP NOT NULL,
	input_data JSONB NOT NULL,
	prediction INTEGER NOT NULL,
	probability FLOAT NOT NULL,
	risk_level VARCHAR(10) NOT NULL
);
```

## Access The API

If `LoadBalancer` does not expose localhost directly, use port forwarding:

```bash
kubectl port-forward service/diabetes-api-service 8000:8000
```

Then open:

- `http://localhost:8000`
- `http://localhost:8000/docs`

## Scaling

Manual scaling:

```bash
kubectl scale deployment diabetes-api --replicas=5
kubectl scale deployment diabetes-api --replicas=2
```

Before using HPA, add CPU and memory resources to `k8s/api-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: diabetes-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: diabetes-api
  template:
    metadata:
      labels:
        app: diabetes-api
    spec:
      containers:
      - name: api
        image: diabetes-api:local
        env:
        - name: DB_HOST
          value: "diabetes-db-service"
        - name: DB_NAME
          value: "diabetes_db"
        - name: DB_USER
          value: "postgres"
        - name: DB_PASSWORD
          value: "password"
        - name: DB_PORT
          value: "5432"
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
```

Apply the deployment update:

```bash
kubectl apply -f k8s/api-deployment.yaml
```

Create `k8s/api-hpa.yaml`:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: diabetes-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: diabetes-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

Apply the HPA:

```bash
kubectl apply -f k8s/api-hpa.yaml
kubectl get hpa
```

This setup keeps at least 2 API pods running, allows scaling up to 10 pods, and uses average CPU usage to decide when to scale.

Useful checks:

```bash
kubectl get hpa
kubectl top nodes
kubectl top pods
```

## Common Issues

`kubectl: command not found`

- install `kubectl`

`kubectl top nodes` or `kubectl top pods` fails

- Metrics Server is not installed yet, or
- the cluster is not running, or
- Metrics Server needs patching

Patch command if needed:

```bash
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
```

## Cleanup

Check what is still running:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get hpa
kubectl get all
```
``` bash
Understanding the output:

Pods — The actual running containers
Deployments — The managers controlling the Pods
Services — The entry points to access your Pods
HPAs — The autoscalers watching your deployments

```
Delete only this project:

```bash
kubectl delete hpa diabetes-api-hpa
kubectl delete service diabetes-api-service
kubectl delete service diabetes-db-service
kubectl delete deployment diabetes-api
kubectl delete deployment diabetes-db
```

Check that the project resources are gone:

```bash
kubectl get all
```

If you only want to stop the API without deleting it:

```bash
kubectl scale deployment diabetes-api --replicas=0
```

Start it again:

```bash
kubectl scale deployment diabetes-api --replicas=2
```

Remove the local Docker image if you do not need it anymore:

```bash
docker rmi diabetes-api:local
```

Avoid `kubectl delete all --all` unless you want to wipe the whole cluster namespace.
