from typing import Callable

from fastapi import Request
from fastapi.responses import JSONResponse


async def key_middleware(request: Request, call_next: Callable):
    key = request.headers.get('x-api-key')

    if key != 'Mu327gTT_KHFaIm85tS8oL8JfPL7EZ40N47PRJNgJg=':
        return JSONResponse({"detail": "Unauthorized"}, status_code=401)

    return await call_next(request)
