import sys, pygame
from assets.defaults.button import Button
from assets.defaults.get_fonts import get_font
from assets.defaults.idioma import cargar_idioma
from assets.defaults.get_imgs import imgs_optionsLvls
from intro import intro

idioma = cargar_idioma()
imgs = imgs_optionsLvls()

def opciones_juego(SCREEN , configJuego, LvlsInfo, elementosFondo):
    """
    Esta función muestra la pantalla de opciones del juego, donde el usuario puede elegir entre continuar, reiniciar o salir del nivel actual.
    """
            
    # Se reduce el volumen del juego y se actualiza el volumen de la música 
    configJuego["Volumen"] /= 4
    pygame.mixer.music.set_volume(configJuego["Volumen"])
    
    # Se muestra una imagen oscura en la pantalla y se reproduce un sonido de pausa
    SCREEN.blit(imgs["oscuro"], (0,0))
    pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/pausar.ogg"))

    # Se cambia el título de la ventana
    pygame.display.set_caption(f'{idioma[configJuego["Idioma"]]["OpcionesLvl"]["Titulo"]} - {idioma[configJuego["Idioma"]]["Nivel1"]["Titulo"]}')

    # Se imprime el título de la pantalla encima de la caja
    MENU_TEXT = get_font(75).render(idioma[configJuego["Idioma"]]["OpcionesLvl"]["Titulo"], True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
    SCREEN.blit(MENU_TEXT, MENU_RECT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Si el usuario cierra la ventana, se llama a la función intro y se cierra el juego
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Si el usuario presiona la tecla ESC, se restaura el volumen del juego y se retorna la acción "continuar"
                        configJuego["Volumen"] *= 4
                        pygame.mixer.music.set_volume(configJuego["Volumen"])
                        accion = "continuar"
                        return SCREEN , configJuego, LvlsInfo, elementosFondo, accion

            if event.type == pygame.MOUSEBUTTONDOWN: # detectamos el click del mouse
                if btnContinuar.checkForInput(OPTIONS_MOUSE_POS): 
                    # Si el usuario hace clic en el botón "Continuar", se restaura el volumen del juego, se reproduce un sonido de despausa y se retorna la acción "continuar"
                    configJuego["Volumen"] *= 4
                    pygame.mixer.music.set_volume(configJuego["Volumen"])
                    accion = "continuar"
                    pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/despausar.mp3"))
                    return SCREEN , configJuego, LvlsInfo, elementosFondo, accion
                
                if btnReiniciar.checkForInput(OPTIONS_MOUSE_POS): 
                    # Si el usuario hace clic en el botón "Reiniciar", se restaura el volumen del juego, se reproduce un sonido de despausa y se retorna la acción "reiniciar"
                    configJuego["Volumen"] *= 4
                    pygame.mixer.music.set_volume(configJuego["Volumen"])
                    accion = "reiniciar"
                    pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/despausar.mp3"))
                    return SCREEN , configJuego, LvlsInfo, elementosFondo, accion 
                
                if btnSalir.checkForInput(OPTIONS_MOUSE_POS): 
                    # Si el usuario hace clic en el botón "Salir", se restaura el volumen del juego, se reproduce un sonido de despausa y se retorna la acción "salir"
                    configJuego["Volumen"] *= 4
                    pygame.mixer.music.set_volume(configJuego["Volumen"])
                    accion = "salir"
                    pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/despausar.mp3"))
                    return SCREEN , configJuego, LvlsInfo, elementosFondo , accion
                
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        letra = 40
        if configJuego["Idioma"] == "es": 
            letra = 32 

        # Se crean los botones "Continuar", "Reiniciar" y "Salir"
        btnContinuar = Button(image1=pygame.transform.scale(imgs["caja"], (300, 100)), pos=(640, 250),  text_input=idioma[configJuego["Idioma"]]["OpcionesLvl"]["Reanudar"], font=get_font(letra), base_color="#d7fcd4", hovering_color="#36ddd4")
        btnReiniciar = Button(image1=pygame.transform.scale(imgs["caja"], (300, 100)), pos=(640, 400), text_input=idioma[configJuego["Idioma"]]["OpcionesLvl"]["Reiniciar"], font=get_font(letra), base_color="#d7fcd4", hovering_color="#3d91da")
        btnSalir = Button(image1=pygame.transform.scale(imgs["caja"], (300, 100)), pos=(640, 550), text_input=idioma[configJuego["Idioma"]]["OpcionesLvl"]["Salir"], font=get_font(letra), base_color="#d7fcd4", hovering_color="Red")

        for button in [btnContinuar, btnReiniciar, btnSalir]: # recorremos los botones
            button.changeColor(OPTIONS_MOUSE_POS) # cambiamos el color de los botones
            button.update(SCREEN) # actualizamos los botones

        # Se actualiza la pantalla
        pygame.display.update()