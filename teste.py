import psycopg2
import dotenv, os


dotenv.load_dotenv('.env')

# Configurações de conexão
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')


try:
    # Conecta ao banco de dados
    conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
    cursor = conn.cursor()

    # Executa a consulta
    cursor.execute('SELECT * FROM pilotos;')
    rows = cursor.fetchall()

    # Exibe os resultados
    for row in rows:
        print(row)

    # Fecha a conexão
    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Erro ao conectar ou executar a consulta: {e}")