# Deploying MYSQL container on Docker

## This tutorial just few step, so i'm just going to straightforward and explain a bit about the command i used

first thing, just pull the official images
```
docker pull mysql:latest
```
if you wanna mount storage to avoid losing data when your apps are down
```
mkdir -p sql-srv
```
after success pulling the images, execute this command to run container
```
docker run --name sql-server -v sql-srv:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=<yoursecurepassword> -p 3306:3306 -d mysql:latest
```
after that, you're good to go, check using
```
docker ps -a
```
to connect your sql server instance, just remember your ip and ports
```
mysql://<your ip>:3306
```
