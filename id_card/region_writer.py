import re
import os
import json
import codecs


def get_results():
    def _get_result(x):
        return rex.search(x).groupdict()

    reg = r'(?P<code>\d+?)\: (?P<city>.*)'
    rex = re.compile(reg)

    with codecs.open(f'{os.getcwd()}/region.txt', 'r', 'utf-8') as fg:
        return [_get_result(x) for x in fg.readlines()]


def write_py():
    result_list = get_results()

    with codecs.open('region.py', 'w', 'utf-8') as fg:
        fg.write('\nresult_list = ')
        data = [{'code': x.get('code'), 'city': x.get('city')} for x in result_list]
        fg.write(json.dumps(data, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    write_py()
