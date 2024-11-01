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
after success pulling the images, execute this command to run container, you can choose between mounting your data into docker volumes or local folder. \
here's to mount into docker volume \
```
create the volumes using

docker volume create sql-srv
```
then :
```
docker run --name sql-server -v sql-srv:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=<yoursecurepassword> -p 3306:3306 -d mysql:latest
```
otherwise, you can use the src to mount all your db config into local folder, here's how : \
create folder name you desired
```
mkdir -p db
```
then, run and bind into your folder :
```
docker run --name mysql-server \
  -v $(pwd)/db:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=<desired-password> \
  -d mysql:latest
```
after that, you're good to go, check using
```
docker ps -a
```
to connect your sql server instance, just remember your ip and ports
```
mysql://<your ip>:3306
```
