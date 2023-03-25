#Создай собственный Шутер!
from pygame import *
from random import randint

font.init()
mixer.init()
mixer.music.load('GalaxyGame.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)

win = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
FPS = 60
game = True

miss_counter = 0
points_counter = 0



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, wid, hei):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (wid, hei))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def go(self):
        keys = key.get_pressed()

        if keys[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x <= 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', rocket.rect.x+12.5, rocket.rect.y - 50, 5, 40, 40)
        Bullets.add(bullet)



font1 = font.SysFont("Arial", 50)

backgroundWIN = transform.scale(image.load('Winner.jpg'), (700, 500))
backgroundLOSE = transform.scale(image.load('LosePicture.jpeg'), (700, 500))

class Enemy(GameSprite):
    def update(self):
        global miss_counter
        if self.rect.y < 435:
            self.rect.y += self.speed
        if self.rect.y >= 435:
            self.rect.x = randint(0, 635)
            self.rect.y = randint(-500, 0)
            miss_counter += 1
            print(miss_counter)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()
        


E1 = Enemy(player_image='ufo.png', player_x= randint(0, 635), player_y = randint(-500, 0), player_speed=1, wid = 65, hei = 65)
E2 = Enemy(player_image='ufo2.png', player_x= randint(0, 635), player_y = randint(-500, 0), player_speed=1, wid = 65, hei = 65)
E3 = Enemy(player_image='ufo3.png', player_x= randint(0, 635), player_y = randint(-500, 0), player_speed=1, wid = 65, hei = 65)
E4 = Enemy(player_image='ufo4.png', player_x= randint(0, 635), player_y = randint(-500, 0), player_speed=1, wid = 65, hei = 65)
E5 = Enemy(player_image='asteroid.png', player_x= randint(0, 635), player_y = randint(-500, 0), player_speed=1, wid = 65, hei = 65)


Enemies = sprite.Group()
Enemies.add(E1)
Enemies.add(E2)
Enemies.add(E3)
Enemies.add(E4)
Enemies.add(E5)

rocket = Player(player_image='rocket.png', player_x=350, player_y=430, player_speed=7, wid = 65, hei = 65)

Bullets = sprite.Group()
sound_fire = mixer.Sound('laser.ogg')

sound_fire.set_volume(0.1)

finish = False

loser = False 
winner = False


secret = mixer.Sound('brue.ogg')
secret.set_volume(0.1)


while game:
    if winner == True:
        win.blit(backgroundWIN, (0, 0)) 
        winner = font1.render('УРА, ТЫ ОФИГЕННЫЙ', True, (255, 255, 255))
        win.blit(winner, (150, 10))
    if loser == True:
        win.blit(backgroundLOSE, (0, 0))
        lose = font1.render('ТЫ НУБ БОТ....', True, (255, 255, 255))
        win.blit(lose, (150, 10))
    
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            print('x', x)
            print('y', y)
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                sound_fire.play()
            
            if e.key == K_f:
                secret.play()
                
    if finish != True:
        win.blit(background, (0, 0))
        rocket.reset()
        rocket.go()

        Enemies.draw(win)
        Enemies.update()

        Bullets.draw(win)
        Bullets.update()
    
        Enemies.draw(win)
        Enemies.update()

        miss_counter_font = font1.render('Пропущено: ' + str(miss_counter), True, (255, 255, 255))
        win.blit(miss_counter_font, (2, 9))
    
        points_counter_font = font1.render('Счет: ' + str(points_counter), True, (255, 255, 255))
        win.blit(points_counter_font, (2, 45))







        collidesBE = sprite.groupcollide(Enemies, Bullets, True, True)
        
        for c in collidesBE:
            points_counter += 1
            a = randint(1, 5)
            if a == 1:
                E = Enemy(player_image='ufo.png', player_x= randint(0, 635), player_y = randint(-500, 0), player_speed=1, wid = 65, hei = 65)           
            elif a == 2:
                E = Enemy(player_image='asteroid.png', player_x= randint(0, 635), player_y = randint(-500, 0), player_speed=1, wid = 65, hei = 65)
            elif a == 3:
                E = Enemy(player_image='ufo2.png', player_x= randint(0, 635), player_y = randint(-500, 0), player_speed=1, wid = 65, hei = 65)
            elif a == 4:
                E = Enemy(player_image='ufo3.png', player_x= randint(0, 635), player_y = randint(-500, 0), player_speed=1, wid = 65, hei = 65)
            elif a == 5:
                E = Enemy(player_image='ufo4.png', player_x= randint(0, 635), player_y = randint(-500, 0), player_speed=1, wid = 65, hei = 65)
            Enemies.add(E)
            

        hits = sprite.spritecollide(rocket, Enemies, False)

        if miss_counter == 3 or hits:
            loser = True
            finish = True
            mixer.music.load('lose_music.ogg')
            mixer.music.play()
            mixer.music.set_volume(0.1)



        if points_counter == 50:
            mixer.music.load('win_music.ogg')
            mixer.music.play()
            mixer.music.set_volume(0.1)
            winner = True
            finish = True
        


    clock.tick(FPS)
    display.update()


