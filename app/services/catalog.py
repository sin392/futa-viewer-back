from schemas.schemas import Catalog
from parser import CatalogParser

parser = CatalogParser()


def get_catalog(board_name: str = 'dec'):
    prefix = f'https://{board_name}.2chan.net/b'
    previews = parser.get_previews(prefix)
    return Catalog(id=0, items=previews)
