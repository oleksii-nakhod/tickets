docker build -t search:latest .
docker tag search:latest wartexnik/search:latest
docker push wartexnik/search:latest
kubectl rollout restart deployment search
minikube service search --url
