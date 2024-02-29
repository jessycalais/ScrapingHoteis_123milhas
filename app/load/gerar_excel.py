# imports de pacotes built-in
import datetime

# imports de pacotes de terceiros
import pandas as pd

# Data da extração dos dados no site da 123milhas
DATA = datetime.date.today().strftime('%d_%m_%Y')
NOME_ARQUIVO = f'scraping_123milhas_{DATA}.xlsx'

def exportar(df: pd.core.frame.DataFrame) -> None:
    """
    Gera um arquivo no formato '.xlsx' e salva na pasta 'data'.

    Parameters:
        df (pandas.core.frame.DataFrame): um DataFrame do Pandas

    Returns:
        None
    """
    df.to_excel(f'.\data\{NOME_ARQUIVO}')
    