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
    def __init__(self, numero, tiempo_encendido, posicion, apagador, posicion_puerta, piso):
        self.numero = numero
        self.estado = 0 # 0 = apagado, 1 = encendido, 2 = amarillo, 3 = rojo, 4 = fundido
        self.ultimo_estado = 1
        self.tiempo_encendido = tiempo_encendido
        self.posicion = posicion
        self.apagador = apagador
        self.estadoPuerta = 1
        self.posicion_puerta = posicion_puerta
        self.piso = piso

    def prender(self):
        self.estado = self.ultimo_estado

    def apagar(self):
        self.ultimo_estado = self.estado
        self.estado = 0

    def aumentarTiempo(self):
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
        self.estadoPuerta = estado

    def pintarFoco(self, SCREEN, imgs):
        if self.estado == 0 and self.estado == 4:
            SCREEN.blit(imgs["sombras"][f"sombra{self.estado}"], (0, 0))
        else:
            SCREEN.blit(imgs["focos"][f"bombilla{self.estado}"], self.posicion)

    def reiniciar(self):
        self.estado = 0
        self.tiempo_encendido = 0
        self.estadoPuerta = 1

class PowerUp():
    def __init__(self, nombre, tiempo, alto):
        self.nombre = nombre
        self.PX = 0
        self.piso = 1
        self.activo = False
        self.suelto = False
        self.tiempoDefault = tiempo
        self.tiempo = self.tiempoDefault
        self.alto = alto

    def soltarP(self):
        self.PX = random.randint(200, 1000)
        self.piso = random.randint(1, 3)
        self.suelto = True

    def activar(self):
        self.suelto = False
        self.activarPowerUp = True

    def bajarTiempo(self):
        if (self.tiempo <= 0):
            self.reiniciar()
        else:
            self.tiempo -= 1

    def reiniciar(self):
        self.activo = False
        self.suelto = False
        self.piso = 1
        self.piso = 0
        self.tiempo = self.tiempoDefault

class Barra():
    def __init__(self, consumoMaximo):
        self.consumoTotal = 0
        self.consumoMaximo = consumoMaximo
        self.color = "#00FF00"

    def aumentarConsumo(self, focos):
        consumo = 0
        for foco in focos.values(): 
            if foco.estado == 1:
                consumo += 1
        self.consumoTotal += consumo

    def obtenerPorcentaje(self):
        return (self.consumoTotal * 100) / self.consumoMaximo
    
    def cambiarColor(self):
        if self.obtenerPorcentaje() > 33:
            self.color = "#FFFF00"
        if self.obtenerPorcentaje() > 66:
            self.color = "#FF0000"

    def pintar(self, SCREEN, imgs): # ! funcionalidad incompleta
        SCREEN.blit(imgs["barra"][f"barra{self.obtenerPorcentaje()}"], (0, 0)) 

    def reiniciar(self):
        self.consumoTotal = 0

class Temporizador():
    def __init__(self):
        self.tiempo = 121
        self.minutos = 2
        self.segundos = 0

    def bajarTiempo(self):
        if self.tiempo <= 0:
            self.tiempo = 0
        else:
            self.tiempo -= 1
        self.minutos = self.tiempo // 60
        self.segundos = self.tiempo % 60

    def pintar(self, SCREEN, lenguaje):
        text = get_font(30).render(f"{idioma[lenguaje]['juego']['Tiempo']}{self.minutos}:{self.segundos}", True, "White")
        rect = text.get_rect(center=(740, 50))
        SCREEN.blit(text, rect)

    def reiniciar(self):
        self.tiempo = 0

class Personaje():
    def __init__(self):
        self.PX = 0
        self.PY = 0
        self.piso = 1
        self.velocidad = 10
        self.orientacion = 0 # 0 = izquierda, 1 = derecha
        self.estado = 0 # 0 = quieto, 1 = caminando
        self.fotograma = 0

    def mover(self, direccion): # 0 = izquierda, 1 = derecha, 2 = quieto
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
        if self.estado == 0:
            if self.orientacion == 0:
                SCREEN.blit(imgs["quieroIzq"][0], (self.PX, self.PY))
            else:
                SCREEN.blit(imgs["quieroDer"][0], (self.PX, self.PY))
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

    while True:
        # Tu código de la pantalla del nivel 1 aquí
        print("Pantalla del nivel 1")