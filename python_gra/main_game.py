import pygame
from player import player
from enemy import enemy
from objects import platform, button, projectile, shoot_enemy

pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((960, 500))
pygame.display.set_caption("Python - projekt")
bg = pygame.image.load('./img/background.jpg')
platform_img = pygame.image.load('./img/platform.png')
plat = pygame.image.load('./img/platform_crop.png')
font = pygame.font.SysFont('comicsans', 30, True)
bulletSound = pygame.mixer.Sound('./sound/Laser_Shoot2.wav')
music = pygame.mixer.music.load('./sound/east.mp3')
#pygame.mixer.music.play(-1)

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
    win.fill((0, 0, 0))
    pygame.display.update()
    intro = False
    run = True


#obsługa zamknięcia gry
def quit_game():
    pygame.quit()
    quit()

#odświeżanie okna aplikacji co iterację
def redrawWindow():
    print("redraw")
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(player1.score), 1, (240, 0, 0))
    win.blit(text, (812, 14))
    player1.draw(win)
    enemy1.draw(win)
    enemy2.draw(win)
    enemy1.shoot()
    enemy2.shoot()
    enemy1.when_shoot()
    enemy2.when_shoot()
    platform1.draw(win)
    platImg(350, 360)
    platImg(390, 360)
    serca(30, 23)
    for bullet in bullets:
        bullet.draw(win)
    for bullet in bullets_enemy:
        bullet.draw(win)

    pygame.display.update()


platform1 = platform(350, 360, 160, 16, (13, 2, 18))
platform1_rect = pygame.Rect(350, 360, 160, 16)
plat1 = plat.get_rect()
player1 = player(300, 405, 64, 64)
bullets_enemy = []
enemy1 = enemy(100, 209, 64, 64, 450, bullets_enemy, player1)
enemy2 = enemy(350, 309, 64, 64, 450, bullets_enemy, player1)
kolizja = False
bullets = []
start_ticks = pygame.time.get_ticks()

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
    print("intro: ", intro)

    pygame.display.update()
    clock.tick(27)



while run:
    clock.tick(27)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    print("Run: ", run)

    if player1.health == 0:
        run = False

    #kolizja hitboxa gracza z platformą
    if player1.hitbox_rect.colliderect(platform1_rect):
        print('kolizja')
        kolizja = True
    else:
        kolizja = False

    if player1.hitbox[0] >= platform1.x and player1.hitbox[0] <= platform1.x + platform1.width and player1.hitbox[1] + 34 == platform1.y:
        player1.hitbox = (player1.hitbox[0], platform1.y, 26, 34)
        print("KOLIZJA")

    #if man.x == devil.hitbox[0] or man.y == devil.hitbox[0] or man.x == devil.hitbox[1] or man.y == devil.hitbox[1]:
    #    print('ala, chyba oberwalem')

    #if man.stopax + 28 >= platform1.x and man.stopax <= platform1.x + platform1.width and man.stopay >= float(platform1.y)and man.stopay <= float(platform1.y) + 16:
    #    onPlat = True
    #    man.y = float(platform1.y - 60)
    #    man.jumpCount = 9
    #    man.isJump = False
    #    if keys[pygame.K_UP]:
    #        man.right_before = man.right
    #        if man.right_before == True:                           #próba ogarnięcia kolizji z platformami
    #            man.facing = 1
    #        left_before = man.left
    #        if left_before == True:
    #            man.facing = -1
    #        man.isJump = True
    #        man.check_right = man.right
    #        man.right = False
    #        man.left = False
    #        man.walkCount = 0
    #else:
    #    onPlat = False

    for event in pygame.event.get():
        #zamkniecie programu x'em
        if event.type == pygame.QUIT:
            run = False

    #ilość pocisków i ich znikanie
    for bullet in bullets:
        if enemy1.visible:
            if bullet.y - bullet.radius < enemy1.hitbox[1] + enemy1.hitbox[3] and bullet.y + bullet.radius > enemy1.hitbox[1]:
               if bullet.x + bullet.radius > enemy1.hitbox[0] and bullet.x - bullet.radius < enemy1.hitbox[0] + enemy1.hitbox[2]:
                   enemy1.hit()
                   bullets.pop(bullets.index(bullet))

        if enemy2.visible:
            if bullet.y - bullet.radius < enemy2.hitbox[1] + enemy2.hitbox[3] and bullet.y + bullet.radius > enemy2.hitbox[1]:
               if bullet.x + bullet.radius > enemy1.hitbox[0] and bullet.x - bullet.radius < enemy2.hitbox[0] + enemy2.hitbox[2]:
                   enemy2.hit()
                   bullets.pop(bullets.index(bullet))

        if bullet.x < 960 and bullet.x > 0:
                bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))


    keys = pygame.key.get_pressed()
    player1.move(keys, bullets, win, projectile, kolizja, bulletSound)  #obsługa klawiszy

    redrawWindow()



pygame.quit()