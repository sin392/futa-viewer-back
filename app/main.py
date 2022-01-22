from fastapi import FastAPI
from routers.catalog import router as catalog_router
from routers.threads import router as threads_router

app = FastAPI()

app.include_router(catalog_router, prefix='/catalog')
app.include_router(threads_router, prefix='/threads')


@app.get('/')
async def root():
    return {'message': 'Hello World'}
