import pytest
from question_one.cipher_helpers import shift_cipher

@pytest.mark.parametrize("word, shift, expected", [
    ("abc", 3, "def"),
    ("xyz", 3, "abc"),
    ("ABC", 2, "CDE"),
    ("ABC", 1, "BCD"),
    ("hello world", 5, "mjqqt btwqi"),
    ("hello!", 2, "jgnnq!"),
    ("abc", 29, "def"),
    ("test", 0, "test"),
    ("", 5, "")
])
def test_shift_cipher_cases(word, shift, expected):
    assert shift_cipher(word, shift) == expected
