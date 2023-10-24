import sys, pygame
from assets.defaults.button import Button
from assets.defaults.get_fonts import get_font
from assets.defaults.idioma import cargar_idioma
from assets.defaults.get_imgs import imgs_opciones
from intro import intro

idioma = cargar_idioma()
imgs = imgs_opciones()

def opciones(SCREEN , configJuego, LvlsInfo, elementosFondo):
    """
    Esta función muestra la pantalla de opciones del juego y permite al usuario cambiar la configuración del juego.
    """
    # Carga la música y la reproduce en bucle si no se está reproduciendo actualmente
    if configJuego["indiceMusic"] != 1:
        configJuego["indiceMusic"] = 1
        pygame.mixer.music.load(f"assets/songs/musica{configJuego['indiceMusic']}.wav")
        pygame.mixer.music.set_volume(configJuego["Volumen"])
        pygame.mixer.music.play(-1)

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # Cambia el título de la ventana
        pygame.display.set_caption(idioma[configJuego["Idioma"]]["Opciones"]["Titulo"])

        # Limpia la pantalla para la nueva pantalla
        SCREEN.blit(imgs["azul"], (0, 0))

        # Genera el título de la pantalla
        MENU_TEXT = get_font(100).render(idioma[configJuego["Idioma"]]["Opciones"]["Titulo"], True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Botón de regresar
        OPTIONS_BACK = Button(image1=None, pos=(50,50), text_input="←", font=get_font(75), base_color="White", hovering_color="Red")

        # Volumen
        txtVolumen = get_font(45).render(idioma[configJuego["Idioma"]]["Opciones"]["Opcion2"], True, "White")
        SCREEN.blit(txtVolumen, (100, 450))
        
        # Imprime el porcentaje del volumen actual
        txtPorcentaje = get_font(45).render(str(int(configJuego["Volumen"] * 100)) + "%", True, "White")
        SCREEN.blit(txtPorcentaje, (850, 450))
        btnVolumen1 = Button(image1=pygame.transform.scale(imgs["caja"], (75, 50)), pos=(1100, 450), text_input="↑", font=get_font(45), base_color="White", hovering_color="Green")
        btnVolumen2 = Button(image1=pygame.transform.scale(imgs["caja"], (75, 50)), pos=(1100, 500), text_input="↓", font=get_font(45), base_color="White", hovering_color="Green")

        # Idioma
        txtIdiomas = get_font(45).render(idioma[configJuego["Idioma"]]["Opciones"]["Opcion1"], True, "White")
        SCREEN.blit(txtIdiomas, (100, 300))
        btnIdioma1 = Button(image1=pygame.transform.scale(imgs["caja"], (350, 100)), pos=(1000, 320), text_input=idioma[configJuego["Idioma"]]["Idioma"], font=get_font(45), base_color="White", hovering_color="Green")

        # Recorre los botones, cambia el color y los actualiza
        for button in [btnIdioma1, btnVolumen1, btnVolumen2, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        # Detecta los eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return SCREEN , configJuego, LvlsInfo, elementosFondo
                if btnVolumen1.checkForInput(OPTIONS_MOUSE_POS):
                    if  configJuego["Volumen"] < 1:
                        configJuego["Volumen"] += 0.01
                        pygame.mixer.music.set_volume(configJuego["Volumen"])
                if btnVolumen2.checkForInput(OPTIONS_MOUSE_POS):
                    if configJuego["Volumen"] > 0:
                        configJuego["Volumen"] -= 0.01
                        pygame.mixer.music.set_volume(configJuego["Volumen"])
                if btnIdioma1.checkForInput(OPTIONS_MOUSE_POS):
                    if configJuego["Idioma"] == "es":
                        configJuego["Idioma"] = "en" 
                    else:
                        configJuego["Idioma"] = "es"

            # Comprueba si el valor del volumen tiene más de 2 decimales
            if len(str(configJuego["Volumen"])) > 4:
                # Si el valor número 5 es un 9, redondea el valor del volumen hacia arriba
                if str(configJuego["Volumen"])[4] == "9":
                    configJuego["Volumen"] = float(str(configJuego["Volumen"])[:4]) + 0.01
                else:
                    configJuego["Volumen"] = float(str(configJuego["Volumen"])[:4])
                pygame.mixer.music.set_volume(configJuego["Volumen"])

        pygame.display.update()