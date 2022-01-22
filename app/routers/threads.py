from fastapi import APIRouter
import services.threads as services
from schemas.schemas import Thread

router = APIRouter()


@router.get('/{thread_id}', response_model=Thread)
async def get_thread(thread_id: int):
    return services.get_thread(thread_id)
