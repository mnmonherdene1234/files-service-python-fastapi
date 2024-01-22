import datetime
import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from models.delete_model import DeleteModel

# Create the folder if it doesn't exist
folder_name = "./files"
os.makedirs(folder_name, exist_ok=True)

app = FastAPI()

# Configure CORS
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )

# Mount the static files directory
app.mount("/files", StaticFiles(directory="files"), name="files")


@app.get("/")
async def info():
    return {"message": "Files Service running", "date": datetime.datetime.now()}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Generate a unique filename using a UUID
        filename = f"{uuid4()}_{file.filename.replace(' ', '_')}"

        # Write the file to disk using a with-statement to automatically close it
        with open(f"files/{filename}", "wb") as f:
            while contents := await file.read(1024 * 1024):  # Use 'await' to read the file asynchronously
                f.write(contents)

        # Return the filename and size
        return {"filename": filename, "size": file.size}

    except Exception as error:
        # Log the error before raising the exception
        import logging
        logging.exception(error)

        # Raise a custom HTTPException
        raise HTTPException(status_code=500, detail="An error occurred while processing the file.")


@app.delete('/delete')
async def delete_file(delete: DeleteModel):
    filepath = f'files/{delete.filename}'

    try:
        os.remove(filepath)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"message": "OK", "filename": delete.filename}
