
class RC5:

    def __init__(self, key, rounds=12):
        # Configurações do RC5
        self.w = 32
        self.r = rounds
        self.b = len(key)
        self.u = self.w // 8

        # Máscara para limitar os valores a 32 bits
        self.mod = (1 << self.w) - 1

        # Constantes do RC5 para palavras de 32 bits
        self.P = 0xB7E15163
        self.Q = 0x9E3779B9

        # Expande a chave
        self.S = self.expand_key(key)

    # Rotação para a esquerda
    def left_rotate(self, value, amount):
        amount %= self.w
        return ((value << amount) | (value >> (self.w - amount))) & self.mod

    # Rotação para a direita
    def right_rotate(self, value, amount):
        amount %= self.w
        return ((value >> amount) | (value << (self.w - amount))) & self.mod

    # Expansão da chave
    def expand_key(self, key):
        c = max(1, (self.b + self.u - 1) // self.u)

        L = [0] * c

        for i in range(self.b - 1, -1, -1):
            L[i // self.u] = (
                (L[i // self.u] << 8) + key[i]
            ) & self.mod

        t = 2 * (self.r + 1)

        S = [0] * t
        S[0] = self.P

        for i in range(1, t):
            S[i] = (S[i - 1] + self.Q) & self.mod

        A = B = i = j = 0

        for _ in range(3 * max(t, c)):
            A = S[i] = self.left_rotate(
                (S[i] + A + B) & self.mod, 3
            )

            B = L[j] = self.left_rotate(
                (L[j] + A + B) & self.mod,
                (A + B) & self.mod
            )

            i = (i + 1) % t
            j = (j + 1) % c

        return S

    # Criptografia de um bloco de 8 bytes
    def encrypt_block(self, block):
        A, B = int.from_bytes(block[:4], "little"), int.from_bytes(block[4:], "little")

        A = (A + self.S[0]) & self.mod
        B = (B + self.S[1]) & self.mod

        for i in range(1, self.r + 1):
            A = (self.left_rotate(A ^ B, B) + self.S[2 * i]) & self.mod
            B = (self.left_rotate(B ^ A, A) + self.S[2 * i + 1]) & self.mod

        return A.to_bytes(4, "little") + B.to_bytes(4, "little")

    # Descriptografia de um bloco de 8 bytes
    def decrypt_block(self, block):
        A, B = int.from_bytes(block[:4], "little"), int.from_bytes(block[4:], "little")

        for i in range(self.r, 0, -1):
            B = self.right_rotate(
                (B - self.S[2 * i + 1]) & self.mod, A
            ) ^ A

            A = self.right_rotate(
                (A - self.S[2 * i]) & self.mod, B
            ) ^ B

        B = (B - self.S[1]) & self.mod
        A = (A - self.S[0]) & self.mod

        return A.to_bytes(4, "little") + B.to_bytes(4, "little")

    # Adiciona preenchimento para completar blocos de 8 bytes
    def pad(self, data):
        quantidade = 8 - (len(data) % 8)
        return data + bytes([quantidade] * quantidade)

    # Remove o preenchimento
    def unpad(self, data):
        quantidade = data[-1]

        if quantidade < 1 or quantidade > 8:
            raise ValueError("Preenchimento inválido")

        if data[-quantidade:] != bytes([quantidade] * quantidade):
            raise ValueError("Preenchimento inválido")

        return data[:-quantidade]

    # Criptografa um arquivo
    def encrypt_file(self, caminho_entrada, caminho_saida):
        with open(caminho_entrada, "rb") as arquivo:
            dados = arquivo.read()

        dados = self.pad(dados)

        resultado = b""

        for i in range(0, len(dados), 8):
            bloco = dados[i:i + 8]
            resultado += self.encrypt_block(bloco)

        with open(caminho_saida, "wb") as arquivo:
            arquivo.write(resultado)

        print("Arquivo criptografado com sucesso!")

    # Descriptografa um arquivo
    def decrypt_file(self, caminho_entrada, caminho_saida):
        with open(caminho_entrada, "rb") as arquivo:
            dados = arquivo.read()

        if len(dados) == 0 or len(dados) % 8 != 0:
            raise ValueError("Arquivo criptografado inválido")

        resultado = b""

        for i in range(0, len(dados), 8):
            bloco = dados[i:i + 8]
            resultado += self.decrypt_block(bloco)

        resultado = self.unpad(resultado)

        with open(caminho_saida, "wb") as arquivo:
            arquivo.write(resultado)

        print("Arquivo descriptografado com sucesso!")
