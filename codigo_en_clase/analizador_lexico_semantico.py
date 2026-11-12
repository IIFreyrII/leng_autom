import re
# ==================
# Analizador Léxico
# ==================
PATRON = re.compile(
    r"(?P<ESPACIO>\s+)"
    r"|(?P<NUMERO>\d+(?:\.\d+)?)"
    r"|(?P<IDENTIFICADOR>[a-zA-Z_]\w*)"
    r"|(?P<OPERADOR>[=+\-*/()])"
)

def analizar_lexico(codigo):
    tokens=[]
    posicion = 0

    while posicion < len(codigo):
        coincidencia = PATRON.match(codigo, posicion)
        if not coincidencia:
            raise SyntaxError(
                f"Símbolo incorrecto en la posición {posicion}: "
                f"{codigo[posicion]!r}"
            )
        tipo = coincidencia.lastgroup
        valor = coincidencia.group()

        if tipo != "ESPACIO":
            tokens.append((tipo,valor))

        posicion = coincidencia.end()
    tokens.append(("EOF",""))
    return tokens

# ======================
# Analizador Sintáctico
# ======================

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def actual(self):
        return self.tokens[self.posicion]

    def aceptar(self, valor):
        if self.actual()[1] == valor:
            token = self.actual()
            self.posicion += 1
            return token
        return None

    # Si devuelve un None, significa que no está definido el token

    def esperar(self, valor):
        token = self.aceptar(valor)
        if token is None:
            encontrado = self.actual()[1] or "FIN"
            raise SyntaxError(
                f"Se esperaba {valor!r}, "
                f"pero se encontró {encontrado!r}"
            )
        return token

    def esperar_tipo(self, tipo):
        if self.actual()[0] != tipo:
            encontrado = self.actual()[1] or "FIN"
            raise SyntaxError(
                f"Se esperaba {tipo}, "
                f"pero se encontró {encontrado!r}"
            )

        token = self.actual()
        self.posicion += 1
        return token

    def analizar(self):
        arbol = self.asignacion()

        if self.actual()[0] != "EOF":
            encontrado = self.actual()[1]
            raise SyntaxError(
                f"Token inesperado al final: {encontrado!r}"
            )
        return arbol

    def asignacion(self):
        nombre = self.esperar_tipo("IDENTIFICADOR")[1]
        self.esperar("=")
        expresion = self.expresion()
        return("ASIGNACION",nombre,expresion)

    def expresion(self):
        nodo = self.termino()

        while self.actual()[1] in ("+", "-"):
            operador = self.actual()[1]
            self.posicion += 1

            derecho = self.termino()

            nodo = ("OPERACION", operador, nodo, derecho)

        return nodo

    def termino(self):
        nodo = self.factor()

        while self.actual()[1] in ("*", "/"):
            operador = self.actual()[1]
            self.posicion += 1
            derecho = self.factor()
            nodo = ("OPERACION", operador, nodo, derecho)
        return nodo
    def factor(self):
        tipo, valor = self.actual()

        if tipo == "NUMERO":
            self.posicion += 1
            return ("NUMERO", valor)

        if tipo == "IDENTIFICADOR":
            self.posicion += 1
            return("VARIABLE", valor)

        if self.aceptar("("):
            nodo = self.expresion()
            self.esperar(")")
            return nodo
        encontrado = valor or "FIN DE ENTRADA"

        raise SyntaxError(
            "Se esperaba un número, una variable "
            f"o un paréntesis de apertura; se encontró {encontrado!r}"
        )

def mostrar_arbol(nodo, prefijo="", ultimo=True):
    conector = "|_ " if ultimo else "|-"

    if nodo[0] == "ASIGNACION":
        print(prefijo + conector + "ASIGNACION")
        nuevo_prefijo = prefijo + ("   " if ultimo else "| ")
        print(nuevo_prefijo + "|- VARIABLE: " + nodo[1])
        print(nuevo_prefijo + "|_ EXPRESIÓN")
        mostrar_arbol(
            nodo[2],
            nuevo_prefijo + "  ",
            True
        )
    elif nodo[0] == "OPERACION":
        print(prefijo + conector + "OPERADOR: " + nodo[1])
        nuevo_prefijo = prefijo + ("   " if ultimo else "| ")

        mostrar_arbol(nodo[2], nuevo_prefijo, False)
        mostrar_arbol(nodo[3], nuevo_prefijo, True)

    elif nodo[0] == "NUMERO":
        print(prefijo + conector + "NUMERO: " + nodo[1])

    elif nodo[0] == "VARIABLE":
        print(prefijo + conector + "VARIABLE: " + nodo[1])

if __name__ == "__main__":
    print("ANALIZADOR SINTÁCTICO")
    print()

    codigo = input("Escribe una igualación: ")

    try:
        tokens = analizar_lexico(codigo)
        print("\nTOKENS: ")
        for tipo, valor in tokens:
            if tipo != "EOF":
                print(f"{tipo} : {valor}")

        analizador = AnalizadorSintactico(tokens)
        arbol = analizador.analizar()

        print("\nSintaxis Correcta")
        print("\nÁRBOL SINTÁCTICO:")
        mostrar_arbol(arbol)
    except SyntaxError as error:
        print("\nERROR SINTÁCTICO")
        print(error)