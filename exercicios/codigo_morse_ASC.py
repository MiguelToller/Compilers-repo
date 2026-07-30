# Dicionário de mapeamento Morse -> ASCII
MORSE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '-----': '0'
}

def morse_para_ascii(codigo_morse):
    """
    Traduz uma string de código Morse para texto ASCII.
    Usa espaço simples para separar letras e '/' ou 3 espaços para palavras.
    """
    if not codigo_morse:
        return ""

    # Normaliza a separação de palavras para '/'
    codigo_morse = codigo_morse.replace('   ', ' / ')
    palavras_morse = codigo_morse.split(' / ')
    
    texto_traduzido = []
    
    for palavra in palavras_morse:
        letras_morse = palavra.strip().split(' ')
        palavra_traduzida = ""
        
        for letra in letras_morse:
            if letra in MORSE_DICT:
                palavra_traduzida += MORSE_DICT[letra]
            elif letra != "": 
                # Coloca uma interrogação se o código não for reconhecido
                palavra_traduzida += "?"
                
        texto_traduzido.append(palavra_traduzida)
        
    return " ".join(texto_traduzido)

# ==========================================
# Execução do Programa
# ==========================================
if __name__ == "__main__":
    print("=== Tradutor Simples de Código Morse ===")
    print("Regras:")
    print("- Separe letras com 1 espaço (ex: .... .)")
    print("- Separe palavras com '/' ou 3 espaços")
    print("- Digite 'sair' para encerrar o programa.\n")

    while True:
        try:
            entrada = input("Digite o código Morse: ").strip()
            
            if entrada.lower() == 'sair':
                print("Até logo!")
                break
                
            resultado = morse_para_ascii(entrada)
            print(f"Tradução: {resultado}\n")
            
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break