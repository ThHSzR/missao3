"""
SecureDocs — Experimento de Cifragem com AES-256-CBC (Missão 3)
Fluxo: Ficheiro original -> AES -> Ficheiro cifrado -> AES -> Ficheiro original

Criador: Mateus Afonso Miranda de Oliveira
"""
import sys
import os
import time
import hashlib
from aes import cifrar, decifrar


def sha256_arquivo(caminho: str) -> str:
    with open(caminho, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def comando_cifrar(caminho_entrada: str):
    if not os.path.exists(caminho_entrada):
        print(f"[ERRO] Ficheiro '{caminho_entrada}' não encontrado.")
        sys.exit(1)

    caminho_cifrado = caminho_entrada + ".aes"
    caminho_chave = caminho_entrada + ".key"

    with open(caminho_entrada, "rb") as f:
        dados_originais = f.read()

    chave = os.urandom(32)  # 256 bits

    inicio = time.perf_counter()
    dados_cifrados = cifrar(dados_originais, chave)
    tempo_ms = (time.perf_counter() - inicio) * 1000

    with open(caminho_cifrado, "wb") as f:
        f.write(dados_cifrados)

    with open(caminho_chave, "w") as f:
        f.write(chave.hex())

    print("\n🔒 [SECUREDOCS — DOCUMENTO CIFRADO COM AES-256-CBC]")
    print(f"  • Ficheiro Original : {caminho_entrada} ({len(dados_originais):,} bytes)")
    print(f"  • Ficheiro Cifrado  : {caminho_cifrado} ({len(dados_cifrados):,} bytes)")
    print(f"  • IV Gerado (16B)   : {dados_cifrados[:16].hex()}")
    print(f"  • Chave Salva em    : {caminho_chave} ({chave.hex()[:24]}...)")
    print(f"  • Tempo Cifragem    : {tempo_ms:.2f} ms")
    print(f"  • SHA-256 Original  : {sha256_arquivo(caminho_entrada)}")


def comando_decifrar(caminho_cifrado: str, caminho_chave: str):
    if not os.path.exists(caminho_cifrado) or not os.path.exists(caminho_chave):
        print("[ERRO] Ficheiro cifrado ou ficheiro de chave não encontrado.")
        sys.exit(1)

    base = caminho_cifrado[:-4] if caminho_cifrado.endswith(".aes") else caminho_cifrado
    nome, ext = os.path.splitext(base)
    caminho_recuperado = f"{nome}_recuperado{ext}"

    with open(caminho_cifrado, "rb") as f:
        dados_cifrados = f.read()

    with open(caminho_chave, "r") as f:
        chave = bytes.fromhex(f.read().strip())

    try:
        inicio = time.perf_counter()
        dados_recuperados = decifrar(dados_cifrados, chave)
        tempo_ms = (time.perf_counter() - inicio) * 1000
    except Exception:
        print("\n❌ [ACESSO NEGADO] Chave inválida ou ficheiro adulterado!\n")
        sys.exit(1)

    with open(caminho_recuperado, "wb") as f:
        f.write(dados_recuperados)

    print("\n🔓 [SECUREDOCS — DOCUMENTO RECUPERADO COM SUCESSO]")
    print(f"  • Ficheiro Cifrado   : {caminho_cifrado} ({len(dados_cifrados):,} bytes)")
    print(f"  • Ficheiro Restaurado: {caminho_recuperado} ({len(dados_recuperados):,} bytes)")
    print(f"  • Tempo Decifragem   : {tempo_ms:.2f} ms")
    print(f"  • SHA-256 Restaurado : {sha256_arquivo(caminho_recuperado)}")


def executar_demonstracao_automatica(caminho_alvo="contrato.pdf"):
    print("=" * 75)
    print("   SECUREDOCS — EXECUÇÃO AUTOMÁTICA DO EXPERIMENTO COM FICHEIROS (AES-256)")
    print("=" * 75)

    if not os.path.exists(caminho_alvo):
        print(f"[AVISO] '{caminho_alvo}' não encontrado. A criar ficheiro de teste...")
        with open(caminho_alvo, "wb") as f:
            f.write(b"CONTRATO TECHSECURE: Documento Confidencial Protegido por AES-256.\n" * 15)

    # 1. Cifra
    comando_cifrar(caminho_alvo)

    # 2. Decifra
    caminho_cifrado = caminho_alvo + ".aes"
    caminho_chave = caminho_alvo + ".key"
    comando_decifrar(caminho_cifrado, caminho_chave)

    # 3. Validação
    nome, ext = os.path.splitext(caminho_alvo)
    recuperado = f"{nome}_recuperado{ext}"
    hash_orig = sha256_arquivo(caminho_alvo)
    hash_rec = sha256_arquivo(recuperado)

    print("\n" + "=" * 75)
    if hash_orig == hash_rec:
        print("✔ [SUCESSO] O ficheiro recuperado é 100% idêntico ao original!")
        print("            Fluxo validado: Original -> AES -> Cifrado -> AES -> Original")
    else:
        print("❌ [FALHA] Os hashes diferem!")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    # Se passares argumentos no terminal, ele comporta-se como ferramenta CLI:
    if len(sys.argv) == 3 and sys.argv[1] == "cifrar":
        comando_cifrar(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "decifrar":
        comando_decifrar(sys.argv[2], sys.argv[3])
    else:
        # Se carregares só no Play do VS Code ou escreveres apenas "python3 experimento_arquivos.py":
        executar_demonstracao_automatica("contrato.pdf")