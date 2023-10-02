import pygame
from JugadorIA import JugadorIA
from Tablero import Tablero

class Reversi:
    def __init__(reversi):
        pygame.init()
        reversi.pantalla = pygame.display.set_mode((1100, 800))
        pygame.display.set_caption('Reversi')

        reversi.jugador1 = 1
        reversi.jugador2 = -1

        reversi.jugadorActual = 1

        reversi.tiempo = 0

        reversi.filas = 8
        reversi.columnas = 8

        reversi.juegoTerminado = True

        reversi.tablero = Tablero(reversi.filas, reversi.columnas, (80, 80), reversi)
        reversi.jugadorIA = JugadorIA(reversi.tablero)

        reversi.EJECUTAR = True

    def ejecutar(reversi):
        while reversi.EJECUTAR == True:
            reversi.entrada()
            reversi.actualizar()
            reversi.dibujar()

    def entrada(reversi):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                reversi.EJECUTAR = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 3:
                    reversi.tablero.imprimirTableroLogico()
                
                if evento.button == 1:
                    if reversi.jugadorActual == 1 and not reversi.juegoTerminado:
                        x, y = pygame.mouse.get_pos()
                        x, y = (x - 80) // 80, (y - 80) // 80
                        celdasValidas = reversi.tablero.encontrarMovimientosDisponibles(reversi.tablero.logicaTablero, reversi.jugadorActual)
                        if not celdasValidas:
                            pass
                        else:
                            if (y, x) in celdasValidas:
                                reversi.tablero.insertarFicha(reversi.tablero.logicaTablero, reversi.jugadorActual, y, x)
                                celdasIntercambiables = reversi.tablero.celdasIntercambiables(y, x, reversi.tablero.logicaTablero, reversi.jugadorActual)
                                for celda in celdasIntercambiables:
                                    reversi.tablero.animarTransiciones(celda, reversi.jugadorActual)
                                    reversi.tablero.logicaTablero[celda[0]][celda[1]] *= -1
                                reversi.jugadorActual *= -1
                                reversi.tiempo = pygame.time.get_ticks()
                
                if reversi.juegoTerminado:
                    x, y = pygame.mouse.get_pos()
                    if x >= 320 and x <= 480 and y >= 400 and y <= 480:
                            reversi.tablero.nuevoJuego()
                            reversi.juegoTerminado = False
                    
                
    def actualizar(reversi):
        if reversi.jugadorActual == -1:
            nuevo_tiempo = pygame.time.get_ticks()
            if nuevo_tiempo - reversi.tiempo >= 1000:
                if not reversi.tablero.encontrarMovimientosDisponibles(reversi.tablero.logicaTablero, reversi.jugadorActual):
                    reversi.juegoTerminado = True
                    return
                celda, puntuacion = reversi.jugadorIA.IADificil(reversi.tablero.logicaTablero, 5, -64, 64, -1)
                reversi.tablero.insertarFicha(reversi.tablero.logicaTablero, reversi.jugadorActual, celda[0], celda[1])
                celdasIntercambiables = reversi.tablero.celdasIntercambiables(celda[0], celda[1], reversi.tablero.logicaTablero, reversi.jugadorActual)
                for teja in celdasIntercambiables:
                    reversi.tablero.animarTransiciones(teja, reversi.jugadorActual)
                    reversi.tablero.logicaTablero[teja[0]][teja[1]] *= -1
                reversi.jugadorActual *= -1
        
        reversi.tablero.puntuacionJugador1 = reversi.tablero.calcularPuntuacionJugador(reversi.jugador1)
        reversi.tablero.puntuacionJugador2 = reversi.tablero.calcularPuntuacionJugador(reversi.jugador2)
        if not reversi.tablero.encontrarMovimientosDisponibles(reversi.tablero.logicaTablero, reversi.jugadorActual):
            reversi.juegoTerminado = True
            return

    def dibujar(reversi):
        reversi.pantalla.fill((0, 0, 0))
        reversi.tablero.dibujarTablero(reversi.pantalla)
        pygame.display.update()
