import os

# Define the JWKS URI where the JSON Web Key Set can be fetched
JWKS_URI = os.environ["JWK_HOST"]

# Define a comma-separated list of algorithms that will be used for JWT decoding.
ALGORITHMS = os.getenv("JWT_ALGORITHMS", "RS256,HS256").split(",")
