from calendar import IllegalMonthError
from pytest import raises

from app.etl.utils import obter_numero_aleatorio_10n_10np1, \
    incrementar_data, dias_do_mes

def test_obter_numero_aleatorio_10n_10np1():
    n = 3
    resultado = obter_numero_aleatorio_10n_10np1(n)
    assert 10 ** n <= resultado < 10 ** (n+1)

def test_incrementar_data():
    assert '02-01-2000' == incrementar_data('01-01-2000')
    assert '01-02-2000' == incrementar_data('31-01-2000')

def test_dias_do_mes():
    assert 31 == dias_do_mes(1, 2000)
    assert 29 == dias_do_mes(2, 2000)
    assert 31 == dias_do_mes(3, 2000)
    assert 30 == dias_do_mes(4, 2000)
    
    with raises(IllegalMonthError):
        dias_do_mes(13, 2000)
