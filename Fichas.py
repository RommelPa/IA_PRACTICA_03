import pygame
import random
import copy

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

class Reversi:
    def __init__(reversi):
        pygame.init()
        reversi.pantalla = pygame.display.set_mode((1100, 800))
        pygame.display.set_caption('Reversi')

        reversi.jugador1 = 1
        reversi.jugador2 = -1

        reversi.jugadorActual = 1

        reversi.filas = 8
        reversi.columnas = 8

        reversi.tablero = Tablero(reversi.filas, reversi.columnas, (80, 80), reversi)

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
                    x, y = pygame.mouse.get_pos()
                    x, y = (x - 80) // 80, (y - 80) // 80
                    reversi.tablero.insertarFicha(reversi.tablero.logicaTablero, reversi.jugadorActual, y, x)
                    reversi.jugadorActual *= -1

    def actualizar(reversi):
        pass

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
        
    def cargarImagenesFondo(reversi):
        alpha = 'ABCDEFGHI'
        hojaSprites = pygame.image.load('assets/mapa.png').convert_alpha()
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
    
    def dibujarTablero(reversi, ventana):
        ventana.blit(reversi.tableroFondo, (0, 0))

        for ficha in reversi.fichas.values():
            ficha.dibujar(ventana)

    def imprimirTableroLogico(reversi):
        print('  | A | B | C | D | E | F | G | H |')
        for i, fila in enumerate(reversi.tableroLogico):
            linea = f'{i} |'.ljust(3, " ")
            for elemento in fila:
                linea += f"{elemento}".center(3, " ") + '|'
            print(linea)
        print()

    def insertarFicha(reversi, tablero, jugadorActual, y, x):
        imagenFicha = reversi.fichaBlanca if jugadorActual == 1 else reversi.fichaNegra
        reversi.fichas[(y, x)] = Ficha(jugadorActual, y, x, imagenFicha, reversi.JUEGO)
        tablero[y][x] = reversi.fichas[(y, x)].jugador

    def animarTransiciones(reversi, celda, jugador):
        if jugador == 1:
            reversi.fichas[(celda[0], celda[1])].transicion(reversi.transitionWhiteToBlack, reversi.whitetoken)
        else:
            reversi.fichas[(celda[0], celda[1])].transicion(reversi.transitionBlackToWhite, reversi.blacktoken)

class Ficha:
    def __init__(reversi, jugador, tableroX, tableroY, imagen, principal):
        reversi.jugador = jugador
        reversi.gridX = tableroX
        reversi.gridY = tableroY
        reversi.posX = 80 + (tableroY * 80)
        reversi.posY = 80 + (tableroX * 80)
        reversi.JUEGO = principal

        reversi.imagen = imagen
    
    def transicion(reversi):
        pass

    def dibujar(reversi, ventana):
        ventana.blit(reversi.imagen, (reversi.posX, reversi.posY))

if __name__ == '__main__':
    juego = Reversi()
    juego.ejecutar()
    pygame.quit()