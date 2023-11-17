import sys, pygame
from niveles import niveles
from opciones import opciones
from assets.defaults.button import Button
from assets.defaults.idioma import cargar_idioma
from assets.defaults.get_fonts import get_font
from assets.defaults.get_imgs import imgs_menu_principal
from cambiarAvatar import pantallaCambiarAvatar
from carga import pantalla_de_carga
from historia import historia
from intro import intro

reloj = pygame.time.Clock()
idioma = cargar_idioma()

def mover_fondo(SCREEN, img, elemento, velocidad):
    posX = (elemento["posX"] - velocidad) % 1280
    SCREEN.blit(img, (posX - 1280, elemento["posY"]))
    if posX < 1280:
        SCREEN.blit(img, (posX, elemento["posY"]))
    elemento["posX"] = posX

def menu_principal(SCREEN , configJuego, LvlsInfo, elementosFondo):
    """
    Función que muestra el menú principal del juego y permite al usuario navegar a través de las diferentes opciones.
    """
    # Cargamos la música y la reproducimos en bucle
    if configJuego["indiceMusic"] != 1:
        configJuego["indiceMusic"] = 1
        pygame.mixer.music.load(f"assets/songs/musica{configJuego['indiceMusic']}.wav")
        pygame.mixer.music.set_volume(configJuego["Volumen"])
        pygame.mixer.music.play(-1)

    # Cargamos las imágenes del menú principal
    imgs = imgs_menu_principal(configJuego["Idioma"])
    
    # Establecemos el título de la ventana
    pygame.display.set_caption(idioma[configJuego["Idioma"]]["MenuInicial"]["Titulo"])

    while True:
        # Movemos los elementos de fondo en bucle
        mover_fondo(SCREEN ,imgs["ciudad"] ,elementosFondo["ciudad"], 2)
        mover_fondo(SCREEN ,imgs["luna"] ,elementosFondo["luna"], 0.5)
        mover_fondo(SCREEN ,imgs["nube"] ,elementosFondo["nube"], 1)

        # Obtenemos la posición del mouse
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Cargamos la imagen del título del menú
        MENU_IMAGE = pygame.image.load("assets/img/titulo.png")
        # Obtenemos el rectángulo de la imagen y lo posicionamos en el centro de la pantalla
        MENU_RECT = MENU_IMAGE.get_rect(center=(640, 100))

        # Dibujamos la imagen en la pantalla
        SCREEN.blit(MENU_IMAGE, MENU_RECT)

        # Creamos los botones del menú
        PLAY_BUTTON = Button(image1=pygame.transform.scale(imgs["botones"][configJuego["Idioma"]]["jugar"]["normal"], (550, 100)), pos=(640, 250),  text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="#48ba84", image2=pygame.transform.scale(imgs["botones"][configJuego["Idioma"]]["jugar"]["presionado"], (550, 100)))
        OPTIONS_BUTTON = Button(image1=pygame.transform.scale(imgs["botones"][configJuego["Idioma"]]["opciones"]["normal"], (550, 100)), pos=(640, 370), text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="#48ba84", image2=pygame.transform.scale(imgs["botones"][configJuego["Idioma"]]["opciones"]["presionado"], (550, 100)))
        CHANGEAVATAR_BUTTON = Button(image1=pygame.transform.scale(imgs["botones"][configJuego["Idioma"]]["avatar"]["normal"], (550, 100)), pos=(640, 490), text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="#48ba84", image2=pygame.transform.scale(imgs["botones"][configJuego["Idioma"]]["avatar"]["presionado"], (550, 100)))
        QUIT_BUTTON = Button(image1=pygame.transform.scale(imgs["botones"][configJuego["Idioma"]]["atras"]["normal"], (550, 100)), pos=(640, 610), text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="#48ba84", image2=pygame.transform.scale(imgs["botones"][configJuego["Idioma"]]["atras"]["presionado"], (550, 100)))

        # Actualizamos los botones y cambiamos su color si el mouse está sobre ellos
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, CHANGEAVATAR_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        # Detectamos los eventos del usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Si el usuario cierra la ventana, cerramos el juego
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si el usuario hace click en un botón, realizamos la acción correspondiente
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if configJuego["historia"]:
                        pantalla_de_carga(SCREEN, configJuego)
                        configJuego["historia"] = False
                    historia(SCREEN, configJuego["personaje"], configJuego["Idioma"])
                    SCREEN , configJuego, LvlsInfo, elementosFondo = niveles(SCREEN , configJuego, LvlsInfo, elementosFondo)
                    pygame.display.set_caption(idioma[configJuego["Idioma"]]["MenuInicial"]["Titulo"])
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    SCREEN , configJuego, LvlsInfo, elementosFondo = opciones(SCREEN , configJuego, LvlsInfo, elementosFondo)
                    pygame.display.set_caption(idioma[configJuego["Idioma"]]["MenuInicial"]["Titulo"])
                if CHANGEAVATAR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    SCREEN , configJuego = pantallaCambiarAvatar(SCREEN , configJuego)
                    pygame.display.set_caption(idioma[configJuego["Idioma"]]["MenuInicial"]["Titulo"])
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # Actualizamos la pantalla y establecemos el límite de FPS
        pygame.display.update()
        reloj.tick(30)