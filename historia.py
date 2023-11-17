import pygame, sys
from assets.defaults.idioma import cargar_idioma
from moviepy.editor import VideoFileClip
from assets.defaults.pyvidplayer import Video 
from intro import intro

reloj = pygame.time.Clock()
idioma = cargar_idioma()

def historia(SCREEN, sexo, lenguaje):
    reloj.tick(30)

    video = VideoFileClip(f"./assets/video/{sexo}_{lenguaje}.mp4")
    duración = video.duration
    vid = Video(f"./assets/video/{sexo}_{lenguaje}.mp4")
    vid.set_size((1280, 720))

    # Esperar a que el video termine
    tiempo_transcurrido = 0
    while tiempo_transcurrido < duración:
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
        tiempo_transcurrido += reloj.tick(30) / 1000

    vid.close()
