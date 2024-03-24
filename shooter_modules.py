from math import sqrt
from random import randint as ri
from typing import Any
from pygame import *
# no god further, i forgot how anything here works

# The `GameSprite` class is a basic structure for generating game sprites with an image, size,
# position, and speed attributes, along with a method to display the sprite on a given surface.
class GameSprite(sprite.Sprite):
    def __init__(self, p_image: str, size: tuple, start_pos: tuple, speed: int):
        super().__init__()
        self.WIN_WIDTH = 1200
        self.WINHEIGHT = 720
        self.width = size[0]
        self.height = size[1]
        self.image = transform.scale(image.load(p_image), size)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.point = (ri(0, self.WIN_WIDTH - self.width), ri(0, 400))
        a = abs(self.rect.x - self.point[0])
        b = abs(self.rect.y - self.point[1])
        c = int(sqrt(a ** 2 + b ** 2))
        dem = int(c/self.speed)
        self.x_move = int(a/dem)
        self.y_move = int(b/dem)
    def show(self, surface: Surface): # need surface
        surface.blit(self.image, (self.rect.x, self.rect.y))


# The Player class is a GameSprite subclass that generates the player sprite, includes an update
# function for movement within the window width, and a fire function to create bullets.
class Player(GameSprite):
    def update(self, fire_cooldown: int): # need width
        keys = key.get_pressed()
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < self.WIN_WIDTH - self.width - 5:
            self.rect.x += self.speed

    def fire(self, b_group: sprite.Group): # changed with surface
        b_group.add(Bullet("bullet.png", (40, 75), (self.rect.centerx - 20, self.rect.top), 7))


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed


class Shield(GameSprite):
    def update(self, player: Player):
        self.rect.x = player.rect.x - 25
        self.rect.y = player.rect.y - 25


class Alien(GameSprite):
    def update(self):
        self.rect.y += self.speed


class Boss(GameSprite):

    def update(self) -> None:
        # Left - True, Right - False
        self.direction = True
        if self.rect.x <= 0:
            self.direction = False
        if self.rect.x >= self.WIN_WIDTH - self.width:
            self.direction = True
        if (abs(self.rect.x - self.point[0]) < 40 
                and abs(self.rect.y - self.point[1]) < 40):
            self.point = (ri(0, self.WIN_WIDTH - self.width), ri(0, 400))
            a = abs(self.rect.x - self.point[0])
            b = abs(self.rect.y - self.point[1])
            c = round(sqrt(a ** 2 + b ** 2))
            dem = round(c/self.speed)
            self.x_move = round(a/dem)
            self.y_move = round(b/dem)
        #self.rect.x += self.x_move if self.rect.x < self.point[0] else -self.x_move
        #self.rect.y += self.y_move if self.rect.y > self.point[1] else -self.y_move
        if self.rect.x < self.point[0]: self.rect.x += self.x_move
        if self.rect.x > self.point[0]: self.rect.x -= self.x_move
        if self.rect.y < self.point[1]: self.rect.y += self.y_move
        if self.rect.y > self.point[1]: self.rect.y -= self.y_move
        
    def fire(self, group: sprite.Group) -> None:
        if ri(0, 500) < 5:
            group.add(Bullet("bullet180.png", (40, 75), (self.rect.centerx, self.rect.bottom), -10))


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed


class HealthBar():
    def __init__(self, x, y, w, h, max_hp) -> None:
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.hp, self.max_hp = max_hp, max_hp
    
    def show(self, hp: int,  surface: Surface):
        ratio = hp / self.max_hp
        draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))


class System():
    """
    Basic checking operations and spawning process. 
    Input variables to be used in text displays.
    """
    def __init__(self, window: Surface,
                bullets_group: sprite.Group, 
                aliens_group: sprite.Group, 
                ast_group: sprite.Group):
        self.window = window
        self.width = 1200
        self.height = 720
        self.hp = 100
        self.killcount = 0
        self.lost_count = 0
        self.timer = 0
        self.fire_cooldown = 25
        self.bullets = bullets_group
        self.aliens = aliens_group
        self.asteroids = ast_group
    
    def collision_check(self, player: Player):
        # aliens check
        for alien in self.aliens:
            if sprite.collide_rect(alien, player):
                self.aliens.remove(alien)
                self.hp -= 20
            if alien.rect.y > self.height + 200:
                self.aliens.remove(alien)
                self.lost_count += 1
                self.hp -= 10
        self.aliens.draw(self.window)
        self.aliens.update()
        # bullets check
        if sprite.groupcollide(self.bullets, self.aliens, True, True):
            self.killcount += 1
        for elem in self.bullets.sprites():
                if elem.rect.y <= -100:
                    self.bullets.remove(elem)
        self.bullets.draw(self.window)
        self.bullets.update()

    def random_spawn(self, ri_range: tuple, timer_reset: int, enemy_speed: int):
        if self.timer < 0:
            if not(ri(ri_range[0], ri_range[1])):
                self.aliens.add(Alien("alien.png",
                                (180, 120), (ri(0, self.width - 180), -100), enemy_speed))
                self.timer = timer_reset
            elif not(ri(ri_range[0]-4, ri_range[1]+4)):
                self.asteroids.add(Asteroid("32728.png", 
                                    (100, 100), (ri(0, self.width - 100), -200), 3))
        self.timer -= 1

    def player_check(self, keys: key.get_pressed, player: Player):
        if (keys[K_w] or keys[K_SPACE] or keys[K_UP]):
                if not self.fire_cooldown:
                    player.fire(self.bullets)
                    self.fire_cooldown = 25
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1