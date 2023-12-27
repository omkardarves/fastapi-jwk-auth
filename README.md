# My JWT Validator

![Project Logo or Banner - Optional]

## Overview

My JWT Validator is a Python package that provides middleware for validating JSON Web Tokens (JWT) in FastAPI applications. It includes a JWT Token Validation Middleware that can be easily integrated into your FastAPI project to secure your API endpoints.

## Features

- JWT token validation using JSON Web Key Set (JWKS)
- Middleware for FastAPI applications
- Easy integration into existing FastAPI projects

## Installation

Install the package using pip:

```bash
pip install my-jwt-validator
```
## Usage
## Example FastAPI Application
```python
from fastapi import FastAPI, Depends, HTTPException
from my_jwt_validator import JWTMiddleware

app = FastAPI()

# Include the JWT Middleware
app.add_middleware(JWTMiddleware)

@app.get("/secure-endpoint")
async def secure_endpoint(current_user: str = Depends(get_current_user)):
    return {"message": "This is a secure endpoint", "user": current_user}
```

## Configuration
Set the following environment variable to the JSON Web Key Set (JWKS) URI:

```bash
JWK_HOST="https://your-identity-server"
```

## Contributing
Feel free to open PR/Issues.

## License
This project is licensed under the MIT License.

## Contact
For questions or feedback, feel free to contact us at [omkardarves@gmail.com].