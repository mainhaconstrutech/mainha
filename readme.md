# MAINHA APP

## --- Python ---

### 1. Virtual Enviroment

#### Create
> python -m venv .venv

#### Activate
> .\.venv\Scripts\activate

#### Deactivate
> deactivate

### 2. Instaling project
> pip install -r requirements.txt
> python manage.py migrate

### 3. Start Project
> python manage.py runserver

### 4. Create Apps
> python manage.py startapp my_apps

### 5. Create Migrations
> python manage.py makemigrations app_name

### 6. Update requiments.txt
> pip freeze > requirements.txt

### 7. Create Super User
> python manage.py createsuperuser

## --- Docker ---

### Create docker image
> docker build -t mainhaconstrutech/mainha:v1 .

### Update docker latest image
> docker tag mainhaconstrutech/mainha:v1 mainhaconstrutech/mainha:latest

### Login to Dockerhub
> docker login

### Logout to Dockerhub
> docker logout

### Push docker image to dockerhub
> docker push mainhaconstrutech/mainha:latest

## --- Envs ---

### To run all app in container, use:
DATABASE_HOST=host.docker.internal

### To run app in local, use:
DATABASE_HOST=localhost