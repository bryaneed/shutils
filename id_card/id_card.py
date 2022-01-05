import re
import datetime
from functools import reduce
from .region import result_list


class IdCardHandle(object):
    @classmethod
    def parser_code(cls, id_code):
        reg = r'(?P<region>\d{6})(?P<date>\d{8})\d{2}(?P<sex>\d)(?P<checksum>\w)$'
        rex = re.compile(reg)
        data = rex.search(id_code)
        if data is None:
            raise ValueError('IdCard is invalid')
        return data.groupdict()

    @classmethod
    def get_birthday(cls, data: dict=None):
        birthday = data.get('date')
        reg = r'(?P<year>\d{4})(?P<mouth>\d{2})(?P<day>\d{2})$'
        rex = re.compile(reg)
        return rex.search(birthday).groupdict()

    @classmethod
    def get_sex(cls, data: dict=None):
        sex = data.get('sex')
        return 'Female' if int(sex) % 2 == 1 else 'Male'

    @classmethod
    def get_region(cls, data: dict=None):
        r = next(filter(lambda o: o['code'] == data.get('region'), result_list), None)
        if not r:
            return '-'
        return r['city']

    @classmethod
    def get_checksum(cls, id_code):
        last_num = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        num_dict = {
            '0': '1',
            '1': '0',
            '2': 'X',
            '3': '9',
            '4': '8',
            '5': '7',
            '6': '6',
            '7': '5',
            '8': '4',
            '9': '3',
            '10': '2'
        }
        checksum = reduce(lambda x, y: x + y, map(lambda x, y: x * y, [int(x) for x in id_code], last_num))
        return num_dict.get(str(checksum % 11))

    def validate_checksum(self, id_code):
        valid_checksum = self.get_checksum(id_code)
        if not valid_checksum == id_code[-1]:
            raise ValueError(f'id_card checksum error. maybe {id_code[:-1]}{valid_checksum}')

    def validate_date(self, data: dict=None):
        birthday = self.get_birthday(data)
        year, mouth, day = int(birthday['year']), int(birthday['mouth']), int(birthday['day'])
        today = datetime.datetime.today()
        if year > today.year or year < today.year - 100:
            raise ValueError('id_card birthday year error')

        if mouth not in range(1, 13):
            raise ValueError('id_card birthday mouth error')

        if mouth == 2 and day not in range(1, 30):
            raise ValueError('id_card birthday mouth day error')

        if day not in range(1, 32):
            raise ValueError('id_card birthday day error')

    def validate(self, id_code, id_data: dict=None):
        self.validate_checksum(id_code)
        self.validate_date(id_data)

    def progress(self, id_code, birthday=False, sex=False, region=False):
        id_data = self.parser_code(id_code)
        self.validate(id_code, id_data)

        result = {'valid_code': id_code}

        if birthday:
            result['birthday'] = self.get_birthday(id_data)
        if sex:
            result['sex'] = self.get_sex(id_data)
        if region:
            result['region'] = self.get_region(id_data)
        return result
