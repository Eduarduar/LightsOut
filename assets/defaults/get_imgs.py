import pygame

def imgs_menu_principal(idioma):
    Caja = pygame.transform.scale(pygame.image.load("assets/img/rect.png"), (550, 100))
    ciudad = pygame.transform.scale(pygame.image.load("assets/backgrounds/ciudad.png"), (1280, 720))
    luna = pygame.image.load("assets/backgrounds/luna.png")
    nube = pygame.image.load("assets/backgrounds/nube.png")

    jugar = pygame.image.load("assets/img/botones/opciones/jugar/jugar.png")
    jugarP = pygame.image.load("assets/img/botones/opciones/jugar/jugarP.png")
    opciones = pygame.image.load("assets/img/botones/opciones/opciones/opciones.png")
    opcionesP = pygame.image.load("assets/img/botones/opciones/opciones/opcionesP.png")
    atras = pygame.image.load("assets/img/botones/opciones/atras/atras.png")
    atrasP = pygame.image.load("assets/img/botones/opciones/atras/atrasP.png")
    play = pygame.image.load("assets/img/botones/opciones/play/play.png")
    playP = pygame.image.load("assets/img/botones/opciones/play/playP.png")
    options = pygame.image.load("assets/img/botones/opciones/opcions/opcions.png")
    optionsP = pygame.image.load("assets/img/botones/opciones/opcions/opcionsP.png")
    back = pygame.image.load("assets/img/botones/opciones/back/back.png")
    backP = pygame.image.load("assets/img/botones/opciones/back/backP.png")

    avatar = pygame.image.load("assets/img/botones/opciones/avatar/avatar.png")
    avatarP = pygame.image.load("assets/img/botones/opciones/avatar/avatarP.png")

    imgs = {
        "ciudad": ciudad,
        "luna": luna,
        "nube": nube,
        "caja": Caja,
        "botones": {
            "es": {
                "jugar": {
                    "normal": jugar,
                    "presionado": jugarP
                },
                "opciones": {
                    "normal": opciones,
                    "presionado": opcionesP
                },
                "atras": {
                    "normal": atras,
                    "presionado": atrasP
                },
                "avatar": {
                    "normal": avatar,
                    "presionado": avatarP
                }
            },
            "en": {
                "jugar": {
                    "normal": play,
                    "presionado": playP
                },
                "opciones": {
                    "normal": options,
                    "presionado": optionsP
                },
                "atras": {
                    "normal": back,
                    "presionado": backP
                },
                "avatar": {
                    "normal": avatar,
                    "presionado": avatarP
                }
            }
        }
    }

    return imgs

def imgs_opciones():
    azul = pygame.image.load("assets/backgrounds/azul.jpg")
    Caja = pygame.transform.scale(pygame.image.load("assets/img/rect.png"), (550, 100))

    imgs = {
        "azul": azul,
        "caja": Caja
    }

    return imgs

def imgs_niveles():
    Caja = pygame.transform.scale(pygame.image.load("assets/img/rect.png"), (550, 100))
    ciudad = pygame.transform.scale(pygame.image.load("assets/backgrounds/ciudad.png"), (1280, 720))
    luna = pygame.image.load("assets/backgrounds/luna.png")
    nube = pygame.image.load("assets/backgrounds/nube.png")
    pasto = pygame.image.load("assets/img/niveles/pasto.png")

    edificios = {
        "edificio1": {
            "estado1": pygame.image.load("assets/img/niveles/edificio1-es1.png"),
            "estado2": pygame.image.load("assets/img/niveles/edificio1-es2.png")
        },
        "edificio2": {
            "estado1": pygame.image.load("assets/img/niveles/edificio2-es1.png"),
            "estado2": pygame.image.load("assets/img/niveles/edificio2-es2.png"),
            "estado3": pygame.image.load("assets/img/niveles/edificio2-es3.png")
        },
        "edificio3": {
            "estado1": pygame.image.load("assets/img/niveles/edificio3-es1.png"),
            "estado2": pygame.image.load("assets/img/niveles/edificio3-es2.png"),
            "estado3": pygame.image.load("assets/img/niveles/edificio3-es3.png")
        },
    }

    imgs = {
        "edificios": edificios,
        "pasto": pasto,
        "ciudad": ciudad,
        "luna": luna,
        "nube": nube,
        "caja": Caja
    }

    return imgs

