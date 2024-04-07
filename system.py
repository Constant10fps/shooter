from shooter_modules import *
# The `System` class in Python manages game elements such as window parameters, health, counters,
# cooldowns, sprite groups, collision checks, random enemy spawns, and player actions.

class System():
    """
    Basic checking operations and spawning processes. 
    
    Window object required to run.
    """
    def __init__(self, window: Surface):
        # window params
        self.window: Surface = window
        self.width: int = 1200
        self.height: int = 720
        # health related 
        self.hp: int = 100
        self.boss_hp: int = 200
        # counters
        self.killcount: int = 0
        self.lost_count: int = 0
        # cooldowns
        self.alien_timer: int = 150
        self.ast_timer: int = 150
        self.restart_timer: int = 250
        self.fire_cooldown: int = 30
        # groups for sprites
        self.bullets: sprite.Group[Bullet] = sprite.Group()
        self.aliens: sprite.Group[Alien] = sprite.Group()
        self.asteroids: sprite.Group[Asteroid] = sprite.Group()
        self.boss_bullets: sprite.Group[Bullet] = sprite.Group()
        # boss
        self.boss = Boss("sprites/alien.png", (360, 240), (self.width//2, 10), 5)
    
    # Checking functions
    # ----Aliens check
    def alien_check(self, player: Player):
        if sprite.spritecollide(player, self.aliens, True):
            self.hp -= 20
        for alien in filter(lambda alien: alien.rect.y > self.height + 200, self.aliens):
            alien.kill()
            self.lost_count += 1
            self.hp -= 10
        self.aliens.draw(self.window)
        self.aliens.update()
    # ----Player's bullets check
    def bullets_check(self):
        if sprite.groupcollide(self.bullets, self.aliens, True, True):
            self.killcount += 1
        for bullet in filter(lambda bullet: bullet.rect.y <= -bullet.height, self.bullets):
            bullet.kill()
        self.bullets.draw(self.window)
        self.bullets.update()
    # ----Boss' bullets check
    def boss_bullets_check(self, player: Player):
        for bullet in filter(lambda b: b.rect.y > self.height + b.height, self.boss_bullets):
            bullet.kill()
        if sprite.spritecollide(player, self.boss_bullets, True):
            self.hp -= 15
        if sprite.spritecollide(self.boss, self.bullets, True):
            self.boss_hp -= 10
        self.boss_bullets.draw(self.window)
        self.boss_bullets.update()
    # ----Player's actions check
    def player_check(self, keys, player: Player):
        if self.fire_cooldown == 0 and (keys[K_w] or keys[K_SPACE] or keys[K_UP]):
            player.fire(self.bullets)
            self.fire_cooldown = 25
        elif self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        player.show(self.window)
        player.update()
    
    # Spawning functions
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
    
    def reset(self):
        # variable reset
        self.boss.rect.x = self.width//2
        self.boss.rect.y = 10
        self.boss_hp = 200
        self.hp = 100
        self.killcount = 0
        self.lost_count = 0
        self.hp = 100
        # groups cleanup
        self.bullets.empty()
        self.aliens.empty()
        self.boss_bullets.empty()