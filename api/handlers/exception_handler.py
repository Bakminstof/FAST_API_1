from starlette.requests import Request
from starlette.responses import JSONResponse

from routes import app
from .exceptions import APIException


@app.exception_handler(APIException)
async def api_exception_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content=exc.content,
        headers=exc.headers
    )
