import re
import json

# Archivos de entrada y salida
leer_archivo = "analizar.txt"
escribir_archivo = "resultado.json"

# Diccionario de tokens con regex
especificacion_tokens = {
    'ESPACIO':      r'[ \t]+',
    'SALTO_LINEA':  r'[ \n]+',
    'COMENTARIO':   r'#.*',
    'ID':           r'[a-zA-Z]1[\w]*',
    'NUM':          r'[\d]+',
    'OP_EQUAL':     r'=',
    'OP_ADD':       r'[+]',
    'OP_SUB':       r'-',
    'OP_MULT':      r'[*]',
    'OP_DIV':       r'/',
    'OP_POT':       r'\^',
    'OP_ROOT':      r'\\',
    'PAR_OPEN':     r'[(]',
    'PAR_CLOSE':    r'[)]',
}

def analizar(codigo):
    tokens_lista = []
    linea = 1
    columna = 1
    pos = 0

    while pos < len(codigo):
        for tipo, patron in especificacion_tokens.items():
            coincidencia = re.match(patron, codigo[pos:])
            if coincidencia:
                valor = coincidencia.group()

                if tipo in ('ESPACIO', 'COMENTARIO', 'SALTO_LINEA'):
                    if '\n' in valor:
                        linea += valor.count('\n')
                        columna = len(valor) - valor.rfind('\n')
                    else:
                        columna += len(valor)
                else:
                    tokens_lista.append({
                        "type": tipo,
                        "value": valor,
                        "linea": linea,
                        "columna": columna
                    })
                    columna += len(valor)

                pos += len(valor)
                break
        else:
            raise SyntaxError(
                f"Carácter no reconocido {codigo[pos]!r} en línea {linea}, columna {columna}"
            )

    tokens_lista.append({"type": "EOF", "value": None, "linea": linea, "columna": columna})

    diccionario_salida = {}
    for indice, token in enumerate(tokens_lista, start=1):
        nombre_token = f"token{indice}"
        diccionario_salida[nombre_token] = token

    return diccionario_salida

def procesar_archivos():
    try:
        with open(leer_archivo, "r", encoding="utf-8") as archivo_txt:
            codigo_fuente = archivo_txt.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo '{leer_archivo}'.")
        return

    try:
        resultado = analizar(codigo_fuente)
    except SyntaxError as error:
        print(f"\nERROR LÉXICO: {error}")
        print("No se generará el archivo JSON.\n")
        return

    with open(escribir_archivo, "w", encoding="utf-8") as archivo_json:
        json.dump(resultado, archivo_json, indent=2, ensure_ascii=False)

    print(f"\nLos resultados se guardaron en '{escribir_archivo}'\n")

if __name__ == '__main__':
    procesar_archivos()