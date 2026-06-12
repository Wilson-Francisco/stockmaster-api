from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database import obter_conexao
from app.auth import gerar_hash_senha



# criar o roteador para agrupar as rotas de usuarios
router = APIRouter(prefix="/auth", tags=["autenticacao"])

# Modelo de dados para validar o que o usuario envia no corpo da requisicao (JSON)
class UsuarioRegistro(BaseModel):
    username: str
    password: str