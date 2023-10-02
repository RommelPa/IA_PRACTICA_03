import pygame

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