# EPAM assessment task

## Running locally

### Prerequisites

Install Python 3.x and docker-compose locally.

### Run the service

Starting the service is fully automated; you need to execute the following command:

``` docker-compose up --build -d ```

As part of the process of creating the Docker containers required to run this service, a 
database instance will be created first (a PostgreSQL database is used), followed by the 
launch of the service itself. 

Since Flask-Migrate was used to create the database schema, the creation of the Books table 
and the insertion of initial data is handled through migrations, which will also be 
automatically executed when the service starts.

All the endpoints requested as part of the task are available on the API itself.

### Running the tests

The specified tests have been added in a separate file, and it is not necessary to run them 
locally, as a GitHub Action has been created to automatically run the tests every time something 
is pushed to the master branch or when a pull request is merged.
