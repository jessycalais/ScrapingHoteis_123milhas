# **Web Scraping - 123milhas**

### :dart: Objetivo:

O objetivo deste projeto é coletar dados sobre diárias em hotéis na cidade de São Paulo durante um período de 20 dias no mês de março (01/03/2024 à 20/03/2024).</p>

<p style="text-align: justify;">Escolhemos este período pois não há feriados nacionais nesta época.</p>  

<p style="text-align: justify;">Após a coleta iremos realizar um projeto de Análise Exploratória (EDA) a fim de detectar padrões (ou não) nos preços de diárias em hotéis em São Paulo.</p>

### :hammer: Principais ferramentas e conceitos utilizados:

* Python orientado a objetos;
* Regex (manipulação de strings);
* Pandas (DataFrames);
* Datetime (manipulação de datas);
* Selenium (navegação e extração de dados);
* Mkdocs (documentação);
* Ambiente virtual e gerenciamento de dependências (Poetry);
* Taskipy (automação de tarefas no terminal);
* Git (para versionamento do código).

### :books: Conteúdo dos arquivos do repositório:
**1) Pasta *app***  
Pacotes para ETL e código principal (`main.py`) para rodar a automação.

**2) Pasta *data***  
Contém o arquivo `.xlsx` gerado após o *web scraping*.  
**Atenção**: O código foi aplicado a apenas 02 dias de busca para gerar arquivo de exemplo no GitHub.

**3) Pasta *docs***  
Documentação desenvolvida com a biblioteca *mkdocs*.  
Acesse a documentação em: <a href="https://jessycalais.github.io/ScrapingHoteis_123milhas/" target="_blank" rel="noopener noreferrer"><b>clique aqui</b></a>.

---
---

### **EXTRAS:**

> **Próximos passos:**

Mapeamos melhorias para este projeto e organizamos na lista abaixo:

:clipboard: **TODO**

* Utilizar *Requests* e *BealtifulSoup* para extração dos dados nos cards dos hotéis;  
* Implementação de testes para garantir o bom funcionamento do código;
* Validação de dados com *Pandera* e/ou *Pydantic*;
* App com *Streamlit* para facilitar o uso pelo usuário final.

---

> **Como usar esse código na sua máquina**

Você pode escolher usar o gerenciador de dependências de sua escolha. 

Abaixo vou descrever como você pode utilizar o `poetry`. :smile:

1. Caso você não tenha a CLI do Git, sugiro que faça a instalação: [clique aqui](https://cli.github.com/).

2. Para clonar este repositório, abra o terminal e altere o diretório de trabalho para o local em que deseja ter o repositório clonado e digite:
```
gh repo clone jessycalais/ScrapingHoteis_123milhas
```

3. Após isso, instale o pacote *pipx* com o comando:
```
pip install pipx
```

4. Instale o pacote *poetry*:
```
pipx install poetry
```

5. Configure a criação do ambiente virtual:
```
poetry config virtualenvs.in-project true
```

6. Ative o ambiente virtual via terminal:
```
poetry shell
```

7. Instale as dependências do projeto:
```
poetry install
```

8. Agora, basta abrir o arquivo `main.py`e *rodar* o código, ou ainda, digitar no terminal:
```
task run
```

---

Caso tenha dificuldade com algum passo acima ou encontre algum erro, fique à vontade para me comunicar. :smile:
