

class SudoKuHandle(object):
    status_valid = 0
    status_review = 1
    status_invalid = 2

    numbers_str = '123456789'
    number_char = '*'

    @classmethod
    def format_nums(cls, nums: str='') -> list:
        result = [list(v.strip()) for v in nums.split('\n') if v.strip()]
        if not len(result) == 9:
            raise ValueError(f'{nums} value error.')

        check_str = ''.join([''.join(result[i]) for i in range(9)])
        if not len(check_str) == 81:
            raise ValueError(f'{nums} value error.')

        check_sum = list(set(check_str) - set(list(cls.numbers_str)) - set(cls.number_char))
        if check_sum:
            raise ValueError(f'{nums} value error.')
        return result

    def __init__(self, nums: str=''):
        self.data = self.format_nums(nums)

    def get_rows(self, i: int = 0):
        value = ''.join(self.data[i])
        return value.replace(self.number_char, '')

    def get_cols(self, j: int = 0):
        value = ''.join([self.data[i][j] for i in range(9)])
        return value.replace(self.number_char, '')

    def get_circles(self, i: int = 0, j: int = 0):
        def g(x):
            return range((x // 3) * 3, (x // 3 + 1) * 3)
        value = ''.join([self.data[m][n] for m in g(i) for n in g(j)])
        return value.replace(self.number_char, '')

    @classmethod
    def verify_ceil(cls, value: str = ''):
        if len(value) == len(cls.numbers_str):
            return cls.status_valid if value == cls.numbers_str else cls.status_invalid

        return cls.status_review if len(set(value)) == len(
            value) else cls.status_invalid

    def verify_row(self, i: int = 0):
        rows = ''.join(sorted(self.get_rows(i)))
        result = self.verify_ceil(rows)
        if result == self.status_invalid:
            raise ValueError(f'row: {i}, data: {rows}')
        return result

    def verify_col(self, j: int = 0):
        cols = ''.join(sorted(self.get_cols()))
        result = self.verify_ceil(cols)
        if result == self.status_invalid:
            raise ValueError(f'col: {j}, data: {cols}')
        return result

    def verify_circle(self, i: int = 0, j: int = 0):
        circles = ''.join(sorted(self.get_circles()))
        result = self.verify_ceil(circles)
        if result == self.status_invalid:
            raise ValueError(f'circle: {i}, {j}. data: {circles}')
        return result

    def verify(self):
        for i in range(9):
            if not self.verify_row(i) == self.status_valid:
                raise ValueError(f'guessing...')

        for j in range(9):
            if not self.verify_col(j) == self.status_valid:
                raise ValueError(f'guessing...')

        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                if not self.verify_circle(i, j) == self.status_valid:
                    raise ValueError(f'guessing...')
        return self.status_valid

    def verify_number(self, i: int = 0, j: int = 0):
        ii = self.verify_row(i)
        jj = self.verify_col(j)
        cc = self.verify_circle(i, j)
        return ii or jj or cc

    def guess_numbers(self, i: int = 0, j: int = 0):
        nums = list(set(self.numbers_str) - set(self.get_rows(i)) -
                    set(self.get_cols(j)) - set(self.get_circles(i, j)))
        if not nums:
            raise ValueError(i, j)
        return nums

    def get_coordinate(self, i, j):
        nums = self.guess_numbers(i, j)
        return (i, j), len(nums), iter(nums)

    def get_mini_coordinate(self):
        m = [self.get_coordinate(i, j) for i in range(9) for j in range(9) if self.data[i][j] == self.number_char]
        if not m:
            raise StopIteration('success')

        return sorted(m, key=lambda k: (k[1], k[0][0], k[0][1]))[0]

    def finish_status(self):
        data_str = ''.join([''.join(self.data[i]) for i in range(9)]).replace(self.number_char, '')
        if len(data_str) == len(self.numbers_str) * 9:
            return self.status_valid
        return self.status_review

    def progress(self):
        def backup_dfs(res: list=None):
            exc = None
            coordinate, _, lst = self.get_mini_coordinate()
            res.append(coordinate)
            for n in lst:
                try:
                    self.data[coordinate[0]][coordinate[1]] = n
                    backup_dfs(res)

                except ValueError as ex:
                    exc = ex
                    continue

            if exc:
                coordinate = res.pop(-1)
                self.data[coordinate[0]][coordinate[1]] = self.number_char
                raise exc
        try:
            backup_dfs([])
        except StopIteration:
            return

    def format_display(self):
        return '\n'.join([''.join(self.data[i]) for i in range(9)])
