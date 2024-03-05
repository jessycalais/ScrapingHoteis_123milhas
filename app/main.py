# imports de pacotes de terceiros
from os import getcwd
from asyncio import run as asyncio_run

from etl.pipeline import aplicar_pipeline

def main():
    n_adultos = 2
    n_criancas = 0
    n_bebes = 0
    duracao = 5

    dia_inicial, mes_inicial, ano_inicial = 1, 5, 2024  

    pasta_raiz = getcwd()+'/data/'
    radical_nome_arquivo = 'scraping_123milhas'

    asyncio_run(
        aplicar_pipeline(
            pasta_raiz, radical_nome_arquivo, 
            n_adultos, n_criancas, n_bebes,
            dia_inicial, mes_inicial, ano_inicial, duracao
        )
    )

if __name__ == "__main__":
    main()