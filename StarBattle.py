import pygame, sys, time, random
from pygame import mixer

pygame.mixer.pre_init(43000, -16, 1, 512)
mixer.init()

#Sounds
hit = pygame.mixer.Sound("sound/hit.ogg")
start_hit = pygame.mixer.Sound("sound/vustrel.ogg")
take_shots_sound = pygame.mixer.Sound("sound/ammon_sound.ogg")
take_healls_sound = pygame.mixer.Sound("sound/healls.ogg")
met_hit_sound = pygame.mixer.Sound("sound/meteorit_sound.ogg")
###

#Create window
wind_width = 500
wind_hieght = 600

window = pygame.display.set_mode((wind_width, wind_hieght))
pygame.display.set_caption("StarBattle")
pygame.display.set_icon(pygame.image.load("icon.ico"))
###

#Create screen
screen_width = wind_width
screen_hieght = wind_hieght
screen = pygame.Surface((screen_width, screen_hieght))
###

#Create info string
info_string_widht = wind_width
info_string_hight = wind_hieght/100*13
info_string = pygame.Surface((info_string_widht, info_string_hight))
game_start_first = True

# text of info string
pygame.font.init()
hells_of_hero = pygame.font.Font("Font.ttf", 32)
bullets_of_hero = pygame.font.Font("Font.ttf", 32)
hells_of_enemy1 = pygame.font.Font("Font.ttf", 25)
hells_of_enemy2 = pygame.font.Font("Font.ttf", 25)
win_or_lose = pygame.font.Font("Font.ttf", 32)
win_or_lose_font = False
###

###
#Collors
gray = (50, 50, 50)
blue = (0, 0, 100)
red = (210, 0, 0)
light_blue = (0, 255, 255)
wight_blue = (150, 150, 200)
###
class Sprite:
    def __init__(self,xpost,ypost,filename):
        self.x = xpost
        self.y = ypost
        self.bitmap = pygame.image.load(filename)
        self.bitmap.set_colorkey((255,255,255))
    def render(self):
        screen.blit(self.bitmap,(self.x, self.y))
def intersect(x1, x2, y1, y2, db1, db2):
    if (x1 > x2 - db1) and (x1 < x2 + db2) and (y1 > y2 - db1) and (y1 < y2 + db2):
        return 1
    else:
        return 0
def intersect2(x1, x2, dbl1, dbl2):
    if (x1 > x2 - dbl1) and (x1 < x2 + dbl2):
        return 1
    else:
        return 0

#-----------------hero-----------#
hero_min_x = screen_width / 100 * (-1.2)
hero_max_x = screen_width / 100 * 83.4
hero_min_y = screen_hieght / 100 * 47
hero_max_y = screen_hieght / 100 * 85
hero_can_move = True
hero_x = screen_width / 100 * 40
hero_y = screen_hieght / 100 * 60
hero = Sprite(hero_x, hero_y, "image\h.png")
hero_hells = 1
bullets = 25
winORlose = ""
def hero_move():
    if hero_can_move == True:
        if e.type == pygame.MOUSEMOTION:
            m = pygame.mouse.get_pos()
            hero.x = m[0] - 45
            hero.y = m[1] - 30
    if hero.y < hero_min_y:
        hero.y = hero_min_y+1
    if hero.x < hero_min_x:
        hero.x = hero_min_x+1
    if hero.x > hero_max_x:
        hero.x = hero_max_x-1
    if hero.y > hero_max_y:
        hero.y = hero_max_y-1
#--------------------------------#

#-----------------enemy1-------------#
emeny_x = 0
emeny_y = wind_hieght/100*11.6
max_speed1 = 4
min_speed1 = 1
enemy1_condition = "image\e.png"
speed = 2
enemy = Sprite(emeny_x, emeny_y, enemy1_condition)
can_enemy_move = True
direction = ["right","left"]
move_direction = direction[0]
moving_enemy_timer = 0
enemy1_hells = 1
hit_anim_enemy_active = False
enemy_hit = False
def conditions_for_enemy1():
    global enemy1_condition
    global enemy
    if enemy1_hells == 10:
        enemy1_condition = "image\e.png"
    if enemy1_hells == 9:
         enemy1_condition = "image\e_b1.png"
    if enemy1_hells == 8:
         enemy1_condition = "image\e_b1.png"
    if enemy1_hells == 7:
        enemy1_condition = "image\e_b2.png"
    if enemy1_hells == 6:
        enemy1_condition = "image\e_b2.png"
    if enemy1_hells == 5:
        enemy1_condition = "image\e_b3.png"
    if enemy1_hells == 4:
        enemy1_condition = "image\e_b3.png"
    if enemy1_hells == 3:
        enemy1_condition = "image\e_b4.png"
    if enemy1_hells == 2:
        enemy1_condition = "image\e_b4.png"
    if enemy1_hells == 1:
        enemy1_condition = "image\e_b5.png"
    if enemy1_hells == 0:
        enemy1_condition = "image\e_b6.png"
    if hit_anim_enemy_active == False:
        enemy = Sprite(enemy.x, enemy.y, enemy1_condition)
