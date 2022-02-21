from fastapi import APIRouter, Path, Query
import services.threads as services
from schemas.schemas import Thread, Catalog

router = APIRouter()


@router.get('/{board_name}', response_model=Catalog)
async def get_catalog(board_name: str = Path('dec'), sort: str = Query('0')):
    return services.get_catalog(board_name, sort)


@router.get('/{board_name}/{thread_id}', response_model=Thread)
async def get_thread(board_name: str = Path('dec'), thread_id: int = Path(0)):
    return services.get_thread(board_name, thread_id)