def imgs_lvl1(idioma):
    reloj = pygame.transform.scale(pygame.image.load("assets/img/sprites/items/powerUps/reloj.png"), (30,40))
    rayo = pygame.transform.scale(pygame.image.load("assets/img/sprites/items/powerUps/rayo.png"), (30,40))
    abierta = pygame.image.load("assets/img/sprites/items/puerta_departamento/SpritePuertaOn.png")
    Caja = pygame.transform.scale(pygame.image.load("assets/img/rect.png"), (550, 100))
    bombilla0 = pygame.image.load("assets/img/sprites/items/bombillas/Bombilla0.png")
    bombilla1 = pygame.image.load("assets/img/sprites/items/bombillas/Bombilla1.png")
    bombilla2 = pygame.image.load("assets/img/sprites/items/bombillas/Bombilla2.png")
    bombilla3 = pygame.image.load("assets/img/sprites/items/bombillas/Bombilla3.png")
    sombra_lvl1 = pygame.image.load("assets/img/lvl1/sombra_lvl1.png")
    fondo = pygame.image.load("assets/img/lvl1/fondo_lvl1.png")
    powerUpsInfo = pygame.image.load("assets/img/powerUps.png")
    sombra1 = pygame.image.load("assets/img/lvl1/sombra1.png")
    sombra2 = pygame.image.load("assets/img/lvl1/sombra2.png")
    sombra3 = pygame.image.load("assets/img/lvl1/sombra3.png")
    sombra4 = pygame.image.load("assets/img/lvl1/sombra4.png")
    sombra5 = pygame.image.load("assets/img/lvl1/sombra5.png")
    oscuro = pygame.image.load("assets/img/oscuro.png")
    w1 = pygame.image.load("assets/img/botones/W1.png")
    w2 = pygame.image.load("assets/img/botones/W2.png")
    

    if idioma == "es":
        faces = pygame.image.load("assets/img/etapasEs.png")
        interface = pygame.image.load("assets/img/interfaceEs.png")
        espacio1 = pygame.image.load("assets/img/botones/Espacio1.png")
        espacio2 = pygame.image.load("assets/img/botones/Espacio2.png")
        controles = pygame.image.load("assets/img/controlesEs.png")
    else:
        faces = pygame.image.load("assets/img/etapasEn.png")
        interface = pygame.image.load("assets/img/interfaceEn.png")
        espacio1 = pygame.image.load("assets/img/botones/Space1.png")
        espacio2 = pygame.image.load("assets/img/botones/Space2.png")
        controles = pygame.image.load("assets/img/controlesEn.png")

    sombras = {
        "sombra1": sombra1,
        "sombra2": sombra2,
        "sombra3": sombra3,
        "sombra4": sombra4,
        "sombra5": sombra5
    }

    imgs = {
        "caja": Caja,
        "fondo": fondo,
        "sombra_lvl1": sombra_lvl1,
        "bombilla0": bombilla0,
        "bombilla1": bombilla1,
        "bombilla2": bombilla2,
        "bombilla3": bombilla3,
        "sombras": sombras,
        "oscuro": oscuro,
        "controles": controles,
        "abierta": abierta,
        "w1": w1,
        "w2": w2,
        "espacio1": espacio1,
        "espacio2": espacio2,
        "powerUps": {
            "info": powerUpsInfo,
            "velocidad": rayo,
            "reducirConsumo": reloj
        },
        "faces": faces,
        "interface": interface
    }

    return imgs

