from schemas.schemas import Thread
from parser import ThreadParser

parser = ThreadParser()


def get_thread(thread_id: int):
    return Thread(id=thread_id, items=[])
