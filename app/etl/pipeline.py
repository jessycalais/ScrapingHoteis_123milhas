from pandas import concat
from concurrent.futures import ThreadPoolExecutor, as_completed

# imports de pacotes pessoais
from etl.transform.gerar_tabela import gerar_tabela_dados
from etl.extract.scraping import Scraping
from etl.utils import calcular_checkin_checkout_inicial,  \
    incrementar_data, \
    dias_do_mes
from etl.load.gerar_dados import exportar

async def process_future(future, dados_gerais, successful_count, checkin, checkout):
    try:
        dados = future.result()
        dados_diaria = gerar_tabela_dados(dados)
        n_linhas = dados_diaria.shape[0]
        dados_diaria.index = [f'{checkin}_{checkout}' for i in range(n_linhas)]
        dados_gerais.append(dados_diaria)

        successful_count += 1
    
    except Exception as e:
        print(f"An error occurred: {e}")

    print(dados_gerais)

async def aplicar_pipeline(
        pasta_raiz: str, radical_nome_arquivo: str,
        n_adultos: int, n_criancas:int, n_bebes:int,
        dia_inicial: int, mes_inicial: int, ano_inicial:int, 
        alcance_dias_:int=31
    ):
    dias_do_mes_ = dias_do_mes(mes_inicial, ano_inicial)
    
    # Dias validos para o mês
    if(alcance_dias_ is None):
        alcance_dias_=dias_do_mes_-dia_inicial+1

    # Instancia da classe Scraping
    tempo_de_espera=10
    scrapper = Scraping(tempo_de_espera) 

    # Lista para receber tabela gerada a cada busca
    dados_gerais = []
        
    checkin, checkout = calcular_checkin_checkout_inicial(dia_inicial, mes_inicial, ano_inicial)
    
    data_inicial = checkin
    data_final = checkin

    # Start the tasks in parallel
    for _ in range(1, alcance_dias_+1):
        dados = scrapper.raspar(
            n_adultos, n_criancas, n_bebes, 
            checkin, checkout
        )
        dados_diaria = gerar_tabela_dados(dados)
        n_linhas = dados_diaria.shape[0]
        dados_diaria.index = [f'{checkin}_{checkout}' for i in range(n_linhas)]
        dados_gerais.append(dados_diaria)
        
        checkin, checkout = checkout, incrementar_data(checkout)

    # Gerar DataFrame unificado
    tabela = concat(dados_gerais)

    # Exportar arquivo para formatos em FORMATOS
    nome_arquivo = f'{radical_nome_arquivo}_{data_inicial}_{data_final}'
    rota_arquivo = pasta_raiz+'/'+nome_arquivo
    
    exportar(rota_arquivo, tabela)