def imgs_lvl2(idioma):
    reloj = pygame.transform.scale(pygame.image.load("assets/img/sprites/items/powerUps/reloj.png"), (30,40))
    rayo = pygame.transform.scale(pygame.image.load("assets/img/sprites/items/powerUps/rayo.png"), (30,40))
    abierta = pygame.image.load("assets/img/lvl2/puertaon.png")
    Caja = pygame.transform.scale(pygame.image.load("assets/img/rect.png"), (550, 100))
    bombilla0 = pygame.image.load("assets/img/sprites/items/bombillas/Bombilla0.png")
    bombilla1 = pygame.image.load("assets/img/sprites/items/bombillas/Bombilla1.png")
    bombilla2 = pygame.image.load("assets/img/sprites/items/bombillas/Bombilla2.png")
    bombilla3 = pygame.image.load("assets/img/sprites/items/bombillas/Bombilla3.png")
    sombra_lvl2 = pygame.image.load("assets/img/lvl2/sombra_lvl2.png")
    fondo = pygame.image.load("assets/img/lvl2/fondo_lvl2.png")
    powerUpsInfo = pygame.image.load("assets/img/powerUps.png")
    sombra1 = pygame.image.load("assets/img/lvl2/sombra1.png")
    sombra2 = pygame.image.load("assets/img/lvl2/sombra2.png")
    sombra3 = pygame.image.load("assets/img/lvl2/sombra3.png")
    sombra4 = pygame.image.load("assets/img/lvl2/sombra4.png")
    sombra5 = pygame.image.load("assets/img/lvl2/sombra5.png")
    oscuro = pygame.image.load("assets/img/oscuro.png")
    w1 = pygame.image.load("assets/img/botones/W1.png")
    w2 = pygame.image.load("assets/img/botones/W2.png")
    instrucciones = pygame.image.load("assets/img/lvl2/instrucciones.png")
    

    if idioma == "es":
        interface = pygame.image.load("assets/img/lvl2/Interface2Es.png")
        espacio1 = pygame.image.load("assets/img/botones/Espacio1.png")
        espacio2 = pygame.image.load("assets/img/botones/Espacio2.png")
    else:
        interface = pygame.image.load("assets/img/lvl2/Interface2En.png")
        espacio1 = pygame.image.load("assets/img/botones/Space1.png")
        espacio2 = pygame.image.load("assets/img/botones/Space2.png")

    sombras = {
        "sombra1": sombra1,
        "sombra2": sombra2,
        "sombra3": sombra3,
        "sombra4": sombra4,
        "sombra5": sombra5
    }

    imgs = {
        "caja": Caja,
        "fondo": fondo,
        "sombra_lvl2": sombra_lvl2,
        "bombilla0": bombilla0,
        "bombilla1": bombilla1,
        "bombilla2": bombilla2,
        "bombilla3": bombilla3,
        "sombras": sombras,
        "oscuro": oscuro,
        "instrucciones": instrucciones,
        "abierta": abierta,
        "w1": w1,
        "w2": w2,
        "espacio1": espacio1,
        "espacio2": espacio2,
        "powerUps": {
            "info": powerUpsInfo,
            "velocidad": rayo,
            "reducirConsumo": reloj
        },
        "interface": interface
    }

    return imgs

def imgs_lvl3(idioma, sexo):
    w1 = pygame.image.load("assets/img/botones/W1.png")
    w2 = pygame.image.load("assets/img/botones/W2.png")
    fondo = pygame.image.load("assets/img/lvl3/fondo_lvl3.png")
    sombrasLvl3 = pygame.image.load("assets/img/lvl3/sombra_lvl3.png")
    quietoIzq = pygame.image.load(f"assets/img/sprites/personajes/{sexo}3/personaje4.png")
    quietoDer = pygame.image.load(f"assets/img/sprites/personajes/{sexo}3/personaje1.png")
    rayo = pygame.transform.scale(pygame.image.load("assets/img/sprites/items/powerUps/rayo.png"), (30,40))
    reloj = pygame.transform.scale(pygame.image.load("assets/img/sprites/items/powerUps/reloj.png"), (30,40))
    puerta = pygame.image.load("assets/img/lvl3/puertaon.png")

    imgs = {
        "w1": w1,
        "w2": w2,
        "rayo": rayo,
        "reloj": reloj,
        "fondo": fondo,
        "quietoIzq": quietoIzq,
        "quietoDer": quietoDer,
        "sombras": sombrasLvl3,
        "puertaon": puerta
    }

    if idioma == "es":
        for espacio in range(1, 3): # va iterando de 1 a 2
            imgs[f"espacio{espacio}"] = pygame.image.load(f"assets/img/botones/Espacio{espacio}.png")
    else:
        for espacio in range(1, 3): # va iterando de 1 a 2
            imgs[f"espacio{espacio}"] = pygame.image.load(f"assets/img/botones/Space{espacio}.png")

    for bombilla in range(0, 4): # va iterando de 1 a 4
        imgs[f"bombilla{bombilla}"] = pygame.image.load(f"assets/img/sprites/items/bombillas/Bombilla{bombilla}.png")

    for derecha in range(1, 4): # va iterando de 1 a 3
        imgs[f"caminandoDer{derecha}"] = pygame.image.load(f"assets/img/sprites/personajes/{sexo}3/personaje{derecha}.png")

    for izquierda in range(4, 7): # va iterando de 4 a 6
        imgs[f"caminandoIzq{izquierda - 3}"] = pygame.image.load(f"assets/img/sprites/personajes/{sexo}3/personaje{izquierda}.png")

    for sombra in range(1, 8):
        imgs[f"sombra{sombra}"] = pygame.image.load(f"assets/img/lvl3/sombra{sombra}.png")

    return imgs

