import pygame
from menu_principal import menu_principal
from intro import intro

print("Lights Out - v0.1.0")

configJuego = {
    "Idioma": "es",
    "Volumen": 0.05,
    "indiceMusic": 0,
    "historia": True,
    "personaje": "hombre",
    "ropa": 1
}

elementosFondo = {
    "luna": {
        "posX" : 1200,
        "posY" : 30
    },
    "nube": {
        "posX" : 0,
        "posY" : 80
    },
    "ciudad": {
        "posX" : -320,
        "posY" : 0
    }
}

LvlsInfo = {
    "LvlDisponibles" : {
        "lvl1": True,
        "lvl2": True,
        "lvl3": True
    },
    "LvlCompletados":{
        "lvl1": True,
        "lvl2": True,
        "lvl3": False
    }
}

def main():
    
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Lights Out")
    icon = pygame.image.load('assets/img/icono.ico')
    pygame.display.set_icon(icon)

    intro(SCREEN)
    menu_principal(SCREEN, configJuego, LvlsInfo, elementosFondo)

main()
