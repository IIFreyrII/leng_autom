class ExpresionMalFormadaError(Exception): pass
class ErrorMatematicoError(Exception): pass

class PilaMemoria:
    """Responsabilidad: Estructura LIFO de capacidad fija."""
    def __init__(self, capacidad):
        self._capacidad = capacidad
        self._memoria = [None] * capacidad
        self._tope = -1

    def esta_vacia(self): return self._tope == -1
    def esta_llena(self): return self._tope == self._capacidad - 1

    def push(self, elemento):
        if self.esta_llena(): raise OverflowError("Stack Overflow.")
        self._tope += 1
        self._memoria[self._tope] = elemento

    def pop(self):
        if self.esta_vacia(): raise IndexError("Stack Underflow.")
        elemento = self._memoria[self._tope]
        self._tope -= 1
        return elemento

    def peek(self):
        if self.esta_vacia(): raise IndexError("Pila vacía.")
        return self._memoria[self._tope]

class GestorOperadores:
    """Responsabilidad: Conocer jerarquía y asociatividad de operadores y funciones."""
    def __init__(self):
        # Jerarquía: 1 (+,-), 2 (*,/), 3 (^), 4 (sqrt - función)
        self._operadores = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        self._funciones = {'sqrt'}
        self._asociatividad_derecha = {'^', 'sqrt'}
        self._parentesis = ('(', ')')

    def obtener_jerarquia(self, operador):
        if operador in self._funciones: return 4
        return self._operadores.get(operador, 0)

    def es_asociativo_derecha(self, operador):
        return operador in self._asociatividad_derecha

    def es_operador(self, token):
        return token in self._operadores or token in self._funciones

    def es_funcion(self, token):
        return token in self._funciones

    def es_parentesis(self, token):
        return token in self._parentesis

class AnalizadorLexico:
    """Responsabilidad: Convertir una cadena cruda en tokens (soporta floats y variables)."""
    def __init__(self, gestor):
        self.gestor = gestor

    def tokenizar(self, expresion):
        tokens = []
        i = 0
        n = len(expresion)
        while i < n:
            c = expresion[i]
            if c.isspace():
                i += 1
                continue

            if c in "+-*/^()":
                tokens.append(c)
                i += 1
            elif c.isalpha():
                token = ""
                while i < n and (expresion[i].isalnum() or expresion[i] == '_'):
                    token += expresion[i]
                    i += 1
                tokens.append(token)
            elif c.isdigit() or c == '.':
                token = ""
                puntos = 0
                while i < n and (expresion[i].isdigit() or expresion[i] == '.'):
                    if expresion[i] == '.': puntos += 1
                    token += expresion[i]
                    i += 1
                if puntos > 1:
                    raise ExpresionMalFormadaError(f"Número mal formado: {token}")
                tokens.append(token)
            else:
                raise ExpresionMalFormadaError(f"Carácter no reconocido: {c}")
        return tokens

class EstrategiaConversion:
    """Clase base para el patrón Strategy de Shunting Yard."""
    def __init__(self, gestor):
        self.gestor = gestor

    def debe_desapilar(self, token, top_pila):
        raise NotImplementedError

    def preparar_tokens(self, tokens):
        return tokens

    def procesar_resultado(self, resultado):
        return resultado

class EstrategiaPosfija(EstrategiaConversion):
    def debe_desapilar(self, token, top_pila):
        j_token = self.gestor.obtener_jerarquia(token)
        j_top = self.gestor.obtener_jerarquia(top_pila)
        if self.gestor.es_asociativo_derecha(token):
            return j_top > j_token
        return j_top >= j_token

class EstrategiaPrefija(EstrategiaConversion):
    def debe_desapilar(self, token, top_pila):
        j_token = self.gestor.obtener_jerarquia(token)
        j_top = self.gestor.obtener_jerarquia(top_pila)
        if self.gestor.es_asociativo_derecha(token):
            return j_top >= j_token
        return j_top > j_token

    def preparar_tokens(self, tokens):
        invertidos = tokens[::-1]
        return [')' if t == '(' else '(' if t == ')' else t for t in invertidos]

    def procesar_resultado(self, resultado):
        return resultado[::-1]

