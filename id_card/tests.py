import pytest
from unittest import TestCase
from id_card.id_card import IdCardHandle


class IdCardTestCase(TestCase):
    def setUp(self):
        self.ins = IdCardHandle()

    def test_valid_idcard(self):
        id_code = '421127199207281934'
        result = self.ins.progress(id_code)
        assert result['valid_code'] == id_code

    def test_invalid_len(self):
        id_code = '4211271992072'
        with pytest.raises(ValueError):
            self.ins.progress(id_code)

    def test_invalid_checksum(self):
        id_code = '421127199207281939'
        with pytest.raises(ValueError):
            self.ins.progress(id_code)

    def test_invalid_birthday(self):
        id_code = '421127199207321932'
        with pytest.raises(ValueError):
            self.ins.progress(id_code)
