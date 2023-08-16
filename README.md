# simple-prod-api
A simple example of a production level API and list out components that make it useful for production



## ENVIRONMENT SETUP

1. Please create a virtual environment either by using python virtualenv or conda.
2. Once the virtualenv is created then install poetry for dependency management
```
pip install poetry
```
3. Once poetry is installed then install dependencies by just running 
```
poetry install
```
4. This project makes use of pre-commit hooks to maintain style and quality of codeso before doing any development please run
```
pre-commit install
```
This will not allow to push code that doesnt meet standards mentioned in the pre-commit-config.yaml file

# HOW TO RUN THE CODE

1. Inside the environment you can startup the server now using uvicorn ASGI server on your localhost using the following command
```
uvicorn src.main:app --reload (if not in dev environment please dont use the reload flag)
```
2. Since the app takes a sentence and generates 500 random numbers the sentence input can be provided as a json using either curl or postman or a client of your choice 

```
curl -X POST -H "Content-Type: application/json" -d '{"sentence": "Hello World"}' http://localhost:8000/get_array
```
3. To run the tests locally you can run 
```
poetry run pytest tests/
```

## Features added to make the functionality production ready are

1. pre-commit hooks to maintain quality and style of code
2. tests that can be run on development environment and also ci using github actions. 
3. The github actions will run for every commit pushed into the repository, since this project is very small no limitations has been placed on the master branch.
4. Typing annotations have been used in order to understand the input and output types, some of the custom types are created using pydantic which comes inbuilt with fastapi.
5. Instead of storing dependencies in a requirements.txt I have made use of poetry package management which comes with poetry.lock file for easy reproduction of the environment and the same has been used in the CI to replicate build and testing. 
6. A health_check endpoint has been added in addition to the functionality endpoint so that there can be checks on whether the issue is with connection to the server or the problem is with a specific endpoint

## Tests

The test suite mainly consists of 3 files
1. **conftest.py** -  which issues a client setup across the test suite and changes the root folder into src/
2. **pytest.ini** - contains a list of modules grouped by names, currently there is only one which is for endpoint checks
3. **test_endpoints.py** -  contains test that validate the response and status codes of the health_check endpoint and the functionality of get_array endpoint. 

