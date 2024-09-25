# Aight, now the DNS configuration
## Pre-requisite
- [active domain name]()
- [access to registrar to configure sub-domain](dash.cloudflare.com)
- [deployment on kubernetes cluster](<../[2] exposing your deployment to internet>)

## Now we configure!
first thing are check your ```deployment``` on your cluster
```
kubectl get deployment -n <your-namespace>

root@gke-remote:~/deployment/docker-deploy# kubectl get deployment -n flask-api
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
flask-api   1/1     1            1           3d18h
```
just remember the deployment name to point into ingress later

next are checking the services, we need to point exposed IP into registrar
```
kubectl get svc -n <your-namespace>
root@gke-remote:~/deployment/docker-deploy# kubectl get svc -n flask-api
NAME         TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)        AGE
api-expose   LoadBalancer   xx.xx.xx.xxx     xx.xxx.xxx.xx   80:30914/TCP   3d18h

```
remember the name, port, and external IP, because we need that to point the name into registrar and manifest later!

### Configure the manifest
This part, we need to create manifest that connecting the ```LoadBalancer Service``` into ```Ingress```

create file named ```ingress.yaml```
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-ingress #name of your ingress
  namespace: flask-api #specified namespace
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  defaultBackend: #define default backend, if not it will give you "Error 404 on Ingress backend"
    service:
      name: api-expose #name of your exposed LoadBalancer Service
      port:
        number: 80 #Port that you exposed!
  rules:
    - host: flask-api.<your-domain-name> #Hostname that you wanna use to point your deployment
      http:
        paths:
          - path: /* #the path that you wanna expose, if you wanna expose all, just use wildcard * to route all available into DNS
            pathType: Prefix
            backend:
              service:
                name: api-expose #same like default backend, but i call this the production or when you have multi deployment but want to expose it using one ingress 
                port:
                  number: 80 #port that you wanna expose
```
don't apply it yet, we need to point the exposed IP from ```LoadBalancer Service``` into DNS from registrar (i'm currently using Cloudflare)
### Cloudflare config
1. Login to your dashboard, and find a domain to configure 
2. Click your activated domain and locate the DNS menu
3. After you found the DNS menu, you'll see DNS management for <your-domain-name>
3. Add new record, select A for the type, fill the name to your desired subdomain, fill the content into your IP, and uncheckthe proxy status into DNS Only
4. Save and wait for the DNS propagation

## Now we Apply!
Next, we're back to our kubernetes cluster and apply the manifest that we've been created before
```
kubectl apply -f ingress.yaml

root@gke-remote:~/deployment/docker-deploy# kubectl apply -f ingress.yaml 
ingress.networking.k8s.io/flask-ingress configured
```
next, check the ingress status 
```
kubectl get ingress

root@gke-remote:~/deployment/docker-deploy# kubectl get ingress
NAME            CLASS    HOSTS                      ADDRESS         PORTS   AGE
flask-ingress   <none>   flask-api.your.domain.name xx.xxx.xxx.xx   80      18h
```
after that, you can tried to ```dig``` and ```curl``` your deployed DNS from service
```
curl :
curl your.domain.name/
root@gke-remote:~/deployment/docker-deploy# curl flask-api.your.domain.name/test
"You've done better!"

dig :
root@gke-remote:~/deployment/docker-deploy# dig your.domain.name

; <<>> DiG 9.18.28-1~deb12u2-Debian <<>> your.domain.name
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 18736
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;your.domain.name.      IN      A

;; ANSWER SECTION:
your.domain.name. 300   IN      A       xx.xxx.xxx.xxx

;; Query time: 124 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Wed Sep 25 09:27:15 UTC 2024
```
when you're got ```status:  NOERROR``` you're ready to go.

the last thing to test are from the browser
you can type ```http://your.domain.name/``` into your browser bar and check the result


for the [9] are configuring SSL to make your deployment HTTPS ready!