
from unittest import TestCase
from sudoku.sudoku import SudoKuHandle


class SudoKuTestCase(TestCase):
    @classmethod
    def generate_todo_value(cls):
        v1 = """
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
        return [v1]

    def test_valid_status(self):
        value_list = self.generate_todo_value()
        for value in value_list:
            inst = SudoKuHandle(value)
            inst.progress()
            print(f'\n{value}\n\n{inst.format_display()}')
            assert inst.verify() == inst.status_valid
