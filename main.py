import datetime
import os
from pathlib import Path

from cryptography.fernet import Fernet
from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from middlewares.key_middleware import key_middleware
from models.delete_model import DeleteModel

folder_name = "./files"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )

app.mount("/files", StaticFiles(directory="files"), name="files")
app.middleware("http")(key_middleware)


@app.get("/")
def info():
    return {"message": "Files Service running!", "date": datetime.datetime.now()}


@app.post('/upload')
def upload(file: UploadFile = File(...)):
    random_filename = os.urandom(32).hex()
    file_extension = Path(file.filename).suffix
    filename = f"{random_filename}{file_extension}"
    filepath = f"files/{filename}"

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    try:
        contents = file.file.read()

        encrypted_content = cipher_suite.encrypt(contents)

        with open(filepath, 'wb') as f:
            f.write(encrypted_content)
    except Exception as error:
        return {"message": "There was an error uploading the file", "error": str(error)}
    finally:
        file.file.close()

    file_size = os.path.getsize(filepath)

    return {"filename": filename, "key": key, "size": file_size}


@app.delete('/delete-file')
def delete_file(delete: DeleteModel):
    filepath = f'files/{delete.filename}'

    try:
        os.remove(filepath)
    except Exception as error:
        return {"message": str(error), "filename": delete.filename}

    return {"message": "OK", "filename": delete.filename}
