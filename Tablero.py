import pygame

from Utilidades import cargarHojaSprites, cargarImagenes, direcciones

class Tablero:
    def __init__(reversi, filas, columnas, tamano, principal):
        reversi.JUEGO = principal
        reversi.y = filas
        reversi.x = columnas
        reversi.tamano = tamano
        reversi.fichaBlanca = cargarImagenes('assets/FichaBlanca.png', tamano)
        reversi.fichaNegra = cargarImagenes('assets/FichaNegra.png', tamano)
        reversi.transicionBlancaANegra = [cargarImagenes(f'assets/NegraABlanca{i}.png', reversi.tamano) for i in range(1, 4)]
        reversi.transicionNegraABlanca = [cargarImagenes(f'assets/BlancaANegra{i}.png', reversi.tamano) for i in range(1, 4)]
        reversi.fondo = reversi.cargarImagenesFondo()

        reversi.fichas = {}

        reversi.tableroFondo = reversi.crearFondoImagen()

        reversi.logicaTablero = reversi.generarTablero(reversi.y, reversi.x)

        reversi.puntuacionJugador1 = 0
        reversi.puntuacionJugador2 = 0

        reversi.fuente = pygame.font.SysFont('Arial', 20, True, False)

    def nuevoJuego(reversi):
        reversi.fichas.clear()
        reversi.logicaTablero = reversi.generarTablero(reversi.y, reversi.x)
        
    def cargarImagenesFondo(reversi):
        alpha = 'ABCDEFGHI'
        hojaSprites = pygame.image.load('assets/Mapa.png').convert_alpha()
        imagenDiccionario = {}
        for i in range(3):
            for j in range(7):
                imagenDiccionario[alpha[j]+str(i)] = cargarHojaSprites(hojaSprites, j, i, (reversi.tamano), (32, 32))
        return imagenDiccionario

    def crearFondoImagen(reversi):
        tableroFondo = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2'],
        ]
        imagen = pygame.Surface((960, 960))
        for j, fila in enumerate(tableroFondo):
            for i, img in enumerate(fila):
                imagen.blit(reversi.fondo[img], (i * reversi.tamano[0], j * reversi.tamano[1]))
        return imagen

    def generarTablero(reversi, filas, columnas):
        tablero = []
        for y in range(filas):
            linea = []
            for x in range(columnas):
                linea.append(0)
            tablero.append(linea)
        reversi.insertarFicha(tablero, 1, 3, 3)
        reversi.insertarFicha(tablero, -1, 3, 4)
        reversi.insertarFicha(tablero, 1, 4, 4)
        reversi.insertarFicha(tablero, -1, 4, 3)

        return tablero
    
    def calcularPuntuacionJugador(reversi, jugador):
        puntuacion = 0
        for fila in reversi.logicaTablero:
            for columna in fila:
                if columna == jugador:
                    puntuacion += 1
        return puntuacion
    
    def dibujarPuntuacion(reversi, jugador, puntuacion):
        textoImg = reversi.fuente.render(f'{jugador} : {puntuacion}', 1, 'White')
        return textoImg

    def pantallaFinal(reversi):
        if reversi.JUEGO.juegoTerminado:
            pantallaFinalImg = pygame.Surface((320, 320))
            textoFinal = reversi.fuente.render(f'{"Felicidades, ganaste!!" if reversi.puntuacionJugador1 > reversi.puntuacionJugador1 else "Mala suerte, perdiste"}', 1, 'White')
            pantallaFinalImg.blit(textoFinal, (0, 0))
            nuevoJuego = pygame.draw.rect(pantallaFinalImg, 'White', (80, 160, 160, 80))
            nuevoJuegoTexto = reversi.fuente.render('Juega de nuevo', 1, 'Black')
            pantallaFinalImg.blit(nuevoJuegoTexto, (120, 190))
        return pantallaFinalImg
            
    def dibujarTablero(reversi, ventana):
        ventana.blit(reversi.tableroFondo, (0, 0))

        ventana.blit(reversi.dibujarPuntuacion('Blancas', reversi.puntuacionJugador1), (900, 100))
        ventana.blit(reversi.dibujarPuntuacion('Negras', reversi.puntuacionJugador2), (900, 200))

        for ficha in reversi.fichas.values():
            ficha.dibujar(ventana)
        
        movimientosDisponibles = reversi.encontrarMovimientosDisponibles(reversi.logicaTablero, reversi.JUEGO.jugadorActual)
        if reversi.JUEGO.jugadorActual == 1:
            for movimiento in movimientosDisponibles:
                pygame.draw.rect(ventana, 'White', (80 + (movimiento[1] * 80) + 30, 80 + (movimiento[0] * 80) + 30, 20, 20))
        
        if reversi.JUEGO.juegoTerminado:
            ventana.blit(reversi.pantallaFinal(), (240, 240))

    def imprimirTableroLogico(reversi):
        print('  | A | B | C | D | E | F | G | H |')
        for i, fila in enumerate(reversi.logicaTablero):
            linea = f'{i} |'.ljust(3, " ")
            for elemento in fila:
                linea += f"{elemento}".center(3, " ") + '|'
            print(linea)
        print()
    
    def encontrarCeldasValidas(reversi, tablero, jugadorActual):
        celdasValidasParaClic = []
        for tableroX, fila in enumerate(tablero):
            for tableroY, columna in enumerate(fila):
                if tablero[tableroX][tableroY] != 0:
                    continue
                DIRECCIONES = direcciones(tableroX, tableroY)

                for direccion in DIRECCIONES:
                    dirX, dirY = direccion
                    celdaVerificada = tablero[dirX][dirY]

                    if celdaVerificada == 0 or celdaVerificada == jugadorActual:
                        continue

                    if (tableroX, tableroY) in celdasValidasParaClic:
                        continue

                    celdasValidasParaClic.append((tableroX, tableroY))
        return celdasValidasParaClic 
    
    def celdasIntercambiables(reversi, x, y, tablero, jugador):
        celdasAlrededor = direcciones(x, y)
        if len(celdasAlrededor) == 0:
            return []

        celdasIntercambiables = []
        for celdaVerificar in celdasAlrededor:
            celdaX, celdaY = celdaVerificar
            difX, difY = celdaX - x, celdaY - y
            lineaActual = []

            EJECUTAR = True
            while EJECUTAR:
                if tablero[celdaX][celdaY] == jugador * -1:
                    lineaActual.append((celdaX, celdaY))
                elif tablero[celdaX][celdaY] == jugador:
                    EJECUTAR = False
                    break
                elif tablero[celdaX][celdaY] == 0:
                    lineaActual.clear()
                    EJECUTAR = False
                celdaX += difX
                celdaY += difY

                if celdaX < 0 or celdaX > 7 or celdaY < 0 or celdaY > 7:
                    lineaActual.clear()
                    EJECUTAR = False

            if len(lineaActual) > 0:
                celdasIntercambiables.extend(lineaActual)

        return celdasIntercambiables
    
    def encontrarMovimientosDisponibles(reversi, tablero, jugadorActual):
        celdasValidas = reversi.encontrarCeldasValidas(tablero, jugadorActual)
        celdasJugables = []

        for celda in celdasValidas:
            x, y = celda
            if celda in celdasJugables:
                continue
            celdasIntercambiables = reversi.celdasIntercambiables(x, y, tablero, jugadorActual)

            if len(celdasIntercambiables) > 0:
                celdasJugables.append(celda)

        return celdasJugables

    def insertarFicha(reversi, tablero, jugadorActual, y, x):
        imagenFicha = reversi.fichaBlanca if jugadorActual == 1 else reversi.fichaNegra
        reversi.fichas[(y, x)] = Ficha(jugadorActual, y, x, imagenFicha, reversi.JUEGO)
        tablero[y][x] = reversi.fichas[(y, x)].jugador

    def animarTransiciones(reversi, celda, jugador):
        if jugador == 1:
            reversi.fichas[(celda[0], celda[1])].transicion(reversi.transicionBlancaANegra, reversi.fichaBlanca)
        else:
            reversi.fichas[(celda[0], celda[1])].transicion(reversi.transicionNegraABlanca, reversi.fichaNegra)

class Ficha:
    def __init__(reversi, jugador, tableroX, tableroY, imagen, principal):
        reversi.jugador = jugador
        reversi.gridX = tableroX
        reversi.gridY = tableroY
        reversi.posX = 80 + (tableroY * 80)
        reversi.posY = 80 + (tableroX * 80)
        reversi.JUEGO = principal

        reversi.imagen = imagen
    
    def transicion(reversi, imagenesTransicion, imagenFicha):
        for i in range(30):
            reversi.imagen = imagenesTransicion[i // 10]
            reversi.JUEGO.dibujar()
        reversi.imagen = imagenFicha

    def dibujar(reversi, ventana):
        ventana.blit(reversi.imagen, (reversi.posX, reversi.posY))