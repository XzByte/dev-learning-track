# Adding certificate into your deployment using cert-manager
## Pre-requisite
- [x] deployment or manifest that contain file deployment, service, and ingress
- [x] valid DNS and the access into registrar

This section will be separated by 3 parts

## Deployment Cert-manager into cluster
In this part, I'm gonna show how to deploy cert manager

1. Deploy cert manager release from manifest
```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.3/cert-manager.yaml
```
check the deployment
```
kubectl get pods --namespace cert-manager

root@gke-remote:~/deployment/docker-deploy# kubectl get po -n cert-manager
NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-7fbbc65b49-pxxdc              1/1     Running   0          12h
cert-manager-cainjector-6664fc84f6-ffqwl   1/1     Running   0          12h
cert-manager-webhook-59598898fd-7sq9k      1/1     Running   0          12h
```
now, we move to manifest config 
## Configure manifest and deployment
In this part, I'm gonna reuse file ```ingress.yaml```, then create file named ```cluster-issuer.yaml```, and ```self-sign.yaml```
```cluster-issuer.yaml``` file
```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: self-signed-cluster-issuer
  namespace: cert-manager
spec:
  selfSigned: {}
```
config above are meant to be certificate issuer inside cluster and cluster-wide range, so you don't need to configure that on every namespaces
then, apply the config
```
root@gke-remote:~/deployment/docker-deploy# kubectl apply -f cluster-issuer.yaml 
clusterissuer.cert-manager.io/self-signed-cluster-issuer created
```
next, the file ```self-sign.yaml```
```
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: flask-api-tls
  namespace: flask-api  # Change to your target desired namespace
spec:
  secretName: honey-pie-tls-secret  # desired secret name
  commonName: honey.pie              # your-domain-name
  dnsNames:
    - honey.pie                         # your-domain-name
    - flask-api.honey.pie               # your-domain-name
  issuerRef:
    name: self-signed-cluster-issuer    # paste your cluster-issuer name
    kind: ClusterIssuer
  duration: 24h                         # how long the cert will be valid
  renewBefore: 12h                      # the renewal cert time
```
save and then execute the config
```
root@gke-remote:~/deployment/docker-deploy# kubectl apply -f self-sign.yaml 
certificate.cert-manager.io/flask-api-tls created
```

next, edit your ```ingress.yaml```
and add block config to apply your cert that been generated before
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-ingress
  namespace: flask-api
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: self-signed-cluster-issuer # add cluster issuer into annotation
spec:
  tls:                                      # add TLS field
  - hosts:                                  # specified the host
    - honey.pie                             # your DNS
    - flask-api.honey.pie                   # your dns
    secretName: honey-pie-tls-secret    # add secret-name that you've created before here
  defaultBackend: 
    service:
      name: api-expose
      port:
        number: 80
  rules:
    - host: flask-api.honey.pie
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-expose
                port:
                  number: 80
```
apply and check the status
```
root@gke-remote:~/deployment/docker-deploy# kubectl apply -f ingress.yaml 
ingress.networking.k8s.io/flask-ingress configured

root@gke-remote:~/deployment/docker-deploy# kubectl get ingress
NAME            CLASS    HOSTS                      ADDRESS         PORTS     AGE
flask-ingress   <none>   flask-api.honey.pie        xx.xxx.xxx.xx   80, 443   3d3h
```
all done, now we should validate it again and edit the IP domain that we've been point before on registrar (mine, cloudflare)
## Validation
1. copy the ingress address that point into your dns on ```kubectl get ingress```
2. go to DNS setting, edit the hostname that you point on ingress
3. change the IP into ingress IP and save
4. wait for some time (under 10 mins) for the changes to be applied
5. now navigate into your domain from browser
for now, the cert are invalid maybe i'm gonna figure it out using some method like issuing using files directly or create valid SSL 
