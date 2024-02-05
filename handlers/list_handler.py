import os

from fastapi import Request

from utils.check_api_key import check_api_key


async def list_handler(request: Request):
    """
    Returns a list of all files in the server
    """
    check_api_key(request)

    # Get the list of files
    files = os.listdir('files')

    # Return the list of files
    return files
