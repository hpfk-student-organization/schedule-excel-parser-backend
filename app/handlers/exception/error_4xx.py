from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException, status

from app.utils.requests.create_json import Status


async def validation_exception_handler(request: Request, exc: HTTPException):
    response_json = {
        'status': Status.ERROR.value,
        'type': "validation_error",
        'errors': [
            {
                "code": "required",
                "detail": "This field is required.",
                "attr": "name"
            },
        ]
    }

    return JSONResponse(content=response_json, status_code=status.HTTP_418_IM_A_TEAPOT)
