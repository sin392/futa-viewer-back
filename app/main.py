from fastapi import FastAPI, APIRouter
from routers.catalog import router as catalog_router
from routers.threads import router as threads_router

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}

router = APIRouter()
router.include_router(catalog_router, prefix='/catalog')
router.include_router(threads_router, prefix='/threads')

app.include_router(router, prefix='v1')
