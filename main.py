#~~~~~~~Import~~~~~~~~#
from random import randint as ri
from pygame import *
winWidth = 1200
winHeight = 900
#~~~~~Background~~~~~~#
window = display.set_mode((winWidth, winHeight)) # Setting the size
display.set_caption("Sʜᴏᴏᴛᴇʀ") # Name of the window
background = transform.scale(image.load("skybox.jpg"), (winWidth, winHeight)) # background
#~~~~~~~~Music~~~~~~~~#
mixer.init()
mixer.music.load("-Electroman-Adventures-.mp3")
mixer.music.play(loops=-1)
mixer.music.set_volume(0.2)
#~~~~~~~Classes~~~~~~~#
class GameSprite(sprite.Sprite):
    def __init__(self, p_image: str, size: tuple, start_pos: tuple, speed: int):
        super().__init__()
        self.width = size[0]
        self.height = size[1]
        self.image = transform.scale(image.load(p_image), size)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < winWidth - self.width - 5:
            self.rect.x += self.speed
        if (keys[K_w] or keys[K_SPACE] or keys[K_UP]):
            global fire_cooldown
            if not fire_cooldown:
                self.fire()
                fire_cooldown = 25
    def fire(self):
        bullets_SPRITE.add(Bullet("bullet.png", (75, 75), (self.rect.x + 37, self.rect.y + 37), 7))
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
class Shield(GameSprite):
    def update(self) -> None:
        self.rect.x = player.rect.x - 25
        self.rect.y = player.rect.y - 25
class Alien(GameSprite):
    def update(self):
        self.rect.y += self.speed
def collision_check(item: sprite.Group):
    for elem in item.sprites():
            if elem.rect.y <= 5:
                item.remove(elem)
    item.draw(window)
    item.update()
def show_update(item):
    item.show()
    item.update()
def random_spawn(ri_range: tuple, timer_reset: int, enemy_speed: int):
    global timer
    if timer < 0:
        if not(ri(ri_range[0], ri_range[1])):
            aliens.add(Alien("alien.png", (180, 120), (ri(0, winWidth - 180), -100), enemy_speed))
            timer = timer_reset
    timer -= 1
fire_cooldown: int = 0
timer: int = 60
player = Player("spaceship.png", (150, 150), (winWidth // 2, winHeight - 150), 10)
shield = Shield("shield.png", (200, 200), ((winWidth // 2) - 25, winHeight - 175), 10)
aliens: sprite.Group = sprite.Group()
bullets_SPRITE: sprite.Group = sprite.Group()
killcount: int = 0
#~~Counter displays~~#
font.init()
stats = font.Font("stats.ttf", 30)
lost = 0
lives = 100
#~~~~~Game phases~~~~~#
menu = False
lvl_play = True
lvl_1 = True
lvl_2 = False
lvl_boss = False
lvl_restart = False
#~~~~~~~~START~~~~~~~~#
game = True
clock = time.Clock()
while game:
    window.blit(background, (0,0))
    if menu:
        pass
    if lvl_play:
        if lvl_1:
            random_spawn((-2, 2), 60, 4)
            if killcount > 50:
                lvl_1 = False
                lvl_2 = True
        if lvl_2:
            random_spawn((-1, 1), 50, 4)
            if killcount > 150:
                lvl_2 = False
                lvl_boss = True
        if lvl_boss:
            # Не забудь убрать когда будешь тестировать игру!
            quit()
            game = False
        for alien in aliens:
            if sprite.spritecollide(alien, bullets_SPRITE, True):
                aliens.remove(alien)
                killcount += 1
            if alien.rect.y > winHeight:
                aliens.remove(alien)
                lost += 1
                lives -= 20
        aliens.draw(window)
        aliens.update()
        collision_check(bullets_SPRITE)
        show_update(player)
        show_update(shield)
        killcount_text = stats.render(f"Killcount: {killcount}", True, (0, 255, 51))
        lost_text = stats.render(f"Lost: {lost}", True, (0, 255, 51))
        lives_text = stats.render(f"Lives: {lives}", True, (0, 255, 51))
        window.blit(killcount_text, (10, 20))
        window.blit(lost_text, (10, 60))
        window.blit(lives_text, (10, 100))
        if lives == 0:
            quit()
            game = False
            # Заменить перед релизом
    if lvl_restart:
        pass
    if fire_cooldown > 0:
        fire_cooldown -= 1
    display.update()
    clock.tick(60)
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
                game = False