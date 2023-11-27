import datetime
import os
from pathlib import Path

from cryptography.fernet import Fernet
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from models.delete_model import DeleteModel

# Create the folder if it doesn't exist
folder_name = "./files"
os.makedirs(folder_name, exist_ok=True)

app = FastAPI()

# Configure CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the files directory
app.mount("/files", StaticFiles(directory="files"), name="files")


@app.get("/")
async def info():
    return {"message": "Files Service running!", "date": datetime.datetime.now()}


@app.post('/upload-video')
async def upload_video(file: UploadFile = File(...)):
    # Generate random filenames
    random_filename = os.urandom(32).hex()
    random_seven_filename = os.urandom(32).hex()

    # Get the file extension
    file_extension = Path(file.filename).suffix

    # Check if the file is an MP4
    if file_extension != '.mp4':
        raise HTTPException(status_code=500, detail="NOT_MP4_CODE")

    # Set the filenames and filepaths
    filename = f"{random_filename}{file_extension}"
    filepath = f"files/{filename}"

    seven_filename = f"{random_seven_filename}{file_extension}"
    seven_filepath = f"files/{seven_filename}"

    encrypted_filename = f"{random_filename}_enc{file_extension}"
    encrypted_filepath = f"files/{encrypted_filename}"

    try:
        # Save the uploaded video file
        with open(filepath, 'wb') as video_file:
            video_file.write(file.file.read())
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        file.file.close()

    # Extract a 7-minute subclip using ffmpeg
    ffmpeg_extract_subclip(filepath, 0, 60 * 7, targetname=seven_filepath)

    # Generate a key and encrypt the video file
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    try:
        with open(filepath, 'rb') as video_file:
            contents = video_file.read()
            encrypted_content = cipher_suite.encrypt(contents)
            with open(encrypted_filepath, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_content)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    # Remove the original video file
    try:
        os.remove(filepath)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    # Get the size of the encrypted file
    file_size = os.path.getsize(encrypted_filepath)

    return {
        "filename": encrypted_filename,
        "seven_minutes_filename": seven_filename,
        "key": key,
        "size": file_size
    }


@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    now = datetime.datetime.now()
    filename = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{file.filename}"

    try:
        contents = file.file.read()

        with open(f"files/{filename}", "wb") as f:
            f.write(contents)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        file.file.close()

    file_size = os.path.getsize(f"files/{filename}")

    return {"filename": filename, "size": file_size}


@app.delete('/delete-file')
async def delete_file(delete: DeleteModel):
    filepath = f'files/{delete.filename}'

    try:
        os.remove(filepath)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"message": "OK", "filename": delete.filename}