def emeny1_move():
    global move_direction
    global enemy1_push
    if move_direction == direction[0] and can_enemy_move == True:
        enemy.x += speed
        if enemy.x > wind_width-90:
            move_direction = direction[1]
    if move_direction == direction[1] and can_enemy_move == True:
        enemy.x -= speed
        if enemy.x < 0 and can_enemy_move == True:
            move_direction = direction[0]
    return move_direction
def random_speed_for_enemy_1():
    global moving_enemy_timer
    global speed
    moving_enemy_timer += 1
    for i in range(2):
        if moving_enemy_timer > 500:
            if can_enemy_move == True:
                speed = random.randint(int(min_speed1), int(max_speed1))
                moving_enemy_timer = 0
def enemy1_live():
    global enemy1_hells
    global can_enemy_move
    global can_enemy_push

    if enemy1_hells == 0:
        can_enemy_move = False
        can_enemy_push = False
        enemy.y += 1
        if enemy.y > wind_hieght:
            enemy.x = -50
def hit_enemy1_anim():
    global can_enemy_move
    global can_enemy_push
    global can_hero_push
    global hit_anim_enemy_active
    global hit_anim_timer
    global enemy
    global enemy_hit
    if enemy_hit == True:
        hit_anim_timer += 1
        can_enemy_move = False
        can_hero_push = False
        can_enemy_push = False
        hit_anim_enemy_active = True
        if hit_anim_timer == 1:
            enemy = Sprite(enemy.x, enemy.y, "image\empty.png")
        if hit_anim_timer == 100:
            enemy = Sprite(enemy.x, enemy.y, enemy1_condition)
        if hit_anim_timer == 200:
            enemy = Sprite(enemy.x, enemy.y, "image\empty.png")
        if hit_anim_timer == 300:
            enemy = Sprite(enemy.x, enemy.y, enemy1_condition)
            hit_anim_enemy_active = False
            hit_anim_timer = 0
        if hit_anim_enemy_active == False:
            can_enemy_move = True
            can_hero_push = True
            can_enemy_push = True
            enemy_hit = False
#----------------------------------------#

#-----------------enemy2-------------#
emeny2_x = wind_width -60
emeny2_y = wind_hieght/100*11.6
max_speed2 = 4
min_speed2 = 1
enemy2_condition = "image\e.png"
speed2 = 2
enemy2 = Sprite (emeny2_x, emeny2_y, enemy2_condition)
can_enemy2_move = True
direction2 = ["right","left"]
move_direction2 = direction2[1]
moving_enemy_timer2 = 0
enemy2_hells = 1
hit_anim_enemy2_active = False
enemy2_hit = False
def emeny2_move():
    global move_direction2
    if move_direction2 == direction2[1] and can_enemy2_move == True:
        enemy2.x -= speed2
        if enemy2.x < 0:
            move_direction2 = direction2[0]
    if move_direction2 == direction2[0] and can_enemy2_move == True:
        enemy2.x += speed2
        if enemy2.x > wind_width - 90 and can_enemy2_move == True:
            move_direction2 = direction2[1]
    return move_direction2
def random_speed_for_enemy_2():
    global moving_enemy_timer2
    global speed2
    moving_enemy_timer2 += 1
    for i in range(2):
        if moving_enemy_timer2 > 500:
            if can_enemy2_move == True:
                speed2 = random.randint(int(min_speed1), int(max_speed1))
                moving_enemy_timer2 = 0
