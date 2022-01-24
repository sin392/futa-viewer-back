from typing import List
from fastapi import APIRouter, Path
import services.threads as services
from schemas.schemas import Thread, ThreadPreview
from . import symbols

router = APIRouter()


@router.get('/{board_name}', response_model=List[ThreadPreview])
async def get_thread_previews(board_name: str = Path('dec')):
    symbol = symbols[board_name]
    return services.get_thread_previews(board_name, symbol)


@router.get('/{board_name}/{thread_id}', response_model=Thread)
async def get_thread(board_name: str = Path('dec'), thread_id: int = Path(0)):
    symbol = symbols[board_name]
    return services.get_thread(board_name, symbol, thread_id)
