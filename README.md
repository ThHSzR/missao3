# Missão 3 — SecureDocs: criptografia simétrica

Implementações didáticas de **DES**, **RC5** e **AES**, acompanhadas de testes e de uma demonstração de cifragem e recuperação de arquivo com AES. O projeto responde à Missão 3 do enunciado *SecureDocs — Como proteger documentos confidenciais em um ambiente digital hostil?*: após a cópia de arquivos protegidos por cifras clássicas, é necessário comparar alternativas atuais e explicar também como entregar a chave ao destinatário.

> **Estado da implementação:** o experimento disponível usa **AES-256-CBC**. A recomendação para uma evolução do SecureDocs é **AES-256-GCM**, mas **GCM e a entrega segura da chave ainda não estão implementados neste repositório**. A demonstração atual salva a chave em texto claro em um arquivo `.key`; portanto, não deve ser usada com documentos ou chaves reais.

## Entregas e estado atual

| Requisito da missão | Evidência na `main` | Estado |
|---|---|---|
| Implementar DES | `des.py`, `testes_des.py` | Implementação e testes presentes |
| Implementar RC5 | `rc5.py`, `teste_rc5.py`, `teste_arquivo.py` | Implementação e demonstrações presentes |
| Implementar AES | `aes.py`, `testes_aes.py` | Implementação e testes presentes |
| Cifrar e recuperar um arquivo com AES | `experimento_arquivos.py`, `contrato.pdf` | Demonstração funcional em AES-256-CBC |
| Comparar os três algoritmos e justificar a escolha | Seções de comparação e decisão deste README | Documentação presente |
| Explicar como entregar a chave secreta | Seção “Entrega da chave” deste README | Proposta conceitual; não implementada |
| Resumo detalhado separado e apresentação de 10 minutos | Não há arquivos próprios desses produtos na `main` | Ainda não identificados no repositório |

**Atribuição observável nos commits:** Nicole adicionou DES; Marini, RC5; Guilherme, AES; Mateus, o experimento de arquivos. Este README reúne a comparação e a decisão atribuídas a Thiago. A presença dos arquivos confirma as contribuições na `main`, mas não confirma a entrega de slides ou de um resumo separado.

## Requisitos e execução

- Python 3. Nenhuma dependência externa é importada pelos scripts versionados.
- Execute os comandos a partir da raiz do repositório.
- Os scripts de demonstração escrevem arquivos de saída no diretório atual; prefira uma cópia de trabalho para executá-los.

```bash
python3 -m unittest testes_des testes_aes -v
python3 teste_rc5.py
python3 teste_arquivo.py
python3 experimento_arquivos.py
```

`experimento_arquivos.py`, sem argumentos, cifra `contrato.pdf` e o recupera automaticamente, comparando SHA-256 do original com o recuperado. Se esse PDF estiver ausente, o script cria um documento fictício de teste. Para selecionar outro arquivo:

```bash
python3 experimento_arquivos.py cifrar arquivo.txt
python3 experimento_arquivos.py decifrar arquivo.txt.aes arquivo.txt.key
```

A cifragem cria `arquivo.txt.aes` e `arquivo.txt.key`; a decifragem cria `arquivo_recuperado.txt`. O hash SHA-256 exibido na demonstração permite **comparar os dois arquivos no teste local**. Ele não autentica o arquivo cifrado nem substitui uma assinatura ou um código de autenticação.

## Como cada implementação funciona

### DES — `des.py`

Cifra blocos de 64 bits mediante permutação inicial, geração de 16 subchaves, 16 rodadas Feistel com expansão, S-boxes e permutação, e permutação final. A chave de entrada tem 64 bits, dos quais 56 são efetivos no DES. `cifrar_bloco` e `decifrar_bloco` operam em um bloco de 8 bytes; `cifrar` e `decifrar` aplicam CBC com IV aleatório e preenchimento no estilo PKCS#7. O resultado de `cifrar` é `IV || blocos_cifrados`. `testes_des.py` verifica um vetor conhecido, ida e volta, IV variável e algumas entradas inválidas.

DES está no projeto para estudo e comparação. Seu padrão foi retirado pelo NIST em 2005 por não oferecer segurança suficiente para novos usos.

### RC5 — `rc5.py`

A classe `RC5` usa palavras de 32 bits, blocos de 64 bits e, por padrão, 12 rodadas; o tamanho da chave é `len(key)` bytes. A expansão de chave produz as subchaves; as rodadas combinam soma modular, XOR e rotações dependentes dos dados. `encrypt_block`/`decrypt_block` tratam um bloco de 8 bytes; `encrypt_file`/`decrypt_file` tratam um arquivo com preenchimento no estilo PKCS#7.

**Limitação:** o método de arquivo cifra cada bloco de forma independente, sem IV e sem autenticação; padrões em blocos iguais podem permanecer visíveis. `teste_rc5.py` verifica uma ida e volta e um vetor conhecido; `teste_arquivo.py` verifica a recuperação de `arquivo.txt`. A configuração descrita é a que está no código: RC5 em geral admite outros parâmetros.

