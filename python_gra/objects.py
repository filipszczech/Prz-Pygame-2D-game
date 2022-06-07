import pygame
import engine

bg = pygame.image.load('./img/background.jpg')

monety_animacja = engine.Animation([
    pygame.image.load('./img/coin_0.png'),
    pygame.image.load('./img/coin_1.png'),
    pygame.image.load('./img/coin_2.png'),
    pygame.image.load('./img/coin_3.png'),
    pygame.image.load('./img/coin_4.png'),
    pygame.image.load('./img/coin_5.png')
])
monety = [
    pygame.Rect(515, 66, 23, 23),
    pygame.Rect(291, 66, 23, 23),
    pygame.Rect(548, 420, 23, 23),
    pygame.Rect(932, 420, 23, 23),
    pygame.Rect(1156, 420, 23, 23),
    pygame.Rect(1060, 130, 23, 23)
]

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 15 * facing
        self.vel_enemy = 7

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

#klasa tworząca platformy
class platform(object):

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.space = (self.x, self.y, self.width, self.height)
        self.gora = ((self.x, self.y), (self.x + width, self.y))
        self.hitbox_plat = pygame.Rect(self.space)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.space)

def text_objects(text, font):
    textSurface = font.render(text, True, (163, 114, 98))
    return textSurface, textSurface.get_rect()

#tworzenie przycisku
def button(msg, x, y, w, h, ic, ac, intro, win, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y and intro == True:
        pygame.draw.rect(bg, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        if intro == True:
            pygame.draw.rect(bg, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    win.blit(textSurf, textRect)


#pojedynczy pocisk przeciwnika
class shoot_enemy(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 15 * facing
        self.vel_enemy = 7

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)
        self.img = pygame.image.load("img\platform_cp.png")

    def update(self, x_shift):
        self.rect.x += x_shift

    def draw(self, win, x, y):
        win.blit(self.img, (x, y))

class Kolce(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)
        self.img = pygame.image.load("img\lava.png")

    def update(self, x_shift):
        self.rect.x += x_shift

    def draw(self, win, x, y):
        win.blit(self.img, (x, y))

class Meta(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)
        self.img = pygame.image.load("img\meta3.png")

    def update(self, x_shift):
        self.rect.x += x_shift

    def draw(self, win, x, y):
        win.blit(self.img, (x, y))