"""
Analisador Sintático e Léxico - Declaração e Inicialização de Variáveis.

Gramática Original:
    [TIPO] -> PR:INT | PR:CHAR | PR:FLOAT | PR:DOUBLE | PR:VOID | PR:BOOLEAN
    Declara -> [TIPO][NOMEVARIAVEL][PV] | [TIPO][NOMEVARIAVEL] DeclaraMultiplo [PV]
    DeclaraMultiplo -> [VG][NOMEVARIAVEL] | [VG][NOMEVARIAVEL] DeclaraMultiplo

Nova Sintaxe (Com Inicialização de Variável):
    [TIPO] -> PR:INT | PR:CHAR | PR:FLOAT | PR:DOUBLE | PR:VOID | PR:BOOLEAN
    Declara -> [TIPO] [DECLARADOR] [PV] | [TIPO] [DECLARADOR] DeclaraMultiplo [PV]
    DeclaraMultiplo -> [VG] [DECLARADOR] | [VG] [DECLARADOR] DeclaraMultiplo
    [DECLARADOR] -> [NOMEVARIAVEL] | [NOMEVARIAVEL] [ATRIBUICAO] [VALOR]
    [VALOR] -> INTEIRO | FRACIONARIO | NOMEVARIAVEL | PR:TRUE | PR:FALSE
"""

import csv
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple

# Suporte a UTF-8 no terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


TIPOS = {
    "int": "PR:INT",
    "char": "PR:CHAR",
    "float": "PR:FLOAT",
    "double": "PR:DOUBLE",
    "void": "PR:VOID",
    "boolean": "PR:BOOLEAN",
}

VALORES_BOOLEANOS = {
    "true": "PR:TRUE",
    "false": "PR:FALSE",
}

TIPOS_DE_VALOR = {
    "INTEIRO",
    "FRACIONARIO",
    "NOMEVARIAVEL",
    "PR:TRUE",
    "PR:FALSE",
}

PADRAO_TOKEN = re.compile(
    r"[+-]?(?:\d+\.\d+|\.\d+)|[+-]?\d+|"
    r"[A-Za-z_][A-Za-z0-9_]*|==|<=|>=|!=|[,;=<>!]|[^\s]"
)


@dataclass
class Token:
    """Token reconhecido, com a posição original na linha."""

    lexema: str
    tipo: str
    linha: int
    coluna: int
    aceito: bool = True


@dataclass
class Declarador:
    """Nome de variável e seu valor inicial opcional."""

    nome: str
    valor: Optional[str] = None


@dataclass
class ResultadoSintatico:
    """Resultado do reconhecimento da regra Declara."""

    aceito: bool
    tipo: Optional[str]
    declaradores: List[Declarador]
    mensagem: str


def classificar_lexema(lexema: str) -> Tuple[str, bool]:
    """Classifica um lexema nos terminais utilizados pela gramática."""
    if lexema in TIPOS:
        return TIPOS[lexema], True

    if lexema in VALORES_BOOLEANOS:
        return VALORES_BOOLEANOS[lexema], True

    if re.fullmatch(r"[+-]?\d+", lexema):
        return "INTEIRO", True

    if re.fullmatch(r"[+-]?(?:\d+\.\d+|\.\d+)", lexema):
        return "FRACIONARIO", True

    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", lexema):
        return "NOMEVARIAVEL", True

    if lexema == "=":
        return "ATRIBUICAO", True

    if lexema == ",":
        return "VIRGULA", True

    if lexema == ";":
        return "PONTO_VIRGULA", True

    return "NAO_RECONHECIDO", False


def tokenizar_linha(linha: str, numero_linha: int) -> List[Token]:
    """Tokeniza uma linha, inclusive quando `=`, `,` ou `;` estão colados."""
    tokens = []

    for correspondencia in PADRAO_TOKEN.finditer(linha):
        lexema = correspondencia.group(0)
        tipo, aceito = classificar_lexema(lexema)
        tokens.append(
            Token(
                lexema=lexema,
                tipo=tipo,
                linha=numero_linha,
                coluna=correspondencia.start() + 1,
                aceito=aceito,
            )
        )

    return tokens


