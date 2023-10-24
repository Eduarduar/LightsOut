import pygame, sys
from assets.defaults.get_fonts import get_font
from assets.defaults.get_imgs import imgs_cambiarAvatar
from assets.defaults.idioma import cargar_idioma
from intro import intro

imgs = imgs_cambiarAvatar()
idioma = cargar_idioma()
reloj = pygame.time.Clock()

def pantallaCambiarAvatar(SCREEN, configJuego):
    """
    Función que muestra la pantalla de cambio de avatar y permite al usuario seleccionar entre un avatar masculino o femenino.
    """
    # Establecemos el título de la ventana con el texto correspondiente
    pygame.display.set_caption(idioma[configJuego["Idioma"]]["CambiarAvatar"]["Titulo"])

    # Creamos el texto del título y lo centramos en la pantalla
    tituloText = get_font(75).render(idioma[configJuego["Idioma"]]["CambiarAvatar"]["Titulo"], True, "#b68f40")
    tituloRect = tituloText.get_rect(center=(640, 100))

    # Creamos el texto para los botones de selección de avatar
    mujerText = get_font(50).render(idioma[configJuego["Idioma"]]["CambiarAvatar"]["Mujer"], True, "#ffffff")
    hombreText = get_font(50).render(idioma[configJuego["Idioma"]]["CambiarAvatar"]["Hombre"], True, "#ffffff")

    while True:
        # Limitamos la velocidad de actualización de la pantalla
        reloj.tick(30)

        # Obtenemos la posición del mouse
        mousePos = pygame.mouse.get_pos()
        posX = mousePos[0]
        posY = mousePos[1]

        # Recorremos los eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Si se cierra la ventana, volvemos a la pantalla de inicio
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si se hace click en alguno de los botones de selección de avatar, actualizamos la configuración y volvemos a la pantalla de inicio
                if posX < 650 and posX > 0:
                    configJuego["personaje"] = "hombre"
                    return SCREEN, configJuego 
                elif posX > 650 and posX < 1280:
                    configJuego["personaje"] = "mujer"
                    return SCREEN ,configJuego

        # Colocamos el fondo
        SCREEN.blit(imgs['fondo'], (0, 0))

        # Colocamos el título
        SCREEN.blit(tituloText, tituloRect)

        # Colocamos los elementos correspondientes al avatar seleccionado
        if posX < 650 and posX > 0:
            SCREEN.blit(imgs["luzHombre"], (0, 0))
            SCREEN.blit(imgs["moldes"], (0, 0))
            SCREEN.blit(imgs["hombre"], (0, 0))
        elif posX > 650 and posX < 1280:
            SCREEN.blit(imgs["luzMujer"], (0, 0))
            SCREEN.blit(imgs["moldes"], (0, 0))
            SCREEN.blit(imgs["mujer"], (0, 0))

        # Colocamos los textos de los botones de selección de avatar
        SCREEN.blit(mujerText, (700, 550))
        SCREEN.blit(hombreText, (350, 550))
        
        # Actualizamos la pantalla
        pygame.display.flip()