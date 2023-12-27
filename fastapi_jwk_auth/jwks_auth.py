from typing import Any, Dict

import jwt
import requests
from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)

__all__ = ["jwk_validator", "JWKMiddleware"]

from .config import ALGORITHMS, JWKS_URI

security = HTTPBearer()


# Function to fetch the JSON Web Key Set (JWKS) from the JWKS URI
def fetch_jwks(jwks_uri: str) -> Dict[str, Any]:
    jwks_response = requests.get(jwks_uri)
    jwks: Dict[str, Any] = jwks_response.json()
    return jwks


def get_validated_payload(token: str) -> Any:
    """
    This function validates the jwt token and extracts
    the payload from it.

    Args:
        token (str): A valid JWT token

    Raises:
        HTTPException: The token uses an unknown algorithm.
        HTTPException: The token uses an unknown key.
        HTTPException: The token has expired.
        HTTPException: The token is invalid.

    Returns:
        Any: The payload of the validated JWT token.
    """
    jwks = fetch_jwks(JWKS_URI)
    public_key = None
    try:
        header = jwt.get_unverified_header(token)
        kid = header["kid"]
        if header["alg"] not in ALGORITHMS:
            raise HTTPException(status_code=401, detail="Invalid token")
        for key in jwks["keys"]:
            if key["kid"] == kid:
                public_key = jwt.algorithms.get_default_algorithms()[
                    header["alg"]
                ].from_jwk(key)
                break
        if public_key is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return jwt.decode(token, public_key, algorithms=[header["alg"]])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# JWT Token Validation Middleware
def jwk_validator(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Request:
    token = credentials.credentials
    if credentials.scheme != "Bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    request.state.payload = get_validated_payload(token)
    return request


# JWT Token Validation Middleware
class JWKMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        bearer_token = request.headers.get("authorization") or request.headers.get(
            "Authorization"
        )
        if not bearer_token or not bearer_token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token")
        token = bearer_token[7:]
        request.state.payload = get_validated_payload(token)
        response = await call_next(request)
        return response
