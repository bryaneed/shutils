import pytest
from unittest import TestCase
from id_card.id_card import IdCardClass


class IdCardTestCase(TestCase):
    def setUp(self):
        self.ins = IdCardClass()

    def test_valid_idcard(self):
        id_code = '421127199207281934'
        result = self.ins.output(id_code)
        assert result['valid_code'] == id_code

    def test_invalid_len(self):
        id_code = '4211271992072'
        with pytest.raises(ValueError):
            self.ins.output(id_code)

    def test_invalid_checksum(self):
        id_code = '421127199207281939'
        with pytest.raises(ValueError):
            self.ins.output(id_code)
