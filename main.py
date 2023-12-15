import datetime
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from models.delete_model import DeleteModel

folder_name = "./files"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

app = FastAPI()
origins = ["*", ]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )
app.mount("/files", StaticFiles(directory="files"), name="files")


@app.get("/")
async def info():
    return {"message": "Files Service running", "date": datetime.datetime.now()}


@app.post('/upload-video')
async def upload(file: UploadFile = File(...)):
    random_filename = os.urandom(32).hex()
    random_seven_filename = os.urandom(32).hex()

    file_extension = Path(file.filename).suffix

    if file_extension != '.mp4':
        raise HTTPException(status_code=500, detail="NOT_MP4_CODE")

    filename = f"{random_filename}{file_extension}"
    filepath = f"files/{filename}"

    seven_filename = f"{random_seven_filename}{file_extension}"
    seven_filepath = f"files/{seven_filename}"

    encrypted_filename = f"{random_filename}_enc{file_extension}"
    encrypted_filepath = f"files/{encrypted_filename}"

    # Save the original video to disk
    try:
        with open(filepath, 'wb') as video_file:
            video_file.write(file.file.read())
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        file.file.close()

    # Save first seven minutes
    ffmpeg_extract_subclip(filepath, 0, 60 * 7, targetname=seven_filepath)

    # Generate key
    key_length = 32
    key = os.urandom(key_length)

    # Byte encryption the file
    try:
        with open(filepath, 'rb') as video_file:
            with open(encrypted_filepath, 'wb') as encrypted_file:
                index = 0
                while True:
                    video_byte = video_file.read(1)

                    if not video_byte:
                        break

                    encrypted_int = video_byte[0] ^ key[index % key_length]
                    encrypted_byte = encrypted_int.to_bytes()
                    index += 1

                    encrypted_file.write(encrypted_byte)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    # Remove the original video from disk
    try:
        os.remove(filepath)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    file_size = os.path.getsize(encrypted_filepath)

    return {"filename": encrypted_filename, "seven_minutes_filename": seven_filename, "key": key.hex(),
            "size": file_size}


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
