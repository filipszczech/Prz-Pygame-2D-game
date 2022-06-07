import pygame

class Animation:
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 3

    def update(self):
        # increment the timer
        self.animationTimer += 1
        # if the timer gets too high...
        if self.animationTimer >= self.animationSpeed:
            # reset the timer
            self.animationTimer = 0
            # increment the current image
            self.imageIndex += 1
            # loop back to the first image in the list
            # once the index gets too high
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0

    def draw(self, win, x, y, ):
        win.blit(self.imageList[self.imageIndex], (x, y))
