import sys, pygame
from assets.defaults.button import Button
from assets.defaults.get_fonts import get_font
from assets.defaults.idioma import cargar_idioma
from assets.defaults.get_imgs import imgs_lvl2

idioma = cargar_idioma()
reloj = pygame.time.Clock()

# JEJE Inicializamos las variables

segundoUltimoFoco = 0
segundoAnterior = 0 
infoPersonaje = 0
LimiteConsumo = 0
segundoAccion = 0
consumoPorSeg = 0
consumoPorTotal = 0
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
def reiniciar (personaje):
    global segundoUltimoFoco
    global segundoAnterior  
    global infoPersonaje  
    global LimiteConsumo  
    global segundoAccion 
    global consumoPorSeg  
    global consumoPorTotal 
    global tiempoPasado 
    global focoPorSeg 
    global barraMax 
    global focos 
    global color 
    global fps 
    global powerUps 
    global imgs 
    global teclaEstado  
    global subida
    
    quietoD = pygame.image.load(f"assets/img/sprites/personajes/{personaje}2/personaje1.png")
    quietoI = pygame.image.load(f"assets/img/sprites/personajes{personaje}2/personaje4.png")

    derecha = [
        pygame.image.load(f"assets/img/sprites/personajes{personaje}2/personaje1.png"),
        pygame.image.load(f"assets/img/sprites/personajes{personaje}2/personaje2.png"),
        pygame.image.load(f"assets/img/sprites/personajes{personaje}2/personaje3.png")
    ]

    izquierda = [
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}2/personaje4.png"),
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}2/personaje5.png"),
        pygame.image.load(f"assets/img/sprites/personajes/{personaje}2/personaje6.png")
    ]
    segundoUltimoFoco = 0
    color = (0, 255, 0)
    segundoAnterior = 0
    LimiteConsumo = 360 # el limite son 350 watts 
    segundoAccion = 0
    consumoPorSeg = 2 # 2 watt por segundo
    consumoTotal = 0 # el consumo total de los focos
    tiempoPasado = 0
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
                pygame.quit()
                sys.exit()
        SCREEN.blit(imgs["fondo"], (0,0))
        SCREEN.blit(izquierda[0], (int(infoPersonaje["PX"]), int(infoPersonaje["PY"])))
        SCREEN.blit(imgs["sombra_lvl1"], (0,0))
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

def moverPersonaje(SCREEN):
    global infoPersonaje
    global segundoAccion
    global tiempoPasado
    global focos
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and infoPersonaje["PX"] > infoPersonaje["velocidad"] and infoPersonaje["PX"] - infoPersonaje["velocidad"] > 100:
        infoPersonaje["PX"] - infoPersonaje["velocidad"] 
        infoPersonaje["direccion"] = "izquierda"
        pintarPersonaje(SCREEN, accion = "caminar")
    elif keys[pygame.K_d] and infoPersonaje["PX"] < 1000:
        infoPersonaje["PX"] = infoPersonaje["velocidad"] 
        infoPersonaje["direccion"] = "derecha"
        #pintarPersonaje(SCREEN, accion = "caminar")
    elif keys[pygame.K_w] and ((infoPersonaje["PX"] >= 205 and infoPersonaje["PX"] <= 252) or (infoPersonaje["ancho"] + infoPersonaje["PX"] >= 205 and infoPersonaje["PX"] + infoPersonaje["ancho"] <= 252)):
        if infoPersonaje["piso"] == 1 and segundoAccion != tiempoPasado:
            infoPersonaje["piso"] = 2
            infoPersonaje["PY"] -= 180
        elif segundoAccion != tiempoPasado:
            infoPersonaje["piso"] = 1
            infoPersonaje["PY"] += 180
        segundoAccion = tiempoPasado
        #pintarPersonaje(SCREEN)
    elif keys[pygame.K_SPACE]:
        for foco in foco["focosEstado"].items():
            if foco[1]["estado"] != 0 and foco[1]["estado"] != 4 and infoPersonaje["piso"] == foco[1]["piso"]:
                if infoPersonaje["PX"] >= foco[1]["apagadorX1"] - infoPersonaje["ancho"] and infoPersonaje["PX"] <= foco[1]["apagadorX2"] + infoPersonaje["ancho"]:
                    foco[1]["anteriorEstado"] = foco[1]["estado"]
                    foco[1]["estado"] = 0
                    focos["focosEncendidos"] -= 1
                    focos["focosApagados"] += 1
                    break 
        #pintarPersonaje(SCREEN, accion = "apagar")
    else: 
        infoPersonaje["cuentaPasos"] = 1
        infoPersonaje["quieto"] = True
        #pintarPersonaje(SCREEN, accion = "quieto")



def pantalla_lvl2(SCREEN , configJuego, LvlsInfo, elementosFondo):
    if configJuego["indiceMusic"] != 2:
        configJuego["indiceMusic"] = 2
        pygame.mixer.music.load(f"assets/songs/musica{configJuego['indiceMusic']}.wav") #cargamos la musica
        pygame.mixer.music.set_volume(configJuego["Volumen"]) #le bajamos el volumen a la musica
        pygame.mixer.music.play(-1) #reproducimos la musica en bucle

        
    imgs = imgs_lvl2(configJuego["Idioma"])

    while True:
        # Tu código de la pantalla del nivel 1 aquí
        print("Pantalla del nivel 1")