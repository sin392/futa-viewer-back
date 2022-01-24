from bs4 import BeautifulSoup
from typing import List
from os.path import join, basename, splitext


# 板名やスレッドの取得も
class CatalogParser:
    def parse(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def get_previews(self, prefix: str = '') -> List[object]:
        objs = []
        for td_tag in self.soup.find('table', id='cattable').find_all('td'):
            obj = {}
            a_tag = td_tag.find('a')
            obj['a'] = {'href': join(prefix, a_tag['href']),
                        'target': a_tag['target']}
            obj['id'] = int(splitext(basename(a_tag['href']))[0])
            img_tag = a_tag.find('img')
            if img_tag is not None:
                obj['img'] = a_tag.find('img').attrs
                obj['img']['src'] = join(
                    prefix, *obj['img']['src'].split('/')[2:])
            else:
                # 画像がない時にはsmallタグで'ｷﾀｰ'という表示
                obj['img'] = None
            small_tag = td_tag.find('small')
            if small_tag is not None:
                obj['title'] = small_tag.string
            else:
                obj['title'] = ''
            obj['resNum'] = td_tag.find('font').string
            objs.append(obj)
        return objs

    def __init__(self, html=None):
        if html is None:
            with open('samples/catalog.html', 'rb') as f:
                html = f.read()

        self.parse(html)


class ThreadParser:
    def parse(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def get_title(self):
        block_quote_tag = self.soup.find('blockquote')
        return block_quote_tag.string

    def get_comments(self) -> list[object]:
        objs = []
        block_quote_tag = self.soup.find('blockquote')
        table_tags = block_quote_tag.find_all_next('table')
        for table_tag in table_tags:
            obj = {}
            header_keys = ['order', 'title', 'name', 'date', 'no']
            header_values = [x.string.strip()
                             for x in table_tag.find_all('span')]
            obj.update({k: v for k, v in zip(header_keys, header_values)})

            sub_block_quote_tag = table_tag.find('blockquote')
            br_tag = sub_block_quote_tag.br
            if br_tag is not None:
                br_tag.extract()
            obj['body'] = sub_block_quote_tag.get_text('\n')
            objs.append(obj)
        return objs

    def __init__(self, html=None):
        if html is None:
            with open('samples/thread.html', 'rb') as f:
                html = f.read()

        self.parse(html)


if __name__ == '__main__':
    c_parser = CatalogParser()
    t_parser = ThreadParser()
    print('-' * 30)
    print(c_parser.get_previews())
    print('-' * 30)
    print(t_parser.get_title())
    print('-' * 30)
    print(t_parser.get_comments())
