# Pipeline CI/CD - Engenharia de Software (C14)

**Disciplina:** C14 - Engenharia de Software | **Professor:** Christopher Lima

Este repositório contém a implementação de um pipeline completo de Integração e Entrega Contínuas (CI/CD) utilizando o **GitHub Actions**. O projeto tem como foco principal garantir a qualidade do software e a organização da automação, validando o código a cada nova alteração.

O sistema alvo das automações é uma API desenvolvida em Python utilizando o framework FastAPI.

## Tecnologias Utilizadas

* **Backend:** Python, FastAPI, Uvicorn
* **Testes Automatizados:** Pytest
* **CI/CD:** GitHub Actions

### Pré-requisitos
Certifique-se de ter o Python e o gerenciador de pacotes pip instalados no seu sistema.

### Como executar o projeto

1.Clone o repositório:
   ```
   git clone https://github.com/joaoryan/C14-Engenharia-de-Software.git
   ```
2.Crie e ative um ambiente virtual:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3.Instale as dependências do projeto:
  ```
  pip install -r requirements.txt
  ```
4.Inicie o servidor local:
  ```
  uvicorn main:app --reload
  ```
5.Executar os testes:
  ```
  pytest
  ```
