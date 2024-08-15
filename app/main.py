
from fastapi import FastAPI
from apis import router


app = FastAPI(docs_url="/")
app.include_router(router)