def enemy2_live():
    global enemy2_hells
    global can_enemy2_move
    global can_enemy2_push

    if enemy2_hells == 0:
        can_enemy2_move = False
        can_enemy2_push = False
        enemy2.y += 1
        if enemy2.y > wind_hieght:
            enemy2.x = -50
def conditions_for_enemy2():
    global enemy2_condition
    global enemy2
    if enemy2_hells == 10:
        enemy2_condition = "image\e.png"
    if enemy2_hells == 9:
        enemy2_condition = "image\e_b1.png"
    if enemy2_hells == 8:
        enemy2_condition = "image\e_b1.png"
    if enemy2_hells == 7:
        enemy2_condition = "image\e_b2.png"
    if enemy2_hells == 6:
        enemy2_condition = "image\e_b2.png"
    if enemy2_hells == 5:
        enemy2_condition = "image\e_b3.png"
    if enemy2_hells == 4:
        enemy2_condition = "image\e_b3.png"
    if enemy2_hells == 3:
        enemy2_condition = "image\e_b4.png"
    if enemy2_hells == 2:
        enemy2_condition = "image\e_b4.png"
    if enemy2_hells == 1:
        enemy2_condition = "image\e_b5.png"
    if enemy2_hells == 0:
        enemy2_condition = "image\e_b6.png"
    if hit_anim_enemy2_active == False:
        enemy2 = Sprite(enemy2.x, enemy2.y, enemy2_condition)
def hit_enemy2_anim():
    global can_enemy2_move
    global can_enemy2_push
    global can_hero_push
    global hit_anim_enemy2_active
    global hit_anim_timer2
    global enemy2
    global enemy2_hit
    if enemy2_hit == True:
        hit_anim_timer2 += 1
        can_enemy2_move = False
        can_hero_push = False
        can_enemy2_push = False
        hit_anim_enemy2_active = True
        if hit_anim_timer2 == 1:
            enemy2 = Sprite(enemy2.x, enemy2.y, "image\empty.png")
        if hit_anim_timer2 == 100:
            enemy2 = Sprite(enemy2.x, enemy2.y, enemy2_condition)
        if hit_anim_timer2 == 200:
            enemy2 = Sprite(enemy2.x, enemy2.y, "image\empty.png")
        if hit_anim_timer2 == 300:
            enemy2 = Sprite(enemy2.x, enemy2.y, enemy2_condition)
            hit_anim_enemy2_active = False
            hit_anim_timer2 = 0
        if hit_anim_enemy2_active == False:
            can_enemy2_move = True
            can_hero_push = True
            can_enemy2_push = True
            enemy2_hit = False
#----------------------------------------#

#--------------hero_bullet-------------#
hb_x = wind_width - 1000
hb_y = wind_hieght - 1000
h_b = Sprite(hb_x, 410, "image\shot1.png")
h_b.push = False
can_hero_push = True
def hb_move():
    global can_hero_push
    global enemy1_hells
    global enemy2_hells
    global bullets
    global hit_anim_enemy_active
    global enemy_hit
    global enemy2_hit
    if e.type == pygame.MOUSEBUTTONDOWN:
        if e.button == 1:
            if hero_can_move == True and can_hero_push and bullets >= 1:
                bullets -= 1
                h_b.x = hero.x + 36
                h_b.y = hero.y - 20
                h_b.push = True
                start_hit.play()
    if h_b.push == True:
         h_b.y -= 1
         can_hero_push = False
    if h_b.y == 0:
        h_b.push = False
        can_hero_push = True
    if intersect(h_b.x, enemy.x, h_b.y, enemy.y, 20, 70):
        h_b.push = False
        can_hero_push = True
        h_b.y = 6000
        enemy1_hells -= 1
        hit.play()
        enemy_hit = True
    if intersect(h_b.x, enemy2.x, h_b.y, enemy2.y, 20, 70):
        h_b.push = False
        can_hero_push = True
        h_b.y = 6000
        enemy2_hells -= 1
        enemy2_hit = True
        hit.play()
#--------------------------------------#

#--------------enemy1_bullet-------------#
eb_x = wind_width - 100
eb_y = wind_hieght - 100
e_b1 = Sprite(hb_x, 410, "image\shot2.png")
e_b1.push = False
e_b1.speed = 2
can_enemy_push = True
enemy1_push = False
#--------------------------------------#

