import psycopg2
import json
import re
import sys

try:
    # conecta com o banco
    conn = psycopg2.connect(
        host="localhost", database="trab_log", user="postgres", password="postgres"
    )

    cursor = conn.cursor()

    # cria tabela
    cursor.execute(
        """
        DROP TABLE IF EXISTS data;
        CREATE TABLE data(
            id integer NOT NULL,
            a integer NOT NULL,
            b integer NOT NULL
        );"""
    )

    # lê arquivo de metadados
    try:
        file = open("files/metadados.json")
        data = json.load(file)["table"]
        file.close()
    except Exception as e:
        print(e)
        exit()

    dados = list(zip(data["id"], data["A"], data["B"]))

    # insere dados na tabela
    for dado in dados:
        cursor.execute(f"INSERT INTO data VALUES ({dado[0]},{dado[1]},{dado[2]})")

    # lê arquivo de log
    try:
        log = open("files/entradaLog")
    except Exception as e:
        print(e)
        exit()

    # cria vetores pra armazenar as transações que começaram e as que fizeram commit
    started = []
    committed = []

    # percorre log de trás pra frente
    for linha in reversed(list(log)):
        # se chegar em um fim de checkpoint, não precisa mais olhar
        if "END CKPT" in linha:
            break

        # se for um commit
        if "commit" in linha:
            # add id da transação no vetor committed
            committed.append(linha.split(" ")[1].replace(">\n", ""))

        # se for um start
        if "start" in linha and "CKPT" not in linha:
            # add id da transação no vetor started
            started.append(linha.split(" ")[1].replace(">\n", ""))

        # se for um registro de transação
        match = re.search("<T.*,.*,.*,.*>", linha)
        if match:
            # remove caracteres <>
            match = match.group(0).replace("<", "").replace(">", "")

            # transforma em vetor
            tupla = match.split(",")

            # se a transação não estiver comitada, faz UNDO
            if tupla[0] not in committed:
                # busca valor atual no banco
                cursor.execute(f"SELECT {tupla[2]}  FROM data WHERE id = {tupla[1]}")
                valor_bd = cursor.fetchone()[0]

                # se o valor no banco for diferente do log, faz update no banco
                if str(valor_bd) != str(tupla[3]):
                    cursor.execute(
                        f"UPDATE data SET {tupla[2]}={tupla[3]} WHERE id={tupla[1]}"
                    )
                    print(
                        f"{tupla[0]}: alteração no BD (linha {tupla[1]}, coluna {tupla[2]}) de {valor_bd} para {tupla[3]}"
                    )

    # percorre as transações começadas e printa as não comitadas
    for t in started:
        if t not in committed:
            print(f"Transação {t} realizou UNDO")
    conn.commit()
    print("\nID\tA\tB")
    cursor.copy_to(sys.stdout, "data", sep="\t")


except (Exception, psycopg2.DatabaseError) as error:
    print(error)
