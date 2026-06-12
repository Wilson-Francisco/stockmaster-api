from fastapi.testclient import TestClient
from app.main import app



# Cria um cliente de teste que consegue disparar requisicoes para a nossa API
client = TestClient(app)

def test_api_raiz_esta_online():
    """Garante que a rota raiz (/) responde com sucesso e status online"""
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "online"

    def test_bloqueio_cadastro_produto_sem_token():
        """Garante que a API bloqueia o cadastro de produtos se o token nao for enviado"""
        dados_produto = {
            "nome": "cadeira Gamer Teste",
            "preco": 899.90,
            "quantidade": 5
        }
        # Tenta enviar o produto sem cabecalho de seguranca(token)
        resposta = client.post("produtos", json=dados_produto)

        # O status esperando e 401 (Nao autorizado)
        assert resposta.status_code == 401