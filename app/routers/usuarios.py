from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database import obter_conexao
from app.auth import gerar_hash_senha, verificar_senha, criar_token_jwt



# criar o roteador para agrupar as rotas de usuarios
router = APIRouter(prefix="/auth", tags=["autenticacao"])

# Modelo de dados para validar o que o usuario envia no corpo da requisicao (JSON)
class UsuarioRegistro(BaseModel):
    username: str
    password: str


@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def registrar_usuario(dados:UsuarioRegistro):
    """Cadastra um novo usuario no sistema com senha criptografada"""
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        # 1. Verifica se a username ja esta cadastrado
        cursor.execute("SELECT id FROM usuarios WHERE username = %s;", (dados.username,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este nome de usuario ja esta sendo utilizado"
            )
        
        # 2. Criptografa a senha pura do usuario
        senha_criptografada = gerar_hash_senha(dados.password)


        # 3. Salva no banco de dados
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash) VALUES (%s, %s);",
            (dados.username, senha_criptografada)
        )

        conexao.commit()

        return {"mensagem": "Usuario registrado com sucesso!"}
    
    except Exception as expt:
        conexao.rollback()
        # Se for um erro do FastAPI(como o do usuario exitnte), repassa ele
        if isinstance(expt, HTTPException):
            raise expt
        # Se for outro erro interno do banco, devolva erro 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao salvar no banco: {str(expt)}"
        )
    finally:
        cursor.close()
        conexao.close()
    


@router.post("/login")
def login_usuario(dados: UsuarioRegistro):
    """Autentica o usuario e rwtorna um Tpken JWT valido"""
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        # 1. Busca o ussuario no banco de dados para capturar o hash da senha
        cursor.execute("SELECT username, password_hash FROM usuarios WHERE username = %s;", (dados.username,))
        usuario = cursor.fetchone()


        # 2. Se usuario nao existir, ou a senha nao bater, barra com Erro 401 (Nao autorrizado)
        # Usamos a mesma mensagem generica para nao dar pistas a possiveis invasores
        if not usuario or not verificar_senha(dados.password, usuario["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nome de usuario ou senha incorreta"
            )
        

        # 3. Se passou na validacao, emite o Token JWT
        token_acesso = criar_token_jwt(usuario["username"])


        # 4. Retorna o token no padrao de mercado
        return {
            "acess_token": token_acesso,
            "token_type": "bearer"
        }

    except Exception as expt:
        if isinstance(expt, HTTPException):
            raise expt
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no Servidor ao fazer login: {str(expt)}"
        )
    finally:
        cursor.close()
        conexao.close() 
