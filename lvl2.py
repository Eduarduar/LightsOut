import sys, pygame, random, time
from assets.defaults.button import Button
from assets.defaults.get_fonts import get_font
from assets.defaults.idioma import cargar_idioma
from assets.defaults.get_imgs import imgs_lvl2
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
teclaEstado = 0
subida = 0

quietoD = ""
quietoI = ""
derecha = []
izquierda = [] 

#funcion para reiniciar las variables
def reiniciar(personaje):
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

    quietoD = pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje1.png")
    quietoI = pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje4.png")

    derecha = [
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje1.png"),
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje2.png"),
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje3.png")]

    izquierda = [
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje4.png"),
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje5.png"),
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje6.png")]
        
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
            SCREEN.blit(imgs["instrucciones"], (0,0))
        elif parte == 2:
            SCREEN.blit(imgs["interface"], (0, 0))
        else:
            configJuego["Volumen"] *= 4
            pygame.mixer.music.set_volume(configJuego["Volumen"])
            detener = False

        # imprimimos texto de presionar cualquier tecla para continuar

        Text_text = get_font(20).render(idioma[configJuego["Idioma"]]["Juego"]["Preciona"], True, "#ffffff")
        Text_rect = Text_text.get_rect(center=(640, 700))
        SCREEN.blit(Text_text, Text_rect)

        pygame.display.flip()
        reloj.tick(10)

# funcion para pintar al personaje
def pintarPersonaje(SCREEN, accion = "caminar"):
        global infoPersonaje
        global fps
        if powerUps["estados"]["Velocidad"]["activo"] == True: # verificamos si el powerUp de velocidad esta activo
            infoPersonaje["velocidad"] = 15 # aumentamos la velocidad
        else:
            infoPersonaje["velocidad"] = 10 # volvemos a la velocidad normal
        reloj.tick(fps) # fps

        if accion == "caminar":

            # colocamos el personaje segun su estado
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

            #reiniciamos el estado del personaje
            infoPersonaje["quieto"] = False
        else:
            if infoPersonaje["direccion"] == "derecha":
                SCREEN.blit(quietoD, (int(infoPersonaje["PX"]), int(infoPersonaje["PY"])))
            elif infoPersonaje["direccion"] == "izquierda":
                SCREEN.blit(quietoI, (int(infoPersonaje["PX"]), int(infoPersonaje["PY"])))

# funcion para mover el personaje
def moverPersonaje(SCREEN):
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

    # Tecla W
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

# función para pintar la barra de consumo
def pintarFocos(SCREEN, segundero):
    global segundoUltimoFoco
    global segundoAnterior
    global consumoTotal
    global consumoPorSeg
    global tiempoPasado
    global focoPorSeg
    global powerUps
    global focos
    global color

    if segundero != segundoAnterior: # verificamos si el tiempo cambio 
        if consumoPorSeg == 2: # verificamos si el consumo por segundo es 2
            consumoPorSeg = 1
        else:
            consumoPorSeg = 2
            
        tiempoPasado += 1 # si el tiempo cambio sumamos un segundo
        if powerUps["estados"]["reducirConsumo"]["activo"] == True:  # verificamos si el powerUp de reducir consumo esta activo
            consumoTotal += (1/2) * focos["focosEncendidos"]  # reducimos a la mitad el consumo de los focos encendidos
        else:
            consumoTotal += consumoPorSeg * focos["focosEncendidos"] # sumamos el consumo de los focos encendidos

        segundoAnterior = segundero # actualizamos el tiempo anterior
        
        for foco in focos["focosEstado"].items(): # recorremos los focos
            if foco[1]["abierta"] == True:
                foco[1]["abierta"] = False
                pygame.mixer.Sound("assets/sounds/cerrarPuerta2.wav").play()

            if foco[1]["estado"] == 1 or foco[1]["estado"] == 2 or foco[1]["estado"] == 3: # verificamos si el foco esta encendido
                foco[1]["tiempoEncendido"] += 1 # si el foco esta encendido sumamos un segundo 

                if foco[1]["tiempoEncendido"] >= 50: # verificamos si el foco esta encendido por mas de 70 segundos
                    foco[1]["estado"] = 4
                    foco[1]["ultimoEstado"] = 4
                    focos["focosFundidos"] += 1
                    focos["focosEncendidos"] -= 1
                    pygame.mixer.Sound("assets/sounds/romper.wav").play() # sonido de fundir foco

                elif foco[1]["tiempoEncendido"] >= 30: # verificamos si el foco esta encendido por mas de 45 segundos
                    foco[1]["estado"] = 3
                    foco[1]["ultimoEstado"] = 3

                elif foco[1]["tiempoEncendido"] >= 20: # verificamos si el foco esta encendido por mas de 30 segundos
                    foco[1]["estado"] = 2
                    foco[1]["ultimoEstado"] = 2

            if segundoUltimoFoco + focoPorSeg <= tiempoPasado and focos["focosEncendidos"] != 5 - focos["focosFundidos"]: # verificamos si pasaron 5 segundos desde que se fundio el ultimo foco
                segundoUltimoFoco = tiempoPasado # actualizamos el tiempo del ultimo foco encendido
                numFoco = 0
                while True: # buscamos un foco apagado
                    numFoco = random.randint(1, focos["focosTotales"]) # elegimos un foco al azar
                    if focos["focosEstado"][f"foco{numFoco}"]["estado"] == 0: # verificamos si el foco esta apagado
                        break
                # abrimos la puerta
                focos["focosEstado"][f"foco{numFoco}"]["abierta"] = True
                pygame.mixer.Sound("assets/sounds/abrirPuerta.wav").play() # sonido de abrir puerta

                # encendemos el foco
                focos["focosEstado"][f"foco{numFoco}"]["estado"] = focos["focosEstado"][f"foco{numFoco}"]["ultimoEstado"] # encendemos el foco
                focos["focosEncendidos"] += 1 # sumamos un foco encendido
                pygame.mixer.Sound("assets/sounds/prenderFoco.wav").play() # sonido de encender foco

    # pintamos los focos encendidos
    for foco in focos["focosEstado"].items(): # recorremos los focos
        if foco[1]["estado"] != 0 and foco[1]["estado"] != 4: # verificamos si el foco esta apagado
            SCREEN.blit(imgs[f"bombilla{foco[1]['estado']}"], foco[1]["posicion"]) # colocamos el foco en pantalla
        else:
            SCREEN.blit(imgs[f"sombras"][f"sombra{foco[1]['numero']}"], (0, 0))

def pantalla_lvl2(SCREEN , configJuego, LvlsInfo, elementosFondo):
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

    if configJuego["indiceMusic"] != 2:
        configJuego["indiceMusic"] = 2
        pygame.mixer.music.load(f"assets/songs/musica{configJuego['indiceMusic']}.wav") #cargamos la musica
        pygame.mixer.music.set_volume(configJuego["Volumen"]) #le bajamos el volumen a la musica
        pygame.mixer.music.play(-1) #reproducimos la musica en bucle

    pygame.display.set_caption(idioma[configJuego["Idioma"]]["Nivel1"]["Titulo"])
    btnOpciones = Button(image1=None, pos=(1047,57), text_input="||", font=get_font(30), base_color="White", hovering_color="#555f68") # boton de pausa
    reiniciar(configJuego["personaje"])
    pausaInicio(SCREEN, configJuego)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

        segundero = time.localtime().tm_sec # obtenemos el tiempo actual

        posicionMause = pygame.mouse.get_pos() # obtenemos la posicion del mouse
        
        SCREEN.blit(imgs["fondo"], (0,0)) # colocamos el fondo del nivel

        btnOpciones.changeColor(posicionMause) # verificamos si el mause esta en el boton de opciones
        btnOpciones.update(SCREEN) #colocamos el boton de pausa

        moverPersonaje(SCREEN) # movemos y pintamos el personaje

        pintarFocos(SCREEN, segundero) # pintamos los focos

        if (consumoTotal > 120):
            color = (255,255,0)
        elif(consumoTotal > 240):
            color = (255,0,0)

        pygame.draw.rect(SCREEN,color, (1147,(509-consumoTotal), 40, consumoTotal))

        SCREEN.blit(imgs["sombra_lvl2"], (0,0)) # colocamos la sombra del nivel

        pygame.display.flip()