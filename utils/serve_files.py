import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def serve_files(app: FastAPI):
    """
    Serves the files from the server
    """
    # Create the folder if it doesn't exist
    folder_name = "./files"
    os.makedirs(folder_name, exist_ok=True)

    # Mount the static files directory
    app.mount("/files", StaticFiles(directory="files"), name="files")
