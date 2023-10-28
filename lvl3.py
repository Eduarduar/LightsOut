import sys, pygame, random, time
from assets.defaults.button import Button
from assets.defaults.get_fonts import get_font
from assets.defaults.idioma import cargar_idioma
from assets.defaults.get_imgs import imgs_lvl3
from intro import intro

idioma = cargar_idioma()
reloj = pygame.time.Clock()
accion = False
segundoUltimoFoco = 0
focosFundidos = 0
focosApagados = 0
focosEncendidos = 0
teclaEstado = 1
ultimoFoco = 0

PISOS = {
    1: 615,
    2: 437,
    3: 248
}

# Inicializamos las variables

class Foco:

    def __init__(self, numero, posicion, apagador1, posicion_puerta, piso):
        """
        Inicializa un objeto Foco con los atributos especificados.

        Parámetros:
        ----------
        numero : int
            Número del foco.
        tiempo_encendido : int
            Tiempo que el foco ha estado encendido.
        posicion : tuple
            Coordenadas (x, y) de la posición del foco en la pantalla.
        apagador : int
            Número del apagador al que está conectado el foco.
        posicion_puerta : tuple
            Coordenadas (x, y) de la posición de la puerta en la pantalla.
        piso : int
            Número del piso en el que se encuentra el foco.
        """
        self.numero = numero
        self.estado = 0 # 0 = apagado, 1 = encendido, 2 = amarillo, 3 = rojo, 4 = fundido
        self.ultimo_estado = 1
        self.tiempo_encendido = 0
        self.posicion = posicion
        self.apagador1 = apagador1
        self.apagador2 = apagador1 + 7
        self.estadoPuerta = 1 # 1 = cerrado, 2 = abierto
        self.posicion_puerta = posicion_puerta
        self.piso = piso

    def prender(self):
        """Enciende el foco."""
        self.estado = self.ultimo_estado
        self.estadoPuerta = 2

    def cerrarPuerta(self):
        """Cierra la puerta."""
        self.estadoPuerta = 1
        pygame.mixer.Sound("assets/sounds/cerrarPuerta2.wav").play()

    def apagar(self):
        """Apaga el foco."""
        self.ultimo_estado = self.estado
        self.estado = 0

    def aumentarTiempo(self):
        """Aumenta el tiempo que el foco ha estado encendido y cambia su estado según el tiempo."""
        global focosFundidos, focosEncendidos
        self.tiempo_encendido += 1
        if self.tiempo_encendido > 60:
            self.estado = 4
            self.ultimo_estado = 4
            pygame.mixer.Sound("assets/sounds/romper.wav").play() # Sonido de fundir foco
            focosFundidos += 1
            focosEncendidos -= 1
        elif self.tiempo_encendido > 30:
            self.estado = 3
            self.ultimo_estado = 3
        elif self.tiempo_encendido > 20:
            self.estado = 2
            self.ultimo_estado = 2

    def pintar(self, SCREEN, imgs):
        """
        Dibuja el foco en la pantalla según su estado.

        Parámetros:
        ----------
        SCREEN : pygame.Surface
            Superficie de la pantalla.
        imgs : dict
            Diccionario con las imágenes de los focos y las sombras.
        """
        if self.estado == 0 or self.estado == 4:
            SCREEN.blit(imgs[f"sombra{self.numero}"], (0, 0))
        else:
            SCREEN.blit(imgs[f"bombilla{self.estado}"], self.posicion)
            if self.estadoPuerta == 2:
                SCREEN.blit(imgs["puertaon"], self.posicion_puerta)

    def reiniciar(self):
        """Reinicia el foco a su estado inicial."""
        self.estado = 0
        self.tiempo_encendido = 0
        self.estadoPuerta = 1

