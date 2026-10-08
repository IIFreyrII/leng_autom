from conversor_expresiones import (
    PilaMemoria,
    GestorOperadores,
    AnalizadorLexico,
    ConvertidorExpresiones,
)


class GeneradorTriplos:
    """
    Responsabilidad: Convertir una expresión posfija en tríplos
    (operador, argumento1, argumento2). Cada tríplo se identifica por su
    índice, y los resultados intermedios se referencian como "(índice)".
    """
    def generar(self, posfijo, destino=None):
        triplos = []
        pila = PilaMemoria(len(posfijo))
        operadores = GestorOperadores()

        for token in posfijo:
            if not operadores.es_operador(token):
                pila.push(token)
            else:
                arg2 = pila.pop()
                arg1 = pila.pop()
                triplos.append((token, arg1, arg2))
                pila.push(f"({len(triplos) - 1})")

        if destino is not None:
            resultado_final = pila.pop()
            triplos.append(('=', destino, resultado_final))

        return triplos


class FormateadorTabla:
    """
    Responsabilidad: Presentar los tríplos como tabla de texto.
    """
    def mostrar(self, triplos):
        print(f"{'Índice':<8}{'Operación':<12}{'Argumento 1':<14}{'Argumento 2':<14}")
        for i, (op, arg1, arg2) in enumerate(triplos):
            print(f"{'(' + str(i) + ')':<8}{op:<12}{arg1:<14}{arg2:<14}")


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

    analizador = AnalizadorLexico()
    convertidor = ConvertidorExpresiones(GestorOperadores())

    tokens = analizador.tokenizar(expresion)
    posfijo = convertidor.infijo_a_posfijo(tokens)
    triplos = GeneradorTriplos().generar(posfijo, destino)

    print(f"\nPosfijo: {' '.join(posfijo)}\n")
    FormateadorTabla().mostrar(triplos)


if __name__ == "__main__":
    main()
