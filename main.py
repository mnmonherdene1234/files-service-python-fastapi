import hashlib
import os
import zlib
from pathlib import Path

from fastapi import FastAPI
from fastapi import File, UploadFile

from cryptography.fernet import Fernet
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/files", StaticFiles(directory="files"), name="files")

folder_name = "files"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)


@app.get("/")
def read_root():
    return {"message": "Files Service running!"}


@app.post('/upload')
def upload(file: UploadFile = File(...)):
    random_name = os.urandom(32).hex()
    filepath = f"files/{random_name}{Path(file.filename).suffix}"

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    try:
        contents = file.file.read()

        encrypted_content = cipher_suite.encrypt(contents)

        with open(filepath, 'wb') as f:
            f.write(encrypted_content)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    compressed_filepath = f'{filepath}.z'

    with open(filepath, 'rb') as f:
        compressed_data = zlib.compress(f.read(), level=9)
        with open(compressed_filepath, 'wb') as ff:
            ff.write(compressed_data)

    os.remove(filepath)

    return {"filename": random_name, "key": key}
