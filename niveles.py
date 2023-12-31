import sys, pygame
from assets.defaults.button import Button
from assets.defaults.get_fonts import get_font
from assets.defaults.idioma import cargar_idioma
from assets.defaults.get_imgs import imgs_niveles
from carga import pantalla_de_carga
from lvl1 import pantalla_lvl1
from lvl2 import pantalla_lvl2
from lvl3 import pantalla_lvl3
from intro import intro

idioma = cargar_idioma()
imgs = imgs_niveles()
reloj = pygame.time.Clock()

edificio1 = ""
edificio2 = ""
edificio3 = ""


def recargarEdificios(LvlsInfo):
    global edificio1
    global edificio2
    global edificio3

    # identificamos que edificios estan disponibles y cuales no

    if LvlsInfo["LvlDisponibles"]["lvl1"] == True:
        if LvlsInfo["LvlCompletados"]["lvl1"] == True:
            edificio1 = imgs["edificios"]["edificio1"]["estado2"]
        else:
            edificio1 = imgs["edificios"]["edificio1"]["estado1"]

    if LvlsInfo["LvlDisponibles"]["lvl2"] == True:
        if LvlsInfo["LvlCompletados"]["lvl2"] == True:
            edificio2 = imgs["edificios"]["edificio2"]["estado3"]
        else:
            edificio2 = imgs["edificios"]["edificio2"]["estado2"]
    else:
        edificio2 = imgs["edificios"]["edificio2"]["estado1"]

    if LvlsInfo["LvlDisponibles"]["lvl3"] == True:
        if LvlsInfo["LvlCompletados"]["lvl3"] == True:
            edificio3 = imgs["edificios"]["edificio3"]["estado3"]
        else:
            edificio3 = imgs["edificios"]["edificio3"]["estado2"]
    else:
        edificio3 = imgs["edificios"]["edificio3"]["estado1"]

def mover_fondo(SCREEN, img, elemento, velocidad):
    posX = (elemento["posX"] - velocidad) % 1280
    SCREEN.blit(img, (posX - 1280, elemento["posY"]))
    if posX < 1280:
        SCREEN.blit(img, (posX, elemento["posY"]))
    elemento["posX"] = posX

