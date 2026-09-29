class Pila:
    """Clase base para el manejo de la pila requerida por el algoritmo"""
    def __init__(self):
        self.items = []

    def push(self, elemento):
        self.items.append(elemento)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0


class ConvertidorExpresiones:
    def __init__(self):
        self.operadores = {'+': 1, '-': 1, '*': 2, '/': 2}

    def obtener_jerarquia(self, operador):
        return self.operadores.get(operador, 0)

    def tokenizar(self, expresion):
        """
        Separa la expresión en operandos y operadores.
        Agrupa múltiples dígitos o letras como un solo elemento.
        Separa letras de números si vienen juntos (ej. 'djeh101' -> 'djeh', '101')
        """
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
                # Si hay caracteres extraños, los ignoramos o saltamos
                i += 1
                
        return tokens

    def infijo_a_posfijo(self, tokens, para_prefijo=False):
        """
        Convierte de infijo a posfijo aplicando las reglas de precedencia.
        El parámetro 'para_prefijo' ajusta la asociatividad al reusar el método para prefijo.
        """
        pila = Pila()
        resultado = []

        for token in tokens:
            if token.isalnum(): # Es un operando (dígitos o letras)
                resultado.append(token)
            elif token == '(':
                pila.push(token)
            elif token == ')':
                # Saca hasta encontrar apertura, maneja si hay ')' sobrantes
                while not pila.is_empty() and pila.peek() != '(':
                    resultado.append(pila.pop())
                if not pila.is_empty() and pila.peek() == '(':
                    pila.pop() # Saca el '(' y se descarta
            else: # Es un operador
                while not pila.is_empty() and pila.peek() != '(':
                    top = pila.peek()
                    # Regla de jerarquías explicada en los requerimientos
                    if para_prefijo:
                        # Para prefijo invertido, necesitamos estricta mayor jerarquía para sacar
                        if self.obtener_jerarquia(top) > self.obtener_jerarquia(token):
                            resultado.append(pila.pop())
                        else:
                            break
                    else:
                        # Para posfijo normal, mayor o igual jerarquía saca al de la pila
                        if self.obtener_jerarquia(top) >= self.obtener_jerarquia(token):
                            resultado.append(pila.pop())
                        else:
                            break
                pila.push(token)

        # Vaciar los operadores restantes en la pila
        while not pila.is_empty():
            op = pila.pop()
            if op != '(': # Si sobraron '(', simplemente no los mandamos al resultado
                resultado.append(op)

        return resultado

    def infijo_a_prefijo(self, tokens):
        """
        Convierte de infijo a prefijo reutilizando el método posfijo.
        1. Invierte la expresión.
        2. Cambia '(' por ')' y viceversa.
        3. Pasa por el algoritmo de posfijo.
        4. Invierte el resultado final.
        """
        tokens_invertidos = tokens[::-1]
        
        tokens_preparados = []
        for t in tokens_invertidos:
            if t == '(': tokens_preparados.append(')')
            elif t == ')': tokens_preparados.append('(')
            else: tokens_preparados.append(t)

        # Llamada al método posfijo dentro de prefijo
        resultado_posfijo = self.infijo_a_posfijo(tokens_preparados, para_prefijo=True)
        
        return resultado_posfijo[::-1]


def main():
    print("CONVERSOR DE EXPRESIONES (Infijo -> Posfijo -> Prefijo)")
    expresion_infija = input("Ingresa la expresión matemática: ").strip()

    # Validación de entrada vacía
    if not expresion_infija:
        print("\nError: No se ingresaron valores. Debes ingresar una expresión matemática para continuar.")
        return

    convertidor = ConvertidorExpresiones()
    
    # 1. Tokenización (separar en partes)
    tokens = convertidor.tokenizar(expresion_infija)
    
    # 2. Conversiones
    posfijo = convertidor.infijo_a_posfijo(tokens)
    prefijo = convertidor.infijo_a_prefijo(tokens)

    # 3. Mostrar los 3 resultados y el final
    print("\n--- RESULTADOS ---")
    print(f"1. Infijo original : {' '.join(tokens)}")
    print(f"2. Expresión Posfija: {' '.join(posfijo)}")
    print(f"3. Expresión Prefija: {' '.join(prefijo)}")

if __name__ == "__main__":
    main()