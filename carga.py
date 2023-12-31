import sys, pygame, random, time
from assets.defaults.idioma import cargar_idioma
from assets.defaults.get_fonts import get_font
from assets.defaults.get_imgs import imgs_carga
from intro import intro

idioma = cargar_idioma()
imgs = []

# crearemos una barra de carga horizontal que avance de poco en 

cuentaPasos = 0
px = 70
py = 40
ultimaFrase = 0
tiempoPasado = 0


def obtenerPausas(maximo):
    """
    Función que devuelve una lista con los porcentajes donde se hará una pausa en la carga.
    """
    pausas = []
    for i in range(0, 3):
        # sacamos un numero aleatorio entre 0 y 1000
        num = (random.randint(0, maximo))
        # redondemao el numero a la decena mas cercana
        num = round(num, -1)
        # si el numero es 0, lo cambiamos a 10
        if num == 0:
            num = 10
        # si el numero es igual al maximo, lo cambiamos a 990
        elif num == maximo:
            num = 990
        # añadimos el numero a la lista de pausas
        pausas.append(num)
    return pausas

def pintarPersonaje(SCREEN, porcentaje, accion):
    """
    Función que pinta al personaje en la pantalla de carga.
    """
    global cuentaPasos, px, py, imgs

    if accion == "parado":
        SCREEN.blit(imgs["quieto"], (int(px + porcentaje), int(py)))
    else:

        if (cuentaPasos + 1) >= 15:
            cuentaPasos = 0

        SCREEN.blit(imgs["derecha"][cuentaPasos // 1], (int(px + porcentaje), int(py)))
        cuentaPasos += 1

def frases():
    """
    Función que devuelve un número aleatorio para elegir una frase aleatoria.
    :return: número aleatorio para elegir una frase aleatoria
    """
    num = random.randint(1, 6)
    return num

def pantalla_de_carga(SCREEN, configJuego):
    """
    Función que muestra una pantalla de carga mientras se carga el juego.
    La pantalla de carga muestra una barra de progreso y un personaje caminando.
    La pantalla también muestra frases aleatorias y un texto que indica al usuario que presione una tecla para continuar.
    """
    # inicializamos nuestros parametros
    global imgs
    global ultimaFrase
    global tiempoPasado
    imgs = imgs_carga(configJuego["personaje"]) # cargamos las imagenes del personaje
    reloj = pygame.time.Clock() # creamos un objeto Clock de pygame
    porcentaje = 0 # porcentaje de carga
    maximo = 1000 # porcentaje máximo de carga
    pausas = obtenerPausas(maximo) # obtenemos los porcentajes donde se hará una pausa en la carga
    pausa = False # indica si se está en una pausa de carga
    detener = True # indica si se debe detener la pantalla de carga
    segundoAnterior = 0 # segundo anterior del reloj
    i = 1 # contador de frases
    num = frases() # número de frase a mostrar
    
    # generamos los texto a usar
    Text_text = get_font(20).render(idioma[configJuego["Idioma"]]["Juego"]["Preciona"], True, "#ffffff")
    Text_rect = Text_text.get_rect(center=(640, 700))

    while detener:
        reloj.tick(60) # limitamos los fps a 60
        segundero = time.localtime().tm_sec # sacamos los segundos del reloj 

        if segundero != segundoAnterior:
            segundoAnterior = segundero
            tiempoPasado += 1
            pausa = False
            if i == 4:
                i = 0
            i += 1

        SCREEN.blit(imgs["fondo"], (0, 0)) # pintamos el fondo

        # Cargamos la barra de carga
        pygame.draw.rect(SCREEN, "WHITE", (100, 100, 1000, 50))
        pygame.draw.rect(SCREEN, "GREEN", (100, 100, 0 + porcentaje, 50))

        if ultimaFrase + 7 <= tiempoPasado: # si han pasado 5 segundos desde la ultima frase, pintamos una nueva
            num = frases()
            ultimaFrase = tiempoPasado

        # generamos el texto a usar
        for c in range(1, len(idioma[configJuego["Idioma"]][f"Frases"][f"frase{num}"]) + 1):
            frase = get_font(20).render(idioma[configJuego["Idioma"]][f"Frases"][f"frase{num}"][f"{c}"], True, "#ffffff")
            frase_rect = frase.get_rect(center=(640, 250 + (c * 30)))
            SCREEN.blit(frase, frase_rect)

        # Actualizamos el porcentaje
        if porcentaje <= maximo:
            pintarPersonaje(SCREEN, porcentaje, accion = "caminar") # pintamos al personaje caminando
            # si el porcentaje es igual a algun numero de la pausa, pausamos un segundo la carga
            if pausa != True:
                porcentaje += 10

            for numero in pausas:
                if porcentaje == numero:
                    pausa = True
                    break
        else:
            pintarPersonaje(SCREEN, porcentaje, accion = "parado") # pintamos al personaje parado
            SCREEN.blit(Text_text, Text_rect)

        # texto de carga
        carga = get_font(30).render(idioma[configJuego["Idioma"]]["Carga"][f"Carga{i}"], True, "WHITE")
        SCREEN.blit(carga, (100, 20))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if porcentaje >= maximo:
                    detener = False
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

        # Actualizamos la pantalla
        pygame.display.flip()