#--------------enemy2_bullet-------------#
eb2_x = wind_width - 100
eb2_y = wind_hieght - 100
e_b2 = Sprite(hb_x, 410, "image\shot3.png")
e_b2.push = False
e_b2.speed = 2
can_enemy2_push = True
enemy2_push = False
#--------------------------------------#

#Loot
loot_x = -50
loot_y = -50
healls_loot = Sprite(loot_x, loot_y, "image\heals.png")
bullets_loot = Sprite(loot_x, loot_y, "image\shots.png")
loot = 0
loot_spawned = False
spawn_time = 100
need_spawn_timer = True
def take_loot():
    global hero_hells, loot_spawn_timer, need_spawn_timer, loot, bullets, loot_spawned, can_hero_push
    if intersect(hero.x, healls_loot.x, hero.y, healls_loot.y, 90, 45):
        hero_hells += 1
        healls_loot.x = loot_x
        healls_loot.y = loot_y
        loot_spawn_timer = 0
        need_spawn_timer = True
        loot_spawned = False
        loot = 0
        take_healls_sound.play()
    if intersect(h_b.x, healls_loot.x, h_b.y, healls_loot.y, 20, 45):
        hero_hells += 1
        healls_loot.x = loot_x
        healls_loot.y = loot_y
        loot_spawn_timer = 0
        need_spawn_timer = True
        loot_spawned = False
        loot = 0
        h_b.push = False
        can_hero_push = True
        h_b.y = 6000
    if intersect(hero.x, bullets_loot.x, hero.y, bullets_loot.y, 90, 45):
        bullets += 3
        bullets_loot.x = loot_x
        bullets_loot.y = loot_y
        loot_spawn_timer = 0
        need_spawn_timer = True
        loot_spawned = False
        loot = 0
        take_shots_sound.play()
    if intersect(h_b.x, bullets_loot.x, h_b.y, bullets_loot.y, 20, 45):
        bullets += 3
        bullets_loot.x = loot_x
        bullets_loot.y = loot_y
        loot_spawn_timer = 0
        need_spawn_timer = True
        loot_spawned = False
        loot = 0
        h_b.push = False
        can_hero_push = True
        h_b.y = 6000
        take_shots_sound.play()
def spawn_loot():
    global healls_loot, bullets_loot, loot, loot_spawned, loot_spawn_timer, spawn_time, need_spawn_timer
    loot_spawn_timer += 1
    if need_spawn_timer == True:
        spawn_time = random.randint(2000, 3000)
        need_spawn_timer = False
    if loot_spawned == False and loot_spawn_timer == spawn_time:
        loot = random.randint(1, 2)
    if loot == 1 and loot_spawned == False:
        loot_spawned = True
        bullets_loot.x = random.randint(screen_width/100*10, screen_width/100*90)
        bullets_loot.y = random.randint(screen_hieght/100*50, screen_width/100*90)
    if loot == 2 and loot_spawned == False:
        loot_spawned = True
        healls_loot.x = random.randint(screen_width/100*10, screen_width/100*90)
        healls_loot.y = random.randint(screen_hieght/100*50, screen_hieght/100*90)
###

#timers
win_or_lose_timer = 0
hit_anim_timer = 0
hit_anim_timer2 = 0
loot_spawn_timer = 0
fly_met_time = 0
fly_met_timer = 0
###

#------Meteorite-------#
met_start_point_x = -50
met_start_point_y = -50
need_met_time = True
need_fly_met_timer = True
met_fly = False

meteorite = Sprite(met_start_point_x, met_start_point_y, "image\meteorit.png")
def met_move():
    global fly_met_time, need_met_time, fly_met_timer, need_fly_met_timer, met_fly
    if need_met_time == True:
        fly_met_time = random.randint(500, 1000)
        need_met_time = False
    if need_fly_met_timer == True:
        fly_met_timer += 1
    if fly_met_timer == fly_met_time:
        meteorite.y = random.randint(100, 200)
        meteorite.x = wind_width
        need_fly_met_timer = False
        fly_met_timer = 0
        met_fly = True
    if met_fly == True:
        meteorite.x -= 3
        meteorite.y += 3
    if meteorite.y > wind_hieght:
        met_fly = False
        need_met_time = True
        need_fly_met_timer = True
        meteorite.x = met_start_point_x
        meteorite.y = met_start_point_y
