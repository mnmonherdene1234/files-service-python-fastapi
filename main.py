import datetime
import logging
import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from models.delete_model import DeleteModel

# Create the folder if it doesn't exist
folder_name = "./files"
os.makedirs(folder_name, exist_ok=True)

# Create the FastAPI app
app = FastAPI()

# Configure CORS
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )

# Mount the static files directory
app.mount("/files", StaticFiles(directory="files"), name="files")


@app.get("/")
async def info():
    """
    Returns the current date and time
    @return:
    """
    return {"message": "Files Service running", "date": datetime.datetime.now()}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file to the server
    @param file:
    @return:
    """
    try:
        # Get the file extension
        extension = file.filename.split('.')[-1]

        # Generate a random filename
        filename = f"{uuid4()}.{extension}"

        # Write the file to disk using a with-statement to automatically close it
        with open(f"files/{filename}", "wb") as f:
            while contents := await file.read(1024 * 1024):
                f.write(contents)

        # Return the filename and size
        return {"filename": filename, "size": file.size}

    except Exception as error:
        # Log the error before raising the exception
        logging.exception(error)

        # Raise a custom HTTPException
        raise HTTPException(status_code=500, detail="An error occurred while processing the file.")


@app.delete('/delete')
async def delete_file(delete: DeleteModel):
    """
    Deletes a file from the server
    @param delete:
    @return:
    """
    # Get the file path
    filepath = f'files/{delete.filename}'

    # Check if the file exists
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")

    # Try to delete the file
    try:
        os.remove(filepath)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    # Return a success message
    return {"message": "OK", "filename": delete.filename}
