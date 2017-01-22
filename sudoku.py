

class Solution(object):
    status_valid = 0
    status_review = 1
    status_invalid = 2

    numbers_str = '123456789'
    number_char = '*'

    def __init__(self, nums: list = None):
        self.data = nums

    def get_rows(self, i: int = 0):
        value = ''.join(self.data[i])
        return value.replace(self.number_char, '')

    def get_lines(self, j: int = 0):
        value = ''.join([self.data[i][j] for i in range(9)])
        return value.replace(self.number_char, '')

    def get_circles(self, i: int = 0, j: int = 0):
        def g(x):
            return range((x // 3) * 3, (x // 3 + 1) * 3)
        value = ''.join([self.data[m][n] for m in g(i) for n in g(j)])
        return value.replace(self.number_char, '')

    @classmethod
    def verify_val(cls, value: str = ''):
        if len(value) == len(cls.numbers_str):
            return cls.status_valid if value == cls.numbers_str else cls.status_invalid

        return cls.status_review if len(set(value)) == len(
            value) else cls.status_invalid

    def verify_row(self, i: int = 0):
        rows = ''.join(sorted(self.get_rows(i)))
        result = self.verify_val(rows)
        if result == self.status_invalid:
            raise ValueError(f'row: {i}, data: {rows}')
        return result

    def verify_line(self, j: int = 0):
        lines = ''.join(sorted(self.get_lines()))
        result = self.verify_val(lines)
        if result == self.status_invalid:
            raise ValueError(f'line: {j}, data: {lines}')
        return result

    def verify_circle(self, i: int = 0, j: int = 0):
        circles = ''.join(sorted(self.get_circles()))
        result = self.verify_val(circles)
        if result == self.status_invalid:
            raise ValueError(f'circle: {i}, {j}. data: {circles}')
        return result

    def verify(self):
        for i in range(9):
            if not self.verify_row(i) == self.status_valid:
                raise ValueError(f'guessing...')

        for j in range(9):
            if not self.verify_line(j) == self.status_valid:
                raise ValueError(f'guessing...')

        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                if not self.verify_circle(i, j) == self.status_valid:
                    raise ValueError(f'guessing...')
        return self.status_valid

    def verify_number(self, i: int = 0, j: int = 0):
        ii = self.verify_row(i)
        jj = self.verify_line(j)
        cc = self.verify_circle(i, j)
        return ii or jj or cc

    def guess_numbers(self, i: int = 0, j: int = 0):
        nums = list(set(self.numbers_str) - set(self.get_rows(i)) -
                    set(self.get_lines(j)) - set(self.get_circles(i, j)))
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

    def handle(self):
        def backup_dfs(res: list=None):
            if self.finish_status() == self.status_valid:
                raise StopIteration()

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

    def output_data(self):
        return '\n'.join([''.join(self.data[i]) for i in range(9)])


def format_val(target_vals: str):
    return [list(v.strip()) for v in target_vals.split('\n') if v.strip()]


if __name__ == '__main__':
    t_vals = """
    *2*74**3*
    8*****2*1
    *******5*
    7***6****
    5**931**8
    ****5***3
    *4*******
    9*8*****7
    *3**75*6*
    """

    # t_vals = """
    # ****45**6
    # 4***965*7
    # *5****4*9
    # 9*****3**
    # 5****39**
    # *********
    # ****3*6**
    # ********5
    # ********3
    # """
    s = Solution(format_val(t_vals))
    s.handle()
    print(s.output_data())
