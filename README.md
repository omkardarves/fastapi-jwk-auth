# Fastapi JWKS Auth(Validator)

## Overview

FastAPI JWK Auth is a Python package designed to enhance [FastAPI](https://fastapi.tiangolo.com/) applications with easy and secure JSON Web Token (JWT) validation using JSON Web Key Sets (JWKS). It simplifies the integration of JWT-based authentication in your FastAPI project when JWKS URLs are employed for key retrieval.


## Features

- **JWKS-Based JWT Validation:** Seamlessly validate JWTs using JWKS obtained from configured URLs.
- **FastAPI Middleware Integration:** Integrate the provided `JWTMiddleware` class into your FastAPI application middleware like `app.add_middleware(JWTMiddleware)` to secure your routes with JWT validation.
- **Fastapi Router dependency:** Integrate the provided `jwk_validator` function into your FastAPI router like `app.include_router(auth_app.router, dependencies=[Depends(jwk_validator)])` to secure your product with JWT validation
- **Efficient JWK Handling:** Retrieve and utilize JSON Web Key Sets efficiently in your FastAPI routes with the `fetch_jwks` function.
- **Exception Handling:** Easily manage JWT validation exceptions using FastAPI's HTTPException.

## Installation

Install the package using pip:

```bash
pip install fastapi-jwk-auth
```
# Usage
## FastAPI Middleware Integration

```python
from fastapi import FastAPI, Depends
from fastapi_jwk_auth.jwks_auth import jwk_validator, JWKMiddleware

app = FastAPI()

# Include the JWT Middleware
app.add_middleware(JWTMiddleware)
```

## FastAPI Route JWT Validation

```python
from fastapi import FastAPI, Depends
from fastapi_jwk_auth.jwks_auth import jwk_validator, JWKMiddleware

app=FastAPI()

app.include_router(auth_app.router, dependencies=[Depends(jwk_validator)])
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