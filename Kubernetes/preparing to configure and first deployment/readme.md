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
2. then, just edit or append line that you wanna add, in this case are KUBECONFIG, so here's the command.
To set it permanently for all future bash sessions add such line to your .bashrc file in your $HOME directory.
```
echo "KUBECONFIG=/path/to/your file"
```
or you could use your desired text editor such as vi/m, nano, atom, etc...
3. after finish write your code or adding values and saving it, simply export/apply your new line using this command
```
source ~/.bashrc
```
4. To set it permanently, and system wide (all users, all processes) add set variable in /etc/environment:
```
sudo -H gedit /etc/environment
```
after finish write your code or adding values and saving it, simply export/apply your new line using this command
```
source ~/.bashrc
```
after that, tried to do same command to show resource on your cluster, when it return same output without error and show what should be shown, you're good to go

# First deployment (nginx web server)

1. now, create folder with desired name (mine are deployment) to store file for deployments and configs
```
mkdir -p deployment
then
cd deployment
```
2. create file for deployment, (for this tutorial, i'm just gonna use official tutor from kubernetes)
```
touch file nginx-deployment.yaml
```
3. after that, copy config below
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment #app name 
spec:
  selector:
    matchLabels:
      app: nginx #labelling the deployment
  replicas: 1 # tells deployment to run 1 pods matching the template
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2 #base image that i'm using on this tutorial
        <!-- resources:
          requests: #requesting resource to be allocated
            memory: "64Mi" #requested memories allocated
            cpu: "250m" #requested cpu allocated
          limits:
            memory: "128Mi" #memmory limit
            cpu: "500m" #cpu limit # i've commented this because i'm not gonna use it, but it's just for trivia to limit kubernetes resource on config file--> 
        ports:
        - containerPort: 80 #service port exposed/alocated
```
4. next, save and deploy using this command
```
kubectl apply -f nginx-deployment.yaml 
```
5. check the resource that been configured, using this command
```
kubectl get deployment
```
the output should be like this
```
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   1/1     1            1           2s
```