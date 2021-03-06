from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routers.threads import router as threads_router
from routers.boards import router as boards_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {'message': 'Hello World'}

router = APIRouter()
router.include_router(threads_router, prefix='/threads')
router.include_router(boards_router, prefix='/boards')

app.include_router(router, prefix='/v1')
