import pytest
from app.calc import add_two, subtract, product, divide

@pytest.mark.parametrize('num1, num2, output', [(1, 2, 3), (3, 4, 7), (8, 9, 17)])
def test_add(num1, num2, output):
    assert add_two(num1, num2) == output

def test_subtract():
    assert subtract(6, 4) == 2

def test_divide():
    assert divide(4, 2) == 2
    
def test_product():
    assert product(2, 3) == 6