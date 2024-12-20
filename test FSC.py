import pygame
import time
import random
import serial
import pygame_menu

rasp_coneccion = serial.Serial('COM3', 9600)

pygame.init()
ANCHO, ALTO = 800, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pantalla de Selección de Equipos")
seleccion_jugador_automatica=['verdadero']



def inicio_juego(seleccion_jugador_automatica):

    #Variables de estadisticas
    tiros_fallidos_visitante=0
    tiros_fallidos_local=0

    acertados_local=0
    acertados_visitante=0

    atajados_portero_alocal=0
    atajados_portero_avisitante=0



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
        inicio_turno = "Local"
    else:
        inicio_turno = "Visitante"

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

    seleccion_jugador_automatica=['falso']

    while corriendo:
        pantalla.fill(NEGRO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

    

        if estado == 1:#Si tira error son los estados


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



        elif estado == 3 and fotograma_moneda < 19:
            pantalla.blit(lista_sprites_lanzamiento_moneda[int(fotograma_moneda)], (2, 3))
            fotograma_moneda += 0.3
            if int(fotograma_moneda ) == 19:
                estado = 4
                texto_pantalla(f'Empieza {inicio_turno}',True,BLANCO,ANCHO/2,ALTO/2)
        
        elif estado == 2 :
            #Mostrar jugadoras en pantalla
            if show_selected_players_screen:
                Mostrar_Jugadora_Seleccionada(Jugadora_selecionada)
            time.sleep(3)
            estado = 3

        elif estado == 4 and turno <= 9 :
            pygame.mixer.Sound.play(pitido_inicial)
            texto_pantalla(f'Turno de {inicio_turno}',True,BLANCO,ANCHO//2,ALTO//2)
            time.sleep(3)
            estado = 'tiro'

            #Cambio boton personalizado
            #pygame.mixer.Sound.play(abucheo)
        


        elif estado == 'tiro':
            #Para encender led de local o visitante 
            if inicio_turno=="Local":
                rasp_coneccion.write((str('ledlocal') + ',').encode()) #Abrir para escribir porteria en rasberry
            elif inicio_turno=="Visitante":
                rasp_coneccion.write((str('ledvisitante') + ',').encode()) #Abrir para escribir porteria en rasberry
            

            #Poscion del portero
            indice = int(  random.uniform(1, 4) )#Generar numero aleatorio para saber que indice es
            if indice==1:
                portero = paletas_indice_1[ int(  random.uniform( 0,3 ) ) ]

            elif indice==2:
                portero = paletas_indice_2[ int(  random.uniform( 0,2 ) ) ]

            elif indice==3:
                portero = paletas_indice_3[ int(  random.uniform( 0,2 ) ) ]

            pygame.mixer.Sound.play(tiros)

        
            while segundos_turno<=4:
                #Para encender led de local o visitante
                """
                if inicio_turno=="Local":
                    rasp_coneccion.write((str('ledlocal') + ',').encode()) #Abrir para escribir porteria en rasberry
                elif inicio_turno=="Visitante":
                    rasp_coneccion.write((str('ledvisitante') + ',').encode()) #Abrir para escribir porteria en rasberry
                """
                texto_pantalla(f"Puntaje visitante: {acertados_visitante}",False,BLANCO,ANCHO/2,ALTO/2-300)
                texto_pantalla(f"Puntaje local: {acertados_local}",False,BLANCO,ANCHO/2,ALTO/2-200)
                rasp_coneccion.write((str('porteria') + ',').encode()) #Abrir para escribir porteria en rasberry
                lectura_porteria = str(rasp_coneccion.readline().decode('unicode_escape')) #Lectura porteria
                lectura_porteria = eliminar_saltos_y_espacios(lectura_porteria) #Quitar espacios y saltos de linea a la lectura de la porteria
                time.sleep(1)
                if lectura_porteria != 'No':# Se esta tocanto alguna paleta,por lo que el no representa que no se toca ninguna
                    break
                segundos_turno +=1

            #Para encender led de local o visitante

            if lectura_porteria == 'No':#Para casos en los que no se jugo
                if inicio_turno=="Local":
                    tiros_fallidos_visitante+=1
                else:
                    tiros_fallidos_local+=1
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
                        #Si fue atajado,entonces se suma a atajados
                        if inicio_turno=="Local":
                            atajados_portero_avisitante+=1
                        else:
                            atajados_portero_alocal+=1
                        break
                    else:
                        anotacion = True
            print("esta aqui")

            if anotacion == True:
                pygame.mixer.Sound.play(gol)
                rasp_coneccion.write((str('gol') + ',').encode()) #Luces de la porteria
                time.sleep(2)
                if inicio_turno == 'Visitante':
                    acertados_visitante+=1
                elif inicio_turno == "Local":
                    acertados_local+=1
            if inicio_turno == 'Visitante':
                inicio_turno = 'Local'
            elif inicio_turno == 'Local':
                inicio_turno = 'Visitante'
            print("o aqui")
            
            """if seleccion_jugador_automatica==['falso']: 
               while True:
                    pantalla.fill(BLANCO)
                    texto_pantalla("Presione el boton para cambiar de jugador a portero y de portero a jugador",False,BLANCO,ANCHO/2,ALTO/2-300)
                    rasp_coneccion.write((str('cambio_jugador') + ',').encode()) 
                    boton = str(rasp_coneccion.readline().decode('unicode_escape')) 
                    boton = eliminar_saltos_y_espacios(boton) 
                    if boton == "cambio":
                        break
            """
            rasp_coneccion.write((str('ledvlapagar') + ',').encode()) #Luces de la porteria para los fallos
            print("aqui2")
            estado = 4
            anotacion = False
            segundos_turno = 0
            print(estado)
            turno += 1


            if turno == 10:
                estado = 5

        elif estado == 5:
            pantalla.fill(NEGRO)
            texto_pantalla("Resumen de estadisticas",False,BLANCO,ANCHO/2,ALTO/2-350)
            texto_pantalla(f"Goles acertados por visitante: {acertados_visitante}",False,BLANCO,ANCHO/2,ALTO/2-300)
            texto_pantalla(f"Goles acertados por local: {acertados_local}",False,BLANCO,ANCHO/2,ALTO/2-200)
            texto_pantalla(f"Atajados por el portero a visitante: {atajados_portero_avisitante}",False,BLANCO,ANCHO/2,ALTO/2-100)
            texto_pantalla(f"Atajados por el portero a local: {atajados_portero_alocal}",False,BLANCO,ANCHO/2,ALTO/2+100)
            texto_pantalla(f"Tiros fallidos de local: {tiros_fallidos_local}",False,BLANCO,ANCHO/2,ALTO/2+200)
            texto_pantalla(f"Tiros fallidos de local:{tiros_fallidos_visitante}",False,BLANCO,ANCHO/2,ALTO/2+300)
            time.sleep(10)
            menu()


        reloj.tick(60)

        pygame.display.flip()

def Cambio_de_jugador(value, value1):#seleccion de menu de dificultad
    seleccion_jugador_automatica[0] = value1


def menu():
    about = ['Nombres: Isaac Valle ,Sergio ',
                'Asignatura: Fundamentos de sistemas computacionales',
                'Carrera:Ingenieria en computadores',
                '2024',
                'Profesor Leonardo Araya',
                'Costa Rica',
                'Version 1',
                'El programa corre como un codigo completo,en el que una vez se inicia hasta que no se termine no se podra cerrar,si se cierra se pierde el progreso']
    menu = pygame_menu.Menu('Bienvenido al CEFoot ver 4.0 Ghost GoalKeeper',
                                800, 
                                800,
                        theme=pygame_menu.themes.THEME_SOLARIZED	)
   
    about_menu = pygame_menu.Menu(
        height=800,
        theme=pygame_menu.themes.THEME_SOLARIZED,
        title='About',
        width=800
    )

    for i in range(0,8):
        about_menu.add.label(about[i], align=pygame_menu.locals.ALIGN_LEFT, font_size=20)


    surface = pygame.display.set_mode((800, 800))# crear ventana para el menu

  

    menu.add.button('Play', inicio_juego,Cambio_de_jugador)#Presionar para jugar
    menu.add.selector('Cambio de jugador',
                            [('automatico', 'verdadero'),
                                ('manual', 'falso')],
                            onchange=Cambio_de_jugador,
                            selector_id='Cambio_de_jugador')
    menu.add.button('About', about_menu)#Presionar para jugar

    menu.add.button('Salir', pygame_menu.events.EXIT)



    menu.mainloop(surface)



menu()