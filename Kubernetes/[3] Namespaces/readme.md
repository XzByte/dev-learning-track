# Namespaces

In this section, i'm gonna performing some steps and giving tips to "production ready" kubernetes deployment

## Start from separating resource by using difference namespaces
In term of deployment on kubernetes, using namespaces the ```right``` way are so important, why? 
here's the logic :
when you need to deploy many development from your project, you should separate them one with another, the reason are to keep your project well structured, easier to arrange, troubleshoot, or even rolling back and delete those resource without worrying about another ```healthy``` resources

## How to do it then?
start from creating namespaces
```
kubectl create namespace <namespace name>
```
when the namespace are successfuly created, it will gave you output like below
```
root@gke-remote:~# kubectl create namespace server-nginx
namespace/server-nginx created
```
tip from official kubernetes website
```
When you create a Service, it creates a corresponding DNS entry. This entry is of the form <service-name>.<namespace-name>.svc.cluster.local, which means that if a container only uses <service-name>, it will resolve to the service which is local to a namespace. This is useful for using the same configuration across multiple namespaces such as Development, Staging and Production. If you want to reach across namespaces, you need to use the fully qualified domain name (FQDN).

```
As a result, all namespace names must be valid [RFC 1123 DNS labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-label-names).

## Next tip, when you're wanna work with one namespaces at a time, here's the method
after creating your namespace, now we need to configure it as default namespaces for current working area
```
kubectl get namespaces
```
you should seen output of all list from your namespaces
```
root@gke-remote:~# kubectl get namespaces
NAME                 STATUS   AGE
default              Active   3d5h
gke-managed-system   Active   3d5h
gmp-public           Active   3d5h
gmp-system           Active   3d5h
kube-node-lease      Active   3d5h
kube-public          Active   3d5h
kube-system          Active   3d5h
server-nginx         Active   6s
```
for now, i just wanna use ```server-nginx``` as my namespaces working area, so here's the command to achieve that
```
kubectl config set-context --current --namespace=server-nginx
```
here's the output
```
root@gke-remote:~# kubectl config set-context --current --namespace=server-nginx
Context "cluster-name" modified.
```
and how to validate it? simple, just execute this command, and check the outputs
```
root@gke-remote:~# kubectl config get-contexts
CURRENT   NAME                                                           CLUSTER                                                        AUTHINFO                                                       NAMESPACE
*         gke_formal-precinct-431212-u7_us-central1-c_superbig-cluster   gke_formal-precinct-431212-u7_us-central1-c_superbig-cluster   gke_formal-precinct-431212-u7_us-central1-c_superbig-cluster   server-nginx
```
or
```
root@gke-remote:~# kubectl config view --minify
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: censored for public
  name: gke_formal-precinct-431212-u7_us-central1-c_superbig-cluster
contexts:
- context:
    cluster: gke_formal-precinct-431212-u7_us-central1-c_superbig-cluster
    namespace: server-nginx
    user: gke_formal-precinct-431212-u7_us-central1-c_superbig-cluster
  name: gke_formal-precinct-431212-u7_us-central1-c_superbig-cluster
current-context: gke_formal-precinct-431212-u7_us-central1-c_superbig-cluster
kind: Config
preferences: {}
users:
- name: gke_formal-precinct-431212-u7_us-central1-c_superbig-cluster
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      args: null
      command: gke-gcloud-auth-plugin
      env: null
      installHint: Install gke-gcloud-auth-plugin for use with kubectl by following
        https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl#install_plugin
      interactiveMode: IfAvailable
      provideClusterInfo: true
```
you could see the current namespaces that you're working now!

## Alternative for deployment without configure working namespaces
if you wanna deploy apps into specified namespaces without select or changing them, here's the way
```
you could add parameter --namespace to your kubectl command like example below

kubectl run nginx --image=nginx --namespace=<insert-namespace-name-here>
kubectl get pods --namespace=<insert-namespace-name-here>
```
