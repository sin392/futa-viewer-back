import requests
from fastapi import HTTPException
from schemas.schemas import Thread, Catalog
from parser import ThreadParser, CatalogParser
from . import symbols

# htmlの構造自体は違うがパーサーまとめるべきか？
t_parser = ThreadParser()
c_parser = CatalogParser()


def get_catalog(board_name: str, sort: str):
    if board_name in symbols:
        prefix = f'https://{board_name}.2chan.net/{symbols[board_name]}'
    else:
        raise HTTPException(
            status_code=404, detail="Board Not Registered OR Not Existed")
    url = f'{prefix}/futaba.php'
    req = requests.get(url,
                       params={'mode': 'cat', 'sort': sort, 'cxyl': '14x6x10x0x0'})

    if req.status_code == 404:
        raise HTTPException(status_code=404, detail="Board Not Found")

    try:
        items = c_parser.parse(req.content, prefix)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return Catalog(items=items)


def get_thread(board_name: str, thread_id: int):
    if board_name in symbols:
        prefix = f'https://{board_name}.2chan.net/{symbols[board_name]}'
    else:
        raise HTTPException(
            status_code=404, detail="Board Not Registered OR Not Existed")

    url = f'{prefix}/res/{thread_id}.htm'
    req = requests.get(url)

    if req.status_code == 404:
        raise HTTPException(status_code=404, detail="Thread Not Found")

    try:
        items = t_parser.parse(req.content, prefix)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return Thread(items=items)
