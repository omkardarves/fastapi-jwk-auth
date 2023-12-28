from setuptools import setup, find_packages

setup(
    name="fastapi-jwk-auth",
    version="0.0.5",
    packages=find_packages(),
    install_requires=["fastapi", "PyJWT", "cryptography"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://github.com/omkardarves/fastapi-jwk-auth",
    },
    license="MIT",
)
