import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


# Carrega as configuracaoes secretas do arquivo .env
load_dotenv()


def obter_conexao():
    """Abre e retorna uma conexao ativa com o banco de dados"""
    try:
        conexao = psycopg2.connect(
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            cursor_factory = RealDictCursor # Faz o banco retornar dados como dicionarios  
        )

        return conexao
    except Exception as expt:
        print(f"Erro critico: Nao foi possivel conectar ao banco: {expt}")
        raise expt