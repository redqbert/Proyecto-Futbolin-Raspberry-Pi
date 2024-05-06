import pygame
import time
import random
pygame.init()

ANCHO, ALTO = 800, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pantalla de Selección de Equipos")

# Crear reloj, para controlar los fps 
reloj = pygame.time.Clock()

# Cargar sprites de moneda
imagen = "gold_{}.png"
lista_sprites_lanzamiento_moneda = []
fotograma_moneda = 0
estado = 1  # Para hacer la secuencia

# Resultado de moneda, se coloca entre 0 y dos debido a que se quiere el entero en este caso.
resultado_moneda = int(random.uniform(0, 2))

if resultado_moneda == 0:
    for i in range(1, 21):
        image_filename = imagen.format(i)
        lista_sprites_lanzamiento_moneda.append(pygame.image.load(image_filename))
else:
    for i in range(20, 0, -1):
        image_filename = imagen.format(i)
        lista_sprites_lanzamiento_moneda.append(pygame.image.load(image_filename))

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Cargar imágenes de jugadoras

#Equipo Boston Breakers

imagen_Allysha_Chapman = pygame.image.load("Jugadoras/allysha chapman.png") # Jugadora 1
imagen_Allysha_Chapman = pygame.transform.scale(imagen_Allysha_Chapman, (100 , 100))

imagen_Brooke_Elby = pygame.image.load("Jugadoras/brooke elby.png") # Jugadora 2 
imagen_Brooke_Elby = pygame.transform.scale(imagen_Brooke_Elby, (100 , 100))

imagen_Alyssa_Naeher = pygame.image.load("Jugadoras/Alyssa Naeher.png") # Portera 1
imagen_Alyssa_Naeher = pygame.transform.scale(imagen_Alyssa_Naeher, (100 , 100))

#Equipo FC Kansas City
imagen_Shea_Groom = pygame.image.load("Jugadoras/Shea Groom.png") # Jugadora 3
imagen_Shea_Groom = pygame.transform.scale(imagen_Shea_Groom, (100, 100))

imagen_Becca_Moros = pygame.image.load("Jugadoras/Becca Moros.png") # Jugadora 4
imagen_Becca_Moros = pygame.transform.scale(imagen_Becca_Moros, (100, 100))

imagen_Jordan_Silkowitz = pygame.image.load("Jugadoras/Jordan Silkowitz.png") # Portera 2
imagen_Jordan_Silkowitz = pygame.transform.scale(imagen_Jordan_Silkowitz, (100, 100))


#Western New York Flash
imagen_Teigen_Allen = pygame.image.load("Jugadoras/Teigen Allen.png") # Jugadora 5
imagen_Teigen_Allen = pygame.transform.scale(imagen_Teigen_Allen, (100, 100))

imagen_Michelle_Heyman = pygame.image.load("Jugadoras/Michelle Heyman.png") # Jugadora 6
imagen_Michelle_Heyman = pygame.transform.scale(imagen_Michelle_Heyman, (100, 100))

imagen_Katelyn_Rowland = pygame.image.load("Jugadoras/katelyn rowland.png") # Portera 3
imagen_Katelyn_Rowland = pygame.transform.scale(imagen_Katelyn_Rowland, (100, 100))


