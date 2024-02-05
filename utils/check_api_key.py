import os

from fastapi import Request, HTTPException


def check_api_key(request: Request):
    """
    Check the API key
    """
    # Get the API key from the header
    request_api_key = request.headers.get('x-api-key')
    if not request_api_key:
        raise HTTPException(status_code=403, detail="API key is missing")

    # Get the API key from the environment
    env_api_key = os.environ.get('API_KEY')

    # If the API key is not set in the environment, use a default value
    if not env_api_key:
        env_api_key = "1234"

    # Compare the API keys
    if request_api_key != env_api_key:
        raise HTTPException(status_code=403, detail="API key is invalid")
