"""Testes do AES. Rodar: python -m unittest testes_aes.py -v

Criador: Guilherme Aguiar Moreira
"""
import os
import unittest
from aes import expandir_chave, cifrar_bloco, decifrar_bloco, cifrar, decifrar

h = bytes.fromhex


class TestAES(unittest.TestCase):
    def test_vetores_oficiais_nist(self):
        """Resultados esperados do FIPS-197 (Apêndice C) para 128, 192 e 256 bits."""
        texto = h("00112233445566778899aabbccddeeff")
        esperados = {
            16: "69c4e0d86a7b0430d8cdb78070b4c55a",
            24: "dda97ca4864cdfe06eaf70a0ec0d7191",
            32: "8ea2b7ca516745bfeafc49904b496089",
        }
        for tam, cifra in esperados.items():
            chaves = expandir_chave(bytes(range(tam)))
            self.assertEqual(cifrar_bloco(texto, chaves), h(cifra))
            self.assertEqual(decifrar_bloco(h(cifra), chaves), texto)

    def test_ida_e_volta(self):
        """Qualquer tamanho de mensagem volta igual."""
        chave = os.urandom(32)
        for n in (0, 1, 15, 16, 17, 1000):
            msg = os.urandom(n)
            self.assertEqual(decifrar(cifrar(msg, chave), chave), msg)

    def test_cifrado_nao_revela_conteudo(self):
        cifrado = cifrar(b"Contrato confidencial", os.urandom(32))
        self.assertNotIn(b"Contrato", cifrado)

    def test_chave_errada_nao_recupera(self):
        cifrado = cifrar(b"segredo", os.urandom(32))
        self.assertNotEqual(decifrar(cifrado, os.urandom(32)), b"segredo")


if __name__ == "__main__":
    unittest.main(verbosity=2)