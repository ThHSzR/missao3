
from rc5 import RC5

# =====================================
# TESTE 1 - Configurações do RC5
# =====================================

chave = b"MinhaChave123456"

algoritmo = RC5(chave)

print("===== TESTE 1: CONFIGURAÇÕES =====")
print("Algoritmo: RC5")
print("Tamanho da palavra:", algoritmo.w, "bits")
print("Quantidade de rodadas:", algoritmo.r)
print("Tamanho da chave:", algoritmo.b, "bytes")
print("Tamanho do bloco:", algoritmo.u * 2, "bytes")


# =====================================
# TESTE 2 - Criptografia
# =====================================

print("\n===== TESTE 2: CRIPTOGRAFIA =====")

mensagem = b"SEGURDOC"

print("Mensagem original:", mensagem)

mensagem_cifrada = algoritmo.encrypt_block(mensagem)

print("Mensagem criptografada:", mensagem_cifrada.hex().upper())


# =====================================
# TESTE 3 - Descriptografia
# =====================================

print("\n===== TESTE 3: DESCRIPTOGRAFIA =====")

mensagem_original = algoritmo.decrypt_block(mensagem_cifrada)

print("Mensagem descriptografada:", mensagem_original)

if mensagem_original == mensagem:
    print("SUCESSO! A mensagem original foi recuperada.")
else:
    print("ERRO! A mensagem não foi recuperada.")


# =====================================
# TESTE 4 - Vetor de teste conhecido
# =====================================

print("\n===== TESTE 4: VETOR DE TESTE =====")

chave_teste = bytes.fromhex(
    "915F4619BE41B2516355A50110A9CE91"
)

mensagem_teste = bytes.fromhex(
    "21A5DBEE154B8F6D"
)

resultado_esperado = "F7C013AC5B2B8952"

rc5_teste = RC5(chave_teste)

resultado = rc5_teste.encrypt_block(mensagem_teste)

print("Chave:", chave_teste.hex().upper())
print("Mensagem:", mensagem_teste.hex().upper())
print("Resultado obtido:", resultado.hex().upper())
print("Resultado esperado:", resultado_esperado)

if resultado.hex().upper() == resultado_esperado:
    print("SUCESSO! O RC5 passou no vetor de teste.")
else:
    print("ERRO! O resultado está diferente do esperado.")
