from bs4 import BeautifulSoup
from typing import List
import re
from os.path import join, basename, splitext

class BaseParser:
    soup = None
    prefix = ''
    items = []

    def __init__(self, html=None):
        pass

    def parse(self, html, prefix=''):
        self.soup = BeautifulSoup(html, 'lxml')
        self.prefix = prefix
        self.items = self.get_items()
        return self.items

    def _extract_image(self, start_tag, default=None):
        img_tag = start_tag.find('img')
        if img_tag is not None:
            obj = img_tag.attrs
            obj['src'] = join(
                self.prefix, *obj['src'].split('/')[2:])
        else:
            # 画像がない時にはsmallタグで'ｷﾀｰ'という表示
            obj = default
        return obj

    def _extract_href(self, start_tag, default=None):
        a_tag = start_tag.find('a')
        if a_tag is not None:
            href = join(
                self.prefix, *a_tag['href'].split('/')[2:])
        else:
            href = default
        return href

    def get_items(self) -> list[object]:
        return []


class CatalogParser(BaseParser):
    def get_items(self) -> List[object]:
        objs = []
        for td_tag in self.soup.find('table', id='cattable').find_all('td'):
            obj = {}
            a_tag = td_tag.find('a')
            # obj['href'] = join(self.prefix, a_tag.get(
            #     'href')) if a_tag is not None else None
            try:
                # 時々,'futaba'などの整数化できない文字列が入ってくる
                obj['id'] = int(
                    splitext(basename(a_tag['href']))[0])  # スレッドへのリンク
            except Exception as e:
                print(e)
                obj['id'] = 0
            obj['img'] = self._extract_image(start_tag=a_tag, default=None)
            # print(obj['img'])
            small_tag = td_tag.find('small')
            obj['title'] = small_tag.text if small_tag is not None else ''
            font_tag = td_tag.find('font')
            obj['resNum'] = font_tag.text if font_tag is not None else 0

            objs.append(obj)
        return objs


class ThreadParser(BaseParser):
    span_key_map = {'rsc': 'order', 'csb': 'title',
                    'cnm': 'name', 'cnw': 'date', 'cno': 'no'}

    def get_items(self) -> list[object]:
        objs = []
        # 0レス目(トピック)
        obj = {}
        thread_div_tag = self.soup.find('div', class_='thre')
        obj['href'] = self._extract_href(
            start_tag=thread_div_tag, default=None)
        obj['img'] = self._extract_image(
            start_tag=thread_div_tag, default=None)

        for x in thread_div_tag.find_all('span', recursive=False):
            class_name = x.get('class')
            if class_name and class_name[0] in self.span_key_map:
                obj[self.span_key_map[class_name[0]]] = x.text.strip()
        # そうだね
        a_sod_tag = thread_div_tag.find('a', class_='sod')
        if a_sod_tag is not None:
            str_sod = re.sub(r'\D', '', a_sod_tag.text)
            obj['sod'] = int(str_sod) if str_sod != '' else 0
        else:
            obj['sod'] = None

        # 本文
        block_quote_tag = thread_div_tag.find('blockquote')
        br_tag = block_quote_tag.br
        if br_tag is not None:
            br_tag.extract()
        obj['body'] = block_quote_tag.get_text('\n')
        objs.append(obj)

        # 1レス目以降をパース
        for table_tag in block_quote_tag.find_all_next('table'):
            obj = {self.span_key_map[x.get('class')[0]]: x.text.strip()
                   for x in table_tag.find_all('span')}
            # 本文
            sub_block_quote_tag = table_tag.find('blockquote')
            br_tag = sub_block_quote_tag.br
            if br_tag is not None:
                br_tag.extract()
            # TODO: 画像付きコメントへの対応
            obj['body'] = sub_block_quote_tag.get_text('\n')
            # そうだね
            a_sod_tag = table_tag.find('a', class_='sod')
            if a_sod_tag is not None:
                str_sod = re.sub(r'\D', '', a_sod_tag.text)
                obj['sod'] = int(str_sod) if str_sod != '' else 0
            else:
                obj['sod'] = None
            objs.append(obj)

        return objs


if __name__ == '__main__':
    c_parser = CatalogParser()
    t_parser = ThreadParser()
    print('-' * 30)
    print(c_parser.get_items())
    print('-' * 30)
    print(t_parser.get_title())
    print('-' * 30)
    print(t_parser.get_items())
