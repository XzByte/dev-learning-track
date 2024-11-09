# Now, i've been employed into local tech company as a DevOps Engineer, rn i'm gonna documenting my learning from day first

## Deploy app and db to Cloud Run using terraform
first step
1. create the terraform file, here i'm gonna test building python apps (fastapi) with database (mysql container)
### python code
```
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "holdtest")

app = FastAPI()

class InputSchema(BaseModel):
    content: str

def get_connection():
    return mysql.connector.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )


@app.post("/store")
def store_string(item: InputSchema):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO input_strings (content) VALUES (%s)", (item.content,))
        connection.commit()
        return {"message": "String stored successfully"}
    except Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()
```
### Dockerfile
```
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port 80 --reload
```
simple, yet working!

### Terraform file, will separated into 3 file(s)
1. variable.tf
this are for passing env or secret to deployment securely without passing a single file(s)
```
variable "project_id" {
  description = "GCP Project ID"
  default     = "project"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "repository" {
  description = "Artifact Registry repository"
  default     = "test-project"
}

variable "image_name" {
  description = "Container image name"
  default     = "python-app"
}


variable "database_user" {
  description = "Database user"
  type        = string
  sensitive   = true
}

variable "database_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "database_port" {
  description = "Database port"
  type        = string
  default     = "3306"  
}

variable "vpc_connector_name" {
  description = "Name for the VPC access connector"
  type        = string
  default     = "vpc-connector"  # Optional default value
}
variable "max_instances" {
  description = "Maximum number of instances for VPC connector"
  type        = number
  default     = 3
}
variable "min_instances" {
  description = "Minimum number of instances for VPC connector"
  type        = number
  default     = 2  # GCP requires minimum of 2 instances
}
variable "service_name" {
  description = "Cloud Run service name"
  type        = string
  default     = "python-app"
}

variable "min_scale" {
  description = "Minimum number of instances for Cloud Run service"
  type        = number
  default     = 1
}

variable "max_scale" {
  description = "Maximum number of instances for Cloud Run service"
  type        = number
  default     = 2
}
```

2. main.tf
here are the main IaC command and declaration (i'm centralized type team btw)
```
provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_service" "app" {
  name     = "python-app"
  location = var.region

  template {
    spec {
      containers {
        image = "image:version"
        ports {
          container_port = 8080
        }
        env {
          name  = "PORT"
          value = "8080"
        }
        env {
          name  = "DATABASE_HOST"
          value = "10.128.0.3"
        }
        env {
          name  = "DATABASE_USER"
          value = var.database_user
        }
        env {
          name  = "DATABASE_PASSWORD"
          value = var.database_password
        }
        env {
          name  = "DATABASE_PORT"
          value = var.database_port
        }
      }
    }

    metadata {
      annotations = {
        "run.googleapis.com/vpc-access-connector" = google_vpc_access_connector.connector.name
        "run.googleapis.com/vpc-access-egress"    = "all-traffic"
        "autoscaling.knative.dev/minScale"       = var.min_scale
        "autoscaling.knative.dev/maxScale"       = var.max_scale
      }
    }
  }
}

resource "google_vpc_access_connector" "connector" {
  name = var.vpc_connector_name
  ip_cidr_range = "10.8.0.0/28"
  network       = "default"
  min_instances = var.min_instances
  max_instances = var.max_instances 
}
resource "google_cloud_run_service_iam_member" "public_access" {
  location = google_cloud_run_service.app.location
  service  = google_cloud_run_service.app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
```
3. terraform.tfvars
this file are the location you used to store or save your "so called" ```secrets``` \
here's how to do that
```
project_id        = "humanis-cloud"
database_user     = "root"
database_password = "turntable"
```

### Maybe you will encounter some errors, but don't worry child, i'm here for ya!

error ```#1``` : Grant required VPC Access Admin role to your account (errors when you're cannot edit the access type, typically when dealing with API that require public access instead of proxying or by IAM access) \
howto? \
```
gcloud projects add-iam-policy-binding humanis-cloud \
    --member="user:YOUR_EMAIL" \
    --role="roles/vpcaccess.admin"
``` 
then :
```
terraform init 
terraform plan
terraform apply
```
### Next, are the apps itself, yeah, FastAPI
```
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "holdtest")

app = FastAPI()

class InputSchema(BaseModel):
    content: str

def get_connection():
    return mysql.connector.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )


@app.post("/store")
def store_string(item: InputSchema):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO input_strings (content) VALUES (%s)", (item.content,))
        connection.commit()
        return {"message": "String stored successfully"}
    except Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

@app.get("/api")
def api_test():
    return {"message": "yay, you did it!"}

if __name__ == "__main__":
    import uvicorn
```

### The time has come!
```LETS BUILD THAT SHIT!```
1. build the images
```
docker build -t us-central1-docker.pkg.dev/humanis-cloud/test-project/test:v1.0 .
```
2. push the images into repos
```
docker push us-central1-docker.pkg.dev/humanis-cloud/test-project/test:v1.0
```
3. then, run :
```
terraform init
terraform plan
terraform apply
```