from typing import Callable
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import requests
from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import os

security = HTTPBearer()

# Define the JWKS URI where the JSON Web Key Set can be fetched
jwks_uri = os.getenv("JWK_HOST")


# Function to fetch the JSON Web Key Set (JWKS) from the JWKS URI
def fetch_jwks(jwks_uri):
    jwks_response = requests.get(jwks_uri)
    jwks = jwks_response.json()
    return jwks


# JWT Token Validation Middleware
async def jwtmiddleware(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = credentials.credentials
        if credentials.scheme == "Bearer" and token:
            jwks = fetch_jwks(jwks_uri)
            public_key = None

            try:
                header = jwt.get_unverified_header(token)
                kid = header["kid"]

                for key in jwks["keys"]:
                    if key["kid"] == kid:
                        public_key = jwt.algorithms.get_default_algorithms()[
                            header["alg"]
                        ].from_jwk(key)
                        break
                if public_key is None:
                    raise HTTPException(status_code=401, detail="Invalid token")

                payload = jwt.decode(token, public_key, algorithms=[header["alg"]])

                # Attach the payload to the request state for use in routes
                request.state.payload = payload
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
        else:
            raise HTTPException(status_code=401, detail="Invalid token")

        return request
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


# JWT Token Validation Middleware
class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            bearer_token = request.headers.get("authorization") or request.headers.get(
                "Authorization"
            )
            if bearer_token and bearer_token.startswith("Bearer "):
                token = bearer_token[7:]

                jwks = fetch_jwks(jwks_uri)
                public_key = None

                try:
                    header = jwt.get_unverified_header(token)
                    kid = header["kid"]

                    for key in jwks["keys"]:
                        if key["kid"] == kid:
                            public_key = jwt.algorithms.get_default_algorithms()[
                                header["alg"]
                            ].from_jwk(key)
                            break

                    if public_key is None:
                        raise HTTPException(status_code=401, detail="Invalid token")

                    payload = jwt.decode(token, public_key, algorithms=[header["alg"]])

                    # Attach the payload to the request state for use in routes
                    request.state.payload = payload
                except jwt.ExpiredSignatureError:
                    raise HTTPException(status_code=401, detail="Token has expired")
                except jwt.InvalidTokenError:
                    raise HTTPException(status_code=401, detail="Invalid token")
            else:
                raise HTTPException(status_code=401, detail="Invalid token")
            response = await call_next(request)

            return response
        except HTTPException as e:
            return JSONResponse(content={"detail": e.detail}, status_code=e.status_code)
