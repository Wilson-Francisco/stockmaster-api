import os
import bcrypt
from dotenv import load_dotenv


# Carrega as variaveis de ambiente (sera util para a chave secreta do JWT mais tarde)
load_dotenv()


def gerar_hash_senha(senha_pura:str) -> str:
    """ Transforma uma senha em texto comum em um hash embaralhado e seguro"""
    # O salt adiciona caracteres aleatorios para tornar o hash totalmente unico
    salt = bcrypt.gensalt()


    # Gera o hash criptografado combinando a senha com o salt
    senha_criptografada = bcrypt.hashpw(senha_pura.encode('utf-8'), salt)
    

    # Converte o resultado de volta para string de texto para salvar no banco
    return senha_criptografada.decode('utf-8')
                                        
                                    