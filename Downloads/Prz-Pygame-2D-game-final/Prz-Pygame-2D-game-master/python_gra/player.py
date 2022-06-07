import pygame

walkRight = [pygame.image.load('./img/rabbit11.png'), pygame.image.load('./img/rabbit12.png'), pygame.image.load('./img/rabbit13.png'), pygame.image.load('./img/rabbit14.png'), pygame.image.load('./img/rabbit15.png'), pygame.image.load('./img/rabbit16.png'), pygame.image.load('./img/rabbit17.png'), pygame.image.load('./img/rabbit18.png'), pygame.image.load('./img/rabbit19.png')]
walkLeft = [pygame.image.load('./img/rabbitl1.png'), pygame.image.load('./img/rabbitl2.png'), pygame.image.load('./img/rabbitl3.png'), pygame.image.load('./img/rabbitl4.png'), pygame.image.load('./img/rabbitl5.png'), pygame.image.load('./img/rabbitl6.png'), pygame.image.load('./img/rabbitl7.png'), pygame.image.load('./img/rabbitl8.png'), pygame.image.load('./img/rabbitl9.png')]



class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8            #prędkość chodzenia
        self.isJump = False     #do obsługi skoku
        self.jumpCount = 9      #do obsługi wysokości skoku
        self.left = False       #w którą strone jest obrócony
        self.right = False
        self.walkCount = 0      #do obliczania jaki obrazek wczytać
        self.standing = True    #tu wczytujemy obrazek stojącego w miejscu
        self.bullets_x = 20
        self.bullets_y = 9
        self.naboje_left = 0    #do ograniczania naboi
        self.check_right = False#do sprawdzania w którą strone jest obrócony, te 2 niżej też
        self.facing = 1
        self.right_before = True
        self.hitbox = (self.x + 20, self.y, 28, 60)     #hitbox (aktualne: x gracza, y gracza, szerokość i wysokość)
        self.hitbox_rect = pygame.Rect(self.hitbox)
        self.score = 0
        self.stopax = self.x + 20       #to coś tam do kolizji, raczej nieważne
        self.stopay = self.y + 60
        self.Fall = False       #obsługa spadania
        self.heart_list = heart_list = [pygame.image.load('./img/heart.png'), pygame.image.load('./img/heart.png'), pygame.image.load('./img/heart.png'), pygame.image.load('./img/heart.png'), pygame.image.load('./img/heart.png')]
        self.health = 5
        self.shootloop = 0

        #kolizje
        self.image = pygame.Surface((30, 50))
        self.rect = self.image.get_rect(topleft = (self.x , self.y ))
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 1
        self.jump_speed = -16
        self.onGround = True



    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            elif self.left:                                               #tu jest lipa, bo przy skoku oba false i sie odwraca smiec w lewo w czasie skoku
                win.blit(walkLeft[0], (self.x, self.y))
            elif self.check_right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
            #elif self.facing == 1:
            #    win.blit(walkRight[0], (self.x, self.y))
            #elif self.facing == -1:
            #    win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = [self.x + 18, self.y+21, 26, 34]
        self.hitbox_rect = pygame.Rect(self.hitbox)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        print('hit')
        if self.health >= 1:
            self.health -= 1
            self.heart_list.pop()
        #else:
        #   run = False

    def aply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    #obsługa klawiszy - poruszanie, skakanie, strzelanie
    def move(self, keys, bullets, win, projectile, kolizja, bulletSound):
        #shootloop daje możliwość delaya między kolejnymi strzałami
        if self.shootloop > 0:
            self.shootloop += 1
        if self.shootloop > 7:
            self.shootloop = 0

        if keys[pygame.K_SPACE] and keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            win.blit(walkLeft[0], (self.x, self.y))

        if keys[pygame.K_SPACE] and self.shootloop == 0:
            bulletSound.play()
            if self.left:
                self.facing = -1
                self.naboje_left = -self.bullets_x
            elif self.right:
                self.facing = 1
            if len(bullets) < 6:
                if self.right and self.right_before:
                    bullets.append(projectile(round(self.x + self.width // 2 + self.bullets_x),
                                              round(self.y + self.height // 2 + self.bullets_y), 6, (0, 0, 0), self.facing))
                    # print(man.facing)
                elif self.right_before and self.left == False:
                    bullets.append(projectile(round(self.x + self.width // 2 + self.bullets_x),
                                              round(self.y + self.height // 2 + self.bullets_y), 6, (0, 0, 0), self.facing))
                    # print(man.facing)
                elif self.right:
                    bullets.append(projectile(round(self.x + self.width // 2 + self.bullets_x),
                                              round(self.y + self.height // 2 + self.bullets_y), 6, (0, 0, 0), self.facing))
                    # print(man.facing)
                else:
                    bullets.append(projectile(round(self.x + self.width // 2 - self.bullets_x),
                                              round(self.y + self.height // 2 + self.bullets_y), 6, (0, 0, 0), self.facing))
                    # print(man.facing)
            self.shootloop = 1

        elif keys[pygame.K_LEFT] and self.x > self.vel and kolizja == False:
            self.x += -self.vel
            self.left = True
            self.right = False
            self.standing = False
            self.stopax += -self.vel

        elif keys[pygame.K_RIGHT] and self.x < 1380 - (self.vel + self.width) and kolizja == False:
            self.x += self.vel
            self.right = True
            self.left = False
            self.standing = False
            self.stopax += self.vel
        else:
            self.standing = True
            self.walkCount = 0

        if keys[pygame.K_UP] and self.onGround == True:
            self.onGround = False
            self.jump()
