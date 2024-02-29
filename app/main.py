# imports de pacotes de terceiros
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# imports de pacotes pessoais
from extract.scraping import Scraping
from load.gerar_excel import exportar
from transform.gerar_tabela import gerar_tabela_dados

# Parametrizar navegador
navegador = webdriver.Edge()
navegador.implicitly_wait(10)
navegador.maximize_window() 

# Instancia da classe Scraping
scraping = Scraping(navegador) 

# Lista para receber tabela gerada a cada busca
dados_gerais = []

# Loop para percorrer datas no mês de março
for dia in range(1, 3):
    checkin = f'0{dia}-03-2024'
    checkout = f'0{dia + 1}-03-2024'

    # Navegar até tela inicial da busca    
    scraping.navegar(2, checkin, checkout)

    # Coletar dados do hotel
    dados = scraping.coletar_dados()

    # Criação e append de tabelas para unificação
    dados_diaria = gerar_tabela_dados(dados)
    dados_diaria.index = [f'{checkin}_{checkout}' for i in range(dados_diaria.shape[0])]
    dados_gerais.append(dados_diaria)

# Fechar navegador
navegador.quit()

# Gerar DataFrame unificado
tabela = pd.concat(dados_gerais)

# Exportar arquivo para o formato '.xlsx'
exportar(tabela)
