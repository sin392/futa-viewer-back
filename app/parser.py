from bs4 import BeautifulSoup
from typing import List
from os.path import join, basename, splitext


# 板名やスレッドの取得も
class CatalogParser:
    soup = None
    prefix = ''

    result = []

    def __init__(self, html=None):
        # if html is None:
        #     with open('samples/catalog.html', 'rb') as f:
        #         html = f.read()

        # self.parse(html)
        pass

    def parse(self, html, prefix=''):
        self.soup = BeautifulSoup(html, 'lxml')
        self.prefix = prefix

        self.result = self.get_previews()
        return self.result

    def get_previews(self) -> List[object]:
        objs = []
        for td_tag in self.soup.find('table', id='cattable').find_all('td'):
            obj = {}
            a_tag = td_tag.find('a')
            obj['a'] = {'href': join(self.prefix, a_tag['href']),
                        'target': a_tag['target']}
            obj['id'] = int(splitext(basename(a_tag['href']))[0])
            img_tag = a_tag.find('img')
            if img_tag is not None:
                obj['img'] = a_tag.find('img').attrs
                obj['img']['src'] = join(
                    self.prefix, *obj['img']['src'].split('/')[2:])
            else:
                # 画像がない時にはsmallタグで'ｷﾀｰ'という表示
                obj['img'] = None
            small_tag = td_tag.find('small')
            if small_tag is not None:
                obj['title'] = small_tag.text
            else:
                obj['title'] = ''
            obj['resNum'] = td_tag.find('font').text
            objs.append(obj)
        return objs



class ThreadParser:
    soup = None
    prefix = ''

    items = []

    result = {}

    def __init__(self, html = None, prefix = ''):
        # if html is None:
        #     with open('samples/catalog.html', 'rb') as f:
        #         html = f.read()
        # self.prefix = prefix
        # if html is not None:
        #     self.soup = BeautifulSoup(html, 'lxml')
        pass

    def parse(self, html, prefix = ''):
        self.soup = BeautifulSoup(html, 'lxml')
        self.prefix = prefix

        self.items = self.get_comments()
        # self.result = {'items': self.items}

        return self.items



    def get_comments(self) -> list[object]:
        key_map = {'rsc':'order', 'csb':'title', 'cnm':'name', 'cnw':'date', 'cno':'no'}

        objs = []
        # 0レス目(トピック)
        obj = {}
        thread_div_tag = self.soup.find('div', class_='thre')
        srcs = [join(self.prefix, *thread_div_tag.find(name)[key].split('/')[2:])
                for name, key in zip(('a', 'img'), ('href', 'src'))]
        obj['srcs'] = srcs

        for x in thread_div_tag.find_all('span', recursive=False):
            class_name = x.get('class')
            if class_name and class_name[0] in key_map:
                obj[key_map[class_name[0]]] = x.text.strip()

        block_quote_tag = thread_div_tag.find('blockquote')
        br_tag = block_quote_tag.br
        if br_tag is not None:
            br_tag.extract()
        obj['body'] = block_quote_tag.get_text('\n')
        objs.append(obj)


        # 1レス目以降をパース
        for table_tag in block_quote_tag.find_all_next('table'):
            # obj = {}
            # Nameはspanで囲まれてない...
            # header_keys = ['order', 'title', 'name', 'date', 'no']
            # header_values = [x.text.strip()
            #                 for x in table_tag.find_all('span')]
            # obj.update({k: v for k, v in zip(header_keys, header_values)})
            # 対応spanがない場合はNoneにするためにdict.get()を利用
            obj = {key_map[x.get('class')[0]]: x.text.strip() for x in table_tag.find_all('span')}
            # print(obj)

            sub_block_quote_tag = table_tag.find('blockquote')
            br_tag = sub_block_quote_tag.br
            if br_tag is not None:
                br_tag.extract()
            obj['body'] = sub_block_quote_tag.get_text('\n')
            objs.append(obj)


        return objs




if __name__ == '__main__':
    c_parser = CatalogParser()
    t_parser = ThreadParser()
    print('-' * 30)
    print(c_parser.get_previews())
    print('-' * 30)
    print(t_parser.get_title())
    print('-' * 30)
    print(t_parser.get_comments())
