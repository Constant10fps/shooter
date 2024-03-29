#~~~~~~~Import~~~~~~~~#
from random import randint as ri
from shooter_modules import *
from pygame import *
#~~~~~Background~~~~~~#
winWidth = 1200
winHeight = 900
window = display.set_mode((winWidth, winHeight)) # Setting the size
display.set_caption("Sʜᴏᴏᴛᴇʀ", "alien.png") # Name of the window
background = transform.scale(image.load("spritePictures/skybox.jpg"), (winWidth, winHeight)) # background
# System Object
system = System(window)

#~~~~~~~~Music~~~~~~~~#
mixer.init()
mixer.music.load("-Electroman-Adventures-.mp3")

mixer.music.play(loops=-1)
mixer.music.set_volume(0)
#~~~~~~~Variables~~~~~~~#
fire_cooldown: int = 0
timer: int = 60
killcount: int = 0
lost_count = 0
restart_timer = 250
# Sprites
boss = Boss("spritePictures/alien.png", (360, 240), (winWidth//2, 10), 5)
player = Player("spritePictures/spaceship.png", (150, 150), (winWidth // 2, winHeight - 150), 10)
shield = Shield("spritePictures/shield.png", (200, 200), ((winWidth // 2) - 25, winHeight - 175), 10)
health_bar = HealthBar(winWidth - 530, 20, 500, 35, 100)

#~~Text displays~~#
font.init()
stats = font.Font("stats.ttf", 30)
saiba_small = font.Font("saiba.otf", 50)
saiba = font.Font("saiba.otf", 100)
# god this is awful
logo = saiba.render("COSMIC BATTLE", True, (0, 255, 51))
start = saiba_small.render("PRESS ENTER TO START", True, (0, 255, 51))

game_over = saiba.render("GAME OVER", True, (0, 255, 51))
restart = saiba_small.render("PRESS TAB TO RETURN TO MENU", True, (0, 255, 51))

#~~~~~Game phases~~~~~#
menu = True
lvl_play = False
lvl_1 = False
lvl_2 = False
lvl_boss = False
lvl_restart = False

#~~~~~~~~START~~~~~~~~#
game = True
clock = time.Clock()
while game:
    keys = key.get_pressed()
    window.blit(background, (0,0))
    if menu:
        system.random_spawn((-2, 2), 60, ri(3, 5))
        for alien in system.aliens:
            if alien.rect.y > winHeight:
                system.aliens.remove(alien)
        system.aliens.draw(window)
        system.aliens.update()
        
        window.blit(logo, (100, 200))
        window.blit(start, (100, 300))
        
        if key.get_pressed()[K_RETURN]:
            system.aliens.empty()
            lvl_play = True
            # Debug!
            lvl_boss = True
            menu = False
        elif key.get_pressed()[K_ESCAPE]:
            quit()
            break

    if lvl_play:
        # aliens lvl 1
        if lvl_1:
            system.random_spawn((-2, 2), 60, ri(3, 5))
            if killcount > 50:
                lvl_1 = False
                lvl_2 = True
        
        # aliens lvl 2
        if lvl_2:
            system.random_spawn((-1, 1), 50, ri(4, 5))
            if killcount > 150:
                lvl_2 = False
                lvl_boss = True
        
        # boss lvl with one enemy
        if lvl_boss:
            boss.show(window)
            boss.update(system.boss_bullets)
        
        system.asteroids.draw(window)
        system.asteroids.update()
        system.boss_bullets.draw(window)
        system.boss_bullets.update()
        system.collision_check(player)
        player.show(window)
        player.update(system.bullets)
        shield.show(window)
        shield.update(player)
        system.player_check(keys, player)
        
        # text rendering
        killcount_text = stats.render(f"Killcount: {system.killcount}", True, (0, 255, 51))
        lost_text = stats.render(f"Lost: {system.lost_count}", True, (0, 255, 51))
        window.blit(killcount_text, (10, 20))
        window.blit(lost_text, (10, 60))
        
        # health check
        health_bar.show(system.hp, window)
        if system.hp <= 0:
            lvl_restart = True
            lvl_play = False
        
    if lvl_restart:
        # draw all sprites
        system.collision_check(player)
        system.aliens.draw(window)
        system.aliens.update()
        window.blit(game_over, (315, 350))
        window.blit(killcount_text, (350, 460))
        window.blit(lost_text, (350, 500))
        
        # check for enter
        if not restart_timer:
            if keys[K_TAB]:
                restart_timer = 250
                system.killcount = 0
                system.lost_count = 0
                system.hp = 100
                
                system.bullets.empty()
                system.aliens.empty()
                
                lvl_restart = False
                menu = True
            window.blit(restart, (250, 600))
        elif restart_timer > 0:
            restart_timer -= 1
    display.update()
    clock.tick(60)
    for e in event.get():
        if e.type == QUIT:
            game = False