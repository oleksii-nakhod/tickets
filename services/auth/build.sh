docker build -t auth:latest .
docker tag auth:latest wartexnik/auth:latest
docker push wartexnik/auth:latest
kubectl rollout restart deployment auth
minikube service auth --url

kubectl apply -f auth.yaml