# Integrantes del equipo:
# Freyre Can Bryan Paul
# Silva Colli Odalys Margely
# Borges Gonzalez Jose Manuel
# Camas Pool Jesús Emilio

import re

# ==================
# Analizador Léxico
# ==================

PATRON = re.compile(
    r"(?P<ESPACIO>\s+)"
    r"|(?P<COMENTARIO_MULTI>/\*[\s\S]*?\*/)"
    r"|(?P<COMENTARIO_LINEA>#.*)"
    r"|(?P<NUMERO>\d+(?:\.\d+)?)"
    r"|(?P<IDENTIFICADOR>[a-zA-Z]\w*)"
    r"|(?P<OPERADOR>[=+\-*/^\\()])"
)

def analizar_lexico(codigo):
    tokens = []
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

        if tipo not in ("ESPACIO", "COMENTARIO_LINEA", "COMENTARIO_MULTI"):
            tokens.append((tipo, valor))

        posicion = coincidencia.end()
    tokens.append(("EOF", ""))
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
        return ("ASIGNACION", nombre, expresion)

    def expresion(self):
        nodo = self.termino()

        while self.actual()[1] in ("+", "-"):
            operador = self.actual()[1]
            self.posicion += 1
            derecho = self.termino()
            nodo = ("OPERACION", operador, nodo, derecho)

        return nodo

    def termino(self):
        nodo = self.potencia()

        while self.actual()[1] in ("*", "/"):
            operador = self.actual()[1]
            self.posicion += 1
            derecho = self.potencia()
            nodo = ("OPERACION", operador, nodo, derecho)
        return nodo

    def potencia(self):
        nodo = self.factor()

        while self.actual()[1] in ("^", "\\"):
            operador = self.actual()[1]
            self.posicion += 1
            derecho = self.factor()
            nodo = ("OPERACION", operador, nodo, derecho)
        return nodo

    def factor(self):
        tipo, valor = self.actual()

        if self.aceptar("-"):
            nodo = self.factor()
            return ("OPERACION", "*", ("NUMERO", "-1"), nodo)

        if tipo == "NUMERO":
            self.posicion += 1
            return ("NUMERO", valor)

        if tipo == "IDENTIFICADOR":
            self.posicion += 1
            return ("VARIABLE", valor)

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

# ======================
# Analizador Semántico
# ======================

class AnalizadorSemantico:
    def __init__(self, tabla_simbolos):
        self.tabla_simbolos = tabla_simbolos

    def analizar(self, nodo):
        tipo = nodo[0]

        if tipo == "ASIGNACION":
            variable = nodo[1]
            self.analizar(nodo[2])
            self.tabla_simbolos.add(variable)

        elif tipo == "OPERACION":
            self.analizar(nodo[2])
            self.analizar(nodo[3])

        elif tipo == "NUMERO":
            pass

        elif tipo == "VARIABLE":
            variable = nodo[1]
            if variable not in self.tabla_simbolos:
                raise NameError(f"Error Semántico, la variable {variable} no ha sido declarada")

# ===========================
# Generador código intermedio
# ===========================

class GeneradorCodigoIntermedio:
    def __init__(self):
        self.cuadruplos = []
        self.contador_temp = 0

    def nueva_temporal(self):
        self.contador_temp += 1
        return f"{self.contador_temp}"

    def generar(self, nodo):
        tipo = nodo[0]

        if tipo == "NUMERO":
            return nodo[1]
        elif tipo == "VARIABLE":
            return nodo[1]
        elif tipo == "OPERACION":
            op = nodo[1]
            izq = self.generar(nodo[2])
            der = self.generar(nodo[3])
            temp = self.nueva_temporal()
            self.cuadruplos.append((op, izq, der, temp))
            return temp
        elif tipo == "ASIGNACION":
            variable = nodo[1]
            origen = self.generar(nodo[2])
            self.cuadruplos.append(("=", origen, "-", variable))

# ======================
# Evaluador / Interprete
# ======================

