import logging
import traceback

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from jwt import InvalidTokenError
from sqlalchemy.exc import IntegrityError

from apis import router

app = FastAPI(docs_url="/")
app.include_router(router)

logger = logging.getLogger(__name__)
# TODO: close connection in lifespan


@app.exception_handler(IntegrityError)
@app.exception_handler(InvalidTokenError)
async def handle_exception(_request: Request, exception: Exception) -> JSONResponse:
    logger.error(f"An unexpected error occurred: {str(exception)}")
    logger.error("".join(traceback.format_exception(exception)))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exception)}
    )
