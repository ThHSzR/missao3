
from rc5 import RC5

# Chave de 16 bytes
chave = b"MinhaChave123456"

# Criando o algoritmo
algoritmo = RC5(chave)

print("===== TESTE DE ARQUIVO RC5 =====")

# Criptografando o arquivo
algoritmo.encrypt_file("arquivo.txt", "arquivo_criptografado.rc5")

# Descriptografando o arquivo
algoritmo.decrypt_file(
    "arquivo_criptografado.rc5",
    "arquivo_recuperado.txt"
)

# Comparando os arquivos
with open("arquivo.txt", "rb") as original:
    dados_originais = original.read()

with open("arquivo_recuperado.txt", "rb") as recuperado:
    dados_recuperados = recuperado.read()

if dados_originais == dados_recuperados:
    print("\nSUCESSO! O arquivo foi recuperado corretamente.")
else:
    print("\nERRO! Os arquivos são diferentes.")
