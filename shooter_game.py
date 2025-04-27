from pygame import *
from random import randint
from time import time as timer

#game scene
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, image_x , image_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(image_x, image_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))




class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 15, 20)
        bullets.add(bullet)


lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


font.init()
font1 = font.Font(None, 36)
win = font1.render('You win!', True, (255, 255, 255))
lose = font1.render('You lost!', True, (255, 255, 255))


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()          

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(30, win_width -30), -40, randint(1, 7), 80, 50)
    asteroids.add(asteroid)       
            

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

FPS = 30
finish = False
run = True

file_sound = mixer.Sound('fire.ogg')

ship = Player('rocket.png', 5, 400, 8, 80, 100)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 620), -40, randint(1, 5), 80, 50)
    monsters.add(monster)

score = 0

life = 3
rel_time = False
num_fire = 0


clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN: 
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    file_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                        last_time = timer()
                        rel_time = True
                
    if not finish:
        window.blit(background,(0, 0))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text = font1.render('Счёт:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        ship.update()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        ship.reset()
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font1.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (250, 450))
            else:
                num_fire = 0
                rel_time = False

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), -40, randint(1, 5), 80, 50)
            monsters.add(monster)
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))
        
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1
        if life == 0 or lost >= 10:
            finish = True
            window.blit(lose, (200, 200))

        if life == 3:
            life_color = (0, 250, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        
        text_life = font1.render(str(life), 1, life_color)
        
            
        
            


        display.update()

       



   
    clock.tick(FPS)
    