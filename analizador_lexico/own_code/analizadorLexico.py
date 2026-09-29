import re
import json

# ------------- Definimos diccionario y archivos -----------

# Diccionario de tokens con regex
tokens = {
    'ESPACIO':      '[ \t]+',               #Así se especifican espaciones según la documentación de Python, el + es para que acepte 1 o más veces
    'SALTO_LINEA':  '[ \n]+',               #Así se especifican saltos de línea según la documentación de Python, el + es para que acepte 1 o más veces
    'COMENTARIO':    '#.*',                 #El punto es para que acepte cualquier caracter, y el asterisco es para que acepte 0 o más veces después del sharp
    'ID':         r'[a-zA-Z]1[\w]*',
    'NUM':        r'[\d]+',
    'OP_EQUAL':   '=',
    'OP_ADD':     '[+]',
    'OP_SUB':     '-',
    'OP_MULT':    '[*]',
    'OP_DIV':     '/',
    'OP_POT':     r'\^',
    'OP_ROOT':    r'\\',
    'PAR_OPEN':   '[(]',
    'PAR_CLOSE':  '[)]',
}

leer_archivo = "analizar.txt"
escribir_archivo = "resultado.json"

# --------------- Terminamos de declarar ------------------

def conversion_tokens (num_linea: int, cont_linea: str):
    print()

# def write_file():
#     with open(escribir_archivo, "w") as archivo_json:
#
#
#         json.dump(tokens, archivo_json, indent=2)

def read_file():
    try:
        with open(leer_archivo, "r") as archivo_txt:
                print(f"La salida se encuentra en el archivo: {escribir_archivo}")
                for numero_linea, contenido_linea in enumerate (archivo_txt, start=1):
                    conversion_tokens(numero_linea, contenido_linea)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo: {leer_archivo}.")
        return

if __name__ == '__main__':
    # write_file()
    # read_file()
    print('Hello world')