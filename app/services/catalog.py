import requests
from schemas.schemas import Catalog
from parser import CatalogParser

parser = CatalogParser()


def get_catalog(board_name: str, symbol: str):
    prefix = f'https://{board_name}.2chan.net/{symbol}'
    req = requests.get(f'{prefix}/futaba.php', params={'mode': 'cat'})
    parser.parse(req.content)
    previews = parser.get_previews(prefix)
    return Catalog(id=0, items=previews)
