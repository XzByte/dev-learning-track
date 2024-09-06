# Fisrt things first

I'm assuming you already had the kuberconfig creds file, if not, copy or export it from your cluster or cloudshell

next are just place your kube/config into your vps, the step are simple
1. when the .kube folder isn't exist, just simply create it with :
```
mkdir -p .kube
```
2. after that, create file such as kubeconfig or config or anything elses that you desired, but always remember it when exporting or placing it inside env on file .bashrc
```
touch kubeconfig
```
3. when you already had the files, simply paste it or place it inside .kube folder
4. if not, just create the file and copast the content from creds you got from cluster or cloudshell, and save then exit
5. now if you wanna use the config to your shell, just simply export it, but it will require redo the step when you close your shell or your shell timed out
```
export KUBECONFIG=/your/dir/file
```
6. after that, tried to check your nodes/pods/cluster info by simply typing
```
kubectl get pods
or
kubectl get nodes
or
kubectl cluster-info
```
when your command return without error and show what it should be shown, you're good to go and ready to deploy

## saving your env into .bashrc
consideration are your creds file are saved and auto exported into env, so be careful when doing this, when you're ready, here's the step
1. go to home or root dir (when you had root privilege)
2. then, just edit or append line that you wanna add, in this case are KUBECONFIG, so here's the command
```
echo "KUBECONFIG=/path/to/your file
```
or you could use your desired text editor such as vi/m, nano, atom, etc...
3. after finish write your code or adding values and saving it, simply export/apply your new line using this command
```
source ~/.bashrc
```
after that, tried to do same command to show resource on your cluster, when it return same output without error and show what should be shown, you're good to go