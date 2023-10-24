import pygame, sys, time
from assets.defaults.get_imgs import imgs_historia
from intro import intro

reloj = pygame.time.Clock()
imgs = []
posx = 1280
posy = 330
parte = 1
cuentaPasos = 0

# funcion para pintar el personaje
def pintarPersonaje(SCREEN, accion):
    """
    Dibuja al personaje en la pantalla según la acción que se le indique.
    """
    global cuentaPasos, px, py

    if accion == "paradoD":
        # Dibuja al personaje parado hacia la derecha
        SCREEN.blit(imgs["paradoD"], (posx, posy))
    elif accion == "paradoI":
        # Dibuja al personaje parado hacia la izquierda
        SCREEN.blit(imgs["paradoI"], (posx, posy))

    elif accion == "izquierda":
        # Dibuja al personaje caminando hacia la izquierda
        if (cuentaPasos + 1) >= 4:
            cuentaPasos = 0
        SCREEN.blit(imgs["izquierda"][cuentaPasos // 1], (posx, posy))
        cuentaPasos += 1

    elif accion == "derecha":
        # Dibuja al personaje caminando hacia la derecha
        if (cuentaPasos + 1) >= 4:
            cuentaPasos = 0
        SCREEN.blit(imgs["derecha"][cuentaPasos // 1], (posx , posy))
        cuentaPasos += 1

def historia(SCREEN, personaje):
    """
    Esta función muestra una secuencia de historia en la pantalla utilizando imágenes y texto.
    
    La función utiliza variables globales para las imágenes, posición, parte de la historia y reloj.
    Comienza estableciendo el reloj a 30 fps y cargando las imágenes para la historia.
    Luego, entra en un bucle que muestra las imágenes y el texto para cada parte de la historia.
    El bucle termina cuando se completa la historia.

    El bucle tiene las siguientes partes:
    - Parte 1: muestra la imagen de entrada y mueve el personaje hacia la izquierda hasta que alcanza una cierta posición.
    - Parte 2: muestra un globo de chat con texto y un foco en el personaje.
    - Parte 3: muestra un globo de chat con un texto diferente y un foco diferente en el personaje.
    - Parte 4: muestra un globo de chat con un rayo y un foco diferente en el personaje.
    - Parte 5: mueve el personaje hacia la izquierda hasta que alcanza una cierta posición.
    """
    global imgs
    global posx
    global posy
    global parte
    global reloj
    reloj.tick(30)
    imgs = imgs_historia(personaje)
    luz = True
    parar = False
    while True:

        SCREEN.blit(imgs["pasillo"], (0, 0))

        # Parte 1: muestra la imagen de entrada y mueve el personaje hacia la izquierda hasta que alcanza una cierta posición.
        if parte == 1:

            if posx >= 700:
                posx -= 10
                pintarPersonaje(SCREEN, "izquierda")    
                SCREEN.blit(imgs["entrada"], (0, 0))
                SCREEN.blit(imgs["sombra"], (0, 0))
            else:
                parte = 2
                pintarPersonaje(SCREEN, "izquierda")    
                SCREEN.blit(imgs["entrada"], (0, 0))
                SCREEN.blit(imgs["sombra"], (0, 0))
            pygame.display.update()

        # Parte 2: muestra un globo de chat con texto y un foco en el personaje.
        elif parte == 2:
            SCREEN.blit(imgs["chat"], (650, 200))
            SCREEN.blit(imgs["foco2"], (675, 215))
            pintarPersonaje(SCREEN, "paradoI")
            SCREEN.blit(imgs["sombra"], (0, 0))
            pygame.display.update()
            time.sleep(1)
            parte = 3

        # Parte 3: muestra un globo de chat con un texto diferente y un foco diferente en el personaje.
        elif parte == 3:
            SCREEN.blit(imgs["chat"], (650, 200))
            SCREEN.blit(imgs["foco"], (675, 215))
            pintarPersonaje(SCREEN, "paradoI")
            SCREEN.blit(imgs["sombra"], (0, 0))
            pygame.display.update()
            time.sleep(1)
            parte = 4

        # Parte 4: muestra un globo de chat con un rayo y un foco diferente en el personaje.
        elif parte == 4:
            SCREEN.blit(imgs["chat"], (650, 200))
            SCREEN.blit(imgs["rayo"], (675, 215))
            pintarPersonaje(SCREEN, "paradoI")
            SCREEN.blit(imgs["sombra"], (0, 0))
            pygame.display.update()
            time.sleep(1)
            parte = 5

        # Parte 5: mueve el personaje hacia la izquierda hasta que alcanza una cierta posición.
        elif parte == 5:

            if posx >= -100:
                posx -= 10
                pintarPersonaje(SCREEN, "izquierda")    
                SCREEN.blit(imgs["entrada"], (0, 0))
                SCREEN.blit(imgs["sombra"], (0, 0))
                pygame.display.update()
            else:
                break

        # Manejo de eventos de Pygame, como salir del juego.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()