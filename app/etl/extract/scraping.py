# imports de pacotes built-in
from time import sleep

# imports de pacotes de terceiros
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from contextlib import contextmanager

class Scraping:
    """
    Classe para representar o Scraping dos dados no site 123milhas.com.

    Attributes
    ----------
    navegador (webdriver): instância de webdriver.Firefox().

    
    Methods
    ----------
    coletar_dados(): coleta os dados dos cards de hotéis encontrados na página de navegação.

    navegar(adultos: int, checkin: str, checkout: str)
    """
    
    def __init__(self, tempo_carregamento) -> None:
        """
        Inicializa a classe.

        Parameters:
            navegador (webdriver): instância de webdriver.Edge().

        Return:
            None
        """
        self.tempo_carregamento=tempo_carregamento
        
    @contextmanager
    def navegador_manager(self):
        navegador = webdriver.Firefox()
        navegador.implicitly_wait(self.tempo_carregamento)
        navegador.maximize_window()

        try:
            self.navegador = navegador
            yield navegador
        finally:
            navegador.quit()
            del self.navegador

    def __validar_entradas_get_url(
            self, 
            adultos: int, criancas: int, bebes: int, 
            checkin: str, checkout: str
        ) -> bool:
        """
        Verifica se os valores de entrada do método privado '__gerar_ulr()' são validos.

        Parameters:
            adultos (int): número de adultos no quarto na diária.
            criancas: int: número de crianças no quarto na diária.
            bebes: int: número de bebês no quarto na diária.
            checkin (str): data de check-in.
            chechout (str): data de check-out.

        Returns:
            bool
        """
        from datetime import datetime

        is_adultos_int=isinstance(adultos, int)
        is_criancas_int=isinstance(criancas, int)
        is_bebes_int=isinstance(bebes, int)
        
        is_pessoas_int=is_adultos_int & is_criancas_int & is_bebes_int
        
        is_checkin_format_dmy=datetime.strptime(checkin, "%d-%m-%Y")
        is_checkout_format_dmy=datetime.strptime(checkout, "%d-%m-%Y")
        
        return is_pessoas_int and is_checkin_format_dmy and is_checkout_format_dmy

    def __montar_url_query(
            self, adultos: int, criancas: int, bebes:int, checkin: str, checkout: str
        ) -> str:
            query_info={}

            # TOME NOTA: Propriedades 'is_loyalty', 'localizacao' e 'tipo' são fixas
            query_info_viagem={
                "adultos": adultos,
                'bebes': bebes,
                'criancas': criancas,
                'quartos': f'{adultos}',
                'checkin': checkin,
                'checkout': checkout,
                'is_loyalty': 0,
                'localizacao': 'S%C3%A3o%20Paulo,%20S%C3%A3o%20Paulo,%20Brasil&',
                'tipo': "City"
            }

            id = 1010502
            search_id = 3399519902

            # TOME NOTA: Propriedades 'id' e 'search_id' são geradas aleatoriamente
            query_info_pesquisa={
                'id': id, 
                'search_id': search_id,
            }

            # Atualiza dicionário de query_info
            query_info.update(query_info_pesquisa)
            query_info.update(query_info_viagem) 

            query = ''.join(['?']+[f'{key}={value}&' for key, value in query_info.items()])
            query=query[:-1]

            return query

    def __gerar_url(
            self, 
            adultos: int, criancas: int, bebes:int, 
            checkin: str, checkout: str
        ) -> str:
        """
        Gera a url de navegação.

        Parameters:
            adultos (int): número de adultos no quarto na diária.
            checkin (str): data de check-in.
            chechout (str): data de check-out.

        Returns:
            url: gera uma url baseada nos parâmetros de entrada.

        """
        if self.__validar_entradas_get_url(adultos, criancas, bebes, checkin, checkout):
            host = 'https://123milhas.com'
            route = '/hoteis'
            query = self.__montar_url_query(
                adultos, criancas, bebes, checkin, checkout
            )

            url = ''.join([host, route, query])
            
            return url
        else:
            raise ValueError('Valores de entrada inválidos.')

    def __coletar_card_hotel(self) -> list:
        """
        Salva o elemento web que contém os dados dos hotéis. 
        
        Parameters: 
            None

        Returns: 
            hoteis: Retorna uma lista contendo todos os cards encontrados.
        """
        hoteis = self.navegador.find_elements(By.TAG_NAME, 'hotel-list-card')
        
        return hoteis

    def __coletar_card_preco(self, hotel): 
        """
        Coleta o card que contém as informações sobre preço e quantidade de diárias.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            card_preco: Retorna um card contendo informações sobre a diária (preço e total de diárias).
        """
        card_preco = hotel.find_element(By.CLASS_NAME, 'hotel-list-card__hotel-prices-holder')
        
        return card_preco

    def __encontrar_titulo_do_elemento(self, card, elemento):
        return card.find_element(By.TAG_NAME, elemento).text.title()


    def __coletar_nome(self, hotel) -> str:
        """
        Coleta o nome do hotel.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            nome: Retorna uma string contendo o nome do hotel.
        """
        return self.__encontrar_titulo_do_elemento(hotel, 'h4')


    def __coletar_localizacao(self, hotel) -> str:
        """
        Coleta a localização do hotel registrada na página web.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            local: Retorna uma string contendo a localização.
        """
        return self.__encontrar_titulo_do_elemento(hotel, 'h5')

    
    def __coletar_rua(self, hotel) -> str:
        """
        Coleta o endereço (rua) do hotel.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            rua: Retorna uma string contendo o endereço (rua) do hotel.
        """
        tag_p = hotel.find_elements(By.TAG_NAME, 'p')
        if len(tag_p) > 2:
            rua = tag_p[1].text
        else:
            rua = tag_p[0].text
        
        return rua.title()


    def __coletar_pontos_fidelidade(self, hotel) -> int:
        """
        Coleta a quantidade de pontos do Programa Fidelidade caso a pessoa opte pelo hotel escolhido.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            pontos: Retorna um float contendo o total de pontos.
        """
        pontos = hotel.find_element(By.CLASS_NAME, 'points-stripe-hotels').text

        return pontos[8:-27]


    def __coletar_nota(self, hotel) -> str:
        """
        Coleta a pontuação (avaliação) do hotel.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            nota: Se existir avaliação, retorna uma string contendo a pontuação (avaliação) do hotel. Caso contrário, retorna 'Sem avaliação'.
        """
        try:          
            bloco_avaliacoes = hotel.find_element(By.TAG_NAME, 'customer-grade')
            nota_avaliacoes = bloco_avaliacoes.find_element(By.CLASS_NAME, 'customer-grade__box-grade')
            nota = nota_avaliacoes.text
        
        except:
            nota = 'Sem avaliação' 

        return nota


    def __coletar_total_de_avaliacoes(self, hotel) -> str:
        """
        Coleta a quantidade de avaliações do hotel no site.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            total_de_avaliacoes: Retorna uma string contendo a quantidade de avaliações do hotel.
        """
        try:          
            bloco_avaliacoes = hotel.find_element(By.TAG_NAME, 'customer-grade')
            total_de_avaliacoes = bloco_avaliacoes.find_element(By.TAG_NAME, 'span').text
        except:
            total_de_avaliacoes = '0 avaliações'
        
        return total_de_avaliacoes[:-11]

    def __coletar_cafe_da_manha(self, hotel) -> str:
        """
        Coleta a informação do oferecimento (incluso ou não) do café da manhã.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            cafe: Retorna uma string contendo a oferta do café da manhã.
        """
        cafe = hotel.find_element(By.TAG_NAME, 'toggle-badge').text

        return cafe


    def __coletar_extras(self, hotel) -> str:  
        """
        Coleta se há ar-condicionado, secador, entre outros itens extras na acomodação.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            opcoes_extras: Se existirem itens extras, retorna uma string contendo-os. Caso contrário, retorna 'Não informado'.
        """
        try:
            opcoes_extras = hotel.find_element(By.TAG_NAME, 'ul').text
        except:
            opcoes_extras = 'Não informado'

        return ' '.join(opcoes_extras.split())     
        

    def __coletar_diarias(self, hotel) -> str:   
        """
        Coleta a quantidade de diárias solicitadas e o total de hóspedes.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_preco(hotel)'.

        Returns: 
            diaria: Retorna uma string contendo a quantidade de diárias e o total de hóspedes.
        """ 
        card_preco = self.__coletar_card_preco(hotel)
        diaria = card_preco.find_elements(By.TAG_NAME, 'span')[1].text
        
        return diaria

    def __coletar_preco(self, hotel) -> float: 
        """
        Coleta o preço total da diária solicitada.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_preco(hotel)'.

        Returns: 
            preco: Retorna uma string contendo o preço total.
        """    
        card_preco = self.__coletar_card_preco(hotel)
        preco = card_preco.find_elements(By.TAG_NAME, 'div')[1].text

        return preco.replace('R$ ', '')

    def coletar_dados(self) -> list:
        """
        Coleta os dados dos cards de hotéis encontrados na página de navegação.

        Paremeters:
            None

        Returns:
            dados_gerais: Retorna uma lista contendo os dados coletados em cada card encontrado (dados por hotel).
        """
        
        hoteis = self.__coletar_card_hotel()
        
        nome = []
        localizacao = []
        rua = []
        nota = []
        total_de_avaliacoes = []
        cafe = []
        opcoes_extras = []
        diaria = []
        preco = []
        pontos = []

        from tqdm import tqdm
        for hotel in tqdm(hoteis):
            nome.append(self.__coletar_nome(hotel))
            localizacao.append(self.__coletar_localizacao(hotel))
            rua.append(self.__coletar_rua(hotel))
            nota.append(self.__coletar_nota(hotel))
            total_de_avaliacoes.append(self.__coletar_total_de_avaliacoes(hotel))
            cafe.append(self.__coletar_cafe_da_manha(hotel))
            opcoes_extras.append(self.__coletar_extras(hotel))
            diaria.append(self.__coletar_diarias(hotel))
            preco.append(self.__coletar_preco(hotel))
            pontos.append(self.__coletar_pontos_fidelidade(hotel))
 
        dados_gerais = [
            nome, localizacao, rua, nota, total_de_avaliacoes, 
            cafe, opcoes_extras, diaria, preco, pontos
        ]

        return dados_gerais  
    
    def navegar(
            self, 
            adultos: int, criancas: int, bebes:int, checkin: str, checkout: str
        ) -> None: 
        """
        Navega até a URL gerada pelo método privado 'Scraping.__gerar_url(adultos, criancas, bebes, checkin, checkout)'.

        Parameters:
            adultos (int): Número de adultos no quarto na diária.
            criancas (int): Número de crianças no quarto na diária.
            bebes (int): Número de bebês no quarto na diária.
            checkin (str): Data de check-in.
            checkout (str): Data de check-out.

        Returns:
            None
        """
        url = self.__gerar_url(adultos, criancas, bebes, checkin, checkout)
        self.navegador.get(url)
        
        sleep(self.tempo_carregamento)

    def raspar(self, adultos, criancas, bebes, checkin, checkout):
        """
        Executa o processo de raspagem de dados.

        Navega até a URL gerada com base nos argumentos fornecidos e coleta os dados da página.

        Parameters:
            adultos (int): Número de adultos no quarto na diária.
            criancas (int): Número de crianças no quarto na diária.
            bebes (int): Número de bebês no quarto na diária.
            checkin (str): Data de check-in.
            checkout (str): Data de check-out.

        Returns:
            dict: Um dicionário contendo os dados coletados da página.
        """
        with self.navegador_manager():
            self.navegar(adultos, criancas, bebes, checkin, checkout)
            dados = self.coletar_dados()

        return dados