from conversor_expresiones import (
    PilaMemoria,
    GestorOperadores,
    AnalizadorLexico,
    ConvertidorExpresiones,
    EvaluadorPosfijo,
    pedir_valores,
    formatear_numero,
)

class GeneradorTriplos:
    """
    Responsabilidad: Convertir una expresión posfija en tríplos
    (operador, argumento1, argumento2, resultado). Cada tríplo se identifica
    por su índice, y los resultados intermedios se referencian como "(índice)".
    El valor de cada operación se calcula reutilizando EvaluadorPosfijo.
    """
    def __init__(self, gestor_operadores, evaluador):
        self.gestor = gestor_operadores
        self.evaluador = evaluador

    def generar(self, posfijo, valores, destino=None):
        triplos = []
        # Cada elemento de la pila es (referencia, valor)
        pila = PilaMemoria(len(posfijo))

        for token in posfijo:
            if not self.gestor.es_operador(token):
                valor = self.evaluador.obtener_valor(token, valores)
                pila.push((token, valor))
            else:
                ref2, valor2 = pila.pop()
                ref1, valor1 = pila.pop()
                resultado = self.evaluador.aplicar(token, valor1, valor2)
                triplos.append((token, ref1, ref2, resultado))
                pila.push((f"({len(triplos) - 1})", resultado))

        if destino is not None:
            ref_final, valor_final = pila.pop()
            triplos.append(('=', destino, ref_final, valor_final))

        return triplos


class FormateadorTabla:
    """
    Responsabilidad: Presentar los tríplos como tabla de texto.
    """
    def mostrar(self, triplos):
        print(f"{'Índice':<8}{'Operación':<12}{'Argumento 1':<14}{'Argumento 2':<14}{'Resultado':<12}")
        for i, (op, arg1, arg2, resultado) in enumerate(triplos):
            indice = f"({i})"
            print(f"{indice:<8}{op:<12}{arg1:<14}{arg2:<14}{formatear_numero(resultado):<12}")


def separar_asignacion(entrada):
    """Devuelve (destino, expresión). Si no hay '=', destino es None."""
    if '=' not in entrada:
        return None, entrada.strip()
    destino, expresion = entrada.split('=', 1)
    return destino.strip(), expresion.strip()


def main():
    print("GENERADOR DE TRÍPLOS")
    entrada = input("Ingresa la expresión (ej. a = ...): ").strip()

    if not entrada:
        print("\nDebes ingresar una expresión.")
        return

    destino, expresion = separar_asignacion(entrada)

    gestor_ops = GestorOperadores()
    analizador = AnalizadorLexico()
    convertidor = ConvertidorExpresiones(gestor_ops)
    generador = GeneradorTriplos(gestor_ops, EvaluadorPosfijo(gestor_ops))

    tokens = analizador.tokenizar(expresion)
    posfijo = convertidor.infijo_a_posfijo(tokens)

    try:
        valores = pedir_valores(tokens, gestor_ops)
        triplos = generador.generar(posfijo, valores, destino)
    except ValueError:
        print("\nLos valores de las variables deben ser numéricos.")
        return
    except ZeroDivisionError:
        print("\nError: división entre cero.")
        return

    print(f"\nPosfijo: {' '.join(posfijo)}\n")
    FormateadorTabla().mostrar(triplos)


if __name__ == "__main__":
    main()
