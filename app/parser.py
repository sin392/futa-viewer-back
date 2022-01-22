from bs4 import BeautifulSoup
from typing import List
from os.path import join


# 板名やスレッドの取得
class CatalogParser:
    def get_previews(self, prefix: str = '') -> List[object]:
        objs = []
        for td_tag in self.soup.find('table', id='cattable').find_all('td'):
            obj = {}
            a_tag = td_tag.find('a')
            obj['a'] = {'href': join(prefix, a_tag['href']),
                        'target': a_tag['target']}
            img_tag = a_tag.find('img')
            if img_tag is not None:
                obj['img'] = a_tag.find('img').attrs
            else:
                # 画像がない時にはsmallタグで'ｷﾀｰ'という表示
                obj['img'] = None
            obj['title'] = td_tag.find('small').string
            obj['resNum'] = td_tag.find('font').string
            objs.append(obj)
        return objs

    def __init__(self):
        with open('sample_catalog.html', 'rb') as f:
            html = f.read()

        self.soup = BeautifulSoup(html, 'lxml')


class ThreadParser:
    pass


if __name__ == '__main__':
    parser = CatalogParser()
    print(parser.get_previews())
