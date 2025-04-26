from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, image1, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(image1), (65, 65))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def more(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > 1000:
            self.rect.x = randint(0, 600)
            self.rect.y = 0
            lose += 1

class Player(GameSprite):
    def __init__(self, image1, speed, x, y):
        super().__init__(image1, speed, x, y)
        self.ammo = 30  # Количество пуль
        self.reload_time = 2000  # Время перезарядки в миллисекундах
        self.last_shot_time = 0  # Время последнего выстрела

    def more(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed

    def fire(self):
        current_time = time.get_ticks()
        if self.ammo > 0 and current_time - self.last_shot_time > 500:  # Задержка между выстрелами
            rocket = Rocket("rocket.png", 20, self.rect.centerx, self.rect.top)
            rockets.add(rocket)
            self.ammo -= 1  # Уменьшаем количество пуль
            self.last_shot_time = current_time  # Обновляем время последнего выстрела

class Rocket(GameSprite):
    def more(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# Инициализация игры
player = Player('bullet.png', 15, 10, 900)

monsters = sprite.Group()
for i in range(20):
    monster = Enemy('ufo.png', randint(1, 5), randint(0, 600), 0)
    monsters.add(monster)

window = display.set_mode((700, 1000)) 
background = transform.scale(image.load("galaxy.jpg"), (700, 7500))
display.set_caption('Шутер')

font.init()
Font = font.Font(None, 30)
win_bbel = Font.render('ТЫ ПОБЕДИЛ', True, (166, 0, 255))
lose_lade0 = Font.render('ТЫ ЧЁРНЫЙ', True, (250, 0, 0))
lose = 0
win = 0
lives = 5  # Количество жизней
font = font.Font(None, 70)
fps = 60
clock = time.Clock()
game = True
mixer.init()
mixer.music.load('gimn-rossii-gimn-rossii-so-slovam2.mp3')
mixer.music.play()
rockets = sprite.Group() 

while game:
    window.blit(background, (0, 0))
    player.reset()
    player.more()
    monsters.draw(window)
    rockets.draw(window)

    for rocket in rockets:
        rocket.more()

    # Проверка на столкновения
    sprites_list = sprite.groupcollide(monsters, rockets, True, True)
    collided_monsters = sprite.spritecollide(player, monsters, True)
    
    for s in sprites_list:
        win += 1
        monster = Enemy('ufo.png', randint(1, 5), randint(0, 600), 0)
        monsters.add(monster)

    for _ in collided_monsters:
        lives -= 1  #? Уменьшаем количество жизней при столкновении
        if lives <= 0:
            window.blit(lose_lade0, (250, 200))
            display.update()
            time.delay(3000)
            game = False

    score = font.render('Очки:' + str(win), True, (255, 255, 255))
    lose_lade = font.render("Пропущено:" + str(lose), True, (255, 255, 255))
    lives_display = font.render("Жизни:" + str(lives), True, (255, 255, 255))  # Отображение жизней
    ammo_display = font.render("Пули:" + str(player.ammo), True, (255, 255, 255))  # Отображение пуль
    window.blit(score, (10, 20))
    window.blit(lose_lade, (10, 60))
    window.blit(lives_display, (10, 100))  #! Отображение жизней на экране
    window.blit(ammo_display, (10, 140))  # Отображение пуль на экране

    for monster in monsters:
        monster.more()

    if win >= 15:
        window.blit(win_bbel, (250, 200))
        display.update()
        time.delay(3000)
        game = True

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    display.update()
    clock.tick(fps)
