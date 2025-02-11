import pygame
pygame.init()
import time
import random

fps = 165
win_w, win_h = 1600, 1100

window = pygame.display.set_mode((win_w, win_h))

timer = pygame.time.Clock()

pygame.display.set_caption("PiuPiu")

background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (win_w, win_h))

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self, a, d,): 
        keys = pygame.key.get_pressed() 
        if keys[d]: 
            self.rect.x += self.speed
        if keys[a]: 
            self.rect.x -= self.speed

    class Enemy(Sprite):
        def __init__(self, x, y, w, h, image, speed):
            super().__init__(x, y, w, h, image)
            self.speed = speed

        def move(self):
            self.rect.x += self.speed
            if self.rect.y >= win_h:
                self.rect.x = 0
            self.rect.x = random.randint(0, win_w - self.rect.width)



player = Player(750, 950, 100, 100, pygame.image.load("rocket.png"), 6)

game = True
finish = False

while game:
    pygame.display.update()
    timer.tick(fps)

    if not finish:
        window.blit(background, (0, 0))
        player.draw()
        player.move(pygame.K_a, pygame.K_d)
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

pygame.time.delay(1000)