def met_hit_hero():
    global fly_met_time, need_met_time, fly_met_timer, need_fly_met_timer, met_fly, hero_hells
    if intersect(hero.x, meteorite.x, hero.y, meteorite.y, 90, 60):
        met_fly = False
        need_met_time = True
        need_fly_met_timer = True
        meteorite.x = met_start_point_x
        meteorite.y = met_start_point_y
        hero_hells -= 5
        met_hit_sound.play()
###


game_start = False
def enemys_push():
    global enemy1_push
    global enemy2_push
    global can_enemy_push
    global can_enemy2_push
    global hero_hells
# first enemy bullets
    if intersect2(enemy.x, hero.x, 10, 10) == True:
        if e_b1.push == False:
            e_b1.push = True
    if e_b1.push == True and can_enemy_push == True:
        e_b1.x = enemy.x + 36
        e_b1.y = enemy.y + 36
        can_enemy_push = False
        enemy1_push = True
        start_hit.play()
    if enemy1_push == True:
        e_b1.y += e_b1.speed
    if e_b1.y > screen_hieght:
        enemy1_push = False
        e_b1.push = False
        can_enemy_push = True
        e_b1.y = eb_y
        e_b1.x = 5000
    if intersect(e_b1.x, hero.x, e_b1.y, hero.y, 20, 60):
        enemy1_push = False
        e_b1.push = False
        can_enemy_push = True
        e_b1.y = eb_y
        e_b1.x = 5000
        hero_hells -= 1
        hit.play()
# second enemy bullets
    if intersect2(enemy2.x, hero.x, 10, 10) == True:
        if e_b2.push == False:
            e_b2.push = True
    if e_b2.push == True and can_enemy2_push == True:
        e_b2.x = enemy2.x + 36
        e_b2.y = enemy2.y + 36
        can_enemy2_push = False
        enemy2_push = True
        start_hit.play()
    if enemy2_push == True:
        e_b2.y += e_b2.speed
    if e_b2.y > screen_hieght:
        enemy2_push = False
        e_b2.push = False
        can_enemy2_push = True
        e_b2.y = eb2_y
        e_b2.x = 5000
    if intersect(e_b2.x, hero.x, e_b2.y, hero.y, 20, 60):
        enemy2_push = False
        e_b2.push = False
        can_enemy2_push = True
        e_b2.y = eb2_y
        e_b2.x = 5000
        hero_hells -= 1
        hit.play()

#----------------------------------MENU-----------------------------------------------#
def menu_buttons():
    global menu_start, game_start, game_play, win_or_lose_font
    if e.type == pygame.MOUSEBUTTONDOWN:
        if intersect(m_x, exit_button_position_x, m_y, exit_button_position_y, mouse_menu_width, exit_button_width) == True:
            sys.exit()
        if intersect(m_x, play_button_position_x, m_y, play_button_position_y, mouse_menu_width, play_button_width) == True:
            menu_start = False
            game_start = True
            game_play = True
            game_options()
            win_or_lose_font = False

def mouse_move():
    global m_x
    global m_y
    if e.type == pygame.MOUSEMOTION:
        m = pygame.mouse.get_pos()
        m_x = m[0] - 25
        m_y = m[1] - 25

m_x = 0
m_y = 0

#####
screen_menu_width = wind_width
screen_menu_hieght = wind_hieght

screen_menu = pygame.image.load("image\menu_screen.jpg")
screen_menu = pygame.transform.scale(screen_menu, (screen_width, screen_menu_hieght))
#####

#####
play_button_width = wind_width/100*37.5
play_button_hieght = wind_hieght/100*12.4

play_button_position_x = wind_width/100*32.5
play_button_position_y = wind_hieght/100*43.5

play_button = pygame.image.load("image\play.png")
play_button = pygame.transform.scale(play_button, (int(play_button_width), int(play_button_hieght)))
#####

#####
exit_button_width = wind_width/100*37.5
exit_button_hieght = wind_hieght/100*12.4

exit_button_position_x = wind_width / 100 * 32.5
exit_button_position_y = wind_hieght / 100 * 70.4

exit_button = pygame.image.load("image\Exit.png")
exit_button = pygame.transform.scale(exit_button, (int(exit_button_width), int(exit_button_hieght)))
#####

#####
mouse_menu_width = 50
mouse_menu_hieght = 50

