import pygame
import time
import random
pygame.init()

ANCHO, ALTO = 800, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pantalla de Selección de Equipos")

#Crear reloj,para controlar los fps 
reloj = pygame.time.Clock()

#Cargar sprites de moneda
imagen = "gold_{}.png"
lista_sprites_lanzamiento_moneda=[]
fotograma_moneda=0
estado = 1 #Para hacer la secuencia

#Resultado de moneda,se coloca entre 0 y dos debido a que se quiere el entero en este caso.
resultado_moneda = int( random.uniform(0,2) )  


#Cargar animacion de la moneda dependiendo del resultado
if resultado_moneda == 0:
    for i in range(1,21):
        image_filename = imagen.format(i)
        lista_sprites_lanzamiento_moneda.append(pygame.image.load(image_filename))
else:
    for i in range(20, 0, -1): 
        image_filename = imagen.format(i)
        lista_sprites_lanzamiento_moneda.append(pygame.image.load(image_filename))

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Define clases de jugadores
class Jugador:
    def __init__(self, equipo, posicion):
        self.equipo = equipo
        self.posicion = posicion

    def dibujar(self):
        pygame.draw.rect(pantalla, self.equipo.color, (self.posicion[0]-45, self.posicion[1]-45, 90, 90))

class Portero(Jugador):
    def __init__(self, equipo, posicion):
        super().__init__(equipo, posicion)

    def dibujar(self):
        pygame.draw.circle(pantalla, self.equipo.color, self.posicion, 60)

class Equipo:
    def __init__(self, nombre, color, jugadores):
        self.nombre = nombre
        self.color = color
        self.jugadores = jugadores
        self.portero = None

# Crear equipos
equipo1 = Equipo("Equipo 1", (255, 0, 0), [])
equipo2 = Equipo("Equipo 2", (0, 255, 0), [])
equipo3 = Equipo("Equipo 3", (0, 0, 255), [])

# Definir jugadores y asignarlos a los equipos
for i in range(2): # 2 jugadores por equipo
    equipo1.jugadores.append(Jugador(equipo1, (150 + i * 200, 200)))
    equipo2.jugadores.append(Jugador(equipo2, (150 + i * 200, 400)))
    equipo3.jugadores.append(Jugador(equipo3, (150 + i * 200, 600)))

# Porteros posicion
equipo1.portero = Portero(equipo1, (ANCHO // 1.5, 200))
equipo2.portero = Portero(equipo2, (ANCHO // 1.5, 400))
equipo3.portero = Portero(equipo3, (ANCHO // 1.5, 600))

equipos = [equipo1, equipo2, equipo3]

# Función que "selecciona" el jugador (No definitivo)
def seleccionar_siguiente_jugador():
    global indice_equipo, indice_jugador
    indice_jugador += 1
    if indice_jugador >= len(equipos[indice_equipo].jugadores):
        indice_jugador = 0
        indice_equipo += 1
        if indice_equipo >= len(equipos):
            indice_equipo = 0

# Main loop
lanzamiento_moneda = 0
corriendo = True
indice_equipo = 0
indice_jugador = 0
inicio_tiempo = time.time()
seleccion_pausada = False  # Flag para controlar el bucle de selección

while corriendo:
    pantalla.fill(NEGRO) 

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                seleccion_pausada = not seleccion_pausada

    if estado == 1 and fotograma_moneda<19:
            pantalla.blit(lista_sprites_lanzamiento_moneda[int(fotograma_moneda )],(2,3))
            fotograma_moneda += 0.32
    else:
        estado = 2

    if estado == 2:
        # Cambia la seleccion del jugador cada 2 segundos
        if not seleccion_pausada:
            tiempo_actual = time.time()
            if tiempo_actual - inicio_tiempo >= 2:
                seleccionar_siguiente_jugador()
                inicio_tiempo = tiempo_actual

        # Nombre de los equipos
        for equipo in equipos:
            fuente = pygame.font.Font(None, 36)
            texto = fuente.render(equipo.nombre, True, BLANCO)
            rect_texto = texto.get_rect(center=(ANCHO // 2, equipo.jugadores[0].posicion[1] - 100))
            pantalla.blit(texto, rect_texto)

            # Jugadores
            for jugador in equipo.jugadores:
                jugador.dibujar()

            # Portero
            equipo.portero.dibujar()

        # Resaltar jugador seleccionado si no es None
        jugador_seleccionado = equipos[indice_equipo].jugadores[indice_jugador]
        if isinstance(jugador_seleccionado, Portero):
            indice_jugador += 1
            if indice_jugador >= len(equipos[indice_equipo].jugadores):
                indice_jugador = 0
            jugador_seleccionado = equipos[indice_equipo].jugadores[indice_jugador]
        pygame.draw.rect(pantalla, (255, 255, 0), (jugador_seleccionado.posicion[0]-45, jugador_seleccionado.posicion[1]-45, 90, 90), width=2)

    reloj.tick(60)

    pygame.display.flip()

pygame.quit()
