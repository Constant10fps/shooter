from math import hypot
from random import randint as ri
from pygame import *
# no god further, i forgot how anything here works

# The `GameSprite` class is a basic structure for generating game sprites with an image, size,
# position, and speed attributes, along with a method to display the sprite on a given surface.
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image: str, size: tuple, start_pos: tuple, speed: int):
        super().__init__()
        # const
        self.WIN_WIDTH = 1200
        self.WIN_HEIGHT = 720
        # size and image 
        self.width = size[0]
        self.height = size[1]
        self.image = transform.scale(image.load(sprite_image), size)
        # movement
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.speed = speed
        # Boss
        self.point_x = self.rect.x
        self.point_y = self.rect.y
        self.x_move = 0
        self.y_move = 0
    def show(self, surface: Surface): # need surface
        surface.blit(self.image, (self.rect.x, self.rect.y))


# The Player class is a GameSprite subclass that generates the player sprite, includes an update
# function for movement within the window width, and a fire function to create bullets.
class Player(GameSprite):
    def update(self): # need width
        keys = key.get_pressed()
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < self.WIN_WIDTH - self.width - 5:
            self.rect.x += self.speed

    def fire(self, b_group: sprite.Group): # changed with surface
        b_group.add(Bullet("sprites/bullet.png", (40, 75), (self.rect.centerx - 20, self.rect.top), 7))


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


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed


class Boss(GameSprite):
    def update(self, bb: sprite.Group) -> None:
        if (hypot(self.rect.x - self.point_x, self.rect.y - self.point_y) < 40 or abs(self.y_move) < 2 or 
            self.rect.x not in range(0, self.WIN_WIDTH - self.width) or self.rect.y not in range(0, 400)):
            # new heading
            self.point_x = ri(0, self.WIN_WIDTH - self.width)
            self.point_y = ri(0, 400)
            # pythagorean theorem
            a = self.rect.x - self.point_x
            b = self.rect.y - self.point_y
            c = hypot(a, b)
            # dividing into steps
            dem = c/self.speed
            self.x_move = round(a/dem)
            self.y_move = round(b/dem)
            
        # moving
        self.rect.x -= self.x_move
        self.rect.y -= self.y_move
        '''
        if self.rect.x < self.point[0]: 
            self.rect.x += self.x_move
        
        if self.rect.x > self.point[0]: 
            self.rect.x -= self.x_move
        
        if self.rect.y < self.point[1]: 
            self.rect.y += self.y_move
        
        if self.rect.y > self.point[1]: 
            self.rect.y -= self.y_move
        '''
        # firing
        if ri(0, 500) < 4:
            self.fire(bb)
    
    def fire(self, group: sprite.Group) -> None:
        group.add(Bullet("sprites/boss_bullet.png", (80, 150), (self.rect.centerx, self.rect.centery), -5))


class HealthBar():
    def __init__(self, x, y, w, h, max_hp) -> None:
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.hp, self.max_hp = max_hp, max_hp
    
    def show(self, hp: int,  surface: Surface):
        ratio = hp / self.max_hp
        draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))