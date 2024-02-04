## Describe how dependency injection works in FastAPI and give an example of its practical use.

Dependency injection in FastAPI is a powerful mechanism that allows you to manage and reuse components or services in a flexible and organized way. FastAPI leverages Python's type hints and function annotations to automatically inject dependencies into your route handlers, making your code clean, modular, and testable.

Here's a brief explanation of how dependency injection works in FastAPI:

1. **Dependency Declaration:**
   - You can declare dependencies using either function parameters or by using FastAPI's `Depends` class.
   - Dependencies are functions or classes that are used to obtain values needed by route handlers.

2. **Automatic Injection:**
   - FastAPI automatically detects dependencies in your route functions by inspecting their parameters and type hints.
   - When a route is called, FastAPI resolves the required dependencies and injects them into the route function.

3. **Dependency Lifecycle:**
   - Dependencies can be reused across multiple routes, and their lifecycle is managed by the FastAPI framework.
   - For example, if a dependency is declared with `scope="session"`, it will be created once per session and reused for subsequent requests.

4. **Type Checking:**
   - FastAPI uses type hints to validate that the provided dependencies match the expected types.
   - If a dependency's type hint is not satisfied, FastAPI raises a validation error.

Now, let's look at a practical example of dependency injection in FastAPI:

```python
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

# Example Dependency
def get_user_agent(user_agent: str = Header(default=None)):
    return user_agent

# Route using the Dependency
@app.get("/user-agent")
async def read_user_agent(user_agent: str = Depends(get_user_agent)):
    return {"User-Agent": user_agent}
```

In this example:

- The `get_user_agent` function is a dependency that retrieves the "User-Agent" header from the request.
- The `Depends` class is used to declare the dependency in the route handler `read_user_agent`.
- When a request is made to the "/user-agent" endpoint, FastAPI automatically calls `get_user_agent` to obtain the value of the "User-Agent" header and injects it into the `read_user_agent` route handler.

Here's how you can run and test this example:

1. Start the FastAPI development server:

    ```bash
    uvicorn your_module_name:app --reload
    ```

2. Open the API documentation at `http://127.0.0.1:8000/docs` and try the "/user-agent" endpoint.

3. You can see the automatic injection of the "User-Agent" header into the route handler.
