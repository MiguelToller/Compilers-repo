# Análise Sintática: Declaração e Inicialização de Variáveis

Este exercício implementa a análise léxica e sintática para declaração de variáveis com inicialização opcional em C, gerando a tabela de símbolos em CSV e validando as sentenças linha a linha.

---

## 1. Enunciado

> A partir da sintaxe original de declaração de variável abaixo, criar uma **NOVA SINTAXE** para declaração **COM inicialização de variável**.

### Sintaxe Original (Sem Inicialização)
```text
[TIPO] -> PR:INT | PR:CHAR | PR:FLOAT | PR:DOUBLE | PR:VOID | PR:BOOLEAN
Declara -> [TIPO][NOMEVARIAVEL][PV] | [TIPO][NOMEVARIAVEL] DeclaraMultiplo [PV]
DeclaraMultiplo -> [VG][NOMEVARIAVEL] | [VG][NOMEVARIAVEL] DeclaraMultiplo
```

---

## 2. Nova Sintaxe Proposta (Com Inicialização de Variável)

Na sintaxe original, a declaração era restrita a `[NOMEVARIAVEL]`.  
Com a nova regra `DECLARADOR`, a variável pode ser declarada apenas com seu identificador ou acompanhada de um operador de atribuição e seu respectivo valor inicial:

```text
[TIPO]           -> PR:INT | PR:CHAR | PR:FLOAT | PR:DOUBLE | PR:VOID | PR:BOOLEAN
Declara          -> [TIPO] [DECLARADOR] [PV] 
                  | [TIPO] [DECLARADOR] DeclaraMultiplo [PV]
DeclaraMultiplo  -> [VG] [DECLARADOR] 
                  | [VG] [DECLARADOR] DeclaraMultiplo

[DECLARADOR]     -> [NOMEVARIAVEL] 
                  | [NOMEVARIAVEL] [ATRIBUICAO] [VALOR]

[VALOR]          -> INTEIRO | FRACIONARIO | NOMEVARIAVEL | PR:TRUE | PR:FALSE
```

### Exemplos Válidos:
- `int x = 10;` (declaração simples com inicialização)
- `char letra;` (declaração simples sem inicialização)
- `double a = 1.5, b, c = 3.14;` (declaração múltipla com inicializações mistas)
- `boolean ativo = true;` (declaração com valor booleano)

---

## 3. Estrutura dos Arquivos

- [`analisador_sintatico.py`](file:///c:/Users/laboratorio/Desktop/Compilers-repo/analise_sintatica/analisador_sintatico.py): Script principal contendo a tokenização, classificação dos lexemas, reconhecimento da regra `Declara` / `DeclaraMultiplo` com `DECLARADOR` e exportação da tabela de símbolos em CSV.
- [`input.c`](file:///c:/Users/laboratorio/Desktop/Compilers-repo/analise_sintatica/input.c): Arquivo de entrada contendo exemplos válidos e linhas com erros sintáticos intencionais.
- [`tabela_simbolos.csv`](file:///c:/Users/laboratorio/Desktop/Compilers-repo/analise_sintatica/tabela_simbolos.csv): Tabela de símbolos exportada após a análise.

---

## 4. Como Executar

Dentro da pasta `analise_sintatica`:
```bash
python analisador_sintatico.py
```

Ou a partir da raiz do repositório:
```bash
python analise_sintatica/analisador_sintatico.py
```

---

## 5. Exemplo de Saída

```text
Linha 1: int x = 10;
  [ACEITO] 'int' -> PR:INT (linha 1, coluna 1)
  [ACEITO] 'x' -> NOMEVARIAVEL (linha 1, coluna 5)
  [ACEITO] '=' -> ATRIBUICAO (linha 1, coluna 7)
  [ACEITO] '10' -> INTEIRO (linha 1, coluna 9)
  [ACEITO] ';' -> PONTO_VIRGULA (linha 1, coluna 11)
  [DECLARACAO ACEITA - DECLARA]
  Tipo: PR:INT
  Declaradores: x = 10
  Mensagem: Declaração aceita com 1 variável(is) e 1 inicialização(ões).

Linha 4: double a = 1.5, b, c = 3.14;
  [ACEITO] 'double' -> PR:DOUBLE (linha 4, coluna 1)
  [ACEITO] 'a' -> NOMEVARIAVEL (linha 4, coluna 8)
  [ACEITO] '=' -> ATRIBUICAO (linha 4, coluna 10)
  [ACEITO] '1.5' -> FRACIONARIO (linha 4, coluna 12)
  [ACEITO] ',' -> VIRGULA (linha 4, coluna 15)
  [ACEITO] 'b' -> NOMEVARIAVEL (linha 4, coluna 17)
  [ACEITO] ',' -> VIRGULA (linha 4, coluna 18)
  [ACEITO] 'c' -> NOMEVARIAVEL (linha 4, coluna 20)
  [ACEITO] '=' -> ATRIBUICAO (linha 4, coluna 22)
  [ACEITO] '3.14' -> FRACIONARIO (linha 4, coluna 24)
  [ACEITO] ';' -> PONTO_VIRGULA (linha 4, coluna 28)
  [DECLARACAO ACEITA - DECLARA_MULTIPLO]
  Tipo: PR:DOUBLE
  Declaradores: a = 1.5, b, c = 3.14
  Mensagem: Declaração aceita com 3 variável(is) e 2 inicialização(ões).

Linha 7: int erro_atribuicao = ;
  [ACEITO] 'int' -> PR:INT (linha 7, coluna 1)
  [ACEITO] 'erro_atribuicao' -> NOMEVARIAVEL (linha 7, coluna 5)
  [ACEITO] '=' -> ATRIBUICAO (linha 7, coluna 21)
  [ACEITO] ';' -> PONTO_VIRGULA (linha 7, coluna 23)
  [DECLARACAO REJEITADA - DECLARA]
  Tipo: PR:INT
  Mensagem: Era esperado VALOR depois de '=' para 'erro_atribuicao', mas foi encontrado ';'.
```
