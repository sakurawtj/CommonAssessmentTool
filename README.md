Team OFFER++

Project -- Feature Development Backend: Create CRUD API's for Client

User Story

As a user of the backend API's, I want to call API's that can retrieve, update, and delete information of clients who have already registered with the CaseManagment service so that I more efficiently help previous clients make better decisions on how to be gainfully employed.

Acceptance Criteria
- Provide REST API endpoints so that the Frontend can use them to get information on an existing client.
- Document how to use the REST API
- Choose and create a database to hold client information
- Add tests


This will contain the model used for the project that based on the input information will give the social workers the clients baseline level of success and what their success will be after certain interventions.

The model works off of dummy data of several combinations of clients alongside the interventions chosen for them as well as their success rate at finding a job afterward. The model will be updated by the case workers by inputing new data for clients with their updated outcome information, and it can be updated on a daily, weekly, or monthly basis.

This also has an API file to interact with the front end, and logic in order to process the interventions coming from the front end. This includes functions to clean data, create a matrix of all possible combinations in order to get the ones with the highest increase of success, and output the results in a way the front end can interact with.

-------------------------How to Use-------------------------
1. In the virtual environment you've created for this project, install all dependencies in requirements.txt (pip install -r requirements.txt)

2. Run the app (uvicorn app.main:app --reload)

3. Load data into database (python initialize_data.py)

4. Go to SwaggerUI (http://127.0.0.1:8080/docs)

4. Log in as admin (username: admin password: admin123)

5. Click on each endpoint to use
-Create User (Only users in admin role can create new users. The role field needs to be either "admin" or "case_worker")

-Get clients (Display all the clients that are in the database)

-Get client (Allow authorized users to search for a client by id. If the id is not in database, an error message will show.)

-Update client (Allow authorized users to update a client's basic info by inputting in client_id and providing updated values.)

-Delete client (Allow authorized users to delete a client by id. If an id is no longer in the database, an error message will show.)

-Get clients by criteria (Allow authorized users to get a list of clients who meet a certain combination of criteria.)

-Get Clients by services (Allow authorized users to get a list of clients who meet a certain combination of service statuses.)

-Get clients services (Allow authorized users to view a client's services' status.)

-Get clients by success rate (Allow authorized users to search for clients whose cases have a success rate beyond a certain number.)

-Get clients by case worker (Allow users to view which clients are assigned to a specific case worker.)

-Update client services (Allow users to update the service status of a case.)

-Create case assignment (Allow authorized users to create a new case assignment.)

-------------------------How to run the application with Docker-------------------------

### Prerequisites
- Docker installed on your machine. Visit [Docker's website](https://www.docker.com/get-started) for installation instructions.

1. Build the Docker image:
   ```bash
   docker build -t common-assessment-tool-app .
   ```

2. Run the application:
    ```bash
    docker run -p :8080 common-assessment-tool-app
    ```
    
3. Go to SwaggerUI (http://127.0.0.1:8080/docs)

-------------------------How to run the application with Docker compose-------------------------

To start the service using Docker Compose, run:
```bash
docker compose up
```

To stop the service, run:
```bash
docker compose down
```

-------------------------CI/CD Pipeline Implementation-------------------------

Overview:
This repository implements a Continuous Integration (CI) pipeline using GitHub Workflows. The pipeline automates the process of code validation, testing, and Docker container verification to ensure high code quality and reliable deployment.

CI Pipeline Features:
The CI pipeline performs the following operations:

Automatically runs on push or pull request events to main/master branches
Executes code linting with Pylint to maintain code quality
Runs automated tests with pytest
Validates Dockerfile syntax
Builds the Docker image
Runs the container to verify it functions as expected

How to Use:
Triggering the CI Pipeline
The CI pipeline is automatically triggered when:

Code is pushed to the main/master branch
A pull request is opened against the main/master branch

Viewing CI Results:

Go to the "Actions" tab in the GitHub repository
Select the workflow run you want to examine
View the results of each job and step

Pipeline Configuration
The CI pipeline is defined in .github/workflows/ci.yml and consists of the following jobs:
Test Job

Sets up Python 3.11
Installs project dependencies
Runs Pylint for code linting
Executes pytest tests

Docker Job:

Verifies Dockerfile syntax
Builds the Docker image
Runs the container and tests connectivity
Verifies the application is accessible

Development Notes:

The pipeline enforces code quality standards using Pylint
Test failures or Docker verification issues will cause the workflow to fail
The CI pipeline will generate test reports for review

Modifying the CI Pipeline
To modify the CI pipeline:

Edit the .github/workflows/ci.yml file
Commit and push your changes
The updated workflow will be used for subsequent runs

By using this CI pipeline, we ensure that code changes meet quality standards and the application can be reliably containerized before deployment.

---------------------- how to access the public address ----------------------

go to the url: https://commen-accessment-tool-app-v43vvietaq-uc.a.run.app/docs