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
        bullets_SPRITE.add(Bullet("bullet.png", (40, 75), (self.rect.centerx - 20, self.rect.top), 7))

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

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
class HealthBar():
    def __init__(self, x, y, w, h, max_hp) -> None:
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.hp, self.max_hp = max_hp, max_hp
    
    def show(self):
        ratio = self.hp / self.max_hp
        draw.rect(window, "red", (self.x, self.y, self.w, self.h))
        draw.rect(window, "green", (self.x, self.y, self.w * ratio, self.h))

def collision_check(item: sprite.Group):
    global killcount
    if sprite.groupcollide(bullets_SPRITE, aliens, True, True):
        killcount += 1
    for elem in item.sprites():
            if elem.rect.y <= -100:
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
        if not(ri(ri_range[0]-1, ri_range[1]+1)):
            asteroids.add(Asteroid("32728.jpg", (100, 100), (ri(0, winWidth - 100), -200), 3))
    timer -= 1

fire_cooldown: int = 0
timer: int = 60
player = Player("spaceship.png", (150, 150), (winWidth // 2, winHeight - 150), 10)
shield = Shield("shield.png", (200, 200), ((winWidth // 2) - 25, winHeight - 175), 10)
aliens: sprite.Group = sprite.Group()
asteroids = sprite.Group()
bullets_SPRITE: sprite.Group = sprite.Group()
killcount: int = 0
#~~Counter displays~~#
font.init()
stats = font.Font("stats.ttf", 30)
saiba_small = font.Font("saiba.otf", 50)
saiba = font.Font("saiba.otf", 100)
# god this is awful
game_over = saiba.render("GAME OVER", True, (0, 255, 51))
restart = saiba_small.render("PRESS TAB TO RETURN TO MENU", True, (0, 255, 51))
logo = saiba.render("COSMIC BATTLE", True, (0, 255, 51))
start = saiba_small.render("PRESS ENTER TO START", True, (0, 255, 51))
lost = 0
restart_timer = 250
health_bar = HealthBar(winWidth - 530, 20, 500, 35, 100)
#~~~~~Game phases~~~~~#
menu = True
lvl_play = False
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
        random_spawn((-2, 2), 60, ri(3, 5))
        for alien in aliens:
            if alien.rect.y > winHeight:
                aliens.remove(alien)
        aliens.draw(window)
        aliens.update()
        window.blit(logo, (100, 200))
        window.blit(start, (100, 300))
        if key.get_pressed()[K_RETURN]:
            aliens.empty()
            lvl_play = True
            lvl_1 = True
            menu = False
        elif key.get_pressed()[K_ESCAPE]:
            quit()
            break
    if lvl_play:
        # aliens lvl 1
        if lvl_1:
            random_spawn((-2, 2), 60, ri(3, 5))
            if killcount > 50:
                lvl_1 = False
                lvl_2 = True
        # aliens lvl 2
        if lvl_2:
            random_spawn((-1, 1), 50, ri(4, 5))
            if killcount > 150:
                lvl_2 = False
                lvl_boss = True
        # boss lvl with one enemy
        if lvl_boss:
            # Не забудь убрать когда будешь тестировать игру!
            quit()
            game = False
            break
        # aliens check
        for alien in aliens:
            if sprite.collide_rect(alien, player):
                aliens.remove(alien)
                health_bar.hp -= 20
            if alien.rect.y > winHeight:
                aliens.remove(alien)
                lost += 1
                health_bar.hp -= 10
        # draw all sprites
        aliens.draw(window)
        aliens.update()
        collision_check(bullets_SPRITE)
        show_update(player)
        show_update(shield)
        # text rendering
        killcount_text = stats.render(f"Killcount: {killcount}", True, (0, 255, 51))
        lost_text = stats.render(f"Lost: {lost}", True, (0, 255, 51))
        window.blit(killcount_text, (10, 20))
        window.blit(lost_text, (10, 60))
        # health check
        health_bar.show()
        if health_bar.hp <= 0:
            lvl_restart = True
            lvl_play = False
    if lvl_restart:
        # draw all sprites
        collision_check(bullets_SPRITE)
        aliens.draw(window)
        aliens.update()
        window.blit(game_over, (315, 350))
        window.blit(killcount_text, (350, 460))
        window.blit(lost_text, (350, 500))
        # check for enter
        keys = key.get_pressed()
        if not restart_timer:
            if keys[K_TAB]:
                killcount = 0
                lost = 0
                health_bar.hp = 100
                bullets_SPRITE.empty()
                aliens.empty()
                menu = True
                restart_timer = 250
                lvl_restart = False
            window.blit(restart, (250, 600))
        else:
            restart_timer -= 1
    if fire_cooldown > 0:
        fire_cooldown -= 1
    display.update()
    clock.tick(60)
    for e in event.get():
        if e.type == QUIT:
            game = False