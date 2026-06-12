from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.database import obter_conexao
from app.auth import validar_token_jwt



# Criar o roteador para produtos com prefixo correto
router = APIRouter(prefix="/produtos", tags=["Produtos"])

# Modelo de dados para garantir validacao de regras de negocio basicas (Pydantic)
class ProdutoEsquema(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    preco: float = Field(..., gt=0, description="O preco deve ser maior que zero")
    quantidade: int =  Field(..., ge=0, description="A quantidade nao pode ser negativa")
