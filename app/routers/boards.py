from fastapi import APIRouter, Path, Query
import services.boards as services
from schemas.schemas import Menu

router = APIRouter()


@router.get('/', response_model=Menu)
async def get_menu():
    return services.get_menu()
