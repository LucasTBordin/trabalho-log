

### Trabalho de Log BD II - Undo

Lucas Trentini Bordin

Como executar:

1. Instalar as dependências do projeto: `pip install -r requirements.txt`
2. Criar database no terminal do postgres: `CREATE DATABASE trab_log;`
   * se necessário, alterar o usuário e senha nas variáveis `user_postgres` e `pswd_postgres` no main.py. Por padrão, está configurado como postgres:postgres
3. Inserir (ou alterar) arquivos de teste na pasta `files` com os nomes `entradaLog` para o log e `metadados.json` para os metadados.
4. rodar `python main.py`
