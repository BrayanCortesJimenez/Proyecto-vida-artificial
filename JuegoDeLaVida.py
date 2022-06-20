import pygame
import time, os
import numpy as np

# Hago que la ventana aparezca centrada en Windows
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

# Establezco el título de la ventana:
pygame.display.set_caption("Juego de la vida - Jonatandb")

# Carga el icono si existe
iconPath = "./icono-2.svg"

if os.path.exists(iconPath):

    icono = pygame.image.load(iconPath)

    # Establece el icono de la ventana
    pygame.display.set_icon(icono)

# Defino ancho y alto de la ventana
width, height = 700, 700

# Creación de la ventana
screen = pygame.display.set_mode((height, width))

# Color de fondo, casi negro
bg = 25, 25, 25

# Pinto el fondo con el color elegido (bg)
screen.fill(bg)

# Cantidad de celdas en cada eje
nxC, nyC = 60, 60

# Ancho y alto de cada celda
dimCW = width / nxC
dimCH = height / nyC

# Estructura de datos que contiene todos los estados de las diferentes celdas
# Estados de las celdas: Vivas = 1 - Muertas = 0
# Inicializo matriz con ceros
gameState = np.zeros((nxC, nyC))

# Autómata palo:
# 0 1 0
# 0 1 0
# 0 1 0
# gameState[5, 3] = 1
# gameState[5, 4] = 1
# gameState[5, 5] = 1

# Autómata móvil:
# 0 1 0
# 0 0 1
# 1 1 1
# gameState[21, 21] = 1
# gameState[22, 22] = 1
# gameState[22, 23] = 1
# gameState[21, 23] = 1
# gameState[20, 23] = 1

# Versión inicial del autómata
posInitX = int((nxC / 2) - 3)
posInitY = int((nyC / 2) - 5)
gameState[posInitX, posInitY] = 1
gameState[posInitX + 1, posInitY] = 1
gameState[posInitX + 2, posInitY] = 1
gameState[posInitX + 3, posInitY] = 1

gameState[posInitX + 3, posInitY + 1] = 1
gameState[posInitX + 3, posInitY + 2] = 1

gameState[posInitX, posInitY + 3] = 1
gameState[posInitX + 3, posInitY + 3] = 1

gameState[posInitX, posInitY + 4] = 1
gameState[posInitX + 1, posInitY + 4] = 1
gameState[posInitX + 2, posInitY + 4] = 1
gameState[posInitX + 3, posInitY + 4] = 1

# Control de la ejecución - En True se inicia pausado (Para poder ver la forma inicial de los aútomatas):
pauseExec = True

# Controla la finalización del juego:
endGame = False

# Acumulador de cantidad de iteraciones:
iteration = 0

# Bucle de ejecución principal (Main Loop):
while not endGame:

    contador = 1
    
    newGameState = np.copy(gameState)

    # Vuelvo a colorear la pantalla con el color de fondo
    screen.fill(bg)

    # Agrego pequeña pausa para que el cpu no trabaje al 100%
    time.sleep(0.1)

    # Registro de eventos de teclado y mouse
    ev = pygame.event.get()

    # Contador de población:
    population = 0

    for event in ev:

        # Si cierran la ventana finalizo el juego
        if event.type == pygame.QUIT:
            endGame = True
            break

        if event.type == pygame.KEYDOWN:

            # Si tocan escape finalizo el juego
            if event.key == pygame.K_ESCAPE:
                endGame = True
                break

            # Si tocan la tecla r limpio la grilla, reseteo población e iteración y pongo pausa
            if event.key == pygame.K_r:
                iteration = 0
                gameState = np.zeros((nxC, nyC))
                newGameState = np.zeros((nxC, nyC))
                pauseExec = True
            else:
                # Si tocan cualquier tecla no contemplada, pauso o reanudo el juego
                pauseExec = not pauseExec

        # Detección de click del mouse:
        mouseClick = pygame.mouse.get_pressed()

        # Obtención de posición del cursor en la pantalla:
        # Si se hace click con cualquier botón del mouse, se obtiene un valor en mouseClick mayor a cero
        if sum(mouseClick) > 0:

            # Click del medio pausa / reanuda el juego
            if mouseClick[1]:

                pauseExec = not pauseExec

            else:

                # Obtengo las coordenadas del cursor del mouse en pixeles
                posX, posY, = pygame.mouse.get_pos()

                # Convierto de coordenadas en pixeles a celda clickeada en la grilla
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))

                # Click izquierdo y derecho permutan entre vida y muerte
                newGameState[celX, celY] = not gameState[celX, celY]

    if not pauseExec:
        # Incremento el contador de generaciones
        iteration += 1

    # Recorro cada una de las celdas generadas
    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExec:

                # Cálculo del número de vecinos cercanos
                n_neigh = (
                    gameState[(x - 1) % nxC, (y - 1) % nyC]
                    + gameState[x % nxC, (y - 1) % nyC]
                    + gameState[(x + 1) % nxC, (y - 1) % nyC]
                    + gameState[(x - 1) % nxC, y % nyC]
                    + gameState[(x + 1) % nxC, y % nyC]
                    + gameState[(x - 1) % nxC, (y + 1) % nyC]
                    + gameState[x % nxC, (y + 1) % nyC]
                    + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )

                
                # Una célula muerta con exactamente 3 células vecinas vivas "nace"
                # (es decir, al turno siguiente estará viva).
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Una célula viva dependiendo de la cantidad de vecinos,
                # se mueve más rápido
                if gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    if n_neigh == 7 and contador % 10 == 0:
                        newGameState[x, y] = 0
                    elif n_neigh == 6 and contador % 20 == 0:
                        newGameState[x, y] = 0
                    elif n_neigh == 5 and contador % 30 == 0:
                        newGameState[x, y] = 0
                    elif n_neigh == 4 and contador % 40 == 0:
                        newGameState[x, y] = 0
                    elif n_neigh == 3 and contador % 50 == 0:
                        gameState[x, y] = newGameState[x + 1, y + 1]
                    elif n_neigh == 2 and contador % 60 == 0:
                        gameState[x, y] = newGameState[x + 1, y + 1]
                    elif n_neigh == 1 and contador % 70 == 0:
                        newGameState[x, y] = 0
                    elif n_neigh == 0 and contador % 80 == 0:
                        newGameState[x, y] = 0

                    contador += 1

                    if contador == 5000:
                        contador = 1

            # Incremento el contador de población:
            if gameState[x, y] == 1:
                population += 1

            # Creación del polígono de cada celda a dibujar
            poly = [
                (int(x * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                (int(x * dimCW), int((y + 1) * dimCH)),
            ]

            if newGameState[x, y] == 0:
                # Dibujado de la celda para cada par de x e y:
                # screen          -> Pantalla donde dibujar
                # (128, 128, 128) -> Color a utilizar para dibujar, en este caso un gris
                # poly            -> Puntos que definan al poligono que se está dibujando
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                if pauseExec:
                    # Con el juego pausado pinto de gris las celdas
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
                else:
                    # Con el juego ejecutándose pinto de blanco las celdas
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizo el título de la ventana
    """title = f"Juego de la vida  - Población: {population} - Generación: {iteration}"
    if pauseExec:
        title += " - [PAUSADO]"
    pygame.display.set_caption(title)
    print(title)"""
    
    # Actualizo gameState
    gameState = np.copy(newGameState)

    # Muestro y actualizo los fotogramas en cada iteración del bucle principal
    pygame.display.flip()

print("Juego finalizado")
