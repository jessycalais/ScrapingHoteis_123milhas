from datetime import datetime, timedelta
from calendar import monthrange
from random import randint

def calcular_checkin_checkout_inicial(dia, mes, ano):
    dia = str(dia).zfill(2)
    checkin=f'{dia}-{mes}-{ano}'
    checkout=incrementar_data(checkin)

    return checkin, checkout

def incrementar_data(data_string: str, n:int=1):
    data = datetime.strptime(data_string, '%d-%m-%Y')
    data_incrementada = data + timedelta(days=n)

    # Convert back to string with the same format
    return data_incrementada.strftime('%d-%m-%Y')

def dias_do_mes(mes: int, ano:int):
    return monthrange(ano, mes)[1]

def obter_numero_aleatorio_10n_10np1(n: int):
    return randint(10 ** n, 10 ** (n+1) - 1)