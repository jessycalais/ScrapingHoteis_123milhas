# imports de pacotes built-in
import re

# imports de pacotes de terceiros
import pandas as pd

def gerar_tabela_reduzida(dados_gerais) -> pd.core.frame.DataFrame:
    """
    Organiza as informações coletadas pelos métodos da classe Scraping num DataFrame.

    Parameters:
        dados_gerais (pandas.core.frame.DataFrame): um dicionário contendo os dados coletados pelos métodos da classe Scraping.

    Returns:
        df: Retorna um DataFrame contendo todas as informações coletadas no scraping.
    """
    dados = { 
            'hotel': dados_gerais[0],
            'localizacao_no_site': dados_gerais[1],
            'endereco': dados_gerais[2],
            'nota': dados_gerais[3],
            'total_de_avaliacoes': dados_gerais[4],
            'cafe_da_manha': dados_gerais[5],
            'opcoes_extras': dados_gerais[6],
            'diarias_hospedes': dados_gerais[7],
            'preco_reais': dados_gerais[8],
            'pontos_fidelidade': dados_gerais[9]
        }

    df = pd.DataFrame(dados)
    
    return df

def gerar_tabela_dados(dados_gerais) -> pd.core.frame.DataFrame:
    """
    Separa a informação sobre diarias e total de hóspedes em duas colunas e gera um DataFrame expandido.

    Parameters:
        dados gerais: um DataFrame do Pandas gerado pela 'função gerar_tabela_reduzida()'.

    Returns:
        df: Retorna um dataframe expandido com duas colunas extras (em relação ao df de entrada) 
                                    contendo infos sobre diárias e hóspedes.
    """
    # Gerar DataFrame reduzido
    df = gerar_tabela_reduzida(dados_gerais)

    # Expande a tabela
    df[['quantidade_de_diarias', 'quantidade_de_hospedes']] = df['diarias_hospedes'].str.split(", ", expand=True)

    # Coleta a parte numérica da string usando regex
    pattern = re.compile('\d+')
    df['quantidade_de_diarias'] = df['quantidade_de_diarias'].apply(lambda string: pattern.search(string).group())
    df['quantidade_de_hospedes'] = df['quantidade_de_hospedes'].apply(lambda string: pattern.search(string).group())

    # Altera a ordem das colunas
    df.insert(8, 'quantidade_de_diarias', df.pop('quantidade_de_diarias'))
    df.insert(9, 'quantidade_de_hospedes', df.pop('quantidade_de_hospedes'))

    return df
    