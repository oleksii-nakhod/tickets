kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f mysql-pvc.yaml
kubectl apply -f mysql.yaml
kubectl apply -f database.yaml

docker build -t wartexnik/database:latest .
docker push wartexnik/database:latest
kubectl rollout restart deployment database
minikube service database --url


kubectl exec -it mysql-6d67799f4d-qbwjk -- mysql -uroot -p