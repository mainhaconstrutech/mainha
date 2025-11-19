# MAINHA APP

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