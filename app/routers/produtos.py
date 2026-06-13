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


@router.post("", status_code=status.HTTP_201_CREATED)
def cadastrar_produto(produto: ProdutoEsquema, usuario_atual: str = Depends(validar_token_jwt)):
    """Cadastra um novo produto no estoque. Rota Protegida por JWT"""
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        # Insercao no banco utilizando placeholders seguros
        cursor.execute(
            "INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s) RETURNING id;",
            (produto.nome, produto.preco, produto.quantidade)
        )
        # Captura o ID gerado automaticamente pelo SERIAL do banco
        novo_id = cursor.fetchone()["id"]
        conexao.commit()

        return {
            "id": novo_id,
            "mensagem": f"Produto '{produto.nome}' cadastrado com sucesso por {usuario_atual}!"
        }
    
    except Exception as expt:
        conexao.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar o produto no banco: {str(expt)}"
        )
    finally:
        cursor.close()
        conexao.close()


@router.get("", status_code=status.HTTP_200_OK)
def lista_produtos(usuario_atual: str = Depends(validar_token_jwt)):
    """Busca e retorna todos os produtos cadastrados no estoque. Rota Protegida por JWT"""
    conexao = obter_conexao()
    cursor = conexao.cursor()


    try:
        # Busca todos os produtos ordenados pelo ID de forma crescente
        cursor.execute("SELECT id, nome, preco, quantidade FROM produtos ORDER BY id ASC;")
        produtos = cursor.fetchall()

        # Se o banco estiver vazio, retornamos uma lista vazia [], o que e padrao de mercado
        return produtos
    
    except Exception as expt:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar produtos no banco: {str(expt)}"
        )
    finally:
        cursor.close()
        conexao.close()


@router.put("/{produto_id}", status_code=status.HTTP_200_OK)
def atualizar_produto(produto_id: int, dados_novos: ProdutoEsquema, usuario_atual: str = Depends(validar_token_jwt)):
    """Atualiza todos os dados de um produto existente pelo ID. Rota protegida por JWT"""
    conexao = obter_conexao()
    cursor = conexao.cursor()


    try:
        # 1. Execute a atualizacao e ja pede para retornar o ID se ele existir
        cursor.execute(
            """
            UPDATE produtos
            SET nome = %s, preco = %s, quantidade = %s
            WHERE id = %s
            RETURNING id
            """,
            (dados_novos.nome, dados_novos.preco, dados_novos.quantidade, produto_id)
        )
        resultado = cursor.fetchone()

        # 2. Se o resultado for nulo, significa que o ID nao foi encontrado no banco
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com o ID {produto_id} nao foi encontrado no estoque"
            )
        
        conexao.commit()
        return {
            "id": produto_id,
            "mensagem": f"Produto ID {produto_id} atualizado com sucesso por {usuario_atual}!"
        }
    
    except Exception as expt:
        conexao.rollback()
        if isinstance(expt, HTTPException):
            raise expt
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao atualizar o produto no banco {str(expt)}"
        )
    finally:
        cursor.close()
        conexao.close()


@router.delete("/{produto_id}", status_code=status.HTTP_200_OK)
def deletar_produto(produto_id: int, usuario_atual: str = Depends(validar_token_jwt)):
    """Remove permanentemente um produto do estoque pelo ID. Rota Protegida por JWT"""
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        # Execute a remocao e tente retornar o ID deletado para checar existencia
        cursor.execute("DELETE FROM produtos WHERE id = %s RETURNING id;", (produto_id,))
        resultado = cursor.fetchone()

        # Se o resultado for nulo, significa que o ID nao existia
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com o ID {produto_id} nao foi encontrado para exclusao"
            )
        
        conexao.commit()
        return {
            "id": produto_id,
            "mensagem": f"Produto ID {produto_id} removido com sucesso por {usuario_atual}!"
        }
    
    except Exception as expt:
        conexao.rollback()
        if isinstance(expt, HTTPException):
            raise expt
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao deletar o produto no banco: {str(expt)}"
        )
    finally:
        cursor.close()
        conexao.close()
