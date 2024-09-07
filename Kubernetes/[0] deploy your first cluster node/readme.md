# First thing first
## I'm using GKE for this project, maybe i'm gonna explore another resource such as AKS or EKS

first, try to deploy your cluster on GKE, you could using autopilot or something, that's doesn't matter
second, tried to connect automatically using default service and then find the kubeconfig on your cloudshell using code-server, after that save the creds on notepad

## VPS prep
in this tutorial, i'm gonna told you step by step how to configure your GKE cluster on Compute Engine

first thing first, just configure your compute engine as usual, but when you scroll or find "accesses scope" choose all enabled to enable access of kubernetes engine remote
next is just you create files config and fill it with your previously copied creds on notepad, after finishing it, start by accessing the VPS

## Configure the plugins and kubectl
straightforward step
```
apt update
apt install kubectl -y
```
after kubectl successfully installed, then install Kubernetes clients because it's require an authentication plugin, gke-gcloud-auth-plugin, which uses the Client-go Credential Plugins framework to provide authentication tokens to communicate with GKE clusters.

here's how
```
apt install google-cloud-sdk-gke-gcloud-auth-plugin
```
after that, export your config into env
```
export KUBECONFIG=/path/to/your/config
```
and then try to type :
```
kubectl get nodes
```