class PilaMemoria:
    """
    Simula una pila a bajo nivel (Memoria pre-asignada y Stack Pointer).
    """
    def __init__(self, tamaño):
        self.tamaño = tamaño
        # Pre-asignamos la "memoria" estática
        self.memoria = [None] * tamaño 
        # Puntero de la pila (Stack Pointer - SP). -1 significa que está vacía.
        self.tope = -1 

    def push(self, elemento):
        if self.tope >= self.tamaño - 1:
            raise OverflowError("Stack Overflow: Límite de memoria alcanzado.")
        self.tope += 1
        self.memoria[self.tope] = elemento

    def pop(self):
        if self.tope < 0: # Chequeo del tope en lugar de is_empty()
            return None
        elemento = self.memoria[self.tope]
        # En ensamblador el dato sigue en memoria, pero el puntero decrementa.
        # Simulamos eso solo moviendo el puntero.
        self.tope -= 1 
        return elemento

    def peek(self):
        if self.tope < 0:
            return None
        return self.memoria[self.tope]


class GestorOperadores:
    """
    Responsabilidad: Conocer las reglas de precedencia de los operadores. (SRP y OCP)
    """
    def __init__(self):
        self._operadores = {'+': 1, '-': 1, '*': 2, '/': 2}

    def obtener_jerarquia(self, operador):
        return self._operadores.get(operador, 0)
    
    def es_operador(self, token):
        return token in self._operadores or token in "()"


class AnalizadorLexico:
    """
    Responsabilidad: Convertir una cadena de texto cruda en tokens. (SRP)
    """
    @staticmethod
    def tokenizar(expresion):
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
    Se le inyecta el GestorOperadores cumpliendo con Inversión de Dependencias (DIP).
    """
    def __init__(self, gestor_operadores):
        self.gestor = gestor_operadores

    def infijo_a_posfijo(self, tokens, para_prefijo=False):
        # El tamaño máximo que puede alcanzar la pila es el total de tokens
        pila = PilaMemoria(len(tokens)) 
        resultado = []

        for token in tokens:
            if not self.gestor.es_operador(token): # Es un operando
                resultado.append(token)
            elif token == '(':
                pila.push(token)
            elif token == ')':
                # Usamos pila.tope > -1 para saber si hay elementos, evitando abstracciones
                while pila.tope > -1 and pila.peek() != '(':
                    resultado.append(pila.pop())
                if pila.tope > -1 and pila.peek() == '(':
                    pila.pop() # Descartamos el '('
            else: # Es un operador matemático
                while pila.tope > -1 and pila.peek() != '(':
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

        # Vaciar los operadores restantes guiándonos por el tope (Stack Pointer)
        while pila.tope > -1:
            op = pila.pop()
            if op != '(': 
                resultado.append(op)

        return resultado

    def infijo_a_prefijo(self, tokens):
        tokens_invertidos = tokens[::-1]

        # Intercambiar paréntesis
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

    # Inyección de dependencias y ensamblaje de la lógica
    gestor_ops = GestorOperadores()
    convertidor = ConvertidorExpresiones(gestor_ops)

    tokens = AnalizadorLexico.tokenizar(expresion_infija)
    posfijo = convertidor.infijo_a_posfijo(tokens)
    prefijo = convertidor.infijo_a_prefijo(tokens)

    print("\n--- RESULTADOS ---")
    print(f"1. Infijo original : {' '.join(tokens)}")
    print(f"2. Expresión Posfija: {' '.join(posfijo)}")
    print(f"3. Expresión Prefija: {' '.join(prefijo)}")

if __name__ == "__main__":
    main()