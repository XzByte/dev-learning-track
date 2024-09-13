# when deleting resource on kubernetes cluster, it had plenty ways to achieve it

## deleting using files

To delete all deployments inside the default namespace, use:
```
kubectl delete deployment --all --namespace=default
```
when it comes to specified resource, use command below
```
kubectl delete deployment <deployment name> --namespace <namespace name>

when you're already set your namespaces, instead

kubectl delete deployment <deployment name>
```
for deleting svc that being deployed
```
kubectl delete svc <svc name>
```

here's the last thing... when you need to delete using the manifest file that you've been created, simply execute command below
```
for one file :
kubectl delete -f /path/to/file.yaml

for entire deployment on folder(s)
kubectl delete -f /foldername
```