def imgs_carga(personaje):
    
    img1 = pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje1.png")
    img2 = pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje2.png")
    img3 = pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje3.png")
    fondo = pygame.image.load("assets/backgrounds/carga.png")
    personaje = [img1, img2, img3]
    derecha = []
    for i in range(0,3):
        for j in range(0,5):
            derecha.append(personaje[i])

    imgs = {
        "derecha": derecha,
        "quieto": img1,
        "fondo": fondo
    }

    return imgs

def imgs_intro():
    imgs = []
    for i in range(1, 63):
        imgs.append(pygame.image.load("./assets/img/intro/" + str(i) + ".png")) 

    return imgs

def imgs_historia(personaje):
    pasillo = pygame.image.load("assets/img/historia/pasillo.png")
    sombra = pygame.image.load("assets/img/historia/sombra.png")
    sombraLuz = pygame.image.load("assets/img/historia/sombra1.png")
    entrada = pygame.image.load("assets/img/historia/entrada.png")
    chat = pygame.transform.scale(pygame.image.load("assets/img/historia/chat.png"), (110, 120))
    #scalamos por 2 los focos
    foco1 = pygame.transform.scale(pygame.image.load("assets/img/sprites/items/bombillas/Bombilla0.png"), (64, 64))
    foco2 = pygame.transform.scale(pygame.image.load("assets/img/sprites/items/bombillas/Bombilla1.png"), (64, 64))
    rayo = pygame.transform.scale(pygame.image.load("assets/img/sprites/items/powerUps/rayo.png"), (64,64))


    derecha = [] 
    izquierda = []
    paradoD = pygame.transform.scale(pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje1.png"), (100, 130))
    paradoI = pygame.transform.scale(pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje4.png"), (100, 130))
    for i in range(1, 4):
        derecha.append(pygame.transform.scale(pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje" + str(i) + ".png"), (100, 130)))

    for i in range(4, 7):
        izquierda.append(pygame.transform.scale(pygame.image.load(f"assets/img/sprites/personajes/{personaje}/personaje" + str(i) + ".png"), (100, 130)))

    imgs = {
        "pasillo": pasillo,
        "sombra": sombra,
        "sombraLuz": sombraLuz,
        "entrada": entrada,
        "derecha": derecha,
        "izquierda": izquierda,
        "paradoD": paradoD,
        "paradoI": paradoI,
        "chat": chat,
        "foco": foco1,
        "foco2": foco2,
        "rayo": rayo
    }

    return imgs

def imgs_cambiarAvatar():
    fondo = pygame.image.load("assets/img/cambiarAvatar/fondo.png")
    moldes = pygame.image.load("assets/img/cambiarAvatar/moldes.png")
    luzHombre = pygame.image.load("assets/img/cambiarAvatar/luzHombre.png")
    luzMujer = pygame.image.load("assets/img/cambiarAvatar/luzMujer.png")
    hombre = pygame.image.load("assets/img/cambiarAvatar/hombre.png")
    mujer = pygame.image.load("assets/img/cambiarAvatar/mujer.png")

    imgs = {
        "fondo": fondo,
        "moldes": moldes,
        "luzHombre": luzHombre,
        "luzMujer": luzMujer,
        "hombre": hombre,
        "mujer": mujer
    }

    return imgs

def imgs_optionsLvls():
    Caja = pygame.transform.scale(pygame.image.load("assets/img/rect.png"), (550, 100))
    oscuro = pygame.image.load("assets/img/oscuro.png")

    imgs = {
        "caja": Caja,
        "oscuro": oscuro
    }

    return imgs