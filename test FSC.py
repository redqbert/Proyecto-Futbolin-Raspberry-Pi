import pygame
import time
import random
import serial
rasp_coneccion = serial.Serial('COM4', 9600)

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
#Lograr saber quien inicia si local o visitante
inicio_turno = 0
if resultado_moneda==0:
    inicio_turno = 'Local'
else:
    inicio_turno = 'Visitante'

#Cargar sonidos
abucheo = pygame.mixer.Sound('boo.mp3')
pitido_inicial = pygame.mixer.Sound('referee.mp3')
tiros = pygame.mixer.Sound('tiros.mp3')
gol = pygame.mixer.Sound('gol.mp3')

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

inicio_tiempo = time.time()

#fuente 
font = pygame.font.Font(None, 24)
fuente = pygame.font.Font(None, 36)

def Mostrar_Jugadora_Seleccionada(players):
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 36)
    texto1 = fuente.render("Jugadoras Seleccionadas:", True, BLANCO)

    pantalla.blit(texto1, (ANCHO // 2 - texto1.get_width() // 2, ALTO // 4))
    for i, player in enumerate(players):
        texto2 = fuente.render(f"{player.equipo.nombre} - {player.nombre}", True, BLANCO)
        pantalla.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 4 + 50 + i * 50))
    pygame.display.flip()

#Renderizar texto en pantalla
def texto_pantalla(texto,aa,color,x,y):
    texto = font.render(texto, aa, color)
    pantalla.blit(texto,(x,y))

turno = 0

segundos_turno = 0

lectura_porteria='No'


#Anotacion inicializa en verdadero,si no hay anotacion se vuelve a falsa
anotacion = False


def eliminar_saltos_y_espacios(texto):
  
  texto_sin_saltos = texto.replace('\n', '')

  texto_sin_espacios = texto_sin_saltos.strip()

  return ' '.join(texto_sin_espacios.split())

#Paletas por indice
paletas_indice_1=[ ['A','B'],['C','D'],['E','F'] ]
paletas_indice_2=[ ['A','B','C'],['D','E','F'] ]
paletas_indice_3= [['A','C','E'],['B','D','F']]

puntaje_visitante = 0
puntaje_local = 0