class PowerUp():
    """
    Una clase que representa un power-up en un juego.

    Atributos:
    - nombre (str): el nombre del power-up.
    - PX (int): la coordenada x del power-up.
    - piso (int): el nivel del piso del power-up.
    - activo (bool): indica si el power-up está activo.
    - suelto (bool): indica si el power-up ha sido liberado.
    - tiempoDefault (int): la duración predeterminada del power-up.
    - tiempo (int): la duración restante del power-up.
    - alto (int): la altura del power-up.

    Métodos:
    - soltarP(): libera el power-up.
    - activar(): activa el power-up.
    - bajarTiempo(): disminuye la duración restante del power-up.
    - reiniciar(): restablece el power-up a su estado predeterminado.
    """

    def __init__(self, nombre, tiempo, alto):
        """
        Inicializa una nueva instancia de la clase PowerUp.

        Parámetros:
        - nombre (str): el nombre del power-up.
        - tiempo (int): la duración del power-up.
        - alto (int): la altura del power-up.
        """
        self.nombre = nombre
        self.PX = 0
        self.piso = 1
        self.activo = False
        self.suelto = False
        self.tiempoDefault = tiempo
        self.tiempo = self.tiempoDefault
        self.alto = alto

    def soltarP(self):
        """
        Libera el power-up estableciendo su posición y nivel de piso al azar.
        """
        self.PX = random.randint(200, 1000)
        self.piso = random.randint(1, 3)
        self.suelto = True

    def activar(self):
        """
        Activa el power-up estableciendo su atributo 'activo' en True y el atributo 'suelto' en False.
        """
        self.suelto = False
        self.activarPowerUp = True

    def bajarTiempo(self):
        """
        Disminuye la duración restante del power-up en 1. Si la duración llega a 0, el power-up se restablece.
        """
        if (self.tiempo <= 0):
            self.reiniciar()
        else:
            self.tiempo -= 1

    def pintar(self, SCREEN, imgs):
        """
        Dibuja el power-up en la pantalla.

        Parámetros:
        - SCREEN (pygame.Surface): la superficie de la pantalla.
        - imgs (dict): el diccionario de imágenes del power-up.
        """
        global PISOS
        if self.suelto:
            SCREEN.blit(imgs[self.nombre], (self.PX, PISOS[self.piso] - self.alto ))

    def reiniciar(self):
        """
        Restablece el power-up a su estado predeterminado.
        """
        self.activo = False
        self.suelto = False
        self.piso = 1
        self.piso = 0
        self.tiempo = self.tiempoDefault

class Barra():
    """
    Clase que representa una barra de consumo de energía eléctrica.

    Atributos:
    - consumoTotal: int que representa el consumo total de la barra.
    - consumoMaximo: int que representa el consumo máximo permitido por la barra.
    - color: str que representa el color actual de la barra.

    Métodos:
    - __init__(self, consumoMaximo): constructor de la clase.
    - aumentarConsumo(self, focos): aumenta el consumo total de la barra en función del estado de los focos.
    - obtenerPorcentaje(self): calcula el porcentaje de consumo actual de la barra.
    - cambiarColor(self): cambia el color de la barra en función del porcentaje de consumo actual.
    - pintar(self, SCREEN, imgs): dibuja la barra en la pantalla.
    - reiniciar(self): reinicia el consumo total de la barra a cero.
    """
    def __init__(self, consumoMaximo):
        """
        Constructor de la clase Barra.

        Parámetros:
        - consumoMaximo: int que representa el consumo máximo permitido por la barra.
        """
        self.consumoTotal = 0
        self.consumoMaximo = consumoMaximo
        self.color = "#00FF00"

    def aumentarConsumo(self, focos):
        """
        Aumenta el consumo total de la barra en función del estado de los focos.

        Parámetros:
        - focos: dict que contiene los focos de la barra.

        Retorna:
        - None
        """
        consumo = 0
        for foco in focos.values(): 
            if foco.estado == 1:
                consumo += 1
        self.consumoTotal += consumo
        self.cambiarColor()

    def obtenerPorcentaje(self):
        """
        Calcula el porcentaje de consumo actual de la barra.

        Retorna:
        - float que representa el porcentaje de consumo actual de la barra.
        """
        return (self.consumoTotal * 100) / self.consumoMaximo
    
    def cambiarColor(self):
        """
        Cambia el color de la barra en función del porcentaje de consumo actual.

        Retorna:
        - None
        """
        if self.obtenerPorcentaje() > 33:
            self.color = "#FFFF00"
        if self.obtenerPorcentaje() > 66:
            self.color = "#FF0000"

    def pintar(self, SCREEN, imgs): # ! funcionalidad incompleta
        """
        Dibuja la barra en la pantalla.

        Parámetros:
        - SCREEN: objeto pygame.Surface que representa la pantalla.
        - imgs: dict que contiene las imágenes de la barra.

        Retorna:
        - None
        """
        SCREEN.blit(imgs["barra"][f"barra{self.obtenerPorcentaje()}"], (0, 0)) 

    def reiniciar(self):
        """
        Reinicia el consumo total de la barra a cero.

        Retorna:
        - None
        """
        self.consumoTotal = 0

