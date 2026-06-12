import jwt
from app.auth import gerar_hash_senha, verificar_senha, criar_token_jwt, SECRET_KEY, ALGORITHM

print("===== INICIANDO TESTES DO MÓDULO DE SEGURANÇA =====\n")

# 1. Teste de Criptografia (Bcrypt)
print("1. [TESTANDO CRIPTOGRAFIA]")
senha_original = "Acesso@2026"
hash_banco = gerar_hash_senha(senha_original)

print(f"-> Senha pura original: {senha_original}")
print(f"-> Hash gerado para o Banco: {hash_banco}")
print("-" * 50)

# 2. Teste de Verificação de Senha
print("2. [TESTANDO VERIFICAÇÃO DE LOGIN]")
login_correto = verificar_senha("Acesso@2026", hash_banco)
login_errado = verificar_senha("SenhaIncorreta", hash_banco)

print(f"-> Tentativa com senha CORRETA: {login_correto} (Esperado: True)")
print(f"-> Tentativa com senha ERRADA: {login_errado} (Esperado: False)")
print("-" * 50)

# 3. Teste de Emissão e Leitura de JWT
print("3. [TESTANDO EMISSÃO DE TOKEN JWT]")
usuario_teste = "gerente_estoque"
token = criar_token_jwt(usuario_teste)
print(f"-> Token JWT emitido: {token[:40]}...[cortado]")

# Vamos abrir o token para ver se a nossa chave secreta consegue ler o dono dele
try:
    dados_decodificados = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"-> Dono do Token identificado com sucesso: {dados_decodificados.get('sub')}")
    print("\n TUDO FUNCIONANDO PERFEITAMENTE!")
except Exception as e:
    print(f" Erro ao ler o token: {e}")

print("\n==================================================")
