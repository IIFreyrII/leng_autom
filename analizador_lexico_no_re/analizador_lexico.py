# Línea de código que será analizada
codigo = """X = 5 + 3
asa"""

operadores = {
    '=':  'OP_IGUAL',
    '+':  'OP_SUMA',
    '-':  'OP_RESTA',
    '*':  'OP_MULT',
    '/':  'OP_DIV',
    '^':  'OP_POT',
    '\\': 'OP_RAIZ',
    '(':  'PAR_ABRE',
    ')':  'PAR_CIERRA',
}

def analizar(codigo):
    tokens = []
    linea = 1
    columna = 1
    pos = 0

    while pos < len(codigo):
        caracter = codigo[pos]

        if caracter in (' ', '\t'):
            # Espacio
            pos += 1
            columna += 1

        elif caracter == '#':
            # Comentario
            pos = len(codigo)

        elif caracter.isalpha():
            # Identificador
            tokens.append({'Type': 'ID', 'Value': caracter, 'Line': linea, 'Col': columna})
            pos += 1
            columna += 1

        elif caracter.isdigit():
            # Número
            tokens.append({'Type': 'NUM', 'Value': caracter, 'Line': linea, 'Col': columna})
            pos += 1
            columna += 1

        elif caracter in operadores:
            tokens.append({'Type': operadores[caracter], 'Value': caracter, 'Line': linea, 'Col': columna})
            pos += 1
            columna += 1

    tokens.append({'Type': 'EOF', 'Value': None, 'Line': linea, 'Col': columna})
    return tokens

if __name__ == '__main__':
    resultado = analizar(codigo)
    for token in resultado:
        print(token)