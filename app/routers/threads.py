from fastapi import APIRouter, Path, Query
import services.threads as services
from schemas.schemas import Thread, Catalog
from . import symbols

router = APIRouter()


@router.get('/{board_name}', response_model=Catalog)
async def get_catalog(board_name: str = Path('dec'), sort: str = Query('0')):
    symbol = symbols[board_name]
    return services.get_catalog(board_name, symbol, sort)


@router.get('/{board_name}/{thread_id}', response_model=Thread)
async def get_thread(board_name: str = Path('dec'), thread_id: int = Path(0)):
    symbol = symbols[board_name]
    return services.get_thread(board_name, symbol, thread_id)
