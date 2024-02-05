import logging
from uuid import uuid4

from fastapi import File, UploadFile, Request, HTTPException

from utils.check_api_key import check_api_key


async def upload_handler(request: Request, file: UploadFile = File(...)):
    """
    Uploads a file to the server
    """
    check_api_key(request)

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
