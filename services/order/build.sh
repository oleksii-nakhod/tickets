docker build -t order:latest .
docker tag order:latest wartexnik/order:latest
docker push wartexnik/order:latest
kubectl rollout restart deployment order
minikube service order --url

kubectl apply -f secret.yaml
kubectl apply -f order.yaml