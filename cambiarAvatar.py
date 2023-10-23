import pygame, sys
from assets.defaults.get_fonts import get_font
from assets.defaults.get_imgs import imgs_cambiarAvatar
from assets.defaults.idioma import cargar_idioma
from intro import intro

imgs = imgs_cambiarAvatar()
idioma = cargar_idioma()
reloj = pygame.time.Clock()

def pantallaCambiarAvatar(SCREEN, configJuego):
    pygame.display.set_caption(idioma[configJuego["Idioma"]]["CambiarAvatar"]["Titulo"])

    tituloText = get_font(75).render(idioma[configJuego["Idioma"]]["CambiarAvatar"]["Titulo"], True, "#b68f40")
    tituloRect = tituloText.get_rect(center=(640, 100))

    mujerText = get_font(50).render(idioma[configJuego["Idioma"]]["CambiarAvatar"]["Mujer"], True, "#ffffff")
    hombreText = get_font(50).render(idioma[configJuego["Idioma"]]["CambiarAvatar"]["Hombre"], True, "#ffffff")

    while True:
        reloj.tick(30)
        mousePos = pygame.mouse.get_pos() # Obtenemos la posicion del mouse
        posX = mousePos[0]
        posY = mousePos[1]
        for event in pygame.event.get(): # Recorremos los eventos
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN: #  Detectamos el click del mouse
                if posX < 650 and posX > 0: # Si el click esta en la posicion del hombre
                    configJuego["personaje"] = "hombre"
                    return SCREEN, configJuego 
                elif posX > 650 and posX < 1280: # Si el click esta en la posicion de la mujer
                    configJuego["personaje"] = "mujer"
                    return SCREEN ,configJuego
        SCREEN.blit(imgs['fondo'], (0, 0)) # Colocamos el fondo

        SCREEN.blit(tituloText, tituloRect) # Colocamos el titulo
        
        if posX < 650 and posX > 0:
            SCREEN.blit(imgs["luzHombre"], (0, 0)) # Colocamos la luz
            SCREEN.blit(imgs["moldes"], (0, 0)) # Colocamos los moldes
            SCREEN.blit(imgs["hombre"], (0, 0)) # Colocamos el hombre
        elif posX > 650 and posX < 1280:
            SCREEN.blit(imgs["luzMujer"], (0, 0)) # Colocamos la luz
            SCREEN.blit(imgs["moldes"], (0, 0)) # Colocamos los moldes
            SCREEN.blit(imgs["mujer"], (0, 0)) # Colocamos la mujer

        SCREEN.blit(mujerText, (700, 550)) # Colocamos el texto de mujer
        SCREEN.blit(hombreText, (350, 550))
        
        pygame.display.flip()