### AES — `aes.py`

Implementa a cifra de bloco AES com S-box, expansão de chave, `SubBytes`, `ShiftRows`, `MixColumns` e `AddRoundKey`, além das transformações inversas. As rotinas de bloco aceitam chaves de 16, 24 ou 32 bytes; `cifrar` e `decifrar` usam CBC, IV aleatório de 16 bytes e preenchimento no estilo PKCS#7, com saída `IV || blocos_cifrados`. No experimento, `experimento_arquivos.py` gera uma chave de **32 bytes (AES-256)** por arquivo.

`testes_aes.py` contém vetores de bloco para AES-128, AES-192 e AES-256 e testes de ida e volta. A API de decifragem atual não autentica o conteúdo, não valida completamente o preenchimento e não garante a detecção de alterações ou chave errada. Uma falha de preenchimento, quando ocorre, não constitui prova de integridade.

## Comparação e decisão para o SecureDocs

| Critério | DES | RC5 nesta implementação | AES nesta implementação |
|---|---|---|---|
| Bloco | 64 bits | 64 bits (duas palavras de 32) | 128 bits |
| Chave | 56 bits efetivos | Comprimento variável; exemplo dos testes: 16 bytes | 128, 192 ou 256 bits; experimento: 256 bits |
| Rodadas | 16 | 12 por padrão | 10, 12 ou 14 conforme a chave |
| Uso de arquivo no código | CBC com IV | Blocos independentes | CBC com IV |
| Emprego proposto | Apenas didático | Apenas didático | Base da solução, após acrescentar autenticação e gestão segura de chaves |

**Decisão de projeto:** recomendar AES-256-GCM para proteger documentos na evolução do SecureDocs. AES possui especificação padronizada; GCM acrescenta autenticação ao processo de cifragem, permitindo rejeitar arquivos alterados quando o modo for implementado corretamente. Isso é uma **proposta**, distinta do AES-256-CBC que o código já demonstra. DES não é adequado para novos arquivos; RC5 exige escolhas de parâmetros e, neste projeto, o modo de arquivo não fornece as propriedades necessárias. As implementações locais são educativas e não foram auditadas para produção.

## Entrega da chave ao destinatário

A chave simétrica usada para cifrar o documento precisa chegar somente ao destinatário autorizado. Como **proposta conceitual**, o sistema deve obter e autenticar a chave pública do destinatário; usar um esquema de transporte de chave adequado, como RSA-OAEP, para proteger a chave aleatória de AES; e permitir que apenas a chave privada correspondente a recupere. O arquivo cifrado pode então ser enviado junto do material de transporte da chave. O sistema também precisaria definir identidade, gestão e proteção das chaves privadas, formato dos dados e tratamento de erros.

**Isso ainda não acontece no código:** `experimento_arquivos.py` escreve a chave hexadecimal diretamente em `*.key`, ao lado do arquivo cifrado. Quem obtiver ambos poderá decifrar o arquivo. Nunca publique o `.key` de uma demonstração com dados reais.

## Limitações e próximos passos

1. Implementar cifragem autenticada para os arquivos, preferencialmente AES-GCM, com armazenamento correto do nonce e da tag, e teste de rejeição após adulteração.
2. Implementar a entrega segura da chave e autenticar a chave pública do destinatário; retirar o `.key` em texto claro do fluxo final.
3. Validar rigorosamente chaves, IV, comprimento do texto cifrado e preenchimento nas APIs públicas de AES; os testes atuais não cobrem esses casos por completo.
4. Preparar o resumo formal separado e os slides de 10 minutos com evidências das execuções reais, se esses produtos forem entregues pelo repositório.

## Referências

- Enunciado da disciplina: `3_M_PBL_simetrica.pdf` (fornecido pelo professor; não versionado neste repositório).
- [NIST FIPS 46-3 — DES (retirado)](https://csrc.nist.gov/pubs/fips/46-3/final).
- [NIST — retirada do DES](https://csrc.nist.gov/news/2005/withdrawal-of-fips-46-3-fips-74-and-fips-81).
- [Ronald Rivest — The RC5 Encryption Algorithm](https://people.csail.mit.edu/rivest/pubs/pubs/Riv94.pdf).
- [NIST FIPS 197 — AES](https://csrc.nist.gov/pubs/fips/197/final).
- [NIST SP 800-38A — modos de confidencialidade, incluindo CBC](https://csrc.nist.gov/pubs/sp/800/38/a/final).
- [NIST SP 800-38D — GCM](https://csrc.nist.gov/pubs/sp/800/38/d/final).
- [NIST SP 800-56B Rev. 2 — estabelecimento e transporte de chaves com RSA](https://csrc.nist.gov/pubs/sp/800/56/b/r2/final).