mouse_menu = pygame.image.load("image\empty.png")
mouse_menu = pygame.transform.scale(mouse_menu, (int(mouse_menu_width), int(mouse_menu_hieght)))
#####


menu_start = True

def game_options():
    global enemy1_hells, enemy2_hells, enemy2_condition, enemy1_condition, hero_hells, bullets, win_or_lose_timer
    enemy1_hells = enemy2_hells = hero_hells = 10
    enemy1_condition = enemy2_condition = "image\e.png"
    bullets = 25
    win_or_lose_timer = 0
while menu_start == True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = False
            sys.exit()

    mouse_move()
    menu_buttons()

    screen_menu.blit(exit_button, (int(exit_button_position_x), int(exit_button_position_y)))
    screen_menu.blit(play_button, (int(play_button_position_x), int(play_button_position_y)))
    window.blit(screen_menu, (0, 0))
    screen_menu.blit(mouse_menu, (m_x, m_y))
    pygame.display.flip()
    pygame.display.update()
    pygame.time.delay(60)
def menu():
    global done
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = False
            sys.exit()

    mouse_move()
    menu_buttons()
    pygame.mouse.set_visible(True)
    screen_menu.blit(exit_button, (int(exit_button_position_x), int(exit_button_position_y)))
    screen_menu.blit(play_button, (int(play_button_position_x), int(play_button_position_y)))
    window.blit(screen_menu, (0, 0))
    screen_menu.blit(mouse_menu, (m_x, m_y))
    pygame.display.flip()
    pygame.display.update()
    pygame.time.delay(60)
#-------------------------------------------------------------------------------------#

def lose():
    global winORlose, game_play
    global win_or_lose_timer
    global win_or_lose_font
    if hero_hells == 0 or hero_hells < 1:
        win_or_lose_timer += 1
        winORlose = "Ты проиграл!"
        if win_or_lose_timer == 10:
            time.sleep(5)
            menu()
            game_play = False
        win_or_lose_font = True
    if enemy1_hells <= 0 and enemy2_hells <= 0:
        win_or_lose_timer += 1
        winORlose = "Ты виграл!"
        if win_or_lose_timer == 10:
            time.sleep(5)
            menu()
            game_play = False
        win_or_lose_font = True
    if game_play == False:
        menu()

def join_in_menu():
    global game_play
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        menu()
        game_play = False
def game():
    global game_start_first
    global wind_hieght
    if game_start_first == True:
        game_start_first = False
        wind_hieght += info_string_hight
def drow():
    screen.fill(gray)
    hero.render()
    enemy.render()
    enemy2.render()
    healls_loot.render()
    bullets_loot.render()
    h_b.render()
    meteorite.render()
    e_b1.render()
    e_b2.render()
    info_string.fill(blue)
    #render text
    if win_or_lose_font == False:
        info_string.blit(hells_of_hero.render("Жизни: " + str(hero_hells), 1, red), (screen_width/100*69, screen_hieght/100*0.70))
        info_string.blit(bullets_of_hero.render(u"ПУЛИ: " + str(bullets), 1, light_blue), (screen_width/100*1, screen_hieght/100*0.83))
        info_string.blit(hells_of_enemy1.render(u"Враг 1: " + str(enemy1_hells) + "/10", 1, wight_blue), (screen_width/100*1, screen_hieght/100*8))
        info_string.blit(hells_of_enemy1.render(u"Враг 2: " + str(enemy2_hells) + "/10", 1, wight_blue),(screen_width/100*68, screen_hieght / 100 * 8))
    if win_or_lose_font == True:
        info_string.blit(win_or_lose.render(winORlose, 1, red), (screen_width/100*35, screen_hieght/100*0.50))
    ###
    window.blit(screen, (0, 0))
    window.blit(info_string, (0, 0))
    pygame.mouse.set_visible(False)
    pygame.display.flip()
while game_start:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
    join_in_menu()
    lose()
    game()
    if game_play == True:
        met_hit_hero()
        met_move()
        take_loot()
        spawn_loot()
        hit_enemy2_anim()
        hit_enemy1_anim()
        enemy2_live()
        enemy1_live()
        emeny1_move()
        emeny2_move()
        conditions_for_enemy1()
        conditions_for_enemy2()
        random_speed_for_enemy_1()
        enemys_push()
        hb_move()
        hero_move()
        drow()
    pygame.time.delay(5)