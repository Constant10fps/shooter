from pygame import *
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
    
    def show(self, surface: Surface): # need surface
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self, win_width: int, fire_cooldown: int): # need width
        keys = key.get_pressed()
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < win_width - self.width - 5:
            self.rect.x += self.speed

    def fire(self, group: sprite.Group): # changed with surface
        group.add(Bullet("bullet.png", (40, 75), (self.rect.centerx - 20, self.rect.top), 7))

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

class HealthBar():
    def __init__(self, x, y, w, h, max_hp) -> None:
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.hp, self.max_hp = max_hp, max_hp
    
    def show(self, surface):
        ratio = self.hp / self.max_hp
        draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))
