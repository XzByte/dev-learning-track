# Exposing your deployment to internet

## This requre you to finish previous task (deploy your first deployment) to perform this task

So, let's begin!

## First things first
In this task, we'll expose our previously deployed app into internet using LoadBalancer service type

This are the to the point step
check your deployment using command below
```
kubectl get deployment
```
```
output :

root@gke-remote:~/deployment# kubectl get deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   1/1     1            1           23h
```
remember the name of your deployment, and then inspect it to reveal the ports that we should expose using proxy
```
kubectl describe deployment/nginx-deployment
```
```
output :

Name:                   nginx-deployment
Namespace:              default
CreationTimestamp:      Fri, 06 Sep 2024 10:01:39 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.14.2
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-deployment-d556bf558 (1/1 replicas created)
Events:          <none>
```
and now we got the port that should we expose or proxied (port 80)
to exposing using ```kubectl``` command, here's the example :
```
kubectl expose deployment nginx-deployment --port=8080 --target-port=80 \
        --name=nginx-expose --type=LoadBalancer
```
```
explaination :

kubectl expose : This is the base command for creating a Service in Kubernetes. It exposes a resource (like a pod, deployment, or service) to other services or external traffic.

deployment nginx-deployment : deployment specifies the type of resource you're exposing. In this case, it’s a Deployment named nginx-deployment
                              nginx-deployment is the name of deployment that you've been created in previous task

--port=8080 : --port specifies the port that the Service will expose. This is the port on which the Service will be accessible from within the cluster or externally (depending on the Service type).
              In this case, the Service will be accessible on port 8080

--target-port=80 : --target-port specifies the port on the containers (pods) managed by the Deployment to which the Service should forward traffic.
                   Here, the Service will forward traffic received on port 8080 to port 80 on the pods.

--name=nginx-expose : --name specifies the name of the Service that will be created.
                      nginx-expose is the name of the Service. This is how you will refer to the Service when interacting with it or querying its status

--type=LoadBalancer : --type specifies the type of Service to create.
                      LoadBalancer is a type of Service that provisions an external load balancer through your cloud provider (like AWS, Azure, or GCP). This load balancer will have an external IP address and will route traffic to the Service.
                      When you use LoadBalancer, Kubernetes will automatically provision a cloud load balancer and assign an external IP to the Service, making it accessible from outside the cluster.
```
after that, you should get ouutput below :
```
service/nginx-expose exposed
```
and then, check the service deployment status
```
root@gke-remote:~/deployment# kubectl get svc
NAME           TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)          AGE
kubernetes     ClusterIP      34.118.224.1     <none>          443/TCP          45h
nginx-expose   LoadBalancer   34.118.237.217   35.184.77.130   8080:30162/TCP   46s
```
external IP has been allocated into your svc, and now you can access it trough internet
```
root@gke-remote:~/deployment# curl 35.184.77.130:8080
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```