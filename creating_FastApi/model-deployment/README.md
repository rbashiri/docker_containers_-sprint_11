# Create multiple tags for the same image
docker tag diabetes-api:latest yourusername/diabetes-prediction-api:latest
docker tag diabetes-api:latest yourusername/diabetes-prediction-api:v1.0
docker tag diabetes-api:latest yourusername/diabetes-prediction-api:production

# Push all versions
docker push yourusername/diabetes-prediction-api:latest
docker push yourusername/diabetes-prediction-api:v1.0
docker push yourusername/diabetes-prediction-api:production