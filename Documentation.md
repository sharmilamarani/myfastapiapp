
# Book Review System API Documentation

## Introduction

This project is a simple RESTful API for a hypothetical book review system. It is built using FastAPI, a modern, fast, web framework for building APIs with Python.

## Code Structure

- **fastapi_app.py**: Contains the main FastAPI application, including endpoints, data models, and database integration.
- **tests/test_main.py**: Test cases for the API using the pytest framework.
- **requirements.txt**: Lists the required Python packages and their versions.

## How to Run

1. **Install Dependencies**: Run the following command to install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the FastAPI Server**: Execute the following command to start the FastAPI development server:

    ```bash
    uvicorn main:app --reload
    ```

    This will start the API server locally at `http://127.0.0.1:8000`.

3. **Access API Documentation**: Visit `http://127.0.0.1:8000/docs` in your web browser to access the Swagger-based interactive API documentation. Alternatively, `http://127.0.0.1:8000/redoc` provides a more human-friendly documentation interface.

## Database

The API is integrated with SQLite for data persistence. The database file is named `test.db`. Ensure the SQLite library is available in your environment.

## How to Test

1. **Install Testing Dependencies**: Run the following command to install the testing dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. **Run Tests**: Execute the following command to run the tests:

    ```bash
    pytest tests/
    ```

    This command will run the test cases in the `tests/` directory and provide feedback on the success or failure of each test.

## Important Notes

- **Environment Variables**: In a production environment, we need to use environment variables to store sensitive information like database connection strings.

- **Security**: This example does not cover security considerations such as authentication and authorization. We can implement these features based on application's requirements.

