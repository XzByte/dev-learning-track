# Upscale, Descale, and Rolling back deployment


## Prerequisite
the main prerequisite are previous deployment, because we deploy a svc and then manually scale it using ```kubectl scale``` to upscale the deployment

Let's start with deployment 

change dedfault context for namespaces: 
```
root@gke-remote:~/deployment/manifest-deploy# kubectl config set-context --current --namespace=wss-nginx
Context "gke_formal-precinct-431212-u7_us-central1-c_superbig-cluster" modified.
```
check deployment pods :
```
root@gke-remote:~/deployment/manifest-deploy# kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-5f77c77f6-7s549   1/1     Running   0          41s
```
check deployment name to make sure the parameter ```deployment/`` are correct
```
root@gke-remote:~/deployment/manifest-deploy# kubectl get deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   1/1     1            1           119s
```

## To manually upscale your kubernetes deployment, you can execute command below
```
kubectl scale --current-replicas=1 --replicas=3 deployment/nginx-deployment

when success :
deployment.apps/nginx-deployment scaled
```
check the pods after upscaling the deployment
```
root@gke-remote:~/deployment/manifest-deploy# kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-5f77c77f6-7s549   1/1     Running   0          2m52s
nginx-deployment-5f77c77f6-b8h26   1/1     Running   0          12s
nginx-deployment-5f77c77f6-gh8qb   1/1     Running   0          12s
```

## When you wanna downscale it, use command below
```
kubectl scale --current-replicas=3 --replicas=1 deployment/nginx-deployment

when success:
deployment.apps/nginx-deployment scaled
```
check the pods after downscaled
```
root@gke-remote:~/deployment/manifest-deploy# kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-5f77c77f6-b8h26   1/1     Running   0          44s
```
## Rolling back deployment
```coming soon!```
