# Resumo: Aula 1 - Introdução aos Compiladores

## 1. Visão Geral
- **Fluxo Básico:** `Código Fonte` ➔ `Compilador` ➔ `Código Executável`
- **Definição:** O compilador é um programa responsável por traduzir um código escrito em linguagem de alto nível (legível para o programador) para uma linguagem de baixo nível ou de máquina (executável pelo computador).

## 2. Tradutores: Direto x Indireto
A principal diferença entre os modelos está na **dependência de contexto** e na complexidade da análise antes da tradução.

- **Tradutor Direto:**
  - Pega o conteúdo de entrada e traduz item por item, mantendo a ordem para a saída.
  - **Não depende de contexto.** O significado de um elemento não muda de acordo com os elementos ao redor.
  - *Aplicação:* Sistemas simples de mapeamento um-para-um (como conversores de base ou cifras básicas).

- **Tradutor Indireto:**
  - **Depende de contexto.** O código precisa ser analisado como um todo (sintaxe e semântica).
  - Geralmente cria uma representação intermediária (como uma Árvore de Sintaxe Abstrata) antes de gerar o código final.
  - Permite reordenar instruções, aplicar otimizações e detectar erros complexos de lógica estrutural.
  - *Aplicação:* Compiladores modernos de linguagens (C, C++, etc).

## 3. Compilação Just-in-Time (JIT)
- **Exemplo Clássico:** Java (através da JVM - Java Virtual Machine).
- **Como funciona:** É uma abordagem híbrida. O compilador tradicional primeiro converte o código-fonte em um código intermediário chamado **Bytecode** (independente de plataforma).
- Em tempo de execução, o compilador JIT atua traduzindo esse *bytecode* para a linguagem de máquina nativa do sistema operacional hospedeiro, apenas no momento em que os blocos de código são necessários ("just in time"). Ele também otimiza partes do código que são executadas com mais frequência.

---