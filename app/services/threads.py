import requests
from schemas.schemas import Thread
from parser import ThreadParser, CatalogParser

# htmlの構造自体は違うがパーサーまとめるべきか？
t_parser = ThreadParser()
c_parser = CatalogParser()


def get_thread_previews(board_name: str, symbol: str):
    prefix = f'https://{board_name}.2chan.net/{symbol}'
    req = requests.get(f'{prefix}/futaba.php', params={'mode': 'cat'})
    c_parser.parse(req.content)
    previews = c_parser.get_previews(prefix)
    return previews


def get_thread(board_name: str, symbol: str, thread_id: int):
    url = f'https://{board_name}.2chan.net/{symbol}/res/{thread_id}.htm'
    req = requests.get(url)
    t_parser.parse(req.content)
    title = t_parser.get_title()
    comments = t_parser.get_comments()
    return Thread(title=title, items=comments)
