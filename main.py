import pygame
from pygame.locals import *
from sys import exit
import math
import time
pygame.init()

#Definindo variáveis iniciais de movimentação

aceleracao_y1 = 0
aceleracao_x1 = 0

aceleracao_y2 = 0
aceleracao_x2 = 0

aceleracao_max = 10

G = 8.5

massa1 = 1
massa2 = 1
velocidadex1 = aceleracao_x1
velocidadey1 = aceleracao_y1
velocidadex2 = aceleracao_x2
velocidadey2 = aceleracao_y2

velocidade = [velocidadex1, velocidadey1, velocidadex2, velocidadey2]

#Definindo variáveis para as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (143, 186, 200)
LIGHTBLUE2 = (193, 236, 250)
GRAY = (100, 100, 100)
LIGHTGRAY = (170, 170, 170)
DARKGRAY = (45, 45, 47)
BROWN = (74, 54, 33)
ORANGE = (255, 117, 24)
PURPLE = (153, 51, 153)
GLASSCOLOR = (70, 250, 250)

color1 = WHITE
color2 = RED

endurecimento1 = False
endurecimento2 = False

#Imagens
telaInicial = pygame.image.load(r'.\telainicialSteX.png')
p1Win = pygame.image.load(r'.\P1Win.png')
p2Win = pygame.image.load(r'.\P2Win.png')

telaInShow = True
P1Show = False
P2Show = False

