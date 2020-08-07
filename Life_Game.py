import pygame
import numpy as np
import time

#Inicializamos la ventana del juego
pygame.init()
pygame.display.set_caption("El juego de la vida")

#Definimos la longitud del tablero y el color de relleno
width, height = 700, 700
screen = pygame.display.set_mode((width, height + 100))


light = (255,255,255)
dark = (25,25,25)
red = (255,0,0)
blue = (0,0,255)

screen.fill(dark)

#Tamaño de las celdas
nxC, nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC

#Estado de las celdas. 1 = Viva, 0 = Muerta
gameState = np.zeros((nxC, nyC))

pauseExect = True

dark_mode = True

spawn = False

speed = 0.1

speed_change = 1


def text_object(string, colour = red):
    text_format = pygame.font.Font('freesansbold.ttf', 20)
    text = text_format.render(string, True, colour)
    return text

def render_text(input, text_colour, pos):
    text = text_object(input, text_colour)
    screen.blit(text,pos)

def draw_rect(theme, cord):
    pygame.draw.rect(screen, theme, cord)


#Iniciamos el loop del juego
while True:

    newGameState = np.copy(gameState)
    

    if dark_mode == True:
        screen_colour = dark
    else:
        screen_colour = light
    
    screen.fill(screen_colour)
    time.sleep(speed)

    events = pygame.event.get()
    
    #Registramos las acciones del usuario, ej. teclado, mouse
    for event in events:
        print(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            
            try:
                if spawn == False:
                    if newGameState[celX, celY] == 0:
                        newGameState[celX, celY] = 1
                    elif newGameState[celX, celY] == 1:
                        newGameState[celX, celY] = 0
                elif spawn == True:
                    if newGameState[celX, celY] == 0:
                        newGameState[celX -1, celY] = 1
                        newGameState[celX -1, celY +1] = 1
                        newGameState[celX, celY-1] = 1
                        newGameState[celX +1, celY +1] = 1
                        newGameState[celX, celY] = 1
                    elif newGameState[celX, celY] == 1:
                        newGameState[celX -1, celY] = 0
                        newGameState[celX -1, celY +1] = 0
                        newGameState[celX, celY-1] = 0
                        newGameState[celX +1, celY +1] = 0
                        newGameState[celX, celY] = 0

            except:
                if 70 > posX > 20 and 775 > posY > 725:
                    dark_mode = not dark_mode
                if 320 > posX > 270 and 775 > posY > 725:
                    spawn = not spawn
                if 530 > posX > 480 and 775 > posY > 725:
                    speed_change += 1
                    if speed_change % 3 == 1:
                        speed = 0.1
                    elif speed_change % 3 == 2:
                        speed = 0.2
                    elif speed_change % 3 == 0:
                        speed = 0.05
                

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    

    #Calculamos el número de vecinas para cada célula
    for y in range(0, nxC):
        for x in range(0, nyC):
            
            if not pauseExect:
                n_neighbors = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                              gameState[(x)     % nxC, (y - 1) % nyC] + \
                              gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                              gameState[(x - 1) % nxC,     (y) % nyC] + \
                              gameState[(x + 1) % nxC,     (y) % nyC] + \
                              gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                              gameState[(x)     % nxC, (y + 1) % nyC] + \
                              gameState[(x + 1) % nxC, (y + 1) % nyC]
                
                #Regla 1: Una celula muerta con 3 vecinas vivas, revive 
                if gameState[x, y] == 0 and n_neighbors == 3:
                    newGameState[x, y] = 1

                #Regla 2: Una celula viva con menos de 2 vecinas vivas muere por soledad,
                # y una con más de 3 vecinas vivas muere por sobrepoblacion
                elif gameState[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                    newGameState[x, y] = 0

            #Creamos el polígono de cada celda para dibujar
            poly = [((x)   * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x)   * dimCW, (y+1) * dimCH)]

            #Dibujamos cada celda de x e y
            if dark_mode == True:            
                if newGameState[x, y] == 0:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, width = 1)
                else:
                    pygame.draw.polygon(screen, light, poly, width = 0)
            else:
                if newGameState[x, y] == 0:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, width = 1)
                else:
                    pygame.draw.polygon(screen, dark, poly, width = 0)

    
    mouseClick = pygame.mouse.get_pressed()
    posX, posY = pygame.mouse.get_pos()
    
    if speed == 0.05:
        spd = 'Speed: 2x'
    elif speed == 0.1:
        spd = 'Speed: 1x'
    elif speed == 0.2:
        spd = 'Speed: 0.5x'
    
    if dark_mode == True:
        if 70 > posX > 20 and 775 > posY > 725:
            draw_rect(light, (20,725,50,50))
        else:
            draw_rect((200,200,200), (20,725,50,50))
            
        if 320 > posX > 270 and 775 > posY > 725: 
            draw_rect(light, (269,724,52,52))
        else:
            draw_rect(light, (270,725,50,50))

        if 530 > posX > 480 and 775 > posY > 725:
            draw_rect(light, (479,724,52,52))
        else:
            draw_rect(light, (480,725,50,50))
        
        render_text(spd, red, (535,740))

        render_text('Dark mode: ON',red,(75,740))
       
        
        if spawn:
            render_text('Spawn: ON', red, (325, 740))
        else: 
            render_text('Spawn: OFF', red, (325, 740))
        
    else:
        if 70 > posX > 20 and 775 > posY > 725:
            draw_rect((0,0,0), (20,725,50,50))
        else:
            draw_rect(dark, (20,725,50,50))
        
        if 320 > posX > 270 and 775 > posY > 725: 
            draw_rect(dark, (269,724,52,52))
        else:
            draw_rect(dark, (270,725,50,50))
        
        if 530 > posX > 480 and 775 > posY > 725:
            draw_rect(dark, (479,724,52,52))
        else:
            draw_rect(dark, (480,725,50,50))
        
        render_text(spd, blue, (535,740))

        render_text('Dark mode: OFF', blue, (75,740))
        
        if spawn:
            render_text('Spawn: ON', blue, (325, 740))
        else: 
            render_text('Spawn: OFF', blue, (325, 740))
        
    #Actualizamos el estado del juego
    gameState = np.copy(newGameState)

    #Actualizamos la pantalla
    pygame.event.pump()
    pygame.display.flip()