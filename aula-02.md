# Resumo: Aula 2 - Fases do Compilador e Pré-processamento

## 1. Pré-processamento (Preprocessor)
O pré-processador é a etapa que antecede a compilação propriamente dita. Ele transforma o código-fonte bruto antes que este seja analisado pelo compilador.

- **Principais Funções:**
  - **Remoção de Comentários:** Elimina comentários e espaços em branco desnecessários, mantendo a estrutura original (como a quebra de linhas para preserve a contagem e localização exata de erros).
  - **Expansão de Macros:** Substitui definições de macros pelo seu valor/código real (ex: `#define MAX 100`).
  - **Inclusão de Arquivos:** Insere o conteúdo de arquivos de cabeçalho/bibliotecas no ponto indicado (ex: `#include <stdio.h>`).
  - **Compilação Condicional:** Inclui ou exclui blocos de código com base em diretivas (ex: `#ifdef DEBUG`).

---

## 2. Fases do Compilador

O processo de compilação é dividido tradicionalmente em duas grandes fases: **Análise (Front-End)** e **Síntese (Back-End)**.

```
Código Fonte -> [ Pré-processador ]
                     ↓
┌─────────────────────────────────────────┐
│              FRONT-END                  │
├─────────────────────────────────────────┤
│  1. Análise Léxica (Scanner)            │ ➔ Gera Tokens
│  2. Análise Sintática (Parser)          │ ➔ Gera Árvore Sintática (AST)
│  3. Análise Semântica                   │ ➔ Verifica Tipos e Escopo
│  4. Geração de Código Intermediário     │ ➔ Gera Código IR (ex: 3-Endereços)
└─────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│               BACK-END                  │
├─────────────────────────────────────────┤
│  5. Otimização de Código                │ ➔ Código IR Otimizado
│  6. Geração de Código Final             │ ➔ Código de Máquina / Assembly
└─────────────────────────────────────────┘
```

### A. Análise (Front-End - Independente de Máquina)

1. **Análise Léxica (Scanner):**
   - **Função:** Lê o fluxo de caracteres do código-fonte e os agrupa em unidades significativas chamadas **tokens** (palavras-chave, identificadores, operadores, pontuação).
   - *Exemplo:* `x = a + 5` ➔ `[id:x] [op:=] [id:a] [op:+] [num:5]`

2. **Análise Sintática (Parser):**
   - **Função:** Verifica se a sequência de tokens obedece às regras gramaticais da linguagem.
   - **Saída:** Constrói uma **Árvore de Sintaxe Abstrata (AST - Abstract Syntax Tree)** que representa a estrutura hierárquica do programa.

3. **Análise Semântica:**
   - **Função:** Verifica a coerência e o significado do código (se faz sentido lógico segundo as regras da linguagem).
   - **Principais tarefas:** Checagem de tipos (*type checking*), verificação de variáveis não declaradas, compatibilidade de parâmetros em chamadas de função.

4. **Geração de Código Intermediário (IR):**
   - **Função:** Converte a AST em uma representação intermediária independente de arquitetura (ex: Código de 3 Endereços / *Three-Address Code*).
   - *Objetivo:* Facilitar a portabilidade para diferentes plataformas e otimizações.

---

### B. Síntese (Back-End - Dependente de Máquina)

5. **Otimização de Código:**
   - **Função:** Melhora o código intermediário para que o programa resultante rode mais rápido, ocupe menos memória ou consuma menos energia.
   - *Técnicas:* Eliminação de código morto (*dead code*), simplificação de expressões, otimização de laços (*loops*).

6. **Geração de Código Final:**
   - **Função:** Mapeia a representação intermediária otimizada para o código de máquina nativo da arquitetura alvo (ex: x86, ARM) ou Assembly.
   - *Atividades:* Alocação de registradores e seleção de instruções de CPU.

---

## 3. Estruturas Transversais (Suporte)

Estas estruturas atuam durante **todas** as fases do compilador:

- **Tabela de Símbolos:**
  - Estrutura de dados central que armazena informações sobre identificadores (nomes de variáveis, funções, tipos, escopos, endereços de memória).
  - É consultada e atualizada do Scanner até a Geração de Código Final.

- **Gerenciador / Tratador de Erros:**
  - Responsável por detectar, reportar mensagens claras ao desenvolvedor e tentar se recuperar de falhas em qualquer fase para continuar a análise.