from shooter_modules import *
from pygame import *
class Spawning():
    def __init__(self, win_width: int, win_height: int):
        self.width = win_width
        self.height = win_height
        self.aliens = sprite.Group()
        self.asteroids = sprite.Group()
    def alien_spawn(self, chance: int, timer_reset: int):
        if self.alien_timer <= 0 and ri(0, 100) <= chance:
                enemy_speed = ri(3, 5)
                self.aliens.add(Alien("sprites/alien.png", (180, 120), (ri(0, self.width - 180), -100), enemy_speed))
                self.alien_timer = timer_reset
        elif self.alien_timer > 0:
            self.alien_timer -= 1
    
    def asteroid_spawn(self, chance: int, asteroid_timer_reset: int):
        if self.ast_timer <= 0 and ri(0, 100) <= chance:
            self.asteroids.add(Asteroid("sprites/asteroid.png", (100, 100), (ri(0, self.width - 100), -150), 3))
            self.ast_timer = asteroid_timer_reset
        elif self.ast_timer > 0:
            self.ast_timer -= 1