import requests
from fastapi import FastAPI, HTTPException
from schemas.schemas import Thread, Catalog
from parser import ThreadParser, CatalogParser

# htmlの構造自体は違うがパーサーまとめるべきか？
t_parser = ThreadParser()
c_parser = CatalogParser() 

# TODO: 名称の統一
def get_catalog(board_name: str, symbol: str, sort: str):
    prefix = f'https://{board_name}.2chan.net/{symbol}'
    req = requests.get(f'{prefix}/futaba.php', params={'mode': 'cat', 'sort': sort})
    items = c_parser.parse(req.content, prefix)
    return Catalog(items=items)


def get_thread(board_name: str, symbol: str, thread_id: int):
    prefix = f'https://{board_name}.2chan.net/{symbol}'
    url = f'{prefix}/res/{thread_id}.htm'

    try:
        req = requests.get(url)
        items = t_parser.parse(req.content, prefix)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="item_not_found")

    return Thread(items=items)
