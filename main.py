import datetime
import os

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
    now = datetime.datetime.now()
    filename = f"{now.strftime('%Y_%m_%d_%H_%M_%S')}_{file.filename.replace(' ', '_')}"

    try:
        contents = file.file.read()

        with open(f"files/{filename}", "wb") as f:
            f.write(contents)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    finally:
        file.file.close()

    file_size = os.path.getsize(f"files/{filename}")

    return {"filename": filename, "size": file.size}


@app.delete('/delete')
async def delete_file(delete: DeleteModel):
    filepath = f'files/{delete.filename}'

    try:
        os.remove(filepath)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"message": "OK", "filename": delete.filename}
