import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


# Carrega as configuracaoes secretas do arquivo .env
load_dotenv()


def obter_conexao():
    """Abre e retorna uma conexão ativa com o PostgreSQL, com tentativas de re-conexão (Retry)."""
    tentativas = 5
    espera = 2  # Segundos entre as tentativas

    for i in range(tentativas):
        try:
            conexao = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                cursor_factory=RealDictCursor,
            )
            return conexao
        except Exception as expt:
            print(
                f"Aviso: Banco de dados ainda inicializando. Tentativa {i+1}/{tentativas} falhou. Aguardando {espera}s..."
            )
            if i == tentativas - 1:
                print(
                    f"Erro crítico: Não foi possível conectar ao PostgreSQL após {tentativas} tentativas."
                )
                raise expt
            time.sleep(espera)

def inicializar_banco():
    """Cria as tabelas do sistema automaticamente se eles nao existirem"""
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        # 1. Tabela de Usuarios (para autenticacao futura)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios(
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            );

            """
        )

        # 2. Tabela de Produtos (nosso CRUD principal)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos(
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                preco NUMERIC(10, 2) NOT NULL,
                quantidade INTEGER NOT NULL
            );

            """)

        # Consolida as alteracoes no banco de dados
        conexao.commit()
        print("Banco de dados inicializado sucesso! Tabelas verificadas/criadas")

    except Exception as expt:
        conexao.rollback()
        print(f"Erro ao inicializar o banco: {expt}")
        raise expt
    finally:
        cursor.close()
        conexao.close()