def niveles(SCREEN, configJuego, LvlsInfo, elementosFondo):
    """
    Esta función muestra la pantalla de selección de niveles del juego LightsOut.
    Recibe como parámetros:
    - SCREEN: la pantalla del juego.
    - configJuego: un diccionario con la configuración del juego.
    - LvlsInfo: un diccionario con la información de los niveles.
    - elementosFondo: un diccionario con los elementos de fondo del juego.
    """
    # Carga la música si no está cargada y la reproduce en bucle
    if configJuego["indiceMusic"] != 1:
        configJuego["indiceMusic"] = 1
        pygame.mixer.music.load(f"assets/songs/musica{configJuego['indiceMusic']}.wav")
        pygame.mixer.music.set_volume(configJuego["Volumen"])
        pygame.mixer.music.play(-1)

    # Recarga los edificios en la pantalla
    recargarEdificios(LvlsInfo)
        
    # Crea los botones de selección de niveles y el botón de regreso
    btnLvl1 = Button(image1=pygame.transform.scale(imgs["caja"], (270, 100)), pos=(300, 200),  text_input=idioma[configJuego["Idioma"]]["Niveles"]["Opcion1"], font=get_font(35), base_color="#d7fcd4", hovering_color="#f9c447")
    btnLvl2 = Button(image1=pygame.transform.scale(imgs["caja"], (270, 100)), pos=(660, 200), text_input=idioma[configJuego["Idioma"]]["Niveles"]["Opcion2"], font=get_font(35), base_color="#d7fcd4", hovering_color="#f9c447")
    btnLvl3 = Button(image1=pygame.transform.scale(imgs["caja"], (270, 100)), pos=(1050, 200), text_input=idioma[configJuego["Idioma"]]["Niveles"]["Opcion3"], font=get_font(35), base_color="#d7fcd4", hovering_color="#f9c447")
    btnBack = Button(image1=None, pos=(50,50), text_input="←", font=get_font(75), base_color="White", hovering_color="Red")

    # Bucle principal de la pantalla de selección de niveles
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Mueve los elementos de fondo de la pantalla
        mover_fondo(SCREEN ,imgs["ciudad"] ,elementosFondo["ciudad"], 2)
        mover_fondo(SCREEN ,imgs["luna"] ,elementosFondo["luna"], 0.5)
        mover_fondo(SCREEN ,imgs["nube"] ,elementosFondo["nube"], 1)

        # Muestra los edificios en la pantalla
        SCREEN.blit(edificio1, (0, 0))
        SCREEN.blit(edificio2, (0, 0))
        SCREEN.blit(edificio3, (0, 0))
        SCREEN.blit(imgs["pasto"], (0, 0))
        
        # Actualiza los botones en la pantalla
        btnBack.update(SCREEN)
        btnLvl1.update(SCREEN)
        btnLvl2.update(SCREEN)
        btnLvl3.update(SCREEN)

        # Cambia el color de los botones según los niveles disponibles
        if LvlsInfo["LvlDisponibles"]["lvl1"] == True:
            btnLvl1.changeColor(PLAY_MOUSE_POS) 

        if LvlsInfo["LvlDisponibles"]["lvl2"] == True:
            btnLvl2.changeColor(PLAY_MOUSE_POS)

        if LvlsInfo["LvlDisponibles"]["lvl3"] == True:
            btnLvl3.changeColor(PLAY_MOUSE_POS)

        btnBack.changeColor(PLAY_MOUSE_POS)

        # Detecta los eventos de la pantalla
        for event in pygame.event.get():
            
            # Cierra el juego si se presiona la X de la ventana
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

            # Detecta si se presiona algún botón
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Regresa a la pantalla anterior si se presiona el botón de regreso
                if btnBack.checkForInput(PLAY_MOUSE_POS):
                    return SCREEN , configJuego, LvlsInfo, elementosFondo
                # Carga el nivel 1 si se presiona el botón correspondiente y el nivel está disponible
                if btnLvl1.checkForInput(PLAY_MOUSE_POS) and LvlsInfo["LvlDisponibles"]["lvl1"] == True:
                    pantalla_de_carga(SCREEN, configJuego)
                    SCREEN , configJuego, LvlsInfo, elementosFondo = pantalla_lvl1(SCREEN , configJuego, LvlsInfo, elementosFondo)
                    recargarEdificios(LvlsInfo)
                # Carga el nivel 2 si se presiona el botón correspondiente y el nivel está disponible
                if btnLvl2.checkForInput(PLAY_MOUSE_POS) and LvlsInfo["LvlDisponibles"]["lvl2"] == True:
                    pantalla_de_carga(SCREEN, configJuego)
                    SCREEN , configJuego, LvlsInfo, elementosFondo = pantalla_lvl2(SCREEN , configJuego, LvlsInfo, elementosFondo)
                    recargarEdificios(LvlsInfo)
                # Carga el nivel 3 si se presiona el botón correspondiente y el nivel está disponible
                if btnLvl3.checkForInput(PLAY_MOUSE_POS) and LvlsInfo["LvlDisponibles"]["lvl3"] == True:
                    pantalla_de_carga(SCREEN, configJuego)
                    SCREEN , configJuego, LvlsInfo, elementosFondo = pantalla_lvl3(SCREEN , configJuego, LvlsInfo, elementosFondo)
                    recargarEdificios(LvlsInfo)
                # Carga la música si no está cargada y la reproduce en bucle
                if configJuego["indiceMusic"] != 1:
                    configJuego["indiceMusic"] = 1
                    pygame.mixer.music.load(f"assets/songs/musica{configJuego['indiceMusic']}.wav")
                    pygame.mixer.music.set_volume(configJuego["Volumen"])
                    pygame.mixer.music.play(-1)

        # Actualiza la pantalla y establece el límite de FPS
        reloj.tick(20)
        pygame.display.update()
