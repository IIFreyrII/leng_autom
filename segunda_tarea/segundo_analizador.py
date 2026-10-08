class PilaMemoria:
    """
    Simula una pila a bajo nivel (memoria pre-asignada y Stack Pointer).
    """

    def __init__(self, capacidad):
        self._capacidad = capacidad
        # Pre-asignamos la "memoria" estática
        self._memoria = [None] * capacidad
        self._tope = -1  # Stack Pointer

    # ---------- Consultas de estado ----------
    def esta_vacia(self):
        return self._tope == -1

    def esta_llena(self):
        return self._tope == self._capacidad - 1

    # ---------- Operaciones principales ----------
    def push(self, elemento):
        if self.esta_llena():
            raise OverflowError("Stack Overflow: Límite de memoria alcanzado.")
        self._tope += 1
        self._memoria[self._tope] = elemento

    def pop(self):
        if self.esta_vacia():
            raise IndexError("Stack Underflow: La pila está vacía.")
        elemento = self._memoria[self._tope]
        self._tope -= 1
        return elemento

    def peek(self):
        if self.esta_vacia():
            raise IndexError("Stack Underflow: La pila está vacía.")
        return self._memoria[self._tope]


class GestorOperadores:
    """
    Responsabilidad: Conocer las reglas de precedencia de los operadores.
    """
    def __init__(self):
        self._operadores = {'+': 1, '-': 1, '*': 2, '/': 2}

    def obtener_jerarquia(self, operador):
        return self._operadores.get(operador, 0)

    def es_operador(self, token):
        return token in self._operadores or token in ("(", ")")


class AnalizadorLexico:
    """
    Responsabilidad: Convertir una cadena de texto cruda en tokens.
    """
    def tokenizar(self, expresion):
        tokens = []
        i = 0
        while i < len(expresion):
            c = expresion[i]

            if c.isspace():
                i += 1
                continue

            if c in "+-*/()":
                tokens.append(c)
                i += 1
            elif c.isalpha():
                token = ""
                while i < len(expresion) and expresion[i].isalpha():
                    token += expresion[i]
                    i += 1
                tokens.append(token)
            elif c.isdigit():
                token = ""
                while i < len(expresion) and expresion[i].isdigit():
                    token += expresion[i]
                    i += 1
                tokens.append(token)
            else:
                i += 1

        return tokens


class ConvertidorExpresiones:
    """
    Responsabilidad: Ejecutar el algoritmo Shunting Yard (Infijo a Posfijo/Prefijo).
    """
    def __init__(self, gestor_operadores):
        self.gestor = gestor_operadores

    def infijo_a_posfijo(self, tokens, para_prefijo=False):
        pila = PilaMemoria(len(tokens))
        resultado = []

        for token in tokens:
            if not self.gestor.es_operador(token):
                resultado.append(token)
            elif token == '(':
                pila.push(token)
            elif token == ')':
                while not pila.esta_vacia() and pila.peek() != '(':
                    resultado.append(pila.pop())
                if not pila.esta_vacia() and pila.peek() == '(':
                    pila.pop()
            else:
                while not pila.esta_vacia() and pila.peek() != '(':
                    top_op = pila.peek()
                    jerarquia_top = self.gestor.obtener_jerarquia(top_op)
                    jerarquia_token = self.gestor.obtener_jerarquia(token)

                    if para_prefijo:
                        if jerarquia_top > jerarquia_token:
                            resultado.append(pila.pop())
                        else:
                            break
                    else:
                        if jerarquia_top >= jerarquia_token:
                            resultado.append(pila.pop())
                        else:
                            break
                pila.push(token)

        while not pila.esta_vacia():
            op = pila.pop()
            if op != '(':
                resultado.append(op)

        return resultado

    def infijo_a_prefijo(self, tokens):
        tokens_invertidos = tokens[::-1]

        tokens_preparados = [
            ')' if t == '(' else '(' if t == ')' else t
            for t in tokens_invertidos
        ]

        resultado_posfijo = self.infijo_a_posfijo(tokens_preparados, para_prefijo=True)
        return resultado_posfijo[::-1]


def main():
    print("CONVERSOR DE EXPRESIONES (Orientado a objetos - Bajo Nivel)")
    expresion_infija = input("Ingresa la expresión matemática: ").strip()

    if not expresion_infija:
        print("\nError: No se ingresaron valores.")
        return

    # 1. Instanciamos todas nuestras clases de forma normal
    gestor_ops = GestorOperadores()
    analizador = AnalizadorLexico()
    convertidor = ConvertidorExpresiones(gestor_ops)

    # 2. Usamos el analizador para obtener los tokens
    tokens = analizador.tokenizar(expresion_infija)

    # 3. Convertimos
    posfijo = convertidor.infijo_a_posfijo(tokens)
    prefijo = convertidor.infijo_a_prefijo(tokens)

    print("\n--- RESULTADOS ---")
    print(f"1. Infijo original : {' '.join(tokens)}")
    print(f"2. Expresión Posfija: {' '.join(posfijo)}")
    print(f"3. Expresión Prefija: {' '.join(prefijo)}")

if __name__ == "__main__":
    main()