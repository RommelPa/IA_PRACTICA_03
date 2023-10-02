import copy
from Utilidades import evaluarTablero

class JugadorIA:
    def __init__(reversi, objetoTablero):
        reversi.tablero = objetoTablero

    def IADificil(reversi, tablero, profundidad, alpha, beta, jugador):
        nuevoTablero = copy.deepcopy(tablero)
        movimientosDisponibles = reversi.tablero.encontrarMovimientosDisponibles(nuevoTablero, jugador)

        if profundidad == 0 or len(movimientosDisponibles) == 0:
            mejorMovimiento, Puntuacion = None, evaluarTablero(tablero, jugador)
            return mejorMovimiento, Puntuacion

        if jugador < 0:
            mejorPuntuacion = -64
            mejorMovimiento = None

            for movimiento in movimientosDisponibles:
                x, y = movimiento
                celdasIntercambiables = reversi.tablero.celdasIntercambiables(x, y, nuevoTablero, jugador)
                nuevoTablero[x][y] = jugador
                for celda in celdasIntercambiables:
                    nuevoTablero[celda[0]][celda[1]] = jugador

                mMovimiento, valor = reversi.IADificil(nuevoTablero, profundidad-1, alpha, beta, jugador *-1)

                if valor > mejorPuntuacion:
                    mejorPuntuacion = valor
                    mejorMovimiento = movimiento
                alpha = max(alpha, mejorPuntuacion)
                if beta <= alpha:
                    break

                nuevoTablero = copy.deepcopy(tablero)
            return mejorMovimiento, mejorPuntuacion

        if jugador > 0:
            mejorPuntuacion = 64
            mejorMovimiento = None

            for movimiento in movimientosDisponibles:
                x, y = movimiento
                celdasIntercambiables = reversi.tablero.celdasIntercambiables(x, y, nuevoTablero, jugador)
                nuevoTablero[x][y] = jugador
                for celda in celdasIntercambiables:
                    nuevoTablero[celda[0]][celda[1]] = jugador

                mMovimiento, valor = reversi.IADificil(nuevoTablero, profundidad-1, alpha, beta, jugador)

                if valor < mejorPuntuacion:
                    mejorPuntuacion = valor
                    mejorMovimiento = movimiento
                beta = min(beta, mejorPuntuacion)
                if beta <= alpha:
                    break

                nuevoTablero = copy.deepcopy(tablero)
            return mejorMovimiento, mejorPuntuacion