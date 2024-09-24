# Finally, i came to this section after a few trial and error

## First thing first..
this section had specified pre-requisite to be fulfiled before executing the tutorials, they're include
- [have coded to deploy into a container](https://github.com/XzByte/dev-learning-track/tree/main/Python/Building%20backend%20and%20api's/flask-api/example-api)
- [Creating a Dockerfile to build a container](link)
- [creating Artifact registy to store containerized app](link)

## Now we start from building the apps
after all pre-requisite above been satisfied, you can build your app into a container and store them into artifact registries

here's how you achieve that
```
how to point your repository from your vm :
gcloud auth configure-docker \
    your-region-docker.pkg.dev

how to build :
docker build -t your-region-docker.pkg.dev/your/created/artifact registries/container-name:version .

how to push :
docker push your-region-docker.pkg.dev/your/created/artifact registries/container-name:version
```
after we done building and storing our API's, now we create manifest to deploy it into kubernetes cluster

## Deploy the apps
in this section, we'll creating the manifest for deployment, for the manifest will be separated into 2 files :

deployment.yaml 
```
apiVersion: v1
kind: Namespace
metadata:
  name: flask-api
---
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: flask-api
  name: flask-api
spec:
  selector:
    matchLabels:
      app: flask-api
  replicas: 3
  template:
    metadata:
      labels:
        app: flask-api
    spec:
      containers:
      - name: flask-api
        image: your-region-docker.pkg.dev/your/created/artifact registries/container-name:version
        ports:
        - containerPort: 5000

```

svc.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: api-expose
  namespace: flask-api
spec:
  type: LoadBalancer
  selector:
    app: flask-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000

```
after all those manifest been stored on one dir, simply use ```kubectl apply -f .``` and then wait for the deployment finished

next are checking the pods that been deployed
```
root@gke-remote:~/deployment/docker-deploy# kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
flask-api-658797d76-55v49   1/1     Running   0          2d15h
flask-api-658797d76-9bfqt   1/1     Running   0          27s
flask-api-658797d76-rsl57   1/1     Running   0          40s
```

check the svc that been exposed using ```LoadBalancer``` type
```
root@gke-remote:~/deployment/docker-deploy# kubectl get svc
NAME         TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)        AGE
api-expose   LoadBalancer   xx.xx.xxx.xxx   xxx.xxx.xxx.xx   80:30914/TCP   2d15h
```
after that, access the Api's gateway using curl
```
root@gke-remote:~/deployment/docker-deploy# curl http://<your external IP>/test
"You've done better!"
```
