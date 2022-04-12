import pygame

bg = pygame.image.load('./img/background.jpg')

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
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

#tworzenie przycisku
def button(msg, x, y, w, h, ic, ac, intro, win, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y and intro == True:
        pygame.draw.rect(bg, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            print("klik")
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
