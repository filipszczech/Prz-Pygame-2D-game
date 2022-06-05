import pygame
from player import player
from objects import projectile

class enemy(object):
    walkLeft = [pygame.image.load('./img/el1.png'), pygame.image.load('./img/el2.png'), pygame.image.load('./img/el3.png'),
                 pygame.image.load('./img/el4.png')]
    walkRight = [pygame.image.load('./img/ep1.png'), pygame.image.load('./img/ep2.png'), pygame.image.load('./img/ep3.png'),
                pygame.image.load('./img/ep4.png')]


    def __init__(self, x, y, width, height, end, be, player, shot_left):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.health = 5
        self.visible = True
        self.dev_shot = 30
        self.lista = []
        self.bullets_enemy = be
        self.player = player
        self.przeciwnicyZabici = 0
        self.shot_left = shot_left

    #pokazanie przeciwnika na ekranie
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 12:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            if self.vel > 0:
                self.hitbox = (self.x + 3, self.y+10, 28, 43)
                pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 10, 50, 10))
                pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 10, 50 - (10 * (5 - self.health)), 10))
            else:
                self.hitbox = (self.x + 32, self.y+10, 28, 43)
                pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0]-8, self.hitbox[1] - 10, 50, 10))
                pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0]-8, self.hitbox[1] - 10, 50 - (10 * (5 - self.health)), 10))
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            #devil_dead = 50 - (5 * (10 - self.health))
            #if devil_dead == 0:                             #do dopracowania, zeby sie punkty dodawaly
            #    man.score += 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    #ilość i lot pocisków
    def shoot(self):
        for bullet in self.bullets_enemy:
            if self.visible:
                if bullet.y - bullet.radius < self.player.hitbox[1] + self.player.hitbox[3] and bullet.y + bullet.radius > self.player.hitbox[1]:
                    if bullet.x + bullet.radius > self.player.hitbox[0] and bullet.x - bullet.radius < self.player.hitbox[0] + self.player.hitbox[2]:
                        self.player.hit()
                        self.bullets_enemy.pop(self.bullets_enemy.index(bullet))
            if bullet.x < 1280 and bullet.x > 0 and bullet.y > 0 and bullet.y < 500:
                if self.shot_left:
                    bullet.x -= bullet.vel_enemy
                else:
                    bullet.x += bullet.vel_enemy
                # bullet.y += bullet.vel
            else:
                self.bullets_enemy.pop(self.bullets_enemy.index(bullet))
    #obsługa strzału
    def when_shoot(self):
        self.dev_shot -= 1
        if self.dev_shot <= 1:
            #bullets_enemy.append(projectile(round(devil.x + devil.width //2 + man.bullets_x), round(devil.y + devil.height //2 + man.bullets_y), 6, (0,0,0), man.facing))
            if self.visible:
                    if self.vel > 0:
                        self.bullets_enemy.append(projectile(round(self.x + self.player.width // 2 + 20),
                                                             round(self.y + self.height // 2 + 9), 6, (200, 0, 0), 1))
                    elif self.vel < 0:
                        self.bullets_enemy.append(projectile(round(self.x + self.player.width // 2 + 20),
                                                             round(self.y + self.height // 2 + 9), 6, (200, 0, 0), 1))
            self.dev_shot = 40
    #otrzymanie obrażeń
    def hit(self):
        print('hit')
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
            self.player.score += 1
            self.przeciwnicyZabici += 1

