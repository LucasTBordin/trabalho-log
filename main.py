import psycopg2
import json

try:
    # conecta com o banco
    conn = psycopg2.connect(
        host="localhost",
        database="trab_log",
        user="postgres",
        password="postgres")

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
        file = open('files/metadados.json')
        data = json.load(file)['table']
        file.close()
    except Exception as e:
        print(e)
        exit()

    
    dados = list(zip(data['id'], data['A'], data['B']))

    # insere dados na tabela
    for dado in dados:
        cursor.execute(f'INSERT INTO data VALUES ({dado[0]},{dado[1]},{dado[2]})')

    conn.commit()


except (Exception, psycopg2.DatabaseError) as error:
    print(error)



