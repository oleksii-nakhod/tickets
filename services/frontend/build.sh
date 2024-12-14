docker build -t frontend:latest .
docker tag frontend:latest wartexnik/frontend:latest
docker push wartexnik/frontend:latest
kubectl rollout restart deployment frontend
minikube service frontend --url

kubectl apply -f frontend.yaml