from fastapi import APIRouter
import services.catalog as services
from schemas.schemas import Thread, Catalog

router = APIRouter()


@router.get('/', response_model=Catalog)
async def get_catalog() -> Catalog:
    return services.get_catalog()
