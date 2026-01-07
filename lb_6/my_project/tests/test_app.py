
import pytest
from app import add, is_even

# 1. Тест для функції add (декілька випадків)
def test_add_simple():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

# 2. Параметризований тест для is_even
@pytest.mark.parametrize("value, expected", [
    (2, True),
    (3, False),
    (10, True),
    (11, False),
    (0, True),
])
def test_is_even(value, expected):
    assert is_even(value) == expected

# 3. Фікстура, що повертає список парних чисел
@pytest.fixture
def sample_numbers():
    return [2, 4, 6, 8, 10]

# 4. Тест, що використовує фікстуру
def test_all_even(sample_numbers):
    for n in sample_numbers:
        assert is_even(n) is True