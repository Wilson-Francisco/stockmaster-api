import os
import datetime
import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



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
    

def criar_token_jwt(username: str) -> str:
    """Gera um Token JWT assinado e valido por 30 minutos"""
    # Define o tempo de expiracao (30 minutos a partir do momento atual)
    tempo_expiracao = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    # O paylood guarda os dados do cracha (sub = dono do token, exp = data de valiadade)
    payload = {
        "sub": username,
        "exp": tempo_expiracao
    }

    # Gera e assina a token usando a nossa chave secreta do .env
    token_assinado = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    
    return token_assinado

# Cria o leitor de cabecalho padrao de seguranca
security = HTTPBearer()

def validar_token_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Validar o Token JWT enviado no cabecalho de requisicao. Deselve o nome do usuario se for valido"""
    token = credentials.credentials
    try:
        # Abre e decodifica o token usando a nossa chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido: Dono do token nao encontrado"
            )
        return username
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="O seu cracha de acesso (Token JWT) expirou. Faca login novamente"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token JWT invalido ou corrimpido"
        )