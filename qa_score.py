import itertools


class QaScore(object):
    def __init__(self, qa_num=4, gen_num=30):
        self.qaNum = qa_num
        self.gen_num = gen_num

    def _cal_res(self, a, b, c, d):
        r = itertools.combinations_with_replacement(
            [a, b, c, d], self.qaNum
        )
        return set(sum(x) for x in r)

    def generator_data(self):
        return (
            (a, b, c, d) for a in range(1, self.gen_num)
            for b in range(a + 1, self.gen_num)
            for c in range(b + 1, self.gen_num)
            for d in range(c + 1, self.gen_num)
        )

    def process(self, with_console=False):
        data = self.generator_data()
        result, max_result, cal_res, = None, 0, None
        for a, b, c, d in data:
            if with_console:
                print('\n', a, b, c, d)

            cal_temp = self._cal_res(a, b, c, d)
            if max_result < len(cal_temp):
                max_result = len(cal_temp)
                cal_res = cal_temp
                result = [a, b, c, d]
        return result, cal_res


if __name__ == '__main__':
    t = QaScore(qa_num=3, gen_num=10)
    print(t.process(with_console=True))
