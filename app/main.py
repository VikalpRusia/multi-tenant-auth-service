import logging
import traceback

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from apis import router

app = FastAPI(docs_url="/")
app.include_router(router)

logger = logging.getLogger(__name__)
# TODO: close connection in lifespan


@app.exception_handler(IntegrityError)
async def handle_db_exception(
    request: Request, exception: IntegrityError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exception)}
    )
