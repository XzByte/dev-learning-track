## In this step, i'm gonna deploy using manifest file

I'm gonna separate the steps into 3 section....

## 1st, create the namespaces
This are the easiest one, because it can be achieved by simply using ```kubectl create namespaces```, but in this section, i'm gonna show how to do that using manifest
create a folder to store all manifest file(s) first, and then write this config inside file called ```namespaces.yaml```
```
create folder and file

mkdir -p manifest-deploy
touch namespaces.yaml
```
next, add configuration below to your script ```namespaces.yaml```
```
apiVersion: v1
kind: Namespace
metadata:
  name: wss-nginx
```
after that, simply execute
```
kubectl apply -f /manifest-deploy/namespaces.yaml
```
you should get output like this
```
root@gke-remote:~/deployment# kubectl apply -f manifest-deploy/wss-namespace.yaml 
namespace/wss-nginx created
root@gke-remote:~/deployment# kubectl get namespaces
NAME                 STATUS   AGE
default              Active   4d23h
gke-managed-system   Active   4d23h
gmp-public           Active   4d23h
gmp-system           Active   4d23h
kube-node-lease      Active   4d23h
kube-public          Active   4d23h
kube-system          Active   4d23h
wss-nginx            Active   60s
```
## 2nd section
next, create deployment for nginx, just create new file ```deployment.yaml``` and paste script below
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: wss-nginx
spec:
  selector:
    matchLabels:
      app: wss-nginx
  replicas: 2 # tells deployment to run 2 pods matching the template
  template:
    metadata:
      labels:
        app: wss-nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```
after that, you can deploy it directly after saving the files, or you can create one more config manifest to expose your deployment
```
if you wanna deploy it now, execute it

kubectl apply -f /manifest-deploy/deployment.yaml
```
after execution, you should get output like this
```
root@gke-remote:~/deployment# kubectl apply -f manifest-deploy/deployment.yaml 
deployment.apps/nginx-deployment created
root@gke-remote:~/deployment# kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-5f77c77f6-mkpl8   1/1     Running   0          7s
nginx-deployment-5f77c77f6-pdtjr   1/1     Running   0          7s
```
## last step, create config manifest to expose your deployment to internet
create one config manifest, called ```service.yaml```
add script below
```
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: wss-nginx
spec:
  type: LoadBalancer
  selector:
    app: wss-nginx
  ports:
  - protocol: TCP
    port: 8080
    targetPort: 80
```
the spec type should marked as LoadBalancer to get external IP from IP Pools.
after successful svc creation, you should get external IP like this
```
root@gke-remote:~/deployment# kubectl get svc
NAME            TYPE           CLUSTER-IP       EXTERNAL-IP         PORT(S)          AGE
nginx-service   LoadBalancer   34.118.237.138   xxx.xxx.xxx.xxx     8080:31124/TCP   71s
```