#Sons
pygame.mixer.music.load('audioTelaInicial.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(99999)
morte = pygame.mixer.Sound('Morte.wav')
#Definindo variáveis para largura e altura
width = 1366
height = 768

#Definindo posições iniciais para os personagens e plataformas
x1 = 50
y1 = 445

x2 = 590
y2 = 445

x3 = 70
y3 = 150

y4 = 740

x5 = 1300
y5 = 200

anel1 = 50
anel2 = 640
vel_anel1 = 1
vel_anel2 = 2

vel_plataforma = 2
vel_elevador = 1
vely_Xmatador = 2
velx_Xmatador = 2

atrito = 0.01

#Definindo score dos jogadores
scoreP1 = 0
scoreP2 = 0

#Criando a tela do jogo, nome do jogo e criando um relógio
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('SteX')
clock1 = pygame.time.Clock()
clock2 = pygame.time.Clock()

#Textos scores
pygame.font.init()

fonte = pygame.font.SysFont('Arial', 30, False, False)

#Definindo variável para quando uma tecla for solta, e pra quando o personagem não estiver pulando

pulo1 = False
pulo2 = False

#Criando função para calcular velocidade das bolas após colisões entre si

#p1 = x1 - x2
#p2 = y1 - y2

def calculavelocidade(vx1,vy1, vx2, vy2, p1, p2):
  projVx1 = (float((p1*vx1 + p2*vy1)) / float((p1**2+p2**2))) * p1  #Projeção da velocidade X da bola 1 em relação ao eixo
  projVy1 = (float((p1*vx1 + p2*vy1)) / float((p1**2+p2**2))) * p2

  projVx2 = (float((p1*vx2 + p2*vy2)) / float((p1**2+p2**2))) * p1
  projVy2 = (float((p1*vx2 + p2*vy2)) / float((p1**2+p2**2))) * p2
  vx1f = vx1 - projVx1 + projVx2 #Velocidade Inicial - velocidade da projeção 1 + velocidade projeção 2
  vy1f = vy1 - projVy1 + projVy2

  vx2f = vx2 - projVx2 + projVx1
  vy2f = vy2 - projVy2 + projVy1
  return vx1f, vy1f, vx2f, vy2f
while True:
 if telaInShow == True:
    surface.blit(telaInicial, (0,0))
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        telaInShow = False
        aceleracao_y1 = 0
        aceleracao_y2 = 0
        clock1 = pygame.time.Clock()
        clock2 = pygame.time.Clock()
      if event.type == QUIT:
        pygame.quit()
        exit()

 elif P1Show == True:
    surface.blit(p1Win, (0,0))
    morte.play()
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        P1Show = False 
        clock1 = pygame.time.Clock()
        clock2 = pygame.time.Clock()
      if event.type == QUIT:
        pygame.quit()
        exit()

 elif P2Show == True:
    surface.blit(p2Win, (0,0))
    morte.play()
   
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        P2Show = False 
        clock1 = pygame.time.Clock()
        clock2 = pygame.time.Clock()
      if event.type == QUIT:
        pygame.quit()
        exit()

 else:    
  #Usando o relógio, definindo o fps do jogo
  clock1.tick(70)
  clock2.tick(70)
  
  #Definindo o fundo como cinza
  surface.fill(GRAY)

  #Definindo a gravidade
  T1 = clock1.get_time() / 1000
  F1 = G * T1
  aceleracao_y1 += F1
  y1 += aceleracao_y1
  x1 += aceleracao_x1

  T2 = clock2.get_time() / 1000
  F2 = G * T2
  aceleracao_y2 += F2
  y2 += aceleracao_y2
  x2 += aceleracao_x2

  #Quando tiver alguma ação/evento no jogo, esse for será iniciado
  for event in pygame.event.get():
  
    #Fechar o Jogo
    if event.type == QUIT:
      pygame.quit()
      exit()

    #Quando P1 e P2 não estiverem pulando, permitir novo pulo
    if pulo1 == False:
      if pygame.key.get_pressed()[K_w]:
        if endurecimento1 == False:
          y1 -=4
          aceleracao_y1 -= 4
        else:
          y1 -= 1.5
          aceleracao_y1 -= 1.5
        pulo1 = True
    if pulo2 == False:  
      if pygame.key.get_pressed()[K_i]:
        if endurecimento2 == False:
          y2 -=4
          aceleracao_y2 -= 4
        else:
          y2 -= 1.5
          aceleracao_y2 -= 1.5
        pulo2 = True

    #Movimentação para baixo
    if pygame.key.get_pressed()[K_s]:
        aceleracao_y1 += 1
    if pygame.key.get_pressed()[K_k]:
        aceleracao_y2 += 1
    if pygame.key.get_pressed()[K_x]:
      endurecimento1 = True
      color1 = GLASSCOLOR
    else:
      endurecimento1 = False
      color1 = WHITE  

    #Definindo aceleração máxima em X / movimentação
    if pygame.key.get_pressed()[K_a]:
        if aceleracao_x1 > -2:
          if endurecimento1 == True:
            aceleracao_x1 -= 0.125
          else:
            aceleracao_x1 -= 0.5
        else:
            aceleracao_x1 = -4

    if pygame.key.get_pressed()[K_d]:
        if aceleracao_x1 < 4:
          if endurecimento1 == True:
            aceleracao_x1 += 0.125
          else:
            aceleracao_x1 += 0.5
        else:
            aceleracao_x1 = 4
      
    if pygame.key.get_pressed()[K_j]:
        if aceleracao_x2 > -4:
          if endurecimento2 == True:
            aceleracao_x2 -= 0.125
          else:
            aceleracao_x2 -= 0.5
        else:
            aceleração_x2 = -4

    if pygame.key.get_pressed()[K_l]:
        if aceleracao_x2 < 4:
          if endurecimento2 == True:
            aceleracao_x2 += 0.125
          else:
            aceleracao_x2 += 0.5
        else:
            aceleração_x2 = 4

    if pygame.key.get_pressed()[K_m]:
      endurecimento2 = True
      color2 = (255, 100, 100)
    else:
      endurecimento2 = False
      color2 = RED      

  #Atrito com o ar
  if pygame.time.get_ticks():
    if aceleracao_x1 != 0:
      if aceleracao_x1 > 0:
        aceleracao_x1 -= atrito
      elif aceleracao_x1 < 0: 
        aceleracao_x1 += atrito
    if aceleracao_x2 != 0:
      if aceleracao_x2 > 0:
        aceleracao_x2 -= atrito
      elif aceleracao_x2 < 0: 
        aceleracao_x2 += atrito

  #Movimentação da Plataforma voadora
  if pygame.time.get_ticks():
    x3 += vel_plataforma
    if x3 >= 570 or x3 <= 67:
      vel_plataforma *= -1

  #Movimentação do elevador
  if pygame.time.get_ticks():
    y4 -= vel_elevador
    if y4 <= 445 or y4 >= 740:
      vel_elevador *= -1
  
  #Movimentação do X matador
  if pygame.time.get_ticks():
    y5 += vely_Xmatador
    x5 -= velx_Xmatador
    if y5 >= 697 or y5 <= 0:
      vely_Xmatador *= -1
    if x5 <= 680 or x5 >= 1366:
      velx_Xmatador *= -1

  #Plataformas transparentes
  protecaochaodeathTransparenteC = pygame.draw.line(surface, LIGHTGRAY, (638, 0), (638, 768), 5)
  vidrotorre = pygame.draw.line(surface, LIGHTGRAY, (1290, 568), (1290, 748), 160)
  torreperigosa_entrada = pygame.draw.line(surface, LIGHTGRAY, (1288, 530), (1365, 530), 90)

  #Criando personagens
  player1 = pygame.draw.circle(surface, color1, (x1, y1), 15)
  player2 = pygame.draw.circle(surface, color2, (x2, y2), 15)
  players = [player1, player2]

  #Criando chão e chão death
  chao = pygame.draw.line(surface, YELLOW, (0, 470), (635, 470), 20)
  quina = pygame.draw.line(surface, YELLOW, (636, 460), (640, 460), 40)
  chaobaixo = pygame.draw.line(surface, YELLOW, (640, 758), (1366, 758), 20)
  chaodeath = pygame.draw.line(surface, BLACK, (0, 758), (640, 758), 20)
  apoio1 = pygame.draw.line(surface, YELLOW, (570, 745), (620, 745), 10)
  apoio2 = pygame.draw.line(surface, YELLOW, (420, 748), (470, 748), 10)
  apoio3 = pygame.draw.line(surface, YELLOW, (270, 748), (320, 748), 10)
  apoio4 = pygame.draw.line(surface, YELLOW, (120, 748), (170, 748), 10)
  apoio5 = pygame.draw.line(surface, YELLOW, (0, 748), (30, 748), 10)

  #Criando plataformas
  plataforma1 = pygame.draw.line(surface, BLUE, (300, 250), (450, 250), 20)
  plat1E = pygame.draw.line(surface, BLUE, (300, 250), (330, 270), 20)
  plat1D = pygame.draw.line(surface, BLUE, (450, 250), (420, 270), 20)
  platdeath1E = pygame.draw.line(surface, BLACK, (300, 260), (330, 280), 5)
  platdeath1D = pygame.draw.line(surface, BLACK, (450, 260), (420, 280), 5)
  trampolimC = pygame.draw.line(surface, ORANGE, (115, 458), (215, 458), 7)
  areiamovediçaverticalD = pygame.draw.line(surface, BROWN, (1365, 568), (1365, 748), 10)
  plat1 = [plataforma1, plat1E, plat1D]
  
  plataforma2 = pygame.draw.line(surface, GREEN, (x3, y3 - 50), (x3, y3 - 40), 100)
  plataformaEdeath = pygame.draw.line(surface, BLACK, (x3 - 59, 90), (x3 - 59, 110), 15)
  plataformaDdeath = pygame.draw.line(surface, BLACK, (x3 + 59, 90), (x3 + 59, 110), 15)

  plataformaDinamica = [plataforma2]

  elevador = pygame.draw.line(surface, YELLOW, (650, y4), (750, y4), 10)
  areiamovediçatorreperigosa = pygame.draw.line(surface, BROWN, (1245, 500), (1245, 485), 82)
  torreperigosa = pygame.draw.line(surface, BLACK, (1245, 568), (1245, 500), 82)
  canhaotorre = pygame.draw.line(surface, PURPLE, (1215, 690), (1215, 660), 10)
  passagemsecretapelocanhao = pygame.draw.line(surface, PURPLE, (1205, 690), (1205, 660), 10)
  protecaotorreC = pygame.draw.line(surface, YELLOW, (1213, 572), (1285, 572), 10)
  protecaotorreE = pygame.draw.line(surface, YELLOW, (1210, 677), (1210, 568), 10)
  trampolimB = pygame.draw.line(surface, ORANGE, (1210, 678), (1210, 748), 10)
  linhamatadora1 = pygame.draw.line(surface, BLACK, (x5, y5), (x5 - 40, y5 + 50), 7)
  linhamatadora2 = pygame.draw.line(surface, BLACK, (x5 - 40, y5), (x5, y5 + 50), 7)    
  if y1 < 0:
    sinalizadorBranco = pygame.draw.line(surface, WHITE, (x1 + 2, 2), (x1 -2, 2), 10)
  if y2 < 0:
    sinalizadorVermelho = pygame.draw.line(surface, RED, (x2 + 2, 2), (x2 -2, 2), 10)
  verticeperigosoD = pygame.draw.polygon(surface, BLACK, ((1347, 0), (1347, 70), (1320, 0)), 40)
  portalB = pygame.draw.ellipse(surface, LIGHTBLUE2, (anel1, 520, 50, 200), 15)
  topoanel = pygame.draw.line(surface, LIGHTBLUE2, (anel1 + 24, 523),(anel1 + 24, 537), 10)
  baseanel = pygame.draw.line(surface, LIGHTBLUE2, (anel1 + 24, 705), (anel1 + 24, 715), 10)
  portalC = pygame.draw.ellipse(surface, LIGHTBLUE, (anel2, 10, 200, 50), 15)
  impulsionador = pygame.draw.line(surface, PURPLE, (670, 748), (950, 748), 5)

  portais = [portalB, portalC]

  plataformasDeath = [platdeath1E, platdeath1D, torreperigosa, linhamatadora1, linhamatadora2, verticeperigosoD, plataformaEdeath, plataformaDdeath, chaodeath]
  
  Allplats = [chao, quina, chaobaixo, apoio1, apoio2, apoio3, apoio4, apoio5, plataforma1, plat1E, plat1D, plataforma2, elevador, areiamovediçatorreperigosa, impulsionador]


  if player1.collidelist(Allplats) >=0:
    pulo1 = False
  if player2.collidelist(Allplats) >=0:
    pulo2 = False
  #Criando textos dos scores
  txtP1 = fonte.render('Score: '+ str(scoreP1), True, WHITE) 
  txtP2 = fonte.render('Score: '+ str(scoreP2), True, RED)

  #Criando morte ao bater em uma plataforma preta, e quando morrer, dizer que não está mais pulando.
  if player1.collidelist(plataformasDeath) >= 0:
    aceleracao_x1 = 0
    aceleracao_y1 = 0
    clock1 = pygame.time.Clock()
    clock2 = pygame.time.Clock()
    x1 = 50
    y1 = 445
    
    x2 = 590
    y2 = 445
    aceleracao_x2 = 0
    aceleracao_y2 = 0

    if pulo1 == True:
      aceleracao_y1 = 0
      pulo1 = False
    scoreP2 +=1
  if player2.collidelist(plataformasDeath) >=0:
    x1 = 50
    y1 = 445
    aceleracao_x1 = 0
    aceleracao_y1 = 0

    x2 = 590  
    y2 = 445
    aceleracao_x2 = 0
    aceleracao_y2 = 0

    if pulo2 == True:
      aceleracao_x2 = 0
      pulo2 = False
    scoreP1 +=1

  if scoreP1 >= 5:
    P1Show = True
    scoreP1 = 0
    scoreP2 = 0
  if scoreP2 >= 5:
    P2Show = True
    scoreP1 = 0
    scoreP2 = 0
  #Renderizando texto dos scores na tela
  surface.blit(txtP1,(15,30))
  surface.blit(txtP2,(1261,30))

  #Criando colisão com o chão
  if player1.colliderect(quina):
    aceleracao_x1 *= -1
    if y1 >= 426:
      y1 = 426
      aceleracao_y1 *= -0.7
    if x1 <= 640:
      aceleracao_x1 *= -1
      if pulo1 == True:
        if aceleracao_x1 > 0:
          aceleracao_x1 = 2
        elif aceleracao_x1 < 0:
          aceleracao_x1 = -2
        pulo1 = False  
  if player2.colliderect(quina):
    aceleracao_x2 *= -1  
    if y2 >= 426:
      y2= 426
      aceleracao_y2 *= -0.7
      if pulo2 == True:
        if aceleracao_x2 > 0:
          aceleracao_x2 = 2
        elif aceleracao_x2 < 0:
          aceleracao_x2 = -2
        pulo2 = False  
  if 445 < y1 < 470 and 15 < x1 <= 620: 
      y1 = 445
      aceleracao_y1 *= -0.7
      clock1 = pygame.time.Clock()
      if pulo1 == True:
        if aceleracao_x1 > 0:
          aceleracao_x1 = 2
        elif aceleracao_x1 < 0:
          aceleracao_x1 = -2
        pulo1 = False  
  elif 470 < y1 < 495 and 0 < x1 <= 625:
      y1 = 495              
      aceleracao_y1 *= -1
  if 445 < y2 < 470 and 15 < x2 <= 620: 
      y2 = 445
      aceleracao_y2 *= -0.7
      clock2 = pygame.time.Clock()
      if pulo2 == True:
        if aceleracao_x2 > 0:
          aceleracao_x2 = 2
        elif aceleracao_x2 < 0:
          aceleracao_x2 = -2
        pulo2 = False  
  elif 470 < y2 < 495 and 0 < x2 <= 625:
      y2 = 495              
      aceleracao_y2 *= -1 
  if y1 > 733 and x1 > 625:
    y1 = 733
    aceleracao_y1 *= -0.7
    clock1 = pygame.time.Clock()
    if pulo1 == True:
      if aceleracao_x1 > 0:
        aceleracao_x1 = 2
      elif aceleracao_x1 < 0:
        aceleracao_x1 = -2
      pulo1 = False 
  if y2 > 733 and x2 > 625:
    y2 = 733
    aceleracao_y2 *= -0.7
    clock2 = pygame.time.Clock()
    if pulo2 == True:
      if aceleracao_x2 > 0:
        aceleracao_x2 = 2
      elif aceleracao_x2 < 0:
        aceleracao_x2 = -2
      pulo2 = False    

  #Criando colisão com a plataforma 1
  if 455 > x1 > 295 and 250 > y1 > 225:
    y1 = 227
    aceleracao_y1 *= -0.5
    clock1 = pygame.time.Clock()
    if pulo1 == True:
      if aceleracao_x1 > 0:
       aceleracao_x1 = 3
      if aceleracao_x1 < 0:
       aceleracao_x1 = -3
      pulo1 = False
  if 455 > x2 > 295 and 250 > y2 > 225:
    y2 = 227
    aceleracao_y2 *= -0.5
    clock2 = pygame.time.Clock()
    if pulo2 == True:
      if aceleracao_x2 > 0:
        aceleracao_x2 = 2
      elif aceleracao_x2 < 0:
        aceleracao_x2 = -2
      pulo2 = False
  if y1 > 250:
    if player1.collidelist(plat1) >=0:
      y1 = 275
      aceleracao_y1 *= -1
  if y2 > 250:
    if player2.collidelist(plat1) >=0:
      y2 = 275
      aceleracao_y2 *= -1

  #Criando colisão com a plataforma 2
  if y1 < 100:
   if player1.collidelist(plataformaDinamica) >=0:
     y1 = 86
     x1 += vel_plataforma
     aceleracao_y1 = 0
     clock1 = pygame.time.Clock()
     if pulo1 == True:
       if aceleracao_x1 > 0:
        aceleracao_x1 = 3
       if aceleracao_x1 < 0:
        aceleracao_x1 = -3
       pulo1 = False
  elif y1 >= 100:
    if player1.collidelist(plataformaDinamica) >=0:
     y1 = 120
     aceleracao_y1 += 10
     clock1 = pygame.time.Clock()
     if pulo1 == True:
       if aceleracao_x1 > 0:
        aceleracao_x1 = 3
       if aceleracao_x1 < 0:
        aceleracao_x1 = -3
       pulo1 = False
  if y2 < 100:
   if player2.collidelist(plataformaDinamica) >=0:
     y2 = 86
     x2 += vel_plataforma
     aceleracao_y2 = 0
     clock2 = pygame.time.Clock()
     if pulo2 == True:
       if aceleracao_x2 > 0:
        aceleracao_x2 = 3
       if aceleracao_x2 < 0:
        aceleracao_x2 = -3
       pulo2 = False
  elif y2 >= 100:
    if player2.collidelist(plataformaDinamica) >=0:
     y2 = 120
     aceleracao_y2 += 10
     clock2 = pygame.time.Clock()
     if pulo2 == True:
       if aceleracao_x2 > 0:
        aceleracao_x2 = 3
       if aceleracao_x2 < 0:
        aceleracao_x2 = -3
       pulo2 = False
  if player1.colliderect(plataformaEdeath):
      aceleracao_x1 *= -1
      aceleracao_y1 *= -1
  if player1.colliderect(plataformaEdeath):
    if y1 <= 140:
      aceleracao_y1 *= -1
    else:
      aceleracao_x1 *= -1
      aceleracao_y1 *= -1
    
  #Coliisão com o elevador
  if player1.colliderect(elevador):
    if y1 < y4 - 15:
      y1 = y4 - 20
      aceleracao_y1 = vel_elevador
      if pulo1 == True:
       if aceleracao_x1 > 0:
        aceleracao_x1 = 3
       if aceleracao_x1 < 0:
        aceleracao_x1 = -3
       pulo1 = False
    else:
      aceleracao_y1 *= -1

  if player2.colliderect(elevador):
    if y2 < y4 - 15:
      y2 = y4 - 22
      aceleracao_y2 = vel_elevador
      if pulo2 == True:
       if aceleracao_x2 > 0:
        aceleracao_x2 = 3
       if aceleracao_x2 < 0:
        aceleracao_x2 = -3
       pulo2 = False
    else:
      aceleracao_y2 *= -1

  #Colisão com apoios e interação com o portal
  if 725 < y1 < 760:
    if 570 <= x1 <= 620 or 420 <= x1 <= 470 or 270 <= x1 <= 320 or 120 <= x1 <= 170 or x1 <= 30:
        y1 = 725
        aceleracao_y1 *= -1
        if pulo1 == True:
          if aceleracao_x1 > 0:
            aceleracao_x1 = 2
          elif aceleracao_x1 < 0:
            aceleracao_x1 = -2
          pulo1 = False
  if 725 < y2 < 760:
    if 570 <= x2 <= 620 or 420 <= x2 <= 470 or 270 <= x2 <= 320 or 120 <= x2 <= 170 or x2 <= 30:
        y2 = 725
        aceleracao_y2 *= -1
        if pulo1 == True:
          if aceleracao_x2 > 0:
            aceleracao_x2 = 2
          elif aceleracao_x2 < 0:
            aceleracao_x2 = -2
          pulo1 = False
  if pygame.time.get_ticks():
    anel1 += vel_anel1
    if anel1 >= 585 or anel1 <= 10:
      vel_anel1 *= -1
    anel2 += vel_anel2
    if anel2 >= 1115 or anel2 <= 640:
      vel_anel2 *= -1
  if player1.colliderect(topoanel):
    if x1 + 2 > anel1 + 24:
     aceleracao_x1 += vel_anel1
    else:
      aceleracao_x1 -= vel_anel1
  if player1.colliderect(baseanel):
    if x1 + 2 >= anel1 + 24:
     aceleracao_x1 += vel_anel1
    else:
      aceleracao_x1 -= vel_anel1
  if player2.colliderect(topoanel):
    if x2 + 2 > anel1 + 24:
     aceleracao_x2 += vel_anel1
    else:
      aceleracao_x2 -= vel_anel1
  if player2.colliderect(baseanel):
    if x2 + 2 >= anel1 + 24:
     aceleracao_x2 += vel_anel1
    else:
      aceleracao_x2 -= vel_anel1
  if 8 < x1 < 586 and 520 < y1 < 710:
    if anel1 - 25 < x1 < anel1 + 25: 
      x1 = anel2 + 100
      y1 = 15
      aceleracao_y1 = aceleracao_x1 * -0.5
      aceleracao_x1 = 0
  if 10 < x2 < 585 and 520 < y2 < 710:
    if anel1 - 25 < x2 < anel1 + 25: 
      x2 = anel2 + 100
      y2 = 15
      aceleracao_y2 = aceleracao_x2 * -0.5
      aceleracao_x2 = 0


  
  #Coliisão com a torre e afins
  if player1.colliderect(areiamovediçatorreperigosa):
    if y1 <= 510:
      aceleracao_y1 *= -0.8
    else:
      aceleracao_x1 *= -1
  if player2.colliderect(areiamovediçatorreperigosa):
    if y2 <= 510:
      aceleracao_y2 *= -0.8
    else:
      aceleracao_x1 *= -1
  if player1.colliderect(protecaotorreE):
    if x1 >= 1190:
      aceleracao_x1 *= -1
  if player2.colliderect(protecaotorreE):
    if x2 >= 1190:
      aceleracao_x2 *= -1
  if player1.colliderect(protecaotorreC):
      aceleracao_y1 *= -1
  if player2.colliderect(protecaotorreC):
      aceleracao_y2 *= -1
      if player1.colliderect(canhaotorre):
        aceleracao_x1 *= 0.5
        if player1.colliderect(protecaotorreE):
            aceleracao_x1 *= 1
            aceleracao_x1 -= 4  
        if player1.colliderect(trampolimB):
            aceleracao_x1 *= -1
      if player2.colliderect(canhaotorre):
          aceleracao_x2 *= 0.5
          if player2.colliderect(protecaotorreE):
              aceleracao_x2 *= 1
              aceleracao_x2 -= 4
          if player2.colliderect(trampolimB):
              aceleracao_x2 *= -1
  if player1.colliderect(areiamovediçaverticalD):
    aceleracao_x1 *= -0.7
    if aceleracao_x1 <= -10 or aceleracao_x1 >= 10:
      aceleracao_x1 = 0
  if player2.colliderect(areiamovediçaverticalD):
    aceleracao_x2 *= -0.7
    if aceleracao_x2 <= -10 or aceleracao_x2 >= 10:
      aceleracao_x2 = 0
        
  #Colisão com impulsionador, trampolins e areamovediça
  if player1.colliderect(impulsionador):
    aceleracao_x1 -= 0.5
  if player2.colliderect(impulsionador):
    aceleracao_x2 -= 0.5
  if player1.colliderect(protecaochaodeathTransparenteC):
      if aceleracao_x1 > 10:
          aceleracao_x1 = 5
  if player2.colliderect(protecaochaodeathTransparenteC):
      if aceleracao_x2 > 10:
          aceleracao_x2 = 5
  if player1.colliderect(trampolimB):
    if x1 >= 1190:
      aceleracao_x1 *= -2
  if player2.colliderect(trampolimB):
    if x2 >= 1190:
      aceleracao_x2 *= -2
  if player1.colliderect(trampolimC):
    if y1 <= 475:
      aceleracao_y1 *= 1.3
      aceleracao_x1 *= -1
  if player2.colliderect(trampolimC):
    if y2 <= 475:
      aceleracao_y2 *= 1.3
      aceleracao_x2 *= -1

  #Fazendo quicar na borda da tela
  if x1 >= 1347:
    aceleracao_x1 *= -1.2
  if x1 <= 14:
    aceleracao_x1 *= -1.2
    if 500 >= y1 >= 485:
        aceleracao_x1 = 0
  if x2 >= 1347:
    aceleracao_x2 *= -1.2
  if x2 <= 14:
    aceleracao_x2 *= -1.2
  
  #Colisão entre as bolas
  dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
  if dist <= 30:
    p1 = x1 - x2
    p2 = y1 - y2
    if endurecimento1 == True:
      p1 = x1 - x2
      p2 = y1 - y2
      vx1, vy1, vx2, vy2 = calculavelocidade(aceleracao_x1 * 2, aceleracao_y1 * 2, aceleracao_x2 * 0.5, aceleracao_y2 * 0.5, p1, p2)
      aceleracao_x1 = vx1
      aceleracao_y1 = vy1
      aceleracao_x2 = vx2
      aceleracao_y2 = vy2 
    elif endurecimento2 == True:
      vx1, vy1, vx2, vy2 = calculavelocidade(aceleracao_x1 * 0.5, aceleracao_y1 * 0.5, aceleracao_x2 * 2, aceleracao_y2 * 2, p1, p2)
      aceleracao_x1 = vx1
      aceleracao_y1 = vy1
      aceleracao_x2 = vx2
      aceleracao_y2 = vy2 
    else:
      vx1, vy1, vx2, vy2 = calculavelocidade(aceleracao_x1 , aceleracao_y1, aceleracao_x2, aceleracao_y2, p1, p2)
      aceleracao_x1 = vx1
      aceleracao_y1 = vy1
      aceleracao_x2 = vx2
      aceleracao_y2 = vy2      



  #Colisão dos X
  colisoesAux = [elevador, areiamovediçatorreperigosa, trampolimB, protecaochaodeathTransparenteC, verticeperigosoD, trampolimB, portalC, torreperigosa]
  if linhamatadora1.collidelist(colisoesAux) >=0 or linhamatadora2.collidelist(colisoesAux) >=0 :
    velx_Xmatador *= -1
    vely_Xmatador *= -1
  
  if aceleracao_y1 >= 8:
    aceleracao_y1 = 8
  if aceleracao_y2 >= 8:
    aceleracao_y2 = 8
  
  if endurecimento1 == True:
    if aceleracao_x1 >= 2:
      aceleracao_x1 = 2
    elif aceleracao_x1 <= -2:
      aceleracao_x1 = -2
    if aceleracao_y1 <= -4:
      aceleracao_y1 = -4

  if endurecimento2 == True:
    if aceleracao_x2 >= 2:
      aceleracao_x2 = 2
    elif aceleracao_x2 <= -2:
      aceleracao_x2 = -2    
    if aceleracao_y2 <= -4:
      aceleracao_y2 = -4
  
 pygame.display.update()