class Jugador:
    def __init__(self, equipo, posicion, nombre, imagen):
        self.equipo = equipo
        self.posicion = posicion
        self.nombre = nombre
        self.imagen = imagen

    def dibujar(self):
        pantalla.blit(self.imagen, (self.posicion[0] - self.imagen.get_width() // 2, self.posicion[1] - self.imagen.get_height() // 2))
        fuente = pygame.font.Font(None, 24)
        texto = fuente.render(self.nombre, True, BLANCO)
        pantalla.blit(texto, (self.posicion[0] - texto.get_width() // 2, self.posicion[1] + 50))

class Portero(Jugador):
    def __init__(self, equipo, posicion, nombre, imagen):
        super().__init__(equipo, posicion, nombre, imagen)

    def dibujar(self):
        pantalla.blit(self.imagen, (self.posicion[0] - self.imagen.get_width() // 2, self.posicion[1] - self.imagen.get_height() // 2))
        fuente = pygame.font.Font(None, 24)
        texto = fuente.render(self.nombre, True, BLANCO)
        pantalla.blit(texto, (self.posicion[0] - texto.get_width() // 2, self.posicion[1] + 50))

class Equipo:
    def __init__(self, nombre, color, jugadoras):
        self.nombre = nombre
        self.color = color
        self.jugadores = jugadoras
        self.portero = None

# Crear equipos
equipo1 = Equipo("Boston Breakers", (255, 0, 0), [])
equipo2 = Equipo("FC Kansas City", (0, 255, 0), [])
equipo3 = Equipo("Western New York Flash", (0, 0, 255), [])

# Definir los nombres de las jugadoras
nombres_jugadores = ["Allysha Chapman", "Brooke Elby", "Shea Groom", "Becca Moros", "Teigen Allen", "Michelle Heyman", "Alyssa Naecher", "Jordan Silkowitz", "katelyn rowland"] 

# Añadir jugadores a los equipos
for i in range(2):
    equipo1.jugadores.append(Jugador(equipo1, (150 + i * 200, 200), nombres_jugadores[i], imagen_Allysha_Chapman))
    equipo2.jugadores.append(Jugador(equipo2, (150 + i * 200, 400), nombres_jugadores[i + 2], imagen_Shea_Groom)) 
    equipo3.jugadores.append(Jugador(equipo3, (150 + i * 200, 600), nombres_jugadores[i + 4], imagen_Teigen_Allen))


# Añadir porteros a los equipos
equipo1.portero = Portero(equipo1, (ANCHO // 1.5, 200), nombres_jugadores[6], imagen_Alyssa_Naeher)
equipo2.portero = Portero(equipo2, (ANCHO // 1.5, 400), nombres_jugadores[7], imagen_Jordan_Silkowitz)
equipo3.portero = Portero(equipo3, (ANCHO // 1.5, 600), nombres_jugadores[8], imagen_Katelyn_Rowland)

equipos = [equipo1, equipo2, equipo3]

def seleccionar_siguiente_jugador():
    global indice_equipo, indice_jugador
    indice_jugador += 1
    if indice_jugador >= len(equipos[indice_equipo].jugadores):
        indice_jugador = 0
        indice_equipo += 1
        if indice_equipo >= len(equipos):
            indice_equipo = 0

lanzamiento_moneda = 0
corriendo = True
indice_equipo = 0
indice_jugador = 0
inicio_tiempo = None
seleccion_pausada = False

Jugadora_selecionada = []

show_selected_players_screen = False

timer_reset_count = 0

def Mostrar_Jugadora_Seleccionada(players):
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 36)
    texto1 = fuente.render("Jugadoras Seleccionadas:", True, BLANCO)
    pantalla.blit(texto1, (ANCHO // 2 - texto1.get_width() // 2, ALTO // 4))
    for i, player in enumerate(players):
        texto2 = fuente.render(f"{player.equipo.nombre} - {player.nombre}", True, BLANCO)
        pantalla.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 4 + 50 + i * 50))
    pygame.display.flip()

while corriendo:
    pantalla.fill(NEGRO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if len(Jugadora_selecionada) < 2:
                    Jugadora_selecionada.append(equipos[indice_equipo].jugadores[indice_jugador])
                if len(Jugadora_selecionada) == 2:
                    show_selected_players_screen = True
            elif evento.key == pygame.K_RIGHT:
                indice_jugador += 1
                if indice_jugador >= len(equipos[indice_equipo].jugadores):
                    indice_jugador = 0
            elif evento.key == pygame.K_LEFT:
                indice_jugador -= 1
                if indice_jugador < 0:
                    indice_jugador = len(equipos[indice_equipo].jugadores) - 1
            elif evento.key == pygame.K_DOWN:
                indice_equipo += 1
                if indice_equipo >= len(equipos):
                    indice_equipo = 0
            elif evento.key == pygame.K_UP:
                indice_equipo -= 1
                if indice_equipo < 0:
                    indice_equipo = len(equipos) - 1

    if estado == 1 and fotograma_moneda < 19:
        pantalla.blit(lista_sprites_lanzamiento_moneda[int(fotograma_moneda)], (2, 3))
        fotograma_moneda += 0.32
    else:
        estado = 2

    if estado == 2:
        for equipo in equipos:
            fuente = pygame.font.Font(None, 36)
            texto = fuente.render(equipo.nombre, True, BLANCO)
            rect_texto = texto.get_rect(center=(ANCHO // 2, equipo.jugadores[0].posicion[1] - 100))
            pantalla.blit(texto, rect_texto)

            for jugador in equipo.jugadores:
                jugador.dibujar()
                pantalla.blit(imagen_Brooke_Elby, (300, 150))
                pantalla.blit(imagen_Becca_Moros, (300, 350))
                pantalla.blit(imagen_Michelle_Heyman, (300, 550))

            equipo.portero.dibujar()

        jugador_seleccionado = equipos[indice_equipo].jugadores[indice_jugador]
        if isinstance(jugador_seleccionado, Portero):
            indice_jugador += 1
            if indice_jugador >= len(equipos[indice_equipo].jugadores):
                indice_jugador = 0
            jugador_seleccionado = equipos[indice_equipo].jugadores[indice_jugador]
        pygame.draw.rect(pantalla, (255, 255, 0), (jugador_seleccionado.posicion[0] - 45, jugador_seleccionado.posicion[1] - 45, 90, 90), width=2)

        if inicio_tiempo is not None:
            elapsed_time = time.time() - inicio_tiempo
            remaining_time = max(0, 5 - elapsed_time)
            font = pygame.font.Font(None, 36)
            text = font.render(f"Tiempo: {remaining_time:.1f}", True, BLANCO)
            pantalla.blit(text, (20, 20))

        # Mensaje para mostrar cómo continuar
        if elapsed_time >= 5:
            font = pygame.font.Font(None, 24)
            text = font.render("El timer ha terminado, presiona espacio para continuar", True, BLANCO)
            text_rect = text.get_rect(center=(ANCHO // 2, ALTO - 20))
            pantalla.blit(text, text_rect)

    reloj.tick(60)

    pygame.display.flip()

    if show_selected_players_screen:
        Mostrar_Jugadora_Seleccionada(Jugadora_selecionada)
        waiting_for_interaction = True
        while waiting_for_interaction:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        waiting_for_interaction = False
                    elif evento.key == pygame.K_ESCAPE:
                        corriendo = False

    if inicio_tiempo is not None:
        elapsed_time = time.time() - inicio_tiempo
        if elapsed_time >= 5 and len(Jugadora_selecionada) < 2 and timer_reset_count < 1:
            Jugadora_selecionada.append(equipos[indice_equipo].jugadores[indice_jugador])
            inicio_tiempo = None
            timer_reset_count += 1
    else:
        inicio_tiempo = time.time()

pygame.quit()