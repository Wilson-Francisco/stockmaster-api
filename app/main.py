from fastapi import FastAPI
from app.database import inicializar_banco
from app.database import inicializar_banco
from app.routers.usuarios import router as usuarios_router



# Cria a instancia principal de API FastAPI
app = FastAPI(
    title="StockMaster API",
    description="Sistema seguro de gerenciamento de produtos e estoque",
    version="1.0.0"
)


# Inclui as rotas de autenticacao de usuarios na API
app.include_router(usuarios_router)


# Evento que roda automaticamente quando a API liga
@app.on_event("startup")
def startup_event():
    print("Iniciando a StockMaster API...")
    inicializar_banco()


# Uma rota simples de teste para verificar se a API  esta online
@app.get("/")
def ler_raiz():
    return {
        "status": "online",
        "sistema": "StockMaster API",
        "mensagem": "Bem-vindo ao sistema de controle de estoque!"
    }