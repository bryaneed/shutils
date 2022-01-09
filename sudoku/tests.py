
from unittest import TestCase
from sudoku.sudoku import SudoKuHandle


class SudoKuTestCase(TestCase):
    @classmethod
    def generate_todo_value(cls):
        v1 = """
        ***87****
        1*76**3**
        ***5*4***
        **4*539**
        ******6**
        52***6***
        9*1******
        *******4*
        7*8****31
        """
        return [v1]

    def test_valid_status(self):
        value_list = self.generate_todo_value()
        for value in value_list:
            inst = SudoKuHandle(value)
            inst.progress()
            print(f'\n{value}\n{inst.format_display()}')
            assert inst.verify() == inst.status_valid
