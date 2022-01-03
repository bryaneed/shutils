# coding: utf-8
import itertools


class QaScore(object):
    def __init__(self, qa_num=4, genNum=30):
        self.qaNum = qa_num
        self.genNum = genNum

    def _caculate_result(self, a, b, c, d):
        r = itertools.combinations_with_replacement(
            [a, b, c, d], self.qaNum
        )
        return set(sum(x) for x in r)

    def generator_data(self):
        return (
            (a, b, c, d) for a in range(1, self.genNum)
            for b in range(a + 1, self.genNum)
            for c in range(b + 1, self.genNum)
            for d in range(c + 1, self.genNum)
        )

    def process(self, with_console=False):
        data = self.generator_data()
        result, max_result, caculate_result, = None, 0, None
        for a, b, c, d in data:
            if with_console:
                print('\n', a, b, c, d)

            _caculate_results = self._caculate_result(a, b, c, d)
            if max_result < len(_caculate_results):
                max_result = len(_caculate_results)
                caculate_result = _caculate_results
                result = [a, b, c, d]
        return result, caculate_result


if __name__ == '__main__':
    t = QaScore(qa_num=3, genNum=10)
    print(t.process(with_console=True))
