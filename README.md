# Missão 3 — SecureDocs: criptografia simétrica

Implementações didáticas de **DES**, **RC5** e **AES**, acompanhadas de testes e de uma demonstração de cifragem e recuperação de arquivo com AES. O projeto responde à Missão 3 do enunciado *SecureDocs — Como proteger documentos confidenciais em um ambiente digital hostil?*: após a cópia de arquivos protegidos por cifras clássicas, é necessário comparar alternativas atuais e explicar também como entregar a chave ao destinatário.

> **Estado da implementação:** a escolha demonstrada neste projeto é **AES-256-CBC**. A cifragem e a recuperação de arquivos funcionam no experimento, mas o modo CBC usado aqui não verifica a integridade nem autentica o conteúdo. A chave também é salva em texto claro em um arquivo `.key`. Esta implementação é didática e não deve ser usada com documentos ou chaves reais.

## Resumo da Missão 3

Este texto também está disponível em [PDF](docs/resumo_missao3.pdf). A [apresentação em PDF](apresentacao/TechSecure_Symmetric_Encryption_Analysis.pdf) e o [PPTX com as falas nas notas](apresentacao/TechSecure_Symmetric_Encryption_Analysis_com_falas.pptx) acompanham a entrega.

### a) Implementações de DES, RC5 e AES

**DES (`des.py`).** O código cifra blocos de 8 bytes. A chave recebida também tem 8 bytes, mas apenas 56 dos seus 64 bits são efetivos. A implementação aplica a permutação inicial, deriva 16 subchaves por meio de PC-1, rotações e PC-2, e executa 16 rodadas Feistel. A função de cada rodada expande a metade direita, combina-a com a subchave por XOR, consulta as oito S-boxes e aplica a permutação P. Após a troca final das metades, aplica a permutação final. A decifragem reutiliza a estrutura com as subchaves em ordem inversa. Para sequências de bytes, `cifrar` e `decifrar` usam CBC com IV aleatório de 8 bytes, preenchimento PKCS#7 e formato `IV || texto cifrado`. `testes_des.py` cobre um vetor conhecido, a recuperação do texto e entradas inválidas.

**RC5 (`rc5.py`).** A classe fixa palavras de 32 bits, formando blocos de 64 bits, e usa 12 rodadas por padrão. A quantidade de rodadas pode ser informada ao construtor, enquanto o comprimento da chave é o número de bytes recebidos. A expansão da chave prepara a tabela de subchaves a partir das constantes P e Q. Cada rodada combina soma módulo 2³², XOR e rotações cuja distância depende dos dados; a decifragem desfaz essas operações em ordem inversa. As rotinas de arquivo completam os dados em blocos de 8 bytes com preenchimento PKCS#7. Nessa rotina, cada bloco é cifrado separadamente, sem IV ou encadeamento: blocos iguais podem revelar padrões. `teste_rc5.py` inclui um vetor conhecido e uma ida e volta; `teste_arquivo.py` demonstra a recuperação de um arquivo. A chave de 16 bytes mostrada nos testes é apenas uma configuração do projeto.

**AES (`aes.py`).** A implementação própria opera sobre blocos de 16 bytes e aceita chaves de 16, 24 ou 32 bytes, correspondentes a AES-128, AES-192 e AES-256. Ela gera a S-box, expande a chave em subchaves de rodada e aplica `SubBytes`, `ShiftRows`, `MixColumns` e `AddRoundKey`, além das operações inversas na decifragem. Para dados com comprimento arbitrário, `cifrar` usa CBC, preenchimento PKCS#7 e um IV aleatório de 16 bytes, colocado antes do texto cifrado. `testes_aes.py` verifica vetores de bloco dos três tamanhos de chave e a ida e volta. `experimento_arquivos.py` gera uma chave aleatória de 32 bytes, cifra `contrato.pdf` por padrão, recupera o arquivo e compara o SHA-256 do original e do recuperado. Esse hash verifica a igualdade no teste local; ele não autentica o arquivo cifrado. O script grava a chave em hexadecimal, sem proteção, em `*.key`.

### b) Algoritmo escolhido para o SecureDocs

O grupo escolheu **AES** e demonstrou **AES-256-CBC** com chave aleatória de 256 bits e IV aleatório. DES, com chave efetiva de 56 bits e padrão retirado, permanece como estudo histórico. RC5 permite diferentes parâmetros, mas sua rotina de arquivo neste projeto cifra blocos independentemente e expõe padrões. O AES possui padronização vigente e, no experimento, permite cifrar e recuperar o documento. A implementação atual de CBC fornece apenas a demonstração da confidencialidade e da reversibilidade: ela não autentica o texto cifrado nem garante a detecção de alterações. Um sistema real também precisaria proteger a chave e acrescentar autenticação dos dados. Não apresentamos esta implementação didática como pronta para produção.

### c) Como entregar a chave secreta ao destinatário?