while corriendo:
    pantalla.fill(NEGRO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

  

    if estado == 4:


        key = pygame.key.get_pressed()

        #Inicializar lectura del potenciometro
        
        rasp_coneccion.write((str('potenciometro') + ',').encode())
        lectura = rasp_coneccion.readline().decode('unicode_escape')
        seleccion_jugador=str(lectura  )

        if key[pygame.K_SPACE]:
            if len(Jugadora_selecionada) < 2:
                Jugadora_selecionada.append(equipos[indice_equipo].jugadores[indice_jugador])
            if len(Jugadora_selecionada) == 2:
                show_selected_players_screen = True
            estado = 2

        #seleccion de jugadores a traves del potenciometro
        elif float( seleccion_jugador  ) < 0.5:        
            indice_equipo = 0
            indice_jugador = 0

        elif float( seleccion_jugador  ) >= 0.5 and float( seleccion_jugador  ) < 1:
            indice_equipo=0
            indice_jugador = 1

        elif float( seleccion_jugador  ) >= 1 and float( seleccion_jugador  ) < 1.5:
            indice_equipo = 1
            indice_jugador = 0

        elif float( seleccion_jugador  ) >= 1.5 and float( seleccion_jugador  ) < 2:
            indice_equipo = 1
            indice_jugador = 1

        elif float( seleccion_jugador  ) >= 2 and float( seleccion_jugador  ) < 2.5:
            indice_equipo = 2
            indice_jugador = 0

        elif float( seleccion_jugador  ) >= 2.5 and float( seleccion_jugador  ) < 3:
            indice_equipo = 2
            indice_jugador = 1


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
            remaining_time = max(0, 10 - elapsed_time)

        # Mensaje para mostrar cómo continuar

        if inicio_tiempo is not None:
            elapsed_time = time.time() - inicio_tiempo
        if elapsed_time >= 5 and len(Jugadora_selecionada) < 2 and timer_reset_count < 1:
            Jugadora_selecionada.append(equipos[indice_equipo].jugadores[indice_jugador])
            timer_reset_count += 1

        if elapsed_time >= 10:
            text = font.render("El timer ha terminado, presiona espacio para continuar", True, BLANCO)
            text_rect = text.get_rect(center=(ANCHO // 2, ALTO - 20))
            pantalla.blit(text, text_rect)
            elapsed_time = 0

        texto_pantalla('Tiene 5 seg para seleccionar al primer jugador,luego otros 5 para el segundo jugador', True, BLANCO,0,0)
        texto_pantalla(f'{int(elapsed_time)}',True,BLANCO,0,20)



    elif estado == 2 and fotograma_moneda < 19:
        pantalla.blit(lista_sprites_lanzamiento_moneda[int(fotograma_moneda)], (2, 3))
        fotograma_moneda += 0.09
        if int(fotograma_moneda ) == 19:
            estado = 3
    
    elif estado == 3 :
        #Mostrar jugadoras en pantalla
        if show_selected_players_screen:
            Mostrar_Jugadora_Seleccionada(Jugadora_selecionada)
        time.sleep(3)
        estado = 4

    elif estado == 1 and turno <= 9 :
        pygame.mixer.Sound.play(pitido_inicial)
        texto_pantalla(f'Turno de {inicio_turno}',True,BLANCO,ANCHO//2,ALTO//2)

        time.sleep(3)
        estado = 'tiro'

        #Cambio boton personalizado
        #pygame.mixer.Sound.play(abucheo)
    


    elif estado == 'tiro':


        #Poscion del portero
        indice = int(  random.uniform(1, 4) )#Generar numero aleatorio para saber que indice es
        if indice==1:
            portero = paletas_indice_1[ int(  random.uniform( 0,3 ) ) ]

        elif indice==2:
            portero = paletas_indice_2[ int(  random.uniform( 0,2 ) ) ]

        elif indice==3:
            portero = paletas_indice_3[ int(  random.uniform( 0,2 ) ) ]

        pygame.mixer.Sound.play(tiros)

    
        while segundos_turno<=6:
            texto_pantalla(f"Puntaje visitante: {puntaje_visitante}",False,BLANCO,ANCHO/2,ALTO/2-300)
            texto_pantalla(f"Puntaje local: {puntaje_local}",False,BLANCO,ANCHO/2,ALTO/2-200)
            rasp_coneccion.write((str('porteria') + ',').encode()) #Abrir para escribir porteria en rasberry
            lectura_porteria = str(rasp_coneccion.readline().decode('unicode_escape')) #Lectura porteria
            lectura_porteria = eliminar_saltos_y_espacios(lectura_porteria) #Quitar espacios y saltos de linea a la lectura de la porteria
            time.sleep(1)
            if lectura_porteria != 'No':# Se esta tocanto alguna paleta,por lo que el no representa que no se toca ninguna
                break
            segundos_turno +=1


        if lectura_porteria == 'No':
            pygame.mixer.Sound.play(abucheo)
            rasp_coneccion.write((str('fallogol') + ',').encode()) #Luces de la porteria para los fallos
            time.sleep(2)
            anotacion = False

        if lectura_porteria !="No":
            for elemento in portero:#Comprobar a cada elemento de portero,para saber si atrapo el balon
                if elemento == lectura_porteria:
                    anotacion = False
                    rasp_coneccion.write((str('fallogol') + ',').encode()) #Luces de la porteria para los fallos
                    time.sleep(2)
                    break
                else:
                    anotacion = True
                    pygame.mixer.Sound.play(abucheo)

        if anotacion == True:
            pygame.mixer.Sound.play(gol)
            rasp_coneccion.write((str('gol') + ',').encode()) #Luces de la porteria
            time.sleep(2)
            if inicio_turno == 'Visitante':
                puntaje_visitante+=1
            elif inicio_turno == "Local":
                puntaje_local+=1 

        if inicio_turno == 'Visitante':
            inicio_turno = 'Local'
        elif inicio_turno == 'Local':
            inicio_turno = 'Visitante'

        # borrelo al momento de crear el menu, seleccion_jugador_automatica es la variable,si se pone que false en el menu,entonces aqui va a meterse hasta que se presione el boton para cambiar jugador
        # if seleccion_jugador_automatica==False: este es el codigo para el menu
        #    while True:
        #        rasp_coneccion.write((str('cambio_jugador') + ',').encode()) 
        #        boton = str(rasp_coneccion.readline().decode('unicode_escape')) 
        #        boton = eliminar_saltos_y_espacios(boton) 
        #        if boton == "cambio":
        #            break
          
        estado = 1#SE modicia al final,es estado 3
        anotacion = False
        segundos_turno = 0
        print(estado)
        turno += 1

    reloj.tick(60)

    pygame.display.flip()

    

pygame.quit()