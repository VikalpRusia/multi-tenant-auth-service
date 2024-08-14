
from fastapi import FastAPI
from api import router


app = FastAPI(docs_url="/")
app.include_router(router)
