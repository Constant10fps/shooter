from pygame import *
winWidth = 1200
winHeight = 900
#~~~~~~~~#
window = display.set_mode((winWidth, winHeight))
display.set_caption("Sʜᴏᴏᴛᴇʀ")
background = transform.scale(image.load("skybox.jpg"), (winWidth, winHeight))

mixer.init()
mixer.music.load("-Electroman-Adventures-.mp3")
mixer.music.play(loops=-1)
mixer.music.set_volume(0.2)
#~~~~~~~#
class GameSprite(sprite.Sprite):
    """docstring for ClassName."""
    def __init__(self, p_image, size: tuple, start_pos: tuple, speed: int):
        super.__init__()
        self.image = transform.scale(image.load(p_image), size)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#~~~~~~~#
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
    display.update()
    clock.tick(60)