def analisar_declaracao(tokens: List[Token]) -> ResultadoSintatico:
    """
    Reconhece a nova sintaxe:

        Declara -> TIPO DECLARADOR PV
                 | TIPO DECLARADOR DeclaraMultiplo PV
        DeclaraMultiplo -> VG DECLARADOR
                        | VG DECLARADOR DeclaraMultiplo

    O `DECLARADOR` possui inicialização opcional: `[NOMEVARIAVEL]` ou `[NOMEVARIAVEL] = [VALOR]`.
    """
    if not tokens:
        return ResultadoSintatico(
            aceito=False,
            tipo=None,
            declaradores=[],
            mensagem="Linha vazia.",
        )

    tipo = tokens[0].tipo
    nomes_tipos = set(TIPOS.values())

    if tipo not in nomes_tipos:
        return ResultadoSintatico(
            aceito=False,
            tipo=None,
            declaradores=[],
            mensagem=f"A linha não começa com um TIPO válido. Encontrado '{tokens[0].lexema}'.",
        )

    indice = 1
    declaradores: List[Declarador] = []

    while True:
        if indice >= len(tokens) or tokens[indice].tipo != "NOMEVARIAVEL":
            encontrado = tokens[indice].lexema if indice < len(tokens) else "fim da linha"
            return ResultadoSintatico(
                aceito=False,
                tipo=tipo,
                declaradores=declaradores,
                mensagem=(
                    "Era esperado NOMEVARIAVEL, "
                    f"mas foi encontrado '{encontrado}'."
                ),
            )

        nome = tokens[indice].lexema
        indice += 1
        valor: Optional[str] = None

        # Verificação da inicialização opcional: [ATRIBUICAO] [VALOR]
        if indice < len(tokens) and tokens[indice].tipo == "ATRIBUICAO":
            indice += 1

            if indice >= len(tokens) or tokens[indice].tipo not in TIPOS_DE_VALOR:
                encontrado = tokens[indice].lexema if indice < len(tokens) else "fim da linha"
                return ResultadoSintatico(
                    aceito=False,
                    tipo=tipo,
                    declaradores=declaradores,
                    mensagem=(
                        f"Era esperado VALOR depois de '=' para '{nome}', "
                        f"mas foi encontrado '{encontrado}'."
                    ),
                )

            valor = tokens[indice].lexema
            indice += 1

        declaradores.append(Declarador(nome=nome, valor=valor))

        if indice >= len(tokens):
            return ResultadoSintatico(
                aceito=False,
                tipo=tipo,
                declaradores=declaradores,
                mensagem="Era esperado PONTO_VIRGULA ao final da declaração.",
            )

        # Se houver vírgula, continua reconhecendo a regra DeclaraMultiplo
        if tokens[indice].tipo == "VIRGULA":
            indice += 1
            continue

        break

    if tokens[indice].tipo != "PONTO_VIRGULA":
        return ResultadoSintatico(
            aceito=False,
            tipo=tipo,
            declaradores=declaradores,
            mensagem=(
                "Era esperado PONTO_VIRGULA, "
                f"mas foi encontrado '{tokens[indice].lexema}'."
            ),
        )

    if indice != len(tokens) - 1:
        encontrado = tokens[indice + 1].lexema
        return ResultadoSintatico(
            aceito=False,
            tipo=tipo,
            declaradores=declaradores,
            mensagem=f"Token inesperado depois de PONTO_VIRGULA: '{encontrado}'.",
        )

    qtd_declaracoes = len(declaradores)
    qtd_inicializacoes = sum(item.valor is not None for item in declaradores)

    return ResultadoSintatico(
        aceito=True,
        tipo=tipo,
        declaradores=declaradores,
        mensagem=(
            f"Declaração aceita com {qtd_declaracoes} variável(is) e "
            f"{qtd_inicializacoes} inicialização(ões)."
        ),
    )


def criar_tabela_simbolos(caminho_csv: str) -> None:
    """Cria o arquivo CSV de saída da análise léxica usada pelo exercício."""
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow(
            ["ID", "token", "tipo", "linha", "coluna"]
        )


def adicionar_simbolo(caminho_csv: str, identificador: int, token: Token) -> None:
    """Adiciona um registro à tabela de símbolos em formato CSV."""
    with open(caminho_csv, "a", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow(
            [identificador, token.lexema, token.tipo, token.linha, token.coluna]
        )


def mostrar_tokens(tokens: List[Token]) -> None:
    """Exibe os tokens reconhecidos e sua classificação."""
    for token in tokens:
        status = "ACEITO" if token.aceito else "REJEITADO"
        print(
            f"  [{status}] {token.lexema!r} -> {token.tipo} "
            f"(linha {token.linha}, coluna {token.coluna})"
        )


def mostrar_declaracao(resultado: ResultadoSintatico) -> None:
    """Exibe o resultado da análise sintática de uma declaração."""
    status = "ACEITA" if resultado.aceito else "REJEITADA"
    categoria = "DECLARA_MULTIPLO" if len(resultado.declaradores) > 1 else "DECLARA"

    print(f"  [DECLARACAO {status} - {categoria}]")
    if resultado.tipo is not None:
        print(f"  Tipo: {resultado.tipo}")
    if resultado.declaradores:
        itens = [
            item.nome if item.valor is None else f"{item.nome} = {item.valor}"
            for item in resultado.declaradores
        ]
        print(f"  Declaradores: {', '.join(itens)}")
    print(f"  Mensagem: {resultado.mensagem}")


def processar_arquivo(caminho_entrada: str, caminho_csv: str) -> None:
    """Processa o arquivo-fonte, gerando a tabela de símbolos e executando a análise sintática."""
    criar_tabela_simbolos(caminho_csv)
    proximo_id = 1

    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            linha_limpa = linha.strip()
            if not linha_limpa:
                continue

            tokens = tokenizar_linha(linha, numero_linha)
            if not tokens:
                continue

            print(f"\nLinha {numero_linha}: {linha.rstrip()}")
            mostrar_tokens(tokens)

            for token in tokens:
                if token.aceito:
                    adicionar_simbolo(caminho_csv, proximo_id, token)
                    proximo_id += 1

            resultado = analisar_declaracao(tokens)
            mostrar_declaracao(resultado)


def main() -> None:
    diretorio = os.path.dirname(os.path.abspath(__file__))

    # Permite passar o caminho do arquivo por linha de comando
    if len(sys.argv) > 1:
        caminho_entrada = sys.argv[1]
    else:
        caminho_entrada = os.path.join(diretorio, "input.c")

    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")

    if not os.path.exists(caminho_entrada):
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {caminho_entrada}")

    print("=" * 65)
    print(" ANALISADOR SINTÁTICO - DECLARAÇÃO COM INICIALIZAÇÃO ")
    print("=" * 65)
    processar_arquivo(caminho_entrada, caminho_csv)
    print(f"\nTabela de símbolos salva em: {caminho_csv}")
    print("=" * 65)


if __name__ == "__main__":
    main()
