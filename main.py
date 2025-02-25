import pygame
pygame.init()
import time
from random import *

fps = 60
win_w, win_h = 1600, 1100

window = pygame.display.set_mode((win_w, win_h))

timer = pygame.time.Clock()

pygame.display.set_caption("PiuPiu")

background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (win_w, win_h))

background1 = pygame.image.load("galaxy2.jpg")
background1 = pygame.transform.scale(background1, (win_w, win_h))

try:
    with open("record.txt", "r", encoding="Utf-8") as file:
        record = int(file.read())
except:
    record = 0

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

    def move(self, a, d): 
        keys = pygame.key.get_pressed() 
        if keys[d] and self.rect.right < win_w: 
            self.rect.x += self.speed
        if keys[a] and self.rect.left > 0: 
            self.rect.x -= self.speed

class Enemy(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self):
        global lost_lb, lost
        self.rect.y += self.speed
        if self.rect.y >= win_h:
            self.rect.x = randint(0, win_w-self.rect.w)
            self.rect.y = randint(-250, -50)
            lost += 1
            lost_lb = font_stat.render(f"пропущено: {lost}", True, (255, 255, 255))

class Bullet(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self):
        self.rect.y -= self.speed

def initialize_game():
    global player, points, lost, enemies, bullets, points_lb, lost_lb, finish, menu, enemy_spawn_counter
    player = Player(750, 950, 100, 100, pygame.image.load("rocket.png"), 15)
    points = 0
    lost = 0
    enemies = []
    for _ in range(4): 
        enemy = Enemy(randint(0, win_w-100), randint(-250, -50), 100, 100, pygame.image.load("ufo.png"), randint(1, 2))
        enemies.append(enemy)
    bullets = []
    points_lb = font_stat.render(f"вбито: {points}", True, (0, 255, 0))
    lost_lb = font_stat.render(f"пропущено: {lost}", True, (255, 255, 255))
    finish = False
    menu = False
    enemy_spawn_counter = 0


player = Player(750, 950, 100, 100, pygame.image.load("rocket.png"), 15)

points = 0
lost = 0

enemies = []

for _ in range(8): 
    enemy = Enemy(randint(0, win_w-100), randint(-250, -50), 100, 100, pygame.image.load("ufo.png"), randint(2, 6))
    enemies.append(enemy)


bullets = []

bullet_image = pygame.image.load("bullet.png")
bullet_speed = 10

font_record = pygame.font.SysFont("Arial", 80)
font_stat = pygame.font.SysFont("Arial", 15)
points_lb = font_stat.render(f"вбито: {points}", True, (0, 255, 0))
lost_lb = font_stat.render(f"вбито: {lost}", True, (0, 255, 0))

font_lost = pygame.font.SysFont("Arial Black", 250)
lost_message = font_lost.render("You Lost", True, (255, 0, 0))
play_again_message = font_record.render("R - play again", True, (255, 0, 0))

but_img = pygame.image.load("button1.png")
button = Sprite(200, 200, 600, 150, but_img)

def new_record(record, score):
    if record < score:
        with open("record.txt", "w", encoding="Utf-8") as file:
            file.write(str(score))
        window.blit(font_record.render(f"Новий рекорд {score}", True,(255,255,255)), (200, 0))   

game = True
finish = False
menu = True

enemy_spawn_counter = 0
enemy_spawn_frequency = 60

pygame.mixer.music.set_volume(0.01)

while game:
    if menu:
        window.blit(background1, (0, 0))
        button.draw()

    if not finish and not menu:
        window.blit(background, (0, 0))
        player.draw()
        player.move(pygame.K_a, pygame.K_d)

        for enemy in enemies:
            enemy.move()
            enemy.draw()

        if lost >= 5:
            new_record(record, points)
            finish = True


        for bullet in bullets:
            bullet.move()
            bullet.draw()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    points += 1
                    points_lb = font_stat.render(f"вбито: {points}", True, (0, 255, 0))
                    break

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                finish = True
                new_record(record, points)
                break

        enemy_spawn_counter += 1
        if enemy_spawn_counter >= enemy_spawn_frequency:
            enemy_spawn_counter = 0
            enemy = Enemy(randint(0, win_w-100), randint(-250, -50), 100, 100, pygame.image.load("ufo.png"), randint(2, 6))
            enemies.append(enemy)
                    
        window.blit(points_lb, (10, 10))
        window.blit(lost_lb, (10, 30))

    if finish:
        window.blit(lost_message, (win_w // 2 - lost_message.get_width() // 2, win_h // 2 - lost_message.get_height() // 2))
        window.blit(play_again_message, (win_w // 2 - play_again_message.get_width() // 2, win_h // 2 + lost_message.get_height() // 2))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if menu and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if button.rect.collidepoint(x, y):
                menu = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("space1.mp3")
                pygame.mixer.music.play(-1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx - 5, player.rect.top, 100, 200, bullet_image, bullet_speed)
                bullets.append(bullet)
            if event.key == pygame.K_r and finish:
                initialize_game()
        

    pygame.display.update()
    timer.tick(fps)


