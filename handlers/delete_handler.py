import os

from fastapi import HTTPException, Request

from models.delete_model import DeleteModel
from utils.check_api_key import check_api_key


async def delete_handler(request: Request, delete: DeleteModel):
    """
    Deletes a file from the server
    """
    check_api_key(request)

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
