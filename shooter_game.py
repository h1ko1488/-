#Создай собственный Шутер!


from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0
score = 0
goal = 10
max_lost = 89

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('шутер')
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

ship = Player('rocket.png', 5, win_height-100, 80, 100, 10)

aliens = sprite.Group()
for i in range(1, 6):
    alien = Enemy('ufo.png', randint(80,win_width-80), -40, 80, 50, randint(1,5))
    aliens.add(alien)

bullets = sprite.Group()

game = True
finish = False
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 36)

win = font1.render('You win:', 1, (255, 255, 255))
lose = font1.render('You lose:', 1, (180, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0,0))


        ship.update()
        aliens.update()
        bullets.update()
        ship.reset()

        aliens.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(aliens, bullets, True, True)
        for c in collides:
            score = score + 1
            alien = Enemy('ufo.png', randint(80,win_width-80), -40, 80, 50, randint(1,5))
            aliens.add(alien)

        if sprite.spritecollide(ship, aliens, False) or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True 
            window.blit(lose, (200, 200))
             
        text = font1.render('Счет:' + str(score), 1, (255, 255, 255))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text, (10, 10))
        window.blit(text_lose, (10, 50))

        display.update()
        
    clock.tick(FPS)
