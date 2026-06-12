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

def inicializar_banco():
    """Cria as tabelas do sistema automaticamente se eles nao existirem"""
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        # 1. Tabela de Usarios (para autenticacao futura)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usarios(
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            );
            """
        )

    except Exception as expt:
        conexao.rollback()
        print(f"Erro ao inicializar o banco: {expt}")
        raise expt
    finally:
        cursor.close()
        conexao.close()
