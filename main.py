#~~~~~~~Import~~~~~~~~#
from typing import Any
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
    def __init__(self, p_image, size: tuple, start_pos: tuple, speed: int):
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
            self.fire()
    def fire(self):
        pass

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
player = Player("spaceship.png", (150, 150), (winWidth//2, winHeight - 150), 10)
bullets = [Bullet("bullet.png", (75, 75), (winWidth//2, winHeight - 150), 10)]
aliens = []
#~~~~~Game phases~~~~~#
menu = False
lvl_play = True
lvl_1 = False
lvl_2 = False
lvl_boss = False
lvl_restart = False
#~~~~~~~~START~~~~~~~~#
game = True
clock = time.Clock()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
                game = False
    window.blit(background, (0,0))
    if menu:
        pass
    if lvl_play:
        if lvl_1:
            pass
        if lvl_2:
            pass
        if lvl_boss:
            pass
        player.show()
        player.update()
        for bullet in bullets:
            if bullet.rect.y > 5:
                bullet.show()
                bullet.update()
            else:
                bullets.remove(bullet)
    if lvl_restart:
        pass
    display.update()
    clock.tick(60)