A proposta é gerar uma chave AES aleatória para cada arquivo e obter a **chave pública autenticada do destinatário**. Antes de usá-la, o sistema precisa confirmar a identidade à qual a chave pública pertence, por exemplo por um certificado validado ou outro canal de confiança. Um mecanismo de encapsulamento ou transporte apropriado, como RSA-OAEP, protege a chave AES para essa chave pública. Enviam-se o documento cifrado e a chave AES protegida; somente quem controla a chave privada correspondente consegue recuperar a chave AES e decifrar o documento. A chave privada deve permanecer protegida pelo destinatário. O código atual **não implementa esse fluxo**: salva o segredo diretamente em `*.key`, que não pode ser entregue junto do documento sem proteção. A autenticação do documento cifrado também continua pendente.

## Entregas e estado atual

| Requisito da missão | Evidência na `main` | Estado |
|---|---|---|
| Implementar DES | `des.py`, `testes_des.py` | Implementação e testes presentes |
| Implementar RC5 | `rc5.py`, `teste_rc5.py`, `teste_arquivo.py` | Implementação e demonstrações presentes |
| Implementar AES | `aes.py`, `testes_aes.py` | Implementação e testes presentes |
| Cifrar e recuperar um arquivo com AES | `experimento_arquivos.py`, `contrato.pdf` | Demonstração funcional em AES-256-CBC |
| Comparar os três algoritmos e justificar a escolha | Seções de comparação e decisão deste README | Documentação presente |
| Explicar como entregar a chave secreta | Seção “Entrega da chave” deste README | Proposta conceitual; não implementada |
| Resumo detalhado separado | `docs/resumo_missao3.pdf` e seção “Resumo da Missão 3” | Presente |
| Apresentação | `apresentacao/` (PDF e PPTX com notas) | Arquivos presentes; conferir o tempo em ensaio |

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
| Emprego no projeto | Apenas didático | Apenas didático | Algoritmo escolhido; experimento implementado em AES-256-CBC |

**Decisão da missão:** escolher **AES**, demonstrado neste repositório como **AES-256-CBC**. O AES possui especificação padronizada, e o experimento mostra a cifragem e a recuperação do arquivo com chave de 256 bits e IV aleatório. DES não é adequado para novos arquivos; RC5 exige escolhas de parâmetros e, neste projeto, cifra cada bloco de arquivo independentemente. **A implementação AES-256-CBC existente atende à demonstração de confidencialidade e recuperação, mas não autentica o arquivo cifrado.** Para atender também à integridade e à entrega segura da chave em um sistema real, são necessários mecanismos adicionais, ainda ausentes do código. As implementações são educativas e não foram auditadas para produção.

## Entrega da chave ao destinatário

A chave simétrica usada para cifrar o documento precisa chegar somente ao destinatário autorizado. Como **proposta conceitual**, o sistema deve obter e autenticar a chave pública do destinatário; usar um esquema de transporte de chave adequado, como RSA-OAEP, para proteger a chave aleatória de AES; e permitir que apenas a chave privada correspondente a recupere. O arquivo cifrado pode então ser enviado junto do material de transporte da chave. O sistema também precisaria definir identidade, gestão e proteção das chaves privadas, formato dos dados e tratamento de erros.

**Isso ainda não acontece no código:** `experimento_arquivos.py` escreve a chave hexadecimal diretamente em `*.key`, ao lado do arquivo cifrado. Quem obtiver ambos poderá decifrar o arquivo. Nunca publique o `.key` de uma demonstração com dados reais.

## Limitações e próximos passos

1. Acrescentar autenticação ao fluxo de arquivos e teste de rejeição após adulteração; o AES-256-CBC atual, sozinho, não fornece essa verificação.
2. Implementar a entrega segura da chave e autenticar a chave pública do destinatário; retirar o `.key` em texto claro do fluxo final.
3. Validar rigorosamente chaves, IV, comprimento do texto cifrado e preenchimento nas APIs públicas de AES; os testes atuais não cobrem esses casos por completo.
4. Revisar os textos visíveis da apresentação: há afirmações imprecisas nos slides 1 e 6, esclarecidas nas notas do PPTX. Ensaiar para verificar o limite de 10 minutos.

## Referências

- Enunciado da disciplina: `3_M_PBL_simetrica.pdf` (fornecido pelo professor; não versionado neste repositório).
- [NIST FIPS 46-3 — DES (retirado)](https://csrc.nist.gov/pubs/fips/46-3/final).
- [NIST — retirada do DES](https://csrc.nist.gov/news/2005/withdrawal-of-fips-46-3-fips-74-and-fips-81).
- [Ronald Rivest — The RC5 Encryption Algorithm](https://people.csail.mit.edu/rivest/pubs/pubs/Riv94.pdf).
- [NIST FIPS 197 — AES](https://csrc.nist.gov/pubs/fips/197/final).
- [NIST SP 800-38A — modos de confidencialidade, incluindo CBC](https://csrc.nist.gov/pubs/sp/800/38/a/final).
- [NIST SP 800-56B Rev. 2 — estabelecimento e transporte de chaves com RSA](https://csrc.nist.gov/pubs/sp/800/56/b/r2/final).
