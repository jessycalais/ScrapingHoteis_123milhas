import datetime
import pandas as pd

FORMATOS = ['xlsx', 'parquet']

def exportar(rota_arquivo: str, df: pd.core.frame.DataFrame) -> None:
    """
    Exporta um DataFrame para diferentes formatos de arquivo.

    Parameters:
        df (pandas.core.frame.DataFrame): um DataFrame do Pandas

    Returns:
        None
    """
    for formato in FORMATOS:
        path = f'{rota_arquivo}.{formato}'
        if formato == 'xlsx':
            df.to_excel(path)
        elif formato == 'parquet':
            df.to_parquet(path)
        else:
            raise ValueError(f'Formato {formato} não suportado')