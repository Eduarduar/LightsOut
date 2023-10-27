import sys, pygame, random, time
from assets.defaults.button import Button
from assets.defaults.get_fonts import get_font
from assets.defaults.idioma import cargar_idioma
from assets.defaults.get_imgs import imgs_lvl2
from intro import intro

idioma = cargar_idioma()
reloj = pygame.time.Clock()

# Inicializamos las variables

class Foco:
    """
    Clase que representa un foco en el juego Lights Out.

    Atributos:
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

    Métodos:
    -------
    prender()
        Enciende el foco.
    apagar()
        Apaga el foco.
    aumentarTiempo()
        Aumenta el tiempo que el foco ha estado encendido y cambia su estado según el tiempo.
    cambiarEstadoPuerta(estado)
        Cambia el estado de la puerta a abierto o cerrado.
    pintarFoco(SCREEN, imgs)
        Dibuja el foco en la pantalla según su estado.
    reiniciar()
        Reinicia el foco a su estado inicial.
    """

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
        self.estadoPuerta = 1
        self.posicion_puerta = posicion_puerta
        self.piso = piso

    def prender(self):
        """Enciende el foco."""
        self.estado = self.ultimo_estado

    def apagar(self):
        """Apaga el foco."""
        self.ultimo_estado = self.estado
        self.estado = 0

    def aumentarTiempo(self):
        """Aumenta el tiempo que el foco ha estado encendido y cambia su estado según el tiempo."""
        if self.tiempo_encendido > 60:
            self.estado = 4
            self.ultimo_estado = 4
        elif self.tiempo_encendido > 30:
            self.estado = 3
            self.ultimo_estado = 3
        elif self.tiempo_encendido > 20:
            self.estado = 2
            self.ultimo_estado = 2

    def cambiarEstadoPuerta(self, estado):
        """
        Cambia el estado de la puerta a abierto o cerrado.

        Parámetros:
        ----------
        estado : int
            Estado de la puerta. 1 = cerrado, 0 = abierto.
        """
        self.estadoPuerta = estado

    def pintarFoco(self, SCREEN, imgs):
        """
        Dibuja el foco en la pantalla según su estado.

        Parámetros:
        ----------
        SCREEN : pygame.Surface
            Superficie de la pantalla.
        imgs : dict
            Diccionario con las imágenes de los focos y las sombras.
        """
        if self.estado == 0 and self.estado == 4:
            SCREEN.blit(imgs["sombras"][f"sombra{self.estado}"], (0, 0))
        else:
            SCREEN.blit(imgs["focos"][f"bombilla{self.estado}"], self.posicion)

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
        self.tiempo = 121
        self.minutos = 2
        self.segundos = 0

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
        text = get_font(30).render(f"{idioma[lenguaje]['juego']['Tiempo']}{self.minutos}:{self.segundos}", True, "White")
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
        self.PX = 0
        self.PY = 0
        self.piso = 1
        self.velocidad = 10
        self.orientacion = 0 # 0 = izquierda, 1 = derecha
        self.estado = 0 # 0 = quieto, 1 = caminando
        self.fotograma = 0

    def mover(self, direccion):
        """
        Mueve al personaje en la dirección especificada.

        Args:
        - direccion (str): dirección hacia la que se moverá el personaje (0 = izquierda, 1 = derecha, 2 = quieto).
        """
        if direccion == "0":
            self.PX -= self.velocidad
            self.orientacion = 0
            self.estado = 1
        elif direccion == "1":
            self.PX += self.velocidad
            self.orientacion = 1
            self.estado = 1
        elif direccion == "2":
            self.estado = 0

    def pintar(self, SCREEN, imgs):
        """
        Dibuja al personaje en la pantalla.

        Args:
        - SCREEN (pygame.Surface): superficie de la pantalla en la que se dibujará el personaje.
        - imgs (dict): diccionario que contiene las imágenes necesarias para dibujar al personaje.
        """
        if self.estado == 0:
            if self.orientacion == 0:
                SCREEN.blit(imgs["quietoIzq"][0], (self.PX, self.PY))
            else:
                SCREEN.blit(imgs["quietoDer"][0], (self.PX, self.PY))
        else:
            if self.orientacion == 0:
                SCREEN.blit(imgs[f"caminandoIzq{self.fotograma}"], (self.PX, self.PY))
            else:
                SCREEN.blit(imgs[f"caminandoDer{self.fotograma}"], (self.PX, self.PY))
            self.fotograma += 1
            if self.fotograma > 3:
                self.fotograma = 0

def pantalla_lvl3(SCREEN , configJuego, LvlsInfo, elementosFondo):
    if configJuego["indiceMusic"] != 2:
        configJuego["indiceMusic"] = 2
        pygame.mixer.music.load(f"assets/songs/musica{configJuego['indiceMusic']}.wav") #cargamos la musica
        pygame.mixer.music.set_volume(configJuego["Volumen"]) #le bajamos el volumen a la musica
        pygame.mixer.music.play(-1) #reproducimos la musica en bucle

        # creamos los objetos
        
        btnPausa = Button(image1=None, pos=(1047,57), text_imput="||", font=get_font(30), text_color="White", hoverring_color="#555f68")

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
        # imprimos el fondo
        SCREEN.blit(elementosFondo["fondo"], (0, 0))

        