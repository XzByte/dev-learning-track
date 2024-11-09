# Centralize 2 API(s) into one gateway
Sorry for long time absent, i've been working on IT Company that should work onsite, and for now i can write my tutorial or learning track from now on!

## #1 Architecture
This system implementation have simple architectural overall, but that's not the case because the tools are provided from user. \
the tools named [KrakenD](), it's similar to [Kong](https://konghq.com/) in general, but claiming to be "better" options than ```kong``` itself. \
but, never judge something from their proclaim or one-sided.. Let's begin!

![Arch](../[10]%20Centralize%20your%20apps%20using%20API%20Gateway/img/Screenshot%202024-11-09%20163032.jpg) 

## #2 Preparation
I've been doing trials and error for 1-2 day straight, and here's what i learn and done..

### The APIs
I've creating simplest APIs that can run smoothly on container without any kind of DB's or anything else.. \
1. Create 1 folder, also create 3 files that became requirement for we build the project, they're ```main.py```, ```requirements.txt```, and ```Dockerfile``` \
The APIs ```main.py```
```
from fastapi import FastAPI

app = FastAPI()

@app.get("pong/")
def ping():
    return{"success!" : {
        "values" : "pong!"
    }}
    
if __name__ == "__main__":
    import uvicorn
```
Requirement file ```requirements.txt```
```
fastapi
uvicorn
```
Last, the ```Dockerfile```
```
FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

ENV VIRTUAL_ENV=/app/venv

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```
2. You can copy into 2nd folder and rename the necessary part like the output gateway and the name of the deployment \
3. Build and push into Repos, if you dk, here's the [reference to build and push](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images) your container into repos \

### Kubernetes Manifest
I've using several file(s) that i used to build this project, they're : \
file ```krakend-deploy.yaml```
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: krakend
  namespace: krakend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: krakend
  template:
    metadata:
      labels:
        app: krakend
    spec:
      containers:
      - name: krakend
        image: <krakend/image:version>
        ports:
        - name: http
          containerPort: 8080
        imagePullPolicy: IfNotPresent
        command: ["/usr/bin/krakend"]
        args: ["run", "-d", "-c", "/etc/krakend/krakend.json"]
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "200m"
            memory: "256Mi"
        volumeMounts:
        - name: krakend-config
          mountPath: /etc/krakend
        livenessProbe:
          httpGet:
            path: /__health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 10
        securityContext:
          allowPrivilegeEscalation: false
          runAsNonRoot: true
          runAsUser: 1000
          readOnlyRootFilesystem: true
      volumes:
      - name: krakend-config
        configMap:
          name: krakend-config
```
you can adjust the spec, according your server capacity and limits \

file ```deployment.yaml``` to deploy your 2 APIs
```
# fastapi-deployment.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: deployment-api
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment-1
  namespace: deployment-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi-deployment-1
  template:
    metadata:
      labels:
        app: fastapi-deployment-1
    spec:
      containers:
      - name: fastapi-deployment-1
        image: repo/address:version
        ports:
        - containerPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment-2
  namespace: deployment-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi-deployment-2
  template:
    metadata:
      labels:
        app: fastapi-deployment-2
    spec:
      containers:
      - name: fastapi-deployment-2
        image: repo/address:version
        ports:
        - containerPort: 8080
```

krakend file for configmap inside ```krakend-config.yaml```
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: krakend-config
  namespace: krakend
data:
  krakend.json: |
    {
      "version": 3,
      "port": 8080,
      "name": "KrakenD API Gateway",
      "cache_ttl": "3600s",
      "timeout": "3000ms",
      "endpoints": [
        {
          "endpoint": "/api/ping",
          "output_encoding": "json",
          "backend": [
            {
              "host": [
                "http://deployment-name.namespaces:port"
              ],
              "url_pattern": "/ping",
              "method": "GET"
            }
          ]
        },
        {
          "endpoint": "/api/pong",
          "output_encoding": "json",
          "backend": [
            {
              "host": [
                "http://deployment-name.namespaces:port"
              ],
              "url_pattern": "/pong",
              "method": "GET"
            }
          ]
        }
      ]
    }
```
the ```krakend-config.yaml``` is quiet tricky, because it's my first time dealt with api gateway svc from external resource, i will gave you some explanation \
the block called ```endpoint``` are the gateway that you wanna expose from your API gateway. \
the block called ```host``` are placement for your apps, it should be routed correctly. how to determine your service discovery from kubernetes, my pattern are ```deployment-name.namespaces:port``` \
the last thing, are the ```url_pattern```, this block are used to get your entrypoint that you wanna route into api gateway \

After configmap are created, we move into ```krakend-svc.yaml```
```
# krakend-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: krakend-service
  namespace: krakend
spec:
  type: LoadBalancer
  selector:
    app: krakend
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8080

```
next are the ```deployment-api-service.yaml```
```
# fastapi-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service-1
  namespace: deployment-api
spec:

  selector:
    app: fastapi-deployment-1
  ports:
    - protocol: TCP
      port: 8081
      targetPort: 8080

---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service-2
  namespace: deployment-api
spec:
  selector:
    app: fastapi-deployment-2
  ports:
    - protocol: TCP
      port: 8082
      targetPort: 8080
```
and the last thing are ```ingress.yaml```, the thing that remain unresolved yet for me
```
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: krakend-ingress
  namespace: krakend
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
  - host: domain.expansion  # Replace with your domain
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: krakend  # Must match your service name
            port:
              number: 80  # Must match your service port
```
idk how this config won't route my deployment...
the error are "there's no default backend", but after i adding defaultBackend the error change into "The server encountered a temporary error and could not complete your request.Please try again in 30 seconds.", so i wait and dive to community, along with discussion with my friends.. and i got some "enlignentment" from someone there
```
Krakend is not fit for an ingress controller because of it non-dynamic nature
It really sucks to have to do double jumps, meaning, to enter kubernetes requests would need to go to nginx, then krakend, then the destination
A way to fix this is to add krakend outside of kubernetes but that will complicate the deployment stack.
```
that's why i creating this tutorial that have checkpoint when doing service as loadbalancer instead of ingress service.
\
btw, after you done setting up all files inside a folder, just simply do 
```
kubectl apply -f .
```
and wait till finish...

### Proof of Concept

deployment apis
```
root@gke-remote:~/python-api/manifest# kubectl get deployment -n deployment-api
NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
fastapi-deployment-1   1/1     1            1           25h
fastapi-deployment-2   1/1     1            1           25h
root@gke-remote:~/python-api/manifest# 
```

krakend deployment
```
root@gke-remote:~/python-api/manifest# kubectl get deployment -n krakend
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
krakend   1/1     1            1           19h
root@gke-remote:~/python-api/manifest# 
```

krakend service
```
root@gke-remote:~/python-api/manifest# kubectl get svc -n krakend
NAME               TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)        AGE
krakend-service    LoadBalancer   xx.xxx.xxx.xxx   xx.xxx.xxx.xx   80:30157/TCP   25h
krakend-service2   ClusterIP      xx.xxx.xxx.xx    <none>          80/TCP         16h
root@gke-remote:~/python-api/manifest# 
```

api service
```
root@gke-remote:~/python-api/manifest# kubectl get svc -n deployment-api
NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
fastapi-service-1   ClusterIP   xx.xxx.xxx.xxx   <none>        8081/TCP   25h
fastapi-service-2   ClusterIP   xx.xxx.xxx.xx    <none>        8082/TCP   25h
```

krakend configmap
```
root@gke-remote:~/python-api/manifest# kubectl get configmap -n krakend
NAME               DATA   AGE
krakend-config     1      25h
kube-root-ca.crt   1      25h
root@gke-remote:~/python-api/manifest#
```
the configmap are created by running the file ```krakend-config.yaml```

last, the frinckin ingress
```
root@gke-remote:~/python-api/manifest# kubectl get ingress -n krakend
NAME              CLASS    HOSTS                    ADDRESS          PORTS   AGE
krakend-ingress   <none>   domain.expansion         xx.xxx.xxx.xxx   80      25h
root@gke-remote:~/python-api/manifest#
```

if you have suggestion to resolve my problem, don't hesistate to reach me out... thanks for advance..

overall, i stuck on svc that can be accessed, but when it's come to ingress, the error remain unresolved....