import io
import tokenize

def string_esta_isolada(indice_atual: int, tokens: list) -> bool:
    """Verifica se uma string está solta (agindo como comentário) ou se faz parte do código."""
    # Olha para os tokens anteriores de trás para frente
    for i in range(indice_atual - 1, -1, -1):
        tipo = tokens[i].type
        
        # Ignora quebras de linha puramente visuais e outros comentários
        if tipo in (tokenize.NL, tokenize.COMMENT):
            continue
            
        # Se o que veio antes foi o começo de uma nova linha ou indentação, ela está isolada
        if tipo in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING):
            return True
            
        # Se encontrou um '=', 'return', '(', etc., ela faz parte do código (ex: x = "texto")
        return False
        
    return True


def apagar_token_do_texto(tok, linhas: list):
    """Apaga o trecho de texto de um token sem bagunçar as outras linhas do arquivo."""
    lin_inicio, col_inicio = tok.start
    lin_fim, col_fim = tok.end
    
    # Ajusta para base 0 (listas em Python começam no índice 0)
    i_inicio, i_fim = lin_inicio - 1, lin_fim - 1
    
    # Se for um comentário de uma linha só
    if i_inicio == i_fim:
        linhas[i_inicio] = linhas[i_inicio][:col_inicio] + linhas[i_inicio][col_fim:]
    
    # Se for um comentário de VÁRIAS linhas (docstrings)
    else:
        linhas[i_inicio] = linhas[i_inicio][:col_inicio] + "\n"
        for i in range(i_inicio + 1, i_fim):
            linhas[i] = "\n"  # Esvazia a linha inteira, deixando apenas a quebra
        linhas[i_fim] = linhas[i_fim][col_fim:]


def limpar_codigo(codigo_fonte: str) -> str:
    """Função principal: recebe o código original e devolve o código limpo."""
    linhas = codigo_fonte.splitlines(keepends=True)
    
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(codigo_fonte).readline))
    except tokenize.TokenError:
        return codigo_fonte  # Retorna original se houver erro grave de sintaxe

    tokens_para_apagar = []

    # 1. Identifica o que precisa ser apagado
    for i, tok in enumerate(tokens):
        if tok.type == tokenize.COMMENT:
            tokens_para_apagar.append(tok)
        elif tok.type == tokenize.STRING and string_esta_isolada(i, tokens):
            tokens_para_apagar.append(tok)

    # 2. Apaga de trás para frente (para não desalinhar os cortes)
    for tok in reversed(tokens_para_apagar):
        apagar_token_do_texto(tok, linhas)

    return "".join(linhas)


# --- Exemplo de Teste ---
if __name__ == "__main__":
    codigo = '''"""
Este é um comentário multilinha
"""
def somar(a, b):
    # Retorna a soma
    resultado = a + b  # Soma os valores
    url = "http://site.com/#ancora"
    return resultado
'''
    print(limpar_codigo(codigo))