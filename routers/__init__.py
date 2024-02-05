import datetime

from fastapi import APIRouter, UploadFile, File, Request

from handlers.delete_handler import delete_handler
from handlers.list_handler import list_handler
from handlers.upload_handler import upload_handler
from models.delete_model import DeleteModel

router = APIRouter()


@router.get("/")
async def info():
    """
    Returns the current date and time
    """
    return {"message": "Files Service running", "date": datetime.datetime.now()}


@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    return await upload_handler(request, file)


@router.get('/list')
async def list_files(request: Request):
    return await list_handler(request)


@router.delete('/delete')
async def delete_file(request: Request, delete: DeleteModel):
    return await delete_handler(request, delete)
