# StockMaster API

O **StockMaster API** é um sistema web profissional e seguro para gerenciamento de produtos e controle de estoque. Desenvolvido em Python com a arquitetura moderna do FastAPI, o projeto conta com banco de dados relacional PostgreSQL, criptografia de ponta para proteção de dados, conteinerização integral via Docker e esteira de testes automatizados com CI/CD na nuvem.

---

## Tecnologias e Ferramentas Utilizadas

*   **[FastAPI](https://tiangolo.com):** Framework web de alta performance e assíncrono para construção da API.
*   **[PostgreSQL](https://postgresql.org):** Banco de dados relacional robusto para persistência de dados.
*   **[Psycopg2 (Binary)](https://psycopg.org):** Driver de conexão nativo entre Python e PostgreSQL.
*   **[Bcrypt](https://pypi.org):** Criptografia adaptativa baseada em *salt* para hashing seguro de senhas.
*   **[PyJWT](https://readthedocs.io):** Emissão, assinatura e validação de tokens JSON Web Tokens (JWT) para autenticação.
*   **[Pydantic](https://pydantic.dev):** Validação estrita de tipos e regras de negócio de entrada e saída.
*   **[Pytest](https://pytest.org):** Framework para execução de testes automatizados unitários e de integração.
*   **[Docker & Docker Compose](https://docker.com):** Isolamento do ecossistema e gerenciamento multi-container da aplicação.
*   **[GitHub Actions](https://github.com):** Automação de CI/CD para execução de testes a cada Pull Request.

---

## Funcionalidades de Segurança e Regras de Negócio

1.  **Criptografia de Senhas:** Nenhuma senha é salva em texto puro. O sistema gera hashes irreversíveis através do algoritmo `bcrypt`.
2.  **Autenticação JWT (Bearer Token):** Rotas operacionais trancadas por autenticação. O usuário recebe um "crachá eletrônico" válido por 30 minutos após o login legítimo.
3.  **Proteção de Rotas:** Tratamento automático nos bastidores para purificação de cabeçalhos de segurança (CORS e remoção automática de prefixos `Bearer`).
4.  **Blindagem do Estoque (Pydantic):** Validações rígidas que impedem o cadastro ou alteração de produtos com preços negativos/zerados (`preco > 0`) ou quantidades em estoque abaixo de zero (`quantidade >= 0`).
5.  **Resiliência de Inicialização:** Sistema com lógica de re-tentativa (*Retry*) automática incorporada na conexão com o banco de dados.

---

## Estrutura do Projeto

```text
stockmaster-api/
│
├── .github/workflows/      # Receita do robô de CI/CD (GitHub Actions)
│   └── testes.yml
│
├── app/                    # Código fonte da aplicação Python
│   ├── __init__.py
│   ├── main.py             # Ponto de entrada (Inicialização da API)
│   ├── database.py         # Configuração e conexões com o PostgreSQL
│   ├── auth.py             # Lógica de criptografia, geração e validação de JWT
│   └── routers/            # Módulos de Endpoints (Rotas da API)
│       ├── __init__.py
│       ├── produtos.py     # CRUD de Produtos (Protegido)
│       └── usuarios.py     # Cadastro e Login de Usuários (Público)
│
├── .env                    # Modelo explicativo das variáveis de ambiente
├── .gitignore              # Proteção para arquivos locais e secretos (.env)
├── Dockerfile              # Receita de construção do container da API
├── docker-compose.yml      # Orquestrador local do ambiente de homologação
└── requirements.txt        # Inventário de dependências do Python
```

---

## Como Executar o Projeto Localmente

Certifique-se de ter o **Docker Desktop** instalado e rodando em sua máquina antes de começar.

### 1. Clonar o repositório
```bash
git clone https://github.com
cd stockmaster-api
```

### 2. Configurar as variáveis de ambiente
Crie um arquivo chamado **`.env`** na raiz do projeto e preencha as credenciais. Exemplo:
```ini
DB_HOST=localhost
DB_PORT=5544
DB_NAME=stockmaster
DB_USER=admin
DB_PASSWORD=senha_secreta
JWT_SECRET=sua_chave_secreta_super_segura_com_mais_de_32_caracteres
```

### 3. Subir o ambiente completo via Docker Compose
Para testar a API integrada a um banco de dados limpo e isolado em ambiente de homologação local, execute:
```bash
docker compose up --build
```
Após o carregamento completo do log `Application startup complete.`, a documentação interativa e os testes das rotas estarão disponíveis no seu navegador através do endereço:
👉 **[http://127.0.0](http://127.0.0)**

---

## Como Rodar os Testes Automatizados Locais

Se preferir rodar a suíte de testes com o `pytest` diretamente no ambiente virtual de desenvolvimento do seu computador:

```bash
# Ativar o ambiente virtual (Windows)
.venv\Scripts\Activate.ps1

# Definir o caminho de escopo e disparar os robôs do Pytest
\$env:PYTHONPATH="."; pytest app/testes/test_api.py
```

---

## Deploy em Produção (Nuvem)

A versão estável e consolidada do projeto encontra-se em produção sob as seguintes infraestruturas de nuvem:
*   **Servidor Web (API):** Hospedado no [Render](https://render.com) com implantação automática via Docker a partir da branch `main`.
*   **Banco de Dados:** Instância gerenciada PostgreSQL hospedada no [Neon.tech](https://neon.tech).
*   **Link Público de Produção:** [https://onrender.com](https://onrender.com)
