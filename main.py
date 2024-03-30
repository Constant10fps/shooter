#~~~~~~~Import~~~~~~~~#
from system import *
#~~~~~Background~~~~~~#
winWidth = 1200
winHeight = 900
window = display.set_mode((winWidth, winHeight)) # Setting the size
display.set_caption("Sʜᴏᴏᴛᴇʀ") # Name of the window
background = transform.scale(image.load("sprites/skybox.jpg"), (winWidth, winHeight)) # background
# System Object
system = System(window)

#~~~~~~~~Music~~~~~~~~#
mixer.init()
mixer.music.load("sounds/-Electroman-Adventures-.mp3")

mixer.music.play(loops=-1)
mixer.music.set_volume(0)

#~~~~~~Variables~~~~~~#
fire_cooldown: int = 0
timer: int = 60
# Sprites
player = Player("sprites/spaceship.png", (150, 150), (winWidth // 2, winHeight - 150), 7)
shield = Shield("sprites/shield.png", (200, 200), ((winWidth // 2) - 25, winHeight - 175), 7)
health_bar = HealthBar(winWidth - 530, 20, 500, 35, 100)

#~~~~Text displays~~~~#
font.init()
# fonts 
stats = font.Font("fonts/stats.ttf", 30)
saiba_small = font.Font("fonts/saiba.otf", 50)
saiba = font.Font("fonts/saiba.otf", 100)
# small font render
restart = saiba_small.render("PRESS TAB TO RETURN TO MENU", True, (0, 255, 51))
start = saiba_small.render("PRESS ENTER TO START", True, (0, 255, 51))
# normal font render
logo = saiba.render("COSMIC BATTLE", True, (0, 255, 51))
game_over = saiba.render("GAME OVER", True, (0, 255, 51))
win = saiba.render("YOU WIN!", True, (0, 255, 51))

#~~~~~Game phases~~~~~#
# Active phases
lvl_play = False
lvl_1 = False
lvl_2 = False
lvl_boss = False
# Static phases
menu = True
lvl_restart = False
lvl_win = False

#~~~~~~~~START~~~~~~~~#
game = True
clock = time.Clock()
while game:
    keys = key.get_pressed()
    window.blit(background, (0,0))
    if menu:
        system.alien_spawn(15, 80)
        system.alien_check(player)
        
        window.blit(logo, (100, 200))
        window.blit(start, (100, 300))
        
        if keys[K_RETURN]:
            system.reset()
            lvl_play = True
            lvl_boss = True
            menu = False
        elif keys[K_ESCAPE]:
            quit()
            break
    
    if lvl_play:
        # aliens lvl 1
        if lvl_1:
            system.alien_spawn(20, 60)
            system.asteroid_spawn(15, 100)
            if system.killcount > 50:
                lvl_1 = False
                lvl_2 = True
        
        # aliens lvl 2
        if lvl_2:
            system.alien_spawn(33, 50)
            system.asteroid_spawn(18, 90)
            if system.killcount > 100:
                lvl_2 = False
                lvl_boss = True
        
        system.asteroids.draw(window)
        system.asteroids.update()
        
        # boss lvl with one enemy
        if lvl_boss:
            system.boss.show(window)
            system.boss.update(system.boss_bullets)
            system.boss_bullets_check(player)
            system.asteroid_spawn(17, 100)
            if system.boss_hp < 0:
                lvl_win = True
                lvl_play = False
                lvl_boss = False
        
        system.alien_check(player)
        system.bullets_check()
        system.boss_bullets_check(player)
        system.player_check(keys, player)
        player.show(window)
        player.update()
        shield.show(window)
        shield.update(player)
        
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
        system.alien_check(player)
        system.asteroids.draw(window)
        system.asteroids.update()
        # text
        window.blit(game_over, (315, 350))
        window.blit(killcount_text, (350, 460))
        window.blit(lost_text, (350, 500))
        
        # await for tab
        if system.restart_timer <= 0:
            window.blit(restart, (250, 600))
            if keys[K_TAB]:
                system.reset()
                lvl_restart = False
                menu = True
        else:
            system.restart_timer -= 1
    if lvl_win:
        window.blit(win, (winWidth//2, winHeight // 2.5))
        window.blit(restart, (250, 600))
        if keys[K_TAB]:
            system.reset()
            lvl_win = False
            menu = True
    
    display.update()
    clock.tick(60)
    for e in event.get():
        if e.type == QUIT:
            game = False