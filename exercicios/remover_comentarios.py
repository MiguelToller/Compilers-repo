import os
import io
import tokenize
import tkinter as tk
from tkinter import filedialog, messagebox

def string_esta_isolada(indice_atual: int, tokens: list) -> bool:
    """Verifica se uma string esta solta (agindo como docstring/comentario) ou se faz parte do codigo."""
    for i in range(indice_atual - 1, -1, -1):
        tipo = tokens[i].type
        if tipo in (tokenize.NL, tokenize.COMMENT):
            continue
        if tipo in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING):
            return True
        return False
    return True


def apagar_token_do_texto(tok, linhas: list):
    """Apaga o trecho de texto de um token mantendo o numero de linhas e a estrutura."""
    lin_inicio, col_inicio = tok.start
    lin_fim, col_fim = tok.end
    
    i_inicio, i_fim = lin_inicio - 1, lin_fim - 1
    
    if i_inicio == i_fim:
        linhas[i_inicio] = linhas[i_inicio][:col_inicio] + linhas[i_inicio][col_fim:]
    else:
        linhas[i_inicio] = linhas[i_inicio][:col_inicio] + "\n"
        for i in range(i_inicio + 1, i_fim):
            linhas[i] = "\n"
        linhas[i_fim] = linhas[i_fim][col_fim:]


def remover_comentarios_do_codigo(codigo_fonte: str) -> str:
    """Remove comentarios (#) e docstrings isoladas, preservando a estrutura."""
    linhas = codigo_fonte.splitlines(keepends=True)
    
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(codigo_fonte).readline))
    except tokenize.TokenError:
        return codigo_fonte

    tokens_para_apagar = []

    for i, tok in enumerate(tokens):
        if tok.type == tokenize.COMMENT:
            tokens_para_apagar.append(tok)
        elif tok.type == tokenize.STRING and string_esta_isolada(i, tokens):
            tokens_para_apagar.append(tok)

    for tok in reversed(tokens_para_apagar):
        apagar_token_do_texto(tok, linhas)

    return "".join(linhas)


def selecionar_e_processar_arquivo():
    """Abre uma janela de selecao de arquivo e processa o arquivo escolhido."""
    # Oculta a janela principal do Tkinter
    root = tk.Tk()
    root.withdraw()

    # Abre a caixa de dialogo para selecionar o arquivo
    caminho_entrada = filedialog.askopenfilename(
        title="Selecione um arquivo Python (.py)",
        filetypes=[("Arquivos Python", "*.py"), ("Todos os arquivos", "*.*")]
    )

    if not caminho_entrada:
        print("Operacao cancelada pelo usuario.")
        return

    # Gera o nome do arquivo de saida
    nome_base, ext = os.path.splitext(caminho_entrada)
    caminho_saida = f"{nome_base}_sem_comentarios{ext}"

    try:
        with open(caminho_entrada, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except UnicodeDecodeError:
        with open(caminho_entrada, "r", encoding="latin-1") as f:
            conteudo = f.read()

    # Remove os comentarios
    codigo_limpo = remover_comentarios_do_codigo(conteudo)

    # Salva o novo arquivo
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(codigo_limpo)

    # Mostra uma mensagem de sucesso na tela
    mensagem = f"Arquivo processado com sucesso!\n\nSalvo como:\n{os.path.basename(caminho_saida)}"
    messagebox.showinfo("Sucesso!", mensagem)
    print(mensagem)


if __name__ == "__main__":
    selecionar_e_processar_arquivo()