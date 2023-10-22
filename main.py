import psycopg2

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
    

    cursor.close()

# printa erros
except (Exception, psycopg2.DatabaseError) as error:
    print(error)



