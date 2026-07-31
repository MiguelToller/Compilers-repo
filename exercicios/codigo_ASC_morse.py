# Dicionário de mapeamento ASCII -> Morse
ASCII_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '0': '-----'
}

def ascii_para_morse(texto):
    """
    Traduz uma string de texto ASCII para Código Morse.
    Letras são separadas por 1 espaço e palavras por ' / '.
    """
    if not texto:
        return ""

    # Converte tudo para maiúsculas para bater com as chaves do dicionário
    texto = texto.upper()
    resultado_morse = []
    
    for caractere in texto:
        if caractere == ' ':
            # Representamos espaços entre palavras com uma barra
            resultado_morse.append('/')
        elif caractere in ASCII_DICT:
            # Adiciona o código morse correspondente à letra
            resultado_morse.append(ASCII_DICT[caractere])
        else:
            # Ignora ou trata caracteres especiais não mapeados (como pontuações)
            pass 
            
    # Junta todos os símbolos e barras com um espaço simples
    return " ".join(resultado_morse)

# ==========================================
# Execução do Programa
# ==========================================
if __name__ == "__main__":
    print("=== Tradutor de ASCII para Código Morse ===")
    print("Regras:")
    print("- Digite qualquer texto alfanumérico.")
    print("- Caracteres especiais e acentos serão ignorados.")
    print("- Digite 'sair' para encerrar o programa.\n")

    while True:
        try:
            entrada = input("Digite o texto: ").strip()
            
            if entrada.lower() == 'sair':
                print("Até logo!")
                break
                
            resultado = ascii_para_morse(entrada)
            print(f"Código Morse: {resultado}\n")
            
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break