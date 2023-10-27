import sys, pygame, random, time
from assets.defaults.button import Button
from assets.defaults.get_fonts import get_font
from assets.defaults.idioma import cargar_idioma
from assets.defaults.get_imgs import imgs_lvl2
from carga import pantalla_de_carga
from opciones_juego import opciones_juego
from intro import intro

idioma = cargar_idioma()
reloj = pygame.time.Clock()

# JEJE Inicializamos las variables

segundoUltimoFoco = 0
segundoAnterior = 0 
infoPersonaje = 0
LimiteConsumo = 0
segundoAccion = 0
consumoPorSeg = 0
consumoTotal = 0
tiempoPasado = 0
focoPorSeg = 5
barraMax = 0
focos = {}
color = ()
fps = 0
powerUps = {}
imgs = {}
teclaEstado = 1
subida = 0

quietoD = ""
quietoI = ""
derecha = []
izquierda = [] 

#funcion para reiniciar las variables
def reiniciar(personaje):
    """
    Esta función reinicia todas las variables globales necesarias para el correcto funcionamiento del juego.
    Recibe como parámetro el nombre del personaje seleccionado por el usuario.
    """
    global segundoUltimoFoco
    global segundoAnterior
    global consumoPorSeg
    global LimiteConsumo
    global consumoTotal
    global infoPersonaje
    global segundoAccion
    global tiempoPasado
    global focoPorSeg
    global izquierda
    global powerUps
    global barraMax
    global quietoD
    global quietoI
    global derecha
    global subida
    global focos
    global color
    global imgs
    global fps

    # Carga las imágenes del personaje seleccionado
    quietoD = pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje1.png")
    quietoI = pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje4.png")

    # Carga las imágenes del personaje seleccionado en movimiento hacia la derecha
    derecha = [
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje1.png"),
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje2.png"),
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje3.png")]

    # Carga las imágenes del personaje seleccionado en movimiento hacia la izquierda
    izquierda = [
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje4.png"),
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje5.png"),
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje6.png")]
        
    # Reinicia todas las variables globales necesarias para el correcto funcionamiento del juego
    segundoUltimoFoco = 0
    color = (0, 255, 0)
    segundoAnterior = 0
    LimiteConsumo = 360 # el limite son 350 watts 
    segundoAccion = 0
    consumoPorSeg = 2 # 2 watt por segundo
    consumoTotal = 0 # el consumo total de los focos
    tiempoPasado = 0
    focoPorSeg = 4
    barraMax = 275
    fps = 10
    subida = 1

    # Define los power-ups disponibles en el juego
    powerUps = {
        "powerUpsActivos": 0,
        "powerUpsTotales": 0,
        "probabilidad": 20,
        "estados": { 
            "reducirConsumo": {
                "nombre": "reducirConsumo",
                "PX": 0,
                "piso": 0,
                "activo": False,
                "suelto": False,
                "tiempo": 10,
                "alto": 40
            },
            "Velocidad": {
                "nombre": "velocidad",
                "PX": 0,
                "piso": 0,
                "activo": False,
                "suelto": False,
                "tiempo": 10,
                "alto": 40
            }
        }
    }

    # Define los focos disponibles en el juego
    focos = {
        "focosFuncionales": 5,
        "focosEncendidos": 0,
        "focosFundidos": 0,
        "focosTotales": 5,
        "focosApagados": 0,
        "focosEstado": { # 0 = apagado, 1 = encendido, 2 = emepezando a calentarce, 3 = a punto de fundirse, 4 = fundido
            "foco1": {
                "numero": 1,
                "estado": 0,
                "ultimoEstado": 1,
                "tiempoEncendido": 0,
                "posicion": (341, 286),
                "apagadorX1": 305,
                "apagadorX2": 312,
                "abierta": False,
                "posPuerta": (300, 335),
                "piso": 2
            },
            "foco2": {
                "numero": 2,
                "estado": 0,
                "ultimoEstado": 1,
                "tiempoEncendido": 0,
                "posicion": (613, 286),
                "apagadorX1": 583,
                "apagadorX2": 590,
                "abierta": False,
                "posPuerta": (572, 335),
                "piso": 2
            },
            "foco3": {
                "numero": 3,
                "estado": 0,
                "ultimoEstado": 1,
                "tiempoEncendido": 0,
                "posicion": (916, 286),
                "apagadorX1": 884,
                "apagadorX2": 891,
                "abierta": False,
                "posPuerta": (879, 335),
                "piso": 2
            },
            "foco4": {
                "numero": 4,
                "estado": 0,
                "ultimoEstado": 1,
                "tiempoEncendido": 0,
                "posicion": (498, 465),
                "apagadorX1": 462,
                "apagadorX2": 469,
                "abierta": False,
                "posPuerta": (456, 513),
                "piso": 1
            },
            "foco5": {
                "numero": 5,
                "estado": 0,
                "ultimoEstado": 1,
                "tiempoEncendido": 0,
                "posicion": (832, 465),
                "apagadorX1": 791,
                "apagadorX2": 798,
                "abierta": False,
                "posPuerta": (792, 513),
                "piso": 1
            }
        }
    }

    # Define la información del personaje seleccionado
    infoPersonaje = {
        "Y": 0,
        "X": 0,
        "PX": 980,
        "PY": 530,
        "ancho": 50,
        "velocidad": 10,
        "direccion": "izquierda",
        "cuentaPasos": 0,
        "quieto": True,
        "piso": 1
    }

# funcion para mostrar una pantalla de pausa antes de iniciar
def pausaInicio(SCREEN, configJuego):
    """
    Esta función muestra una pantalla de pausa al inicio del nivel 2 del juego LightsOut.
    La pantalla muestra instrucciones y la interfaz del juego.
    El usuario debe presionar cualquier tecla para continuar.
    La función recibe como parámetros la pantalla del juego (SCREEN) y la configuración del juego (configJuego).
    La función modifica el volumen de la música del juego y lo restaura al finalizar la pausa.
    """
    global infoPersonaje
    detener = True
    parte = 1
    configJuego["Volumen"] /= 4
    pygame.mixer.music.set_volume(configJuego["Volumen"])
    while detener:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                parte += 1            
                
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()
        SCREEN.blit(imgs["fondo"], (0,0))
        SCREEN.blit(izquierda[0], (int(infoPersonaje["PX"]), int(infoPersonaje["PY"])))
        SCREEN.blit(imgs["sombra_lvl2"], (0,0))
        SCREEN.blit(imgs["sombras"]["sombra1"], (0,0))
        SCREEN.blit(imgs["sombras"]["sombra2"], (0,0))
        SCREEN.blit(imgs["sombras"]["sombra3"], (0,0))
        SCREEN.blit(imgs["sombras"]["sombra4"], (0,0))
        SCREEN.blit(imgs["sombras"]["sombra5"], (0,0))
        if parte == 1:
            # Mostramos las instrucciones del juego
            SCREEN.blit(imgs["instrucciones"], (0,0))
        elif parte == 2:
            # Mostramos la interfaz del juego
            SCREEN.blit(imgs["interface"], (0, 0))
        else:
            # Restauramos el volumen de la música del juego y salimos del ciclo while
            configJuego["Volumen"] *= 4
            pygame.mixer.music.set_volume(configJuego["Volumen"])
            detener = False

        # Imprimimos texto de presionar cualquier tecla para continuar
        Text_text = get_font(20).render(idioma[configJuego["Idioma"]]["Juego"]["Preciona"], True, "#ffffff")
        Text_rect = Text_text.get_rect(center=(640, 700))
        SCREEN.blit(Text_text, Text_rect)

        pygame.display.flip()
        reloj.tick(10)

# funcion para pintar al personaje
def pintarPersonaje(SCREEN, accion = "caminar"):
    """
    Dibuja al personaje en la pantalla según su estado y acción.
    """
    global infoPersonaje
    global fps

    # Verificamos si el powerUp de velocidad está activo
    if powerUps["estados"]["Velocidad"]["activo"] == True:
        infoPersonaje["velocidad"] = 15 # aumentamos la velocidad
    else:
        infoPersonaje["velocidad"] = 10 # volvemos a la velocidad normal

    # fps
    reloj.tick(fps)

    if accion == "caminar":
        # Colocamos el personaje según su estado
        if (infoPersonaje["cuentaPasos"] + 1) >= 3:
            infoPersonaje["cuentaPasos"] = 0

        if infoPersonaje["direccion"] == "derecha" and infoPersonaje["quieto"] != True:
            SCREEN.blit(derecha[infoPersonaje["cuentaPasos"] // 1], (int(infoPersonaje["PX"]), int(infoPersonaje["PY"])))
            infoPersonaje["cuentaPasos"] += 1
            
        elif infoPersonaje["direccion"] == "izquierda" and infoPersonaje["quieto"] != True:
            SCREEN.blit(izquierda[infoPersonaje["cuentaPasos"] // 1], (int(infoPersonaje["PX"]), int(infoPersonaje["PY"])))
            infoPersonaje["cuentaPasos"] += 1

        elif infoPersonaje["direccion"] == "derecha" and infoPersonaje["quieto"] == True:
            SCREEN.blit(quietoD, (int(infoPersonaje["PX"]), int(infoPersonaje["PY"])))

        elif infoPersonaje["direccion"] == "izquierda" and infoPersonaje["quieto"] == True:
            SCREEN.blit(quietoI, (int(infoPersonaje["PX"]), int(infoPersonaje["PY"])))

        # Reiniciamos el estado del personaje
        infoPersonaje["quieto"] = False
    else:
        if infoPersonaje["direccion"] == "derecha":
            SCREEN.blit(quietoD, (int(infoPersonaje["PX"]), int(infoPersonaje["PY"])))
        elif infoPersonaje["direccion"] == "izquierda":
            SCREEN.blit(quietoI, (int(infoPersonaje["PX"]), int(infoPersonaje["PY"])))

# funcion para mover el personaje
def moverPersonaje(SCREEN):
    """
    Mueve al personaje en la pantalla y realiza acciones dependiendo de las teclas presionadas.
    """
    global infoPersonaje
    global segundoAccion
    global tiempoPasado
    global focos

    keys = pygame.key.get_pressed() # eventos del teclado

    # Tecla A
    if keys[pygame.K_a] and infoPersonaje["PX"] > infoPersonaje["velocidad"] and infoPersonaje["PX"] - infoPersonaje["velocidad"] > 100:
        infoPersonaje["PX"] -= infoPersonaje["velocidad"]
        infoPersonaje["direccion"] = "izquierda"
        pintarPersonaje(SCREEN, accion="caminar")

    # Tecla D
    elif keys[pygame.K_d] and infoPersonaje["PX"] < 1000 :
        infoPersonaje["PX"] += infoPersonaje["velocidad"]
        infoPersonaje["direccion"] = "derecha"
        pintarPersonaje(SCREEN, accion="caminar")

    elif keys[pygame.K_w] and ((infoPersonaje["PX"] >= 205 and infoPersonaje["PX"] <= 252) or (infoPersonaje["ancho"] + infoPersonaje["PX"] >= 205 and infoPersonaje["PX"] + infoPersonaje["ancho"] <= 252)):
        if infoPersonaje["piso"] == 1 and segundoAccion != tiempoPasado:
            infoPersonaje["piso"] = 2
            infoPersonaje["PY"] -= 180
        elif segundoAccion != tiempoPasado:
            infoPersonaje["piso"] = 1
            infoPersonaje["PY"] += 180
        segundoAccion = tiempoPasado
        pintarPersonaje(SCREEN)   

    # Tecla Espacio
    elif keys[pygame.K_SPACE]:
        for foco in focos["focosEstado"].items(): # recorremos los focos
            if foco[1]["estado"] != 0 and foco[1]["estado"] != 4 and infoPersonaje["piso"] == foco[1]["piso"]: # verificamos si el foco esta apagado
                if infoPersonaje["PX"] >= foco[1]["apagadorX1"] - infoPersonaje["ancho"] and infoPersonaje["PX"] <= foco[1]["apagadorX2"] + infoPersonaje["ancho"]:
                    foco[1]["anteriorEstado"] = foco[1]["estado"]
                    foco[1]["estado"] = 0
                    focos["focosEncendidos"] -= 1
                    focos["focosApagados"] += 1
                    # soltarPowerUp()
                    break
        pintarPersonaje(SCREEN, accion="apagar")

    #personaje quieto
    else:
        infoPersonaje["cuentaPasos"] = 1
        infoPersonaje["quieto"] = True
        pintarPersonaje(SCREEN, accion="quieto")

# función pinta las teclas que se puede usar
def pintarTeclas(SCREEN):
    """
    Dibuja las teclas de acción en la pantalla dependiendo de la posición del personaje y los focos cercanos.
    """
    global infoPersonaje
    global segundoAccion
    global teclaEstado
    global focos
    for foco in focos["focosEstado"].items(): # recorremos los focos
        if foco[1]["estado"] != 0 and foco[1]["estado"] != 4 and infoPersonaje["piso"] == foco[1]["piso"]: # verificamos si el foco esta apagado
            if infoPersonaje["PX"] >= foco[1]["apagadorX1"] - infoPersonaje["ancho"] and infoPersonaje["PX"] <= foco[1]["apagadorX2"] + infoPersonaje["ancho"]:
                SCREEN.blit(imgs[f"espacio{teclaEstado}"], (int(infoPersonaje["PX"]) - 20, int(infoPersonaje["PY"]) + 80))
                teclaEstado += 1

    if (infoPersonaje["PX"] >= 205 and infoPersonaje["PX"] <= 252) or (infoPersonaje["ancho"] + infoPersonaje["PX"] >= 205 and infoPersonaje["PX"] + infoPersonaje["ancho"] <= 252):
        SCREEN.blit(imgs[f"w{teclaEstado}"], (int(infoPersonaje["PX"]), int(infoPersonaje["PY"]) - 50))
        teclaEstado += 1

    if teclaEstado > 2:
        teclaEstado = 1

# pinta las puertas abiertas
def pintarPuerta(SCEEN):
    """
    Dibuja la puerta en la pantalla basándose en el estado de las luces.
    """
    global focos
    for foco in focos["focosEstado"].items(): # recorremos los focos
        if foco[1]["abierta"] == True:
            SCEEN.blit(imgs["abierta"], foco[1]["posPuerta"])
            
# funcion para pintar los focos
def pintarFocos(SCREEN, segundero):
    """
    Pinta los focos en la pantalla y actualiza su estado según el tiempo transcurrido.
    También se encarga de encender nuevos focos y de actualizar el consumo de energía.
    """
    global segundoUltimoFoco
    global segundoAnterior
    global consumoPorSeg
    global consumoTotal
    global tiempoPasado
    global focoPorSeg
    global powerUps
    global focos
    global color

    # Verificamos si el tiempo ha cambiado
    if segundero != segundoAnterior:
        # Verificamos si el consumo por segundo es 2
        if consumoPorSeg == 2:
            consumoPorSeg = 1
        else:
            consumoPorSeg = 2
        tiempoPasado += 1 # Si el tiempo cambió, sumamos un segundo
        # Verificamos si el powerUp de reducir consumo está activo
        if powerUps["estados"]["reducirConsumo"]["activo"] == True:
            # Reducimos a la mitad el consumo de los focos encendidos
            consumoTotal += (1 / 2) * focos["focosEncendidos"]
        else:
            # Sumamos el consumo de los focos encendidos
            consumoTotal += consumoPorSeg * focos["focosEncendidos"]
        segundoAnterior = segundero # Actualizamos el tiempo anterior

        # Recorremos los focos
        for foco in focos["focosEstado"].items():
            # Verificamos si la puerta está abierta
            if foco[1]["abierta"] == True:
                foco[1]["abierta"] = False
                pygame.mixer.Sound("assets/sounds/cerrarPuerta2.wav").play()
            # Verificamos si el foco está encendido
            if foco[1]["estado"] == 1 or foco[1]["estado"] == 2 or foco[1]["estado"] == 3:
                # Si el foco está encendido, sumamos un segundo
                foco[1]["tiempoEncendido"] += 1 

                # Verificamos si el foco está encendido por más de 70 segundos
                if foco[1]["tiempoEncendido"] >= 50:
                    foco[1]["estado"] = 4
                    foco[1]["ultimoEstado"] = 4
                    focos["focosFundidos"] += 1
                    focos["focosEncendidos"] -= 1
                    pygame.mixer.Sound("assets/sounds/romper.wav").play() # Sonido de fundir foco

                # Verificamos si el foco está encendido por más de 45 segundos
                elif foco[1]["tiempoEncendido"] >= 30:
                    foco[1]["estado"] = 3
                    foco[1]["ultimoEstado"] = 3

                # Verificamos si el foco está encendido por más de 30 segundos
                elif foco[1]["tiempoEncendido"] >= 20:
                    foco[1]["estado"] = 2
                    foco[1]["ultimoEstado"] = 2

    # Verificamos si han pasado 5 segundos desde que se fundió el último foco
    if segundoUltimoFoco + focoPorSeg <= tiempoPasado and focos["focosEncendidos"] != 5 - focos["focosFundidos"]:
        segundoUltimoFoco = tiempoPasado # Actualizamos el tiempo del último foco encendido
        numFoco = 0
        while True:
            # Elegimos un foco al azar
            numFoco = random.randint(1, focos["focosTotales"])
            # Verificamos si el foco está apagado
            if focos["focosEstado"][f"foco{numFoco}"]["estado"] == 0:
                break
        # Abrimos la puerta
        focos["focosEstado"][f"foco{numFoco}"]["abierta"] = True
        pygame.mixer.Sound("assets/sounds/abrirPuerta.wav").play() # Sonido de abrir puerta
        # Encendemos el foco
        focos["focosEstado"][f"foco{numFoco}"]["estado"] = focos["focosEstado"][f"foco{numFoco}"]["ultimoEstado"]
        # Sumamos un foco encendido
        focos["focosEncendidos"] += 1
        pygame.mixer.Sound("assets/sounds/prenderFoco.wav").play() # Sonido de encender foco

    # Pintamos los focos encendidos
    for foco in focos["focosEstado"].items():
        # Verificamos si el foco está apagado
        if foco[1]["estado"] != 0 and foco[1]["estado"] != 4:
            # Colocamos el foco en pantalla
            SCREEN.blit(imgs[f"bombilla{foco[1]['estado']}"], foco[1]["posicion"])
        else:
            SCREEN.blit(imgs[f"sombras"][f"sombra{foco[1]['numero']}"], (0, 0))
def perder(SCREEN, configJuego, LvlsInfo, elementosFondo):
    global focos
    pygame.mixer.Sound("assets/sounds/perder.ogg").play() # reproducimos el sonido en bucle
    configJuego["Volumen"] /= 4 # bajamos el volumen de la musica
    pygame.mixer.music.set_volume(configJuego["Volumen"])
    pausa = True
    moverPersonaje(SCREEN)
    for foco in focos["focosEstado"].items(): # recorremos los focos
            SCREEN.blit(imgs["bombilla0"], foco[1]["posicion"]) # colocamos el foco en pantalla
            SCREEN.blit(imgs[f"sombras"][f"sombra{foco[1]['numero']}"], (0, 0))
    pygame.display.flip()
    time.sleep(2)
    pygame.image.save(SCREEN, "assets/img/pantalla.png")
    ultimoFrame = pygame.image.load("assets/img/pantalla.png")
    while True:
        SCREEN.blit(ultimoFrame, (0,0))
        SCREEN.blit(imgs["oscuro"], (0,0))

        TITULO_TEXT = get_font(100).render(idioma[configJuego["Idioma"]]["Juego"]["Perdiste"], True, "#a1040f")
        TITULO_RECT = TITULO_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(TITULO_TEXT, TITULO_RECT)

        Text_text = get_font(20).render(idioma[configJuego["Idioma"]]["Juego"]["Preciona"], True, "#ffffff")
        Text_rect = Text_text.get_rect(center=(640, 500))
        SCREEN.blit(Text_text, Text_rect)

        perder_text = get_font(27).render(idioma[configJuego["Idioma"]]["perder"]["t1"], True, "#FFA500")
        perder_rect = perder_text.get_rect(center=(640, 400))
        SCREEN.blit(perder_text, perder_rect)

        pygame.display.flip()
        if pausa == True:
            time.sleep(1)
            pygame.event.clear(pygame.KEYDOWN)
            pausa = False
        
        for event in pygame.event.get():
            # si preciona cualquier tecla retorna al menu principal
            if event.type == pygame.KEYDOWN:
                # subimos el volumen de la musica
                configJuego["Volumen"] *= 4
                pygame.mixer.music.set_volume(configJuego["Volumen"])
                pygame.mixer.Sound("assets/sounds/viento.wav").stop()
                return SCREEN , configJuego, LvlsInfo, elementosFondo
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

def ganar(SCREEN, configJuego, LvlsInfo, elementosFondo):
    global focos
    # calvulamos el score

    score = (focos["focosApagados"] * 50) - (focos["focosFundidos"] * 100)

    # mostramos una pantalla de ganaste o un mensaje de ganaste
    pygame.image.save(SCREEN, "assets/img/pantalla.png")
    ultimoFrame = pygame.image.load("assets/img/pantalla.png")
    pygame.mixer.Sound("assets/sounds/ganar.wav").play()
    # bajamos el volumen de la musica
    configJuego["Volumen"] /= 4
    pygame.mixer.music.set_volume(configJuego["Volumen"])
    pausa  = True

    while True:
        SCREEN.blit(ultimoFrame, (0,0))
        SCREEN.blit(imgs["oscuro"], (0,0))

        TITULO_TEXT = get_font(100).render(idioma[configJuego["Idioma"]]["Juego"]["Ganaste"], True, "#70f4c1")
        TITULO_RECT = TITULO_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(TITULO_TEXT, TITULO_RECT)

        Text_text = get_font(20).render(idioma[configJuego["Idioma"]]["Juego"]["Preciona"], True, "#ffffff")
        Text_rect = Text_text.get_rect(center=(640, 600))
        SCREEN.blit(Text_text, Text_rect)

        ganar_text = get_font(27).render(idioma[configJuego["Idioma"]]["ganar"]["t1"], True, "#FFA500")
        ganar_rect = ganar_text.get_rect(center=(640, 400))
        SCREEN.blit(ganar_text, ganar_rect)

        score_text = get_font(27).render(idioma[configJuego["Idioma"]]["ganar"]["t2"] + f" {score}", True, "#FFA500")
        score_rect = score_text.get_rect(center=(640, 450))
        SCREEN.blit(score_text, score_rect)

        apagadas_text = get_font(27).render(idioma[configJuego["Idioma"]]["ganar"]["t3"] + f' {focos["focosApagados"]}', True, "#FFA500")
        apagadas_rect = apagadas_text.get_rect(center=(640, 500))
        SCREEN.blit(apagadas_text, apagadas_rect)

        fundidas_text = get_font(27).render(idioma[configJuego["Idioma"]]["ganar"]["t4"] + f' {focos["focosFundidos"]}', True, "#FFA500")
        fundidas_rect = fundidas_text.get_rect(center=(640, 550))
        SCREEN.blit(fundidas_text, fundidas_rect)

        pygame.display.flip() 
        if pausa == True:
            time.sleep(5)
            pygame.event.clear(pygame.KEYDOWN)
            pausa = False
        
        for event in pygame.event.get():
            # si preciona cualquier tecla retorna al menu principal
            if event.type == pygame.KEYDOWN:
                LvlsInfo["LvlCompletados"]["lvl1"] = True
                LvlsInfo["LvlDisponibles"]["lvl2"] = True
                # subimos el volumen de la musica
                configJuego["Volumen"] *= 4
                pygame.mixer.music.set_volume(configJuego["Volumen"])
                return SCREEN , configJuego, LvlsInfo, elementosFondo
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

# funcion para pintar el tiempo transcurrido
def pintarTiempo(SCREEN, tiempoPasado, configJuego):    
    """
    Esta función pinta el tiempo transcurrido en la pantalla del juego.
    Recibe como parámetros la pantalla del juego (SCREEN), el tiempo transcurrido (tiempoPasado) y la configuración del juego (configJuego).
    Devuelve el tiempo restante en segundos.
    """
    #a 120 le restamos el tiempoPasado para tener un temporizador de 2 minutos
    relojF = 121 - tiempoPasado

    # formateamos los segundos de relojF para que se muestre con el formato mm:ss
    minutos = relojF // 60
    segundos = relojF % 60 

    # creamos e imprimimos el tiempo transcurrido

    tiempo = get_font(30).render(f"{idioma[configJuego['Idioma']]['Juego']['Tiempo']}{minutos}:{segundos}s", True, "White")
    tiempoRect = tiempo.get_rect(center=(740, 50))

    # colocamos el tempo
    SCREEN.blit(tiempo, tiempoRect)

    return relojF

def pantalla_lvl2(SCREEN , configJuego, LvlsInfo, elementosFondo):
    """
    Función encargada de mostrar la pantalla del nivel 2 del juego LightsOut.
    """
    global segundoUltimoFoco
    global segundoAnterior
    global consumoPorSeg
    global LimiteConsumo
    global consumoTotal
    global infoPersonaje
    global segundoAccion
    global tiempoPasado
    global barraMax
    global focos
    global color
    global imgs
    
    imgs = imgs_lvl2(configJuego["Idioma"])

    # Cambiamos la música si es necesario
    if configJuego["indiceMusic"] != 2:
        configJuego["indiceMusic"] = 2
        pygame.mixer.music.load(f"assets/songs/musica{configJuego['indiceMusic']}.wav") #cargamos la musica
        pygame.mixer.music.set_volume(configJuego["Volumen"]) #le bajamos el volumen a la musica
        pygame.mixer.music.play(-1) #reproducimos la musica en bucle

    # Cambiamos el título de la ventana
    pygame.display.set_caption(idioma[configJuego["Idioma"]]["Nivel1"]["Titulo"])

    # Creamos el botón de pausa y reiniciamos el personaje
    btnOpciones = Button(image1=None, pos=(1047,57), text_input="||", font=get_font(30), base_color="White", hovering_color="#555f68") # boton de pausa
    reiniciar(configJuego["personaje"])

    # Mostramos la pantalla de pausa si es necesario
    pausaInicio(SCREEN, configJuego)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # comprobamos si preciono la tecla escape
                if event.key == pygame.K_ESCAPE:
                    SCREEN , configJuego, LvlsInfo, elementosFondo, accion = opciones_juego(SCREEN , configJuego, LvlsInfo, elementosFondo)
                    pygame.display.set_caption(idioma[configJuego["Idioma"]]["Nivel1"]["Titulo"])
                    if accion == "salir":
                        pantalla_de_carga(SCREEN, configJuego)
                        return SCREEN , configJuego, LvlsInfo, elementosFondo
                    elif accion == "reiniciar":
                        pausaInicio(SCREEN, configJuego)
                        reiniciar(configJuego["personaje"])

            # eventos del raton
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnOpciones.checkForInput(posicionMause):
                    SCREEN , configJuego, LvlsInfo, elementosFondo, accion = opciones_juego(SCREEN , configJuego, LvlsInfo, elementosFondo)
                    pygame.display.set_caption(idioma[configJuego["Idioma"]]["Nivel1"]["Titulo"])
                    if accion == "salir":
                        pantalla_de_carga(SCREEN, configJuego)
                        return SCREEN , configJuego, LvlsInfo, elementosFondo
                    elif accion == "reiniciar":
                        pausaInicio(SCREEN, configJuego)
                        reiniciar(configJuego["personaje"])

        # Obtenemos el tiempo actual
        segundero = time.localtime().tm_sec 

        # Obtenemos la posición del mouse
        posicionMause = pygame.mouse.get_pos() 
        
        # Colocamos el fondo del nivel
        SCREEN.blit(imgs["fondo"], (0,0)) 

        # Verificamos si el mouse está en el botón de pausa
        btnOpciones.changeColor(posicionMause) 
        # Colocamos el botón de pausa
        btnOpciones.update(SCREEN) 

        # Movemos y pintamos el personaje
        moverPersonaje(SCREEN) 

        # Pintamos los focos
        pintarFocos(SCREEN, segundero) 

        # Cambiamos el color de la barra de consumo según el consumo total
        if (consumoTotal > 120):
            color = (255,255,0)
        elif(consumoTotal > 240):
            color = (255,0,0)

        # Pintamos la barra de consumo
        pygame.draw.rect(SCREEN,color, (1147,(509-consumoTotal), 40, consumoTotal))

        # pintamos las puertas abiertas
        pintarPuerta(SCREEN)

        # pintamos los indicadores de las teclas
        pintarTeclas(SCREEN)

        relojF = pintarTiempo(SCREEN, tiempoPasado, configJuego) # colocamos el tiempo transcurrido y obtenemos el tiempo restante

        apagadosText = get_font(25).render(f"X{focos['focosApagados']}", True, "White")
        apagadosRect = apagadosText.get_rect(center=(1229, 667))
        SCREEN.blit(apagadosText, apagadosRect)

        fundidosText = get_font(25).render(f"X{focos['focosFundidos']}", True, "White")
        fundidosRect = fundidosText.get_rect(center=(1229, 583))
        SCREEN.blit(fundidosText, fundidosRect)

        # Colocamos la sombra del nivel
        SCREEN.blit(imgs["sombra_lvl2"], (0,0)) 

        # Actualizamos la pantalla
        pygame.display.flip()

        if relojF <= 0 and focos["focosFundidos"] < 5: # verificamos si el jugador gano
            SCREEN , configJuego, LvlsInfo, elementosFondo = ganar(SCREEN, configJuego, LvlsInfo, elementosFondo)
            return SCREEN , configJuego, LvlsInfo, elementosFondo
        
        if consumoTotal >= LimiteConsumo or(relojF > 0 and focos["focosFundidos"] == 5): # verificamos si el jugador perdio
            SCREEN , configJuego, LvlsInfo, elementosFondo = perder(SCREEN, configJuego, LvlsInfo, elementosFondo)
            return SCREEN , configJuego, LvlsInfo, elementosFondo
        