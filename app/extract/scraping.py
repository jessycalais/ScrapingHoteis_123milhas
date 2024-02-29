# imports de pacotes built-in
from datetime import datetime
from time import sleep

# imports de pacotes de terceiros
from selenium.webdriver.common.by import By

class Scraping:
    """
    Classe para representar o Scraping dos dados no site 123milhas.com.

    Attributes
    ----------
    navegador (webdriver): instância de webdriver.Edge().

    
    Methods
    ----------
    coletar_dados(): coleta os dados dos cards de hotéis encontrados na página de navegação.

    navegar(adultos: int, checkin: str, checkout: str)
    """
    
    def __init__(self, navegador) -> None:
        """
        Inicializa a classe.

        Parameters:
            navegador (webdriver): instância de webdriver.Edge().

        Return:
            None
        """
        self.navegador = navegador


    def __validar_entradas_get_url(self, adultos: int, checkin: str, checkout: str) -> bool:
        """
        Verifica se os valores de entrada do método privado '__gerar_ulr()' são validos.

        Parameters:
            adultos (int): número de adultos no quarto na diária.
            checkin (str): data de check-in.
            chechout (str): data de check-out.

        Returns:
            bool
        """
        if isinstance(adultos, int) and datetime.strptime(checkin, "%d-%m-%Y") and datetime.strptime(checkout, "%d-%m-%Y"):
            return True
        else:
            return False


    def __gerar_url(self, adultos: int, checkin: str, checkout: str) -> str:
        """
        Gera a url de navegação.

        Parameters:
            adultos (int): número de adultos no quarto na diária.
            checkin (str): data de check-in.
            chechout (str): data de check-out.

        Returns:
            url: gera uma url baseada nos parâmetros de entrada.

        """
        if self.__validar_entradas_get_url(adultos, checkin, checkout):
            url = ''.join(['https://123milhas.com/hoteis?adultos=', str(adultos),
                        '&bebes=0', '&checkin=', checkin, '&checkout=', checkout,
                        '&criancas=0&id=1010502&localizacao=', 
                        'S%C3%A3o%20Paulo,%20S%C3%A3o%20Paulo,%20Brasil&',
                        '&quartos=', str(adultos), 
                        '&tipo=City&is_loyalty=0&search_id'])
            return url
        else:
            raise

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


    def __coletar_nome(self, hotel) -> str:
        """
        Coleta o nome do hotel.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            nome: Retorna uma string contendo o nome do hotel.
        """
        nome = hotel.find_element(By.TAG_NAME, 'h4').text

        return nome


    def __coletar_localizacao(self, hotel) -> str:
        """
        Coleta a localização do hotel registrada na página web.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            local: Retorna uma string contendo a localização.
        """
        localizacao = hotel.find_element(By.TAG_NAME, 'h5').text

        return localizacao

    
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

        return rua


    def __coletar_pontos_fidelidade(self, hotel) -> int:
        """
        Coleta a quantidade de pontos do Programa Fidelidade caso a pessoa opte pelo hotel escolhido.
        
        Parameters: 
            hotel: Subitem da lista gerada pelo método privado 'Scraping.__coletar_card_hotel()'.

        Returns: 
            pontos: Retorna um float contendo o total de pontos.
        """
        pontos = hotel.find_element(By.CLASS_NAME, 'points-stripe-hotels').text

        return pontos


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
        
        return total_de_avaliacoes

    
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

        return opcoes_extras     
        

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

        return preco

                       
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

        for hotel in hoteis:
            nome.append(self.__coletar_nome(hotel).title())
            localizacao.append(self.__coletar_localizacao(hotel).title())
            rua.append(self.__coletar_rua(hotel).title())
            nota.append(self.__coletar_nota(hotel))
            total_de_avaliacoes.append(self.__coletar_total_de_avaliacoes(hotel)[:-11])
            cafe.append(self.__coletar_cafe_da_manha(hotel))
            opcoes_extras.append(' '.join(self.__coletar_extras(hotel).split()))
            diaria.append(self.__coletar_diarias(hotel))
            preco.append(self.__coletar_preco(hotel).replace('R$ ', ''))
            pontos.append(self.__coletar_pontos_fidelidade(hotel)[8:-27])
 
        dados_gerais = [nome, localizacao, rua, nota, total_de_avaliacoes, cafe, opcoes_extras, diaria, preco, pontos]

        return dados_gerais  
         

    def navegar(self, adultos: int, checkin: str, checkout: str) -> None: 
        """
        Navega até a url gerada pelo método privado 'Scraping.__gerar_url(adultos, checkin, checkout)'.

        Parameters:
            adultos (int): número de adultos no quarto na diária.
            checkin (str): data de check-in.
            chechout (str): data de check-out.

        Returns:
            None
        """
        url = self.__gerar_url(adultos, checkin, checkout)     
        self.navegador.get(url)
        sleep(10)
