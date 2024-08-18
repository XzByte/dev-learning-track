# Deploy MongoDB for storing files and records 

## just use docker
I just need to run container and serve mongodb, then use it as my env to learn how to "dev"

ensure docker have installed, here's the deployment on docker
```
docker pull mongo:latest
```
next, create folder's on your desired location
```
mkdir -p mongodb_data
```
after that, just adjust this script to mount the folders 
```
docker run -d -v mongodb_data:/data/db -p 27017:27017 mongo:latest --name mongodb
or
docker run --name mongodb -p 27017:27017 -d -v /mongodb_data:/data/db mongo:latest
```
when you need more "security" you can use this script instead
```
docker run -d -v mongodb_data:/data/db -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=mongopasswd mongo:latest --name mongodb
```
after that, you can check the deployment of your mongodb
```
docker ps -a
```
## optional
if you using firewall, and not enabled the port's number (eg. ufw, iptables, firewall-cmd, etc..) you should enable those ports to gain access into your mongodb instances
