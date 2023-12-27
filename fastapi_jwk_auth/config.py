import os

# Define the JWKS URI where the JSON Web Key Set can be fetched
JWKS_URI = os.environ["JWK_HOST"]

# Define a comma-separated list of algorithms that will be used for JWT decoding.
# The list of algorithms is not extracted directly form the unverified header
# because a bad actor could just provide `none` and that could skip verification.
# See: https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/
ALGORITHMS = os.getenv("JWT_ALGORITHMS", "RS256,HS256").split(",")
