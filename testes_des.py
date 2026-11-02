"""Testes do DES. Rodar: python -m unittest testes_des.py -v"""
import unittest

from des import cifrar, cifrar_bloco, decifrar, decifrar_bloco


class TestDES(unittest.TestCase):
    def test_vetor_conhecido(self):
        chave = bytes.fromhex("133457799BBCDFF1")
        claro = bytes.fromhex("0123456789ABCDEF")
        cifrado = bytes.fromhex("85E813540F0AB405")
        self.assertEqual(cifrar_bloco(claro, chave), cifrado)
        self.assertEqual(decifrar_bloco(cifrado, chave), claro)

    def test_ida_e_volta_cbc(self):
        chave = bytes.fromhex("133457799BBCDFF1")
        for tamanho in (0, 1, 7, 8, 9, 1000):
            mensagem = bytes((indice % 256 for indice in range(tamanho)))
            self.assertEqual(decifrar(cifrar(mensagem, chave), chave), mensagem)

    def test_cifragem_usa_iv_aleatorio(self):
        chave = bytes.fromhex("133457799BBCDFF1")
        primeira = cifrar(b"documento confidencial", chave)
        segunda = cifrar(b"documento confidencial", chave)
        self.assertNotEqual(primeira, segunda)

    def test_rejeita_bloco_e_chave_invalidos(self):
        with self.assertRaises(ValueError):
            cifrar_bloco(b"curto", bytes(8))
        with self.assertRaises(ValueError):
            cifrar_bloco(bytes(8), bytes(7))

    def test_rejeita_cifrado_truncado(self):
        with self.assertRaises(ValueError):
            decifrar(bytes(8), bytes(8))


if __name__ == "__main__":
    unittest.main(verbosity=2)