class ConvertidorExpresiones:
    """Responsabilidad: Orquestar el algoritmo usando la estrategia inyectada."""
    def __init__(self, estrategia: EstrategiaConversion):
        self.estrategia = estrategia
        self.gestor = estrategia.gestor

    def convertir(self, tokens):
        tokens_preparados = self.estrategia.preparar_tokens(tokens)
        pila = PilaMemoria(len(tokens_preparados))
        resultado = []

        for token in tokens_preparados:
            if not self.gestor.es_operador(token) and not self.gestor.es_parentesis(token):
                resultado.append(token)
            elif token == '(':
                pila.push(token)
            elif token == ')':
                try:
                    while not pila.esta_vacia() and pila.peek() != '(':
                        resultado.append(pila.pop())
                    pila.pop() # descarta '('
                except IndexError:
                    raise ExpresionMalFormadaError("Paréntesis desbalanceados (falta apertura).")
            else: # Es operador o función
                while not pila.esta_vacia() and pila.peek() != '(':
                    if self.estrategia.debe_desapilar(token, pila.peek()):
                        resultado.append(pila.pop())
                    else:
                        break
                pila.push(token)

        while not pila.esta_vacia():
            op = pila.pop()
            if op == '(':
                raise ExpresionMalFormadaError("Paréntesis desbalanceados (falta cierre).")
            resultado.append(op)

        return self.estrategia.procesar_resultado(resultado)

class Evaluador:
    def __init__(self, gestor):
        self.gestor = gestor

    def es_numero(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def resolver_operacion(self, operador, operandos):
        if operador == '+': return operandos[0] + operandos[1]
        if operador == '-': return operandos[0] - operandos[1]
        if operador == '*': return operandos[0] * operandos[1]
        if operador == '/':
            if operandos[1] == 0: raise ErrorMatematicoError("División entre cero.")
            return operandos[0] / operandos[1]
        if operador == '^': return operandos[0] ** operandos[1]
        if operador == 'sqrt':
            if operandos[0] < 0: raise ErrorMatematicoError("Raíz cuadrada de número negativo.")
            # Cálculo de raíz cuadrada sin depender de la librería math
            return operandos[0] ** 0.5

class GeneradorTriplos:
    def __init__(self, gestor, evaluador):
        self.gestor = gestor
        self.evaluador = evaluador

    def generar(self, posfijo, valores):
        triplos = []
        pila = PilaMemoria(len(posfijo))

        for token in posfijo:
            if not self.gestor.es_operador(token):
                val = float(token) if self.evaluador.es_numero(token) else float(valores[token])
                pila.push((token, val))
            else:
                if self.gestor.es_funcion(token):
                    ref1, val1 = pila.pop() # type: ignore
                    res = self.evaluador.resolver_operacion(token, [val1])
                    triplos.append((token, ref1, "N/A", res))
                else:
                    ref2, val2 = pila.pop() # type: ignore
                    ref1, val1 = pila.pop() # type: ignore
                    res = self.evaluador.resolver_operacion(token, [val1, val2])
                    triplos.append((token, ref1, ref2, res))

                pila.push((f"({len(triplos)-1})", res))

        _, res_final = pila.pop() # type: ignore
        return triplos, res_final

def formatear_numero(valor):
    if isinstance(valor, float) and valor.is_integer(): return str(int(valor))
    return f"{valor:.4f}" if isinstance(valor, float) else str(valor)

def main():
    expresion = input("Ingresa la expresión matemática: ").strip()
    gestor = GestorOperadores()
    lexico = AnalizadorLexico(gestor)

    try:
        tokens = lexico.tokenizar(expresion)


        posfijo = ConvertidorExpresiones(EstrategiaPosfija(gestor)).convertir(tokens)
        prefijo = ConvertidorExpresiones(EstrategiaPrefija(gestor)).convertir(tokens)

        print("\n--- NOTACIONES ---")
        print(f"Infija : {' '.join(tokens)}")
        print(f"Prefija: {' '.join(prefijo)}")
        print(f"Posfija: {' '.join(posfijo)}")


        variables = {t for t in tokens if not gestor.es_operador(t) and not gestor.es_parentesis(t) and not Evaluador(gestor).es_numero(t)}
        valores = {}
        if variables:
            print("\n--- VALORES DE VARIABLES ---")
            for var in variables:
                while True:
                    try:
                        valores[var] = float(input(f"Valor para '{var}': "))
                        break
                    except ValueError:
                        print("Error: Ingresa un número válido.")


        generador = GeneradorTriplos(gestor, Evaluador(gestor))
        triplos, resultado = generador.generar(posfijo, valores)

        print("\n--- TABLA DE TRÍPLOS ---")
        print(f"{'Índice':<8}{'Op':<8}{'Arg1':<12}{'Arg2':<12}{'Res'}")
        for i, (op, a1, a2, res) in enumerate(triplos):
            print(f"({i})     {op:<8}{str(a1):<12}{str(a2):<12}{formatear_numero(res)}")

        print(f"\n=> RESULTADO FINAL: {formatear_numero(resultado)}")

    except (ExpresionMalFormadaError, ErrorMatematicoError, IndexError) as e:
        print(f"\nERROR DE EVALUACIÓN: {e}")

if __name__ == "__main__":
    main()