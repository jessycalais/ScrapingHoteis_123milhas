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

8. Agora, basta abrir o arquivo `main.py` e *rodar* o código, ou ainda, digitar no terminal:
```
task run
```

---

Caso tenha dificuldade com algum passo acima ou encontre algum erro, fique à vontade para me contatar. :smile:
