import pygame
import copy

def direcciones(x, y, minX=0, minY=0, maxX=7, maxY=7):
    direccionesValidas = []
    if x != minX:
        direccionesValidas.append((x - 1, y))
    if x != minX and y != minY:
        direccionesValidas.append((x - 1, y - 1))
    if x != minX and y != maxY:
        direccionesValidas.append((x - 1, y + 1))

    if x != maxX:
        direccionesValidas.append((x + 1, y))
    if x != maxX and y != minY:
        direccionesValidas.append((x + 1, y - 1))
    if x != maxX and y != maxY:
        direccionesValidas.append((x + 1, y + 1))

    if y != minY:
        direccionesValidas.append((x, y - 1))
    if y != maxY:
        direccionesValidas.append((x, y + 1))

    return direccionesValidas

def cargarImagenes(ruta, tamano):
    img = pygame.image.load(f"{ruta}").convert_alpha()
    img = pygame.transform.scale(img, tamano)
    return img

def cargarHojaSprites(hoja, fila, columna, nuevoTamano, tamano):
    imagen = pygame.Surface((32, 32)).convert_alpha()
    imagen.blit(hoja, (0, 0), (fila * tamano[0], columna * tamano[1], tamano[0], tamano[1]))
    imagen = pygame.transform.scale(imagen, nuevoTamano)
    imagen.set_colorkey('Black')
    return imagen

def evaluarTablero(tablero, jugador):
        puntuacion = 0
        for y, fila in enumerate(tablero):
            for x, columna in enumerate(fila):
                puntuacion -= columna
        return puntuacion

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
            endText = reversi.fuente.render(f'{"Felicidades, ganaste!!" if reversi.puntuacionJugador1 > reversi.puntuacionJugador1 else "Mala suerte, perdiste"}', 1, 'White')
            pantallaFinalImg.blit(endText, (0, 0))
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

if __name__ == '__main__':
    juego = Reversi()
    juego.ejecutar()
    pygame.quit()
