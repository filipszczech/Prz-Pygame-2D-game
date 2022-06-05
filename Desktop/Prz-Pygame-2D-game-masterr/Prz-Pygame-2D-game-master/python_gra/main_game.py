import pygame
import engine
from player import player
from enemy import enemy
from objects import platform, button, projectile, monety, monety_animacja, shoot_enemy
from level import Level


pygame.init()

clock = pygame.time.Clock()
win = pygame.display.set_mode((960, 500))
pygame.display.set_caption("Python - projekt")
bg = pygame.image.load('./img/background.jpg')
platform_img = pygame.image.load('./img/platform.png')
plat = pygame.image.load('./img/platform_crop.png')
font = pygame.font.SysFont('comicsans', 30, True)


#-----muzyka---------
pygame.mixer.init()
bulletSound = pygame.mixer.Sound('./sound/Laser_Shoot2.wav')
music = pygame.mixer.music.load('./sound/east.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)


run = False

#umieszczenie tekstury na platformie
def platImg(x, y):
    win.blit(plat, (x,y))

def serca(x, y):
    for el in player1.heart_list:
        win.blit(el, (x,y))
        x += 20

def start_run():
    global run
    global intro
    global deadscreen
    global outro
    player1.score = 0
    win.fill((0, 0, 0))
    run = True
    intro = False
    deadscreen = False

    redrawWindow()
    pygame.display.update()


#obsługa zamknięcia gry
def quit_game():
    pygame.quit()
    quit()

#odświeżanie okna aplikacji co iterację
def redrawWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(player1.score), 1, (240, 0, 0))
    win.blit(text, (812, 14))
    level.run()
    player1.rect.x = player1.x
    player1.rect.y = player1.y
    #print(player1.rect)
    level.horizontal_movement_collision(player1)
    player1.x = player1.rect.x
    level.vertical_movement_collision(player1)
    player1.x = player1.rect.x
    player1.y = player1.rect.y
    player1.draw(win)


    for e in przeciwnicy:
        e.draw(win)
        e.shoot()
        e.when_shoot()
    serca(30, 23)
    for bullet in bullets:
        bullet.draw(win)
    for bullet in bullets_enemy:
        bullet.draw(win)
    for c in monety:
        #win.blit(moneta, (c[0], c[1]))
        monety_animacja.draw(win, c.x, c.y)


    monety_animacja.update()
    pygame.display.update()


#---gracz-----------------------------
player1 = player(300, 405, 64, 64)
#--przeciwnicy------------------------
bullets_enemy = []

przeciwnicy = [
     enemy(20, 209, 64, 64, 120, bullets_enemy, player1),
     enemy(350, 305, 64, 64, 450, bullets_enemy, player1)
]


kolizja = False
bullets = []
start_ticks = pygame.time.get_ticks()
outro = False
deadscreen = False
level=Level(win)

#---koniec gierki-------------------

punkty = len(przeciwnicy) + len(monety) - 2
if punkty == player1.score:
    pygame.time.wait(5000)
    outro = True
    run = False
#------------------------------




intro = True
while intro:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    win.blit(bg, (0, 0))
    b1 = button("PLAY",420,170,100,50, (0, 200, 100), (0, 80, 50), intro, win, start_run)
    b2 = button("ABOUT",420,240,100,50, (130, 50, 200), (80, 50, 150), intro, win, quit)
    b3 = button("QUIT",420,310,100,50, (200, 0, 0), (130, 0, 0), intro, win, quit)
    #print("intro: ", intro)
    #print("punkty: ", punkty)
    pygame.display.update()
    clock.tick(27)

monetyZebrane = 0

while run:
    clock.tick(27)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000

    #----Zbieranie monet -----
    player_rect = pygame.Rect(player1.x, player1.y, player1.width, player1.height)
    for c in monety:
        if c.colliderect(player_rect):
            monety.remove(c)
            player1.score += 1
            monetyZebrane += 1
    #-----------------------

    if punkty == player1.score:
        outro = True
        run = False

    if player1.health == 0:
        deadscreen = True
        run = False

    #jeśli wypadniemy poza mape
    if player1.y > 500:
        player1.hit()

    for event in pygame.event.get():
        #zamkniecie programu x'em
        if event.type == pygame.QUIT:
            run = False

    #ilość pocisków i ich znikanie
    for bullet in bullets:
        if przeciwnicy[0].visible:
            if bullet.y - bullet.radius < przeciwnicy[0].hitbox[1] + przeciwnicy[0].hitbox[3] and bullet.y + bullet.radius > przeciwnicy[0].hitbox[1]:
               if bullet.x + bullet.radius > przeciwnicy[0].hitbox[0] and bullet.x - bullet.radius < przeciwnicy[0].hitbox[0] + przeciwnicy[0].hitbox[2]:
                   przeciwnicy[0].hit()
                   bullets.pop(bullets.index(bullet))

        if przeciwnicy[1].visible:
            if bullet.y - bullet.radius < przeciwnicy[1].hitbox[1] + przeciwnicy[0].hitbox[3] and bullet.y + bullet.radius > przeciwnicy[1].hitbox[1]:
               if bullet.x + bullet.radius > przeciwnicy[1].hitbox[0] and bullet.x - bullet.radius < przeciwnicy[1].hitbox[0] + przeciwnicy[1].hitbox[2]:
                   przeciwnicy[1].hit()
                   bullets.pop(bullets.index(bullet))

        if bullet.x < 960 and bullet.x > 0:
                bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))


    keys = pygame.key.get_pressed()
    player1.move(keys, bullets, win, projectile, kolizja, bulletSound)  #obsługa klawiszy

    redrawWindow()

    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

while outro:
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    win.blit(bg, (0, 0))
    przeciwnicy_zabici = player1.score - monetyZebrane
    EndScore = font.render('YOUR FINAL SCORE: ' + str(player1.score), 1, (240, 0, 0))
    EndScore2 = font.render('Coins: ' + str(monetyZebrane), 1, (240, 0, 0))
    EndScore3 = font.render('Enemies: ' + str(przeciwnicy_zabici), 1, (240, 0, 0))
    win.blit(EndScore, (300, 14))
    win.blit(EndScore2, (400, 50))
    win.blit(EndScore3, (400, 90))
    b1 = button("PLAY AGAIN", 420, 170, 100, 50, (0, 200, 100), (0, 80, 50), outro, win, start_run)
    b2 = button("NEXT LEVEL",420,240,100,50, (130, 50, 200), (80, 50, 150), outro, win, quit)
    b3 = button("QUIT",420,310,100,50, (200, 0, 0), (130, 0, 0), outro, win, quit)
    pygame.display.update()
    clock.tick(27)


while deadscreen:
    print("Run:", run)
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit_game()
            if event.key == pygame.K_c:
                run = True
    win.blit(bg, (0, 0))
    EndScore = font.render('YOU DIED! ', 1, (240, 0, 0))
    win.blit(EndScore, (400, 45))
    b1 = button("PLAY AGAIN", 420, 170, 100, 50, (0, 200, 100), (0, 80, 50), deadscreen, win, start_run)
    b3 = button("QUIT",420,310,100,50, (200, 0, 0), (130, 0, 0), deadscreen, win, quit)
    pygame.display.update()
    clock.tick(27)



pygame.quit()