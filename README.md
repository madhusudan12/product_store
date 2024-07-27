# Product Metadata Store

This is used to store and retrieve metadata of sku/product efficiently.


## Getting Started for setting this up

### Prerequisites

- Python 3.x
- PostgresSQL
- Redis


### Installation

1. Clone the repository
    ```sh
    git clone git@github.com:madhusudan12/product_store.git
    ```
2. Navigate to the project directory
    ```sh
    cd product_store
    ```
3. Create a virtual environment
    ```sh
    python3 -m venv env
    ```
4. Activate the virtual environment
    - On Windows:
        ```sh
        .\env\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source env/bin/activate
        ```
5. Install the required packages
    ```sh
    pip install -r requirements.txt
    ```
   
### Postgres setup

create database with the name you want to create it and grant all permissions to the user

```sh
CREATE DATABASE product_store;
```


### start redis

start the redis server 
```sh
brew services start redis
```



### env setup

add a `.env` file that should include the following keys

```sh
DB_NAME=db-name
DB_USER=db-user
DB_PASSWORD=db-password
DB_HOST=host(localhost)
DB_PORT=5432
SECRET_KEY=django-secret-key
REDIS_HOST_LOCATION=redis-host
```


### Populate the Data and start the server

1. Run the following to populate the sample data 
    ```sh
    python manage.py populate_data
    ```
2. Apply the migrations
    ```sh
    python manage.py migrate
    ```
3. Start the development server
    ```sh
    python manage.py runserver
    ```
4. You can test the APIs using the following postman collection
https://elements.getpostman.com/redirect?entityId=9824612-eb3082c1-8e11-42a0-b081-93839edb4cbf&entityType=collection