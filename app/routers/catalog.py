from fastapi import APIRouter, Path
import services.catalog as services
from schemas.schemas import Catalog
from . import symbols

router = APIRouter()


@router.get('/{board_name}', response_model=Catalog, deprecated=True)
async def get_catalog(board_name: str = Path('dec')):
    symbol = symbols[board_name]
    return services.get_catalog(board_name, symbol)
