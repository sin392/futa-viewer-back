import requests
from fastapi import HTTPException
from schemas.schemas import Menu
from bs4 import BeautifulSoup



def get_menu():
    req = requests.get('https://www.2chan.net/index2.html')
    if req.status_code == 404:
        raise HTTPException(status_code=404, detail="Menu Not Found")

    items = []
    try:
        soup = BeautifulSoup(req.content, 'lxml')
        items = [{'href': 'https:' + a_tag['href'], 'name': a_tag.text} for a_tag in soup.find('table').find_all('a')]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return Menu(items=items)