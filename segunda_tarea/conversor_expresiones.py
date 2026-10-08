class PilaMemoria:
    """
    Responsabilidad: Simular una pila de capacidad fija.
    Los atributos son privados: el exterior solo interactúa
    mediante push, pop, peek, esta_vacia y esta_llena.
    """
    def __init__(self, capacidad):
        self._capacidad = capacidad
        # Pre-asignamos la "memoria" estática
        self._memoria = [None] * capacidad
        self._tope = -1

    def esta_vacia(self):
        return self._tope == -1

    def esta_llena(self):
        return self._tope == self._capacidad - 1

    def push(self, elemento):
        if self.esta_llena():
            raise OverflowError("Stack Overflow: la pila está llena.")
        self._tope += 1
        self._memoria[self._tope] = elemento

    def pop(self):
        if self.esta_vacia():
            raise IndexError("Stack Underflow: la pila está vacía.")
        elemento = self._memoria[self._tope]
        self._tope -= 1
        return elemento

    def peek(self):
        """Consulta el elemento del tope sin sacarlo."""
        if self.esta_vacia():
            raise IndexError("La pila está vacía.")
        return self._memoria[self._tope]


class GestorOperadores:
    """
    Responsabilidad: Conocer las reglas de precedencia de los operadores.
    """
    def __init__(self):
        self._operadores = {'+': 1, '-': 1, '*': 2, '/': 2}
        self._parentesis = ('(', ')')

    def obtener_jerarquia(self, operador):
        return self._operadores.get(operador, 0)

    def es_operador(self, token):
        return token in self._operadores or token in self._parentesis


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
                if not pila.esta_vacia():
                    pila.pop()  # descarta el '('
            else:
                while not pila.esta_vacia() and pila.peek() != '(':
                    jerarquia_top = self.gestor.obtener_jerarquia(pila.peek())
                    jerarquia_token = self.gestor.obtener_jerarquia(token)

                    if para_prefijo:
                        debe_salir = jerarquia_top > jerarquia_token
                    else:
                        debe_salir = jerarquia_top >= jerarquia_token

                    if not debe_salir:
                        break
                    resultado.append(pila.pop())
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
    print("CONVERSOR DE EXPRESIONES (Orientado a objetos)")
    expresion_infija = input("Ingresa la expresión matemática: ").strip()

    if not expresion_infija:
        print("\nDebes ingresar una expresión.")
        return

    gestor_ops = GestorOperadores()
    analizador = AnalizadorLexico()
    convertidor = ConvertidorExpresiones(gestor_ops)

    tokens = analizador.tokenizar(expresion_infija)

    posfijo = convertidor.infijo_a_posfijo(tokens)
    prefijo = convertidor.infijo_a_prefijo(tokens)

    print("\n--- RESULTADOS ---")
    print(f"1. Infijo original : {' '.join(tokens)}")
    print(f"2. Expresión Posfija: {' '.join(posfijo)}")
    print(f"3. Expresión Prefija: {' '.join(prefijo)}")


if __name__ == "__main__":
    main()
