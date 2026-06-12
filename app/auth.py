import os
import datetime
import bcrypt
import jwt
from dotenv import load_dotenv



# Carrega as variaveis de ambiente (sera util para a chave secreta do JWT mais tarde)
load_dotenv()

# configuracoes do JWT puxadas com seguranca do .env
SECRET_KEY = os.getenv("JWT_SECRET", "chave_padrao_caso_nao_encontre")
ALGORITHM = "HS256" # Algoritmo padrao de mercado para assinar token


def gerar_hash_senha(senha_pura:str) -> str:
    """ Transforma uma senha em texto comum em um hash embaralhado e seguro"""
    # O salt adiciona caracteres aleatorios para tornar o hash totalmente unico
    salt = bcrypt.gensalt()


    # Gera o hash criptografado combinando a senha com o salt
    senha_criptografada = bcrypt.hashpw(senha_pura.encode('utf-8'), salt)
    

    # Converte o resultado de volta para string de texto para salvar no banco
    return senha_criptografada.decode('utf-8')
                                        

def verificar_senha(senha_digitada: str, hash_salvo_no_banco: str) -> bool:
    """ Verifica se a senha que o usuario digitou confere com hash salvo no banco"""
    try:
        # O bcryp compara a senha pura com o hash de forma segura contra ataques de tempo
        return bcrypt.checkpw(senha_digitada.encode('utf-8'), hash_salvo_no_banco.encode('utf-8'))
    except Exception:
        return False