class Temporizador():
    """
    Clase que representa un temporizador para el juego Lights Out.

    Atributos:
    - tiempo (int): el tiempo restante en segundos.
    - minutos (int): los minutos restantes en el tiempo.
    - segundos (int): los segundos restantes en el tiempo.

    Métodos:
    - bajarTiempo(): reduce el tiempo en 1 segundo y actualiza los minutos y segundos restantes.
    - pintar(SCREEN, lenguaje): dibuja el temporizador en la pantalla del juego.
    - reiniciar(): reinicia el tiempo a cero.
    """

    def __init__(self):
        """
        Inicializa un objeto Temporizador con un tiempo predeterminado de 2 minutos (120 segundos).
        """
        self.tiempoActual = time.localtime().tm_sec
        self.tiempoAnterior = 0
        self.tiempoPasado = 0
        self.tiempo = 121
        self.minutos = 2
        self.segundos = 0

    def actualizarTiempo(self):
        if self.tiempoActual != self.tiempoAnterior:
            self.tiempoPasado += 1
            self.tiempoAnterior = self.tiempoActual
        self.tiempoActual = time.localtime().tm_sec

    def comprobarTiempo(self):
        if self.tiempoActual != self.tiempoAnterior:
            return True
        return False

    def bajarTiempo(self):
        """
        Reduce el tiempo en 1 segundo y actualiza los minutos y segundos restantes.
        """
        if self.tiempo <= 0:
            self.tiempo = 0
        else:
            self.tiempo -= 1
        self.minutos = self.tiempo // 60
        self.segundos = self.tiempo % 60

    def pintar(self, SCREEN, lenguaje):
        """
        Dibuja el temporizador en la pantalla del juego.

        Args:
        - SCREEN (pygame.Surface): la superficie de la pantalla del juego.
        - lenguaje (str): el idioma del juego.

        Returns:
        - None
        """
        text = get_font(30).render(f"{idioma[lenguaje]['Juego']['Tiempo']}{self.minutos}:{self.segundos}", True, "White")
        rect = text.get_rect(center=(740, 50))
        SCREEN.blit(text, rect)

    def reiniciar(self):
        """
        Reinicia el tiempo a cero.
        """
        self.tiempo = 0

class Personaje():
    """
    Clase que representa al personaje del juego.

    Atributos:
    - PX (int): posición en el eje X del personaje.
    - PY (int): posición en el eje Y del personaje.
    - piso (int): número del piso en el que se encuentra el personaje.
    - velocidad (int): velocidad de movimiento del personaje.
    - orientacion (int): dirección hacia la que está mirando el personaje (0 = izquierda, 1 = derecha).
    - estado (int): estado actual del personaje (0 = quieto, 1 = caminando).
    - fotograma (int): número del fotograma actual de la animación del personaje.
    """

    def __init__(self):
        """
        Inicializa los atributos del personaje.
        """
        global PISOS
        self.PX = 876
        self.PY = PISOS[1]
        self.piso = 1
        self.velocidad = 15
        self.orientacion = 0 # 0 = izquierda, 1 = derecha
        self.estado = 0 # 0 = quieto, 1 = caminando
        self.fotograma = 1
        self.ancho = 50

    def mover(self, key, focos, SCREEN, imgs):
        """
        Mueve al personaje en la dirección especificada.

        Args:
        - key (pygame.key.get_pressed()): tecla presionada por el usuario.
        - focos (Foco): diccionario que contiene los focos del juego.
        """
        global accion, focosApagados, focosEncendidos, teclaEstado
        presiono = False

        if key[pygame.K_a] and self.PX > 100 and self.PX - self.velocidad > 100:
            self.PX -= self.velocidad
            self.orientacion = 0
            self.estado = 1
            presiono = True
        elif key[pygame.K_d] and self.PX < 1050 and self.PX + self.velocidad < 1050:
            self.PX += self.velocidad
            self.orientacion = 1
            self.estado = 1
            presiono = True
            
        if self.piso == 1 and ((self.PX >= 205 and self.PX <= 252) or (self.ancho + self.PX >= 205 and self.PX + self.ancho <= 252)):
            comprobarTeclaEstado()
            SCREEN.blit(imgs[f"w{teclaEstado}"], (self.PX, self.PY - 50))
            teclaEstado += 1
            if key[pygame.K_w] and accion == True:
                self.PY = PISOS[2]
                self.piso = 2
                accion = False
                presiono = True
        elif self.piso == 2:
            if (self.PX + (self.ancho / 2) >= 205 and self.PX + (self.ancho / 2) <= 252) or (self.PX + self.ancho >= 205 and self.PX + self.ancho <= 252):
                comprobarTeclaEstado()
                SCREEN.blit(imgs[f"w{teclaEstado}"], (self.PX, self.PY - 50))
                teclaEstado += 1
                if key[pygame.K_w] and accion == True:
                    self.PY = PISOS[1]
                    self.piso = 1
                    accion = False
                    presiono = True
            if (self.PX + self.ancho >= 141 and self.PX + self.ancho <= 188) or (self.PX + (self.ancho / 2) >= 141 and self.PX + (self.ancho / 2) <= 188):
                comprobarTeclaEstado()
                SCREEN.blit(imgs[f"w{teclaEstado}"], (self.PX, self.PY - 50))
                teclaEstado += 1
                if key[pygame.K_w] and accion == True:
                    self.PY = PISOS[3]
                    self.piso = 3
                    accion = False
                    presiono = True
        elif self.piso == 3 and ((self.PX >= 141 and self.PX <= 188) or (self.ancho + self.PX >= 141 and self.PX + self.ancho <= 188)):
            comprobarTeclaEstado()
            SCREEN.blit(imgs[f"w{teclaEstado}"], (self.PX, self.PY - 50))
            teclaEstado += 1
            if key[pygame.K_w] and accion == True:
                self.PY = PISOS[2]
                self.piso = 2
                presiono = True
                accion = False

        for foco in focos.values():
            if foco.estado != 0 and foco.estado != 4 and self.piso == foco.piso:
                if self.PX >= foco.apagador1 - self.ancho and self.PX <= foco.apagador2 + self.ancho:
                    comprobarTeclaEstado()
                    SCREEN.blit(imgs[f"espacio{teclaEstado}"], (self.PX - 20, self.PY + 80))
                    teclaEstado += 1
                    if key[pygame.K_SPACE]:
                        foco.apagar()
                        focosApagados += 1
                        focosEncendidos -= 1
                        
        if presiono != True:
            self.estado = 0
            self.fotograma = 1

    def pintar(self, SCREEN, imgs):
        """
        Dibuja al personaje en la pantalla.

        Args:
        - SCREEN (pygame.Surface): superficie de la pantalla en la que se dibujará el personaje.
        - imgs (dict): diccionario que contiene las imágenes necesarias para dibujar al personaje.
        """
        if self.estado == 0:
            if self.orientacion == 0:
                SCREEN.blit(imgs["quietoIzq"], (self.PX, self.PY))
            else:
                SCREEN.blit(imgs["quietoDer"], (self.PX, self.PY))
        else:
            if self.orientacion == 0:
                SCREEN.blit(imgs[f"caminandoIzq{self.fotograma}"], (self.PX, self.PY))
            else:
                SCREEN.blit(imgs[f"caminandoDer{self.fotograma}"], (self.PX, self.PY))
            self.fotograma += 1
            if self.fotograma > 3:
                self.fotograma = 1

def comprobarTeclaEstado():
    global teclaEstado
    if teclaEstado > 2:
        teclaEstado = 1

def prenderFocoAzar(focos, Contador):
    """
    Función que prende o apaga un foco al azar.

    Args:
    - focos: diccionario que contiene los focos del juego.
    - Contador: Objeto Temporizador que contiene el tiempo del juego.

    Returns:
    - None
    """
    global segundoUltimoFoco, focosFundidos, focosEncendidos, ultimoFoco
    if segundoUltimoFoco + 4 <= Contador.tiempoPasado and focosEncendidos != 7 - focosFundidos:
        segundoUltimoFoco = Contador.tiempoPasado
        while True:
            numFoco = random.randint(1, 7)
            if focos[f"foco{numFoco}"].estado == 0:
                if focosEncendidos != 6 - focosFundidos and numFoco != ultimoFoco:
                    focos[f"foco{numFoco}"].prender()
                    focosEncendidos += 1
                    ultimoFoco = numFoco
                    break
                if focosEncendidos == 6 - focosFundidos:
                    focos[f"foco{numFoco}"].prender()
                    focosEncendidos += 1
                    ultimoFoco = numFoco
                    break
        pygame.mixer.Sound("assets/sounds/abrirPuerta.wav").play() # Sonido de abrir puerta
        pygame.mixer.Sound("assets/sounds/prenderFoco.wav").play() # Sonido de encender foco

def pantalla_lvl3(SCREEN , configJuego, LvlsInfo, elementosFondo):
    """
    Función que muestra la pantalla del nivel 3 del juego LightsOut.

    Args:
    - SCREEN: objeto pygame.Surface que representa la pantalla del juego.
    - configJuego: diccionario con la configuración actual del juego.
    - LvlsInfo: diccionario con la información de los niveles del juego.
    - elementosFondo: diccionario con los elementos de fondo del juego.

    Returns:
    - None
    """
    # cargamos la música si no está cargada
    if configJuego["indiceMusic"] != 2:
        configJuego["indiceMusic"] = 2
        pygame.mixer.music.load(f"assets/songs/musica{configJuego['indiceMusic']}.wav") #cargamos la musica
        pygame.mixer.music.set_volume(configJuego["Volumen"]) #le bajamos el volumen a la musica
        pygame.mixer.music.play(-1) #reproducimos la musica en bucle

        global accion

        # improtamos imagenes
        imgs = imgs_lvl3(configJuego["Idioma"], configJuego["personaje"])

        # creamos los objetos
        
        btnPausa = Button(image1=None, pos=(1047,57), text_input="||", font=get_font(30), base_color="White", hovering_color="#555f68")

        Jugador = Personaje()

        Contador = Temporizador()

        BarraConsumo = Barra(700)

        # creamos los focos
        focos = {
            "foco1": Foco(1, (462, 181), 434, (426, 231), 3),
            "foco2": Foco(2, (764, 181), 730, (724, 234), 3),
            "foco3": Foco(3, (332, 371), 301, (295, 419), 2),
            "foco4": Foco(4, (604, 371), 579, (568, 419), 2),
            "foco5": Foco(5, (907, 371), 880, (879, 423), 2),
            "foco6": Foco(6, (489, 550), 458, (453, 598), 1),
            "foco7": Foco(7, (823, 550), 787, (789, 601), 1)
        }

        # creamos los power-ups
        powerUps = {
            "powerUp1": PowerUp("rayo", 10, 50),
            "powerUp2": PowerUp("consumo", 10, 50)
        }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro(SCREEN, accion = "cerrar")
                pygame.quit()
                sys.exit()

        evento = pygame.key.get_pressed()

        reloj.tick(10)

        # imprimos el fondo
        SCREEN.blit(imgs["fondo"], (0, 0))

        # imprimimos el boton de pausa
        btnPausa.changeColor(pygame.mouse.get_pos())
        btnPausa.update(SCREEN)

        Contador.actualizarTiempo()
        if  Contador.comprobarTiempo(): 
            Contador.bajarTiempo()
            for foco in focos.values():
                if foco.estadoPuerta == 2:
                    foco.cerrarPuerta()
                if foco.estado != 0 and foco.estado != 4:
                    foco.aumentarTiempo()
                    
            BarraConsumo.aumentarConsumo(focos)
            if accion == False:
                accion = True

        Contador.pintar(SCREEN, configJuego["Idioma"])

        Jugador.mover(evento, focos, SCREEN, imgs)
        Jugador.pintar(SCREEN, imgs)

        prenderFocoAzar(focos, Contador)

        # imprimimos los focos
        for foco in focos.values():
            foco.pintar(SCREEN, imgs)

        # imprimimos los power-ups
        for powerUp in powerUps.values():
            powerUp.pintar(SCREEN, imgs)

        SCREEN.blit(imgs["sombras"], (0, 0))

        pygame.display.flip()