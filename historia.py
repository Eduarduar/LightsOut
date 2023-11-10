import pygame, sys
from assets.defaults.idioma import cargar_idioma
from intro import intro
from assets.defaults.pyvidplayer import Video 

reloj = pygame.time.Clock()
idioma = cargar_idioma()

def historia(SCREEN, sexo, lenguaje):
    reloj.tick(30)

    vid = Video(f"./assets/video/{sexo}_{lenguaje}.mp4")
    vid.set_size((1280, 720))

    # Esperar a que el video termine
    while True:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                return None

            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

        vid.draw(SCREEN, (0,0))
        pygame.display.flip()
