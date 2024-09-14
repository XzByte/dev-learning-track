# Deploying kubernetes dashboard
when you're tired for configuring your cluster or resource using terminal, use this one

## install helm chart
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
## Deploy the dashboard using helm command
```
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard --set kong.admin.tls.enabled=false
```
after that, check your deployment
```
(optional)
change your namespaces into "kubernetes-dashboard"
kubectl config set-context --current --namespace=kubernetes-dashboard

next : 
kubectl get pods

you should get output like this
root@gke-remote:~/deployment# kubectl get pods
NAME                                                    READY   STATUS    RESTARTS   AGE
kubernetes-dashboard-api-6549f8f9d6-djdf2               1/1     Running   0          155m
kubernetes-dashboard-auth-6d588b9f7-vjbgq               1/1     Running   0          155m
kubernetes-dashboard-kong-6d6dbcb577-lsj9k              1/1     Running   0          155m
kubernetes-dashboard-metrics-scraper-6b6f6f5d5c-rvbbw   1/1     Running   0          155m
kubernetes-dashboard-web-75cccd6488-4wk6b               1/1     Running   0          155m
```

to delete deployment of kubernetes-dashboard, you can execute this command directly 
```
helm delete kubernetes-dashboard --namespace kubernetes-dashboard

delete user and it's rolebinding
kubectl delete -f /path/to/file.yaml
```