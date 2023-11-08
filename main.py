import datetime
import os
from pathlib import Path

from cryptography.fernet import Fernet
from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

folder_name = "./files"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

app = FastAPI()
app.mount("/files", StaticFiles(directory="files"), name="files")


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

    return {"filename": filename, "key": key}


class Delete(BaseModel):
    filename: str


@app.delete('/delete-file')
def delete_file(delete: Delete):
    filepath = f'files/{delete.filename}'

    try:
        os.remove(filepath)
    except Exception as error:
        return {"message": str(error), "filename": delete.filename}

    return {"message": "OK", "filename": delete.filename}