class Evaluador:
    def __init__(self, memoria):
        self.memoria = memoria

    def evaluar(self, nodo):
        tipo = nodo[0]

        if tipo == "ASIGNACION":
            variable = nodo[1]
            valor = self.evaluar(nodo[2])
            self.memoria[variable] = valor
            return valor
        elif tipo == "OPERACION":
            op = nodo[1]
            izq = self.evaluar(nodo[2])
            der = self.evaluar(nodo[3])

            if op == "+": return izq + der
            if op == "-": return izq - der
            if op == "*": return izq * der
            if op == "/":
                if der == 0:
                    raise ZeroDivisionError("Error de división entre cero")
                return izq / der
            if op == "^":
                if izq == 0 and der < 0:
                    raise ZeroDivisionError("Error de división entre cero en potencia negativa")
                return izq ** der
            if op == "\\":
                if der == 0:
                    raise ZeroDivisionError("Error: el índice de la raíz no puede ser cero")
                if izq < 0:
                    if der % 2 == 0:
                        raise ValueError("Error: no existen raíces pares de números negativos")
                    return -((-izq) ** (1 / der))
                return izq ** (1 / der)

        elif tipo == "NUMERO":
            return float(nodo[1]) if "." in nodo[1] else int(nodo[1])

        elif tipo == "VARIABLE":
            var = nodo[1]
            if var not in self.memoria:
                raise NameError(f"Variable no definida: {var!r}")
            return self.memoria[var]

def ejecutar_linea(codigo, memoria_valores):
    tokens = analizar_lexico(codigo)
    if len(tokens) == 1 and tokens[0][0] == "EOF":
        return

    print("\nTOKENS: ")
    for tipo, valor in tokens:
        if tipo != "EOF":
            print(f"{tipo} : {valor}")

    analizador = AnalizadorSintactico(tokens)
    arbol = analizador.analizar()

    print("\nSintaxis Correcta")
    print("\nÁRBOL SINTÁCTICO:")
    mostrar_arbol(arbol)

    # Validación Semántica
    semantico = AnalizadorSemantico(set(memoria_valores))
    semantico.analizar(arbol)

    # Generación de cuádruplos
    gen_inter = GeneradorCodigoIntermedio()
    gen_inter.generar(arbol)

    print("   CUADRUPLOS   ")
    for idx, cuad in enumerate(gen_inter.cuadruplos, 1):
        print(f"    {idx}. {cuad}")

    # Ejecutamos el evaluador
    evaluador = Evaluador(memoria_valores)
    resultado = evaluador.evaluar(arbol)
    print("\nRESULTADO DE LA OPERACIÓN:")
    print(f"Valor calculado: {resultado}")
    print(f"Memoria (variables): {evaluador.memoria}")

# =====================
# Ejecutamos el código
# =====================

if __name__ == "__main__":
    print("ANALIZADOR Y EVALUADOR\n")
    print("1. Modo terminal")
    print("2. Modo archivo")
    print("Escribe \"salir\" para salir\n")
    opcion = input("Selecciona una opción: ")

    memoria_valores = {}

    if opcion == "1":
        while True:
            codigo = input("\n>> ")

            if codigo.lower() == "salir":
                break

            if not codigo.strip():
                continue

            try:
                ejecutar_linea(codigo, memoria_valores)
            except (SyntaxError, NameError, ZeroDivisionError, ValueError) as error:
                print("\nERROR")
                print(error)

    elif opcion == "2":
        nombre_archivo = "analizar.txt"
        try:
            with open(nombre_archivo, "r") as archivo:
                en_comentario = False
                for numero_linea, linea in enumerate(archivo, start=1):
                    linea = linea.strip()
                    if not linea:
                        continue

                    if en_comentario:
                        if "*/" in linea:
                            linea = linea.split("*/", 1)[1].strip()
                            en_comentario = False
                            if not linea:
                                continue
                        else:
                            continue

                    if "/*" in linea and "*/" not in linea:
                        linea = linea.split("/*", 1)[0].strip()
                        en_comentario = True
                        if not linea:
                            continue

                    print(f"\n Línea {numero_linea}: {linea} ")
                    try:
                        ejecutar_linea(linea, memoria_valores)
                    except (SyntaxError, NameError, ZeroDivisionError, ValueError) as error:
                        print(f"\nError en línea : {numero_linea}")
                        print(error)

                if en_comentario:
                    print("\nError: Comentario multilínea sin cerrar")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo: {nombre_archivo}")