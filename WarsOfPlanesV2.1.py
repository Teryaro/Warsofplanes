import pygame
import random
import os
import time

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 480
HEIGHT = 700
FPS = 120

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('飞机大战')
clock = pygame.time.Clock()

# 图片
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
player_img = pygame.image.load(os.path.join(img_folder, 'me1.png'))
player_life_img = pygame.image.load(os.path.join(img_folder, 'life.png'))
pause_img = pygame.image.load(os.path.join(img_folder, 'pause_nor.png'))
pausep_img = pygame.image.load(os.path.join(img_folder, 'pause_pressed.png'))
bomb_img = pygame.image.load(os.path.join(img_folder, 'bomb.png'))
restart_img = pygame.image.load(os.path.join(img_folder, 'resume_nor.png'))
speed_level_img = pygame.image.load(os.path.join(img_folder, 'speed_level.png'))
power_level_img = pygame.image.load(os.path.join(img_folder, 'power_level.png'))

Mob_img1 = 'enemy1.png'
Mob_img2 = 'enemy2.png'
Mob_img3 = 'enemy3.png'
Bullet_mob_img = pygame.image.load(os.path.join(img_folder, 'bullet1.png'))
Bullet_img = pygame.image.load(os.path.join(img_folder, 'bullet2.png'))
background_img = pygame.image.load(os.path.join(img_folder, 'background.png'))
background_rect = background_img.get_rect()

# 循环添加爆炸图片
explosion_anim = {'player': [], 'mob1': [], 'mob2': [], 'mob3': []}
for i in range(4):
    explosion_player = 'me_destroy_{}.png'.format(i + 1)
    playerimg = pygame.image.load(os.path.join(img_folder, explosion_player))
    explosion_anim['player'].append(playerimg)
    explosion_mob1 = 'enemy1_down{}.png'.format(i + 1)
    mob1 = pygame.image.load(os.path.join(img_folder, explosion_mob1))
    explosion_anim['mob1'].append(mob1)
    explosion_mob2 = 'enemy2_down{}.png'.format(i + 1)
    mob2 = pygame.image.load(os.path.join(img_folder, explosion_mob2))
    explosion_anim['mob2'].append(mob2)
    explosion_mob3 = 'enemy3_down{}.png'.format(i + 1)
    mob3 = pygame.image.load(os.path.join(img_folder, explosion_mob3))
    explosion_anim['mob3'].append(mob3)
# 添加
# 声音
snd_dir = os.path.join(game_folder, 'snd')
shoot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'pew.wav'))
expl_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'expl3.wav'))
pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.7)


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bomb_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 10
        self.rect.bottom = HEIGHT - 75


class Goods(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.goods_type = ''
        self.goods_img1 = 'speed.png'  # 射速
        self.goods_img2 = 'bullet_supply.png'  # 子弹
        self.goods_img3 = 'bomb_supply.png'  # 大炸弹
        self.goods_img4 = 'hp.png'  # 血量
        r = random.randint(0, 9)
        if r >= 0 and r <= 2:
            self.image = pygame.image.load(os.path.join(img_folder, self.goods_img1))
            self.goods_type = self.goods_img1
        elif r >= 3 and r <= 5:
            self.image = pygame.image.load(os.path.join(img_folder, self.goods_img2))
            self.goods_type = self.goods_img2  # 子弹
        elif r >= 6 and r <= 8:
            self.image = pygame.image.load(os.path.join(img_folder, self.goods_img3))
            self.goods_type = self.goods_img3  # 加大炸弹
        elif r == 9:
            self.image = pygame.image.load(os.path.join(img_folder, self.goods_img4))
            self.goods_type = self.goods_img4  # 加血量

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200, -150)
        self.speedy = random.randrange(1, 2)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.kill()


class Life(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_life_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 10
        self.rect.bottom = HEIGHT - 10


class Pause(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pause_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.rect.width - 10  #410
        self.rect.y = 20                #20


class Restart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = restart_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

class speed_level(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = speed_level_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = HEIGHT - 100


class power_level(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = power_level_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = HEIGHT - 50


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.lifes = 3
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.level = 1
        self.bomb_num = 1
        self.speed_level = 1
        self.speed = 20

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_w]:
            self.speedy = -4
        if keystate[pygame.K_s]:
            self.speedy = 4
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        self.speedx = 0
        self.speedy = 0

    def shoot(self):
        if self.level == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

        elif self.level == 2:
            bullet = Bullet(self.rect.centerx + 30, self.rect.top + 10)
            all_sprites.add(bullet)
            bullets.add(bullet)
            bullet2 = Bullet(self.rect.centerx - 30, self.rect.top + 10)
            all_sprites.add(bullet2)
            bullets.add(bullet2)

        elif self.level == 3:
            bullet = Bullet(self.rect.centerx + 30, self.rect.top + 10)
            all_sprites.add(bullet)
            bullets.add(bullet)
            bullet2 = Bullet(self.rect.centerx - 30, self.rect.top + 10)
            all_sprites.add(bullet2)
            bullets.add(bullet2)
            bullet3 = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet3)
            bullets.add(bullet3)

        elif self.level == 4:
            bullet = Bullet(self.rect.centerx + 30, self.rect.top + 10)
            all_sprites.add(bullet)
            bullets.add(bullet)
            bullet2 = Bullet(self.rect.centerx - 30, self.rect.top + 10)
            all_sprites.add(bullet2)
            bullets.add(bullet2)
            bullet3 = Bullet(self.rect.centerx + 15, self.rect.top + 5)
            all_sprites.add(bullet3)
            bullets.add(bullet3)
            bullet4 = Bullet(self.rect.centerx - 15, self.rect.top + 5)
            all_sprites.add(bullet4)
            bullets.add(bullet4)

        else:
            bullet = Bullet(self.rect.centerx + 30, self.rect.top + 10)
            all_sprites.add(bullet)
            bullets.add(bullet)
            bullet2 = Bullet(self.rect.centerx - 30, self.rect.top + 10)
            all_sprites.add(bullet2)
            bullets.add(bullet2)
            bullet3 = Bullet(self.rect.centerx + 15, self.rect.top + 5)
            all_sprites.add(bullet3)
            bullets.add(bullet3)
            bullet4 = Bullet(self.rect.centerx - 15, self.rect.top + 5)
            all_sprites.add(bullet4)
            bullets.add(bullet4)
            bullet5 = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet5)
            bullets.add(bullet5)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.mob_type = ''
        self.Mob_img1 = 'enemy1.png'
        self.Mob_img2 = 'enemy2.png'
        self.Mob_img3 = 'enemy3_n1.png'
        self.hp = 0
        r = random.randint(0, 9)
        if r >= 0 and r <= 5:
            self.image = pygame.image.load(os.path.join(img_folder, self.Mob_img1))
            self.mob_type = self.Mob_img1

        elif r <= 8:
            self.image = pygame.image.load(os.path.join(img_folder, self.Mob_img2))
            self.mob_type = self.Mob_img2
            self.hp = 1
        else:
            self.hp = 2
            self.image = pygame.image.load(os.path.join(img_folder, self.Mob_img3))
            self.mob_type = self.Mob_img3
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        w = self.rect.width / 2
        if self.rect.right > WIDTH + w or self.rect.left < -w:
            self.speedx = -self.speedx
        if self.rect.top > HEIGHT + 10:
            r = random.randint(0, 9)
            if r >= 0 and r <= 5:
                self.image = pygame.image.load(os.path.join(img_folder, self.Mob_img1))
                self.mob_type = self.Mob_img1
            elif r <= 8:
                self.image = pygame.image.load(os.path.join(img_folder, self.Mob_img2))
                self.mob_type = self.Mob_img2
            else:
                self.image = pygame.image.load(os.path.join(img_folder, self.Mob_img3))
                self.mob_type = self.Mob_img3
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-200, -150)
            self.speedy = random.randrange(1, 4)
            self.speedx = random.randrange(-3, 3)

    def shoot(self):
        bullet = Bullet_mob(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        bullets_mob.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Bullet_mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Bullet_mob_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def pause_ui(score, now_str):
    draw_text(screen, "Pause!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Score:" + str(score), 22, WIDTH / 2, HEIGHT / 4 + 70)
    draw_text(screen, "Time:" + now_str, 22, WIDTH / 2, HEIGHT / 4 + 90)
    draw_text(screen, "Click on the J to continue the game", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_j:
                    waiting = False
                try:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                finally:
                    pass
def show_go_screen(score, now_str):
    screen.fill(WHITE)
    screen.blit(background_img, background_rect)
    draw_text(screen, "START!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Score:" + str(score), 22, WIDTH / 2, HEIGHT / 4 + 70)
    draw_text(screen, "Time:" + now_str, 22, WIDTH / 2, HEIGHT / 4 + 90)
    draw_text(screen, "W A S D keys move, Space to fire, key Z Cannonball", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Click on the J to start t he game", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    pygame.init()
    pygame.mixer.init()
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            pygame.init()
            pygame.mixer.init()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_j:
                    waiting = False
                try:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                finally:
                    pass

def creatmod():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
# 人物组
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
goods = pygame.sprite.Group()
player = Player()

all_sprites.add(player)
life = Life()
bomb = Bomb()
pause = Pause()
speed_le = speed_level()
power_le = power_level()
all_sprites.add(pause)
all_sprites.add(life)
all_sprites.add(bomb)
all_sprites.add(speed_le)
all_sprites.add(power_le)
bullets = pygame.sprite.Group()
bullets_mob = pygame.sprite.Group()
n = 4
for i in range(n):
    creatmod()
pygame.mixer.music.play(loops=-1)
running = True
game_over = True
count = 1
speed_mob = 100
score = 0
starttime = time.time()
now_str = '0s'
total_pause = 0

while running:
    if game_over:
        show_go_screen(score, now_str)
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        goods = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        life = Life()
        bomb = Bomb()
        pause = Pause()
        speed_le = speed_level()
        power_le = power_level()
        all_sprites.add(pause)
        all_sprites.add(life)
        all_sprites.add(bomb)
        all_sprites.add(speed_le)
        all_sprites.add(power_le)
        bullets = pygame.sprite.Group()
        bullets_mob = pygame.sprite.Group()
        starttime = time.time()
        n = 4
        for i in range(n):
            creatmod()
        pygame.mixer.music.play(loops=-1)  ###
        running = True
        count = 1
        speed_mob = 100
        total_pause = 0
    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x >= 410 and x <= 470:
                if y >= 20 and y <= 65:
                    pressed_array = pygame.mouse.get_pressed()
                    for index in range(len(pressed_array)):
                        if pressed_array[index]:
                            if index == 0:
                                pause_time = time.time()
                                pause_ui(score, now_str)
                                total_pause += int(round(time.time() * 1000)) - int(round(pause_time * 1000))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_ui(score, now_str)
            elif event.key == pygame.K_z:
                if player.bomb_num > 0:
                    player.bomb_num -= 1
                    for mob in mobs:
                        if mob.mob_type == 'enemy1.png':
                            score += 100
                            expl = Explosion(mob.rect.center, 'mob1')
                        elif mob.mob_type == 'enemy2.png':
                            score += 200
                            expl = Explosion(mob.rect.center, 'mob2')
                        elif mob.mob_type == 'enemy3_n1.png':
                            score += 300
                            expl = Explosion(mob.rect.center, 'mob3')
                        all_sprites.add(expl)
                        mob.kill()

                        creatmod()
                for bm in bullets_mob:
                    bm.kill()
    endtime = time.time()
    now = int(round(endtime * 1000)) - int(round(starttime * 1000)) - total_pause

    if now >= 20000 and n == 4:
        n += 1
        creatmod()
    elif now >= 50000 and n == 5:
        n += 1
        creatmod()
    elif now >= 80000 and n == 6:
        n += 1
        creatmod()
    elif now >= 120000 and n == 7:
        n += 1
        creatmod()
    elif now >= 180000 and n == 8:
        n += 1
        creatmod()
    elif now >= 240000 and n == 9:
        n += 1
        creatmod()
    elif now >= 300000 and n == 10:
        n += 1
        creatmod()
    elif now >= 360000 and n == 11:
        n += 1
        creatmod()
    elif now >= 420000 and n == 12:
        n += 1
        creatmod()
    r = random.randint(0, 99)
    r2 = random.randint(0, 9)
    if r == 0 and r2 == 1:
        good = Goods()
        goods.add(good)
        all_sprites.add(good)
    key_pressed = pygame.key.get_pressed()


    if count % player.speed == 0:
        if key_pressed[pygame.K_SPACE]:
            player.shoot()

    if count % speed_mob == 0:
        for mob in mobs:
            if mob.mob_type == 'enemy2.png':
                mob.shoot()
    all_sprites.update()
    screen.fill(WHITE)
    screen.blit(background_img, background_rect)

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_rect_ratio(0.7))
    for hit in hits:
        if player.lifes > 0:
            player.lifes -= 1
            creatmod()
        else:
            player_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(player_explosion)
            player.kill()
    if not player.alive() and not player_explosion.alive():
        game_over = True

    hits = pygame.sprite.spritecollide(player, bullets_mob, True, pygame.sprite.collide_rect_ratio(0.7))
    for hit in hits:
        if player.lifes > 0:
            player.lifes -= 1
        else:
            player_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(player_explosion)
            player.kill()
    if not player.alive() and not player_explosion.alive():
        game_over = True

    pygame.sprite.groupcollide(bullets, bullets_mob, True, True)

    hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for hit in hits:
        expl_sound.play()
        if hit.mob_type == 'enemy1.png':
            hit.kill()
            score += 100
            expl = Explosion(hit.rect.center, 'mob1')
            all_sprites.add(expl)
            creatmod()
        elif hit.mob_type == 'enemy2.png':
            if hit.hp >= 0:
                hit.hp -= 1
            else:
                hit.kill()
                score += 200
                expl = Explosion(hit.rect.center, 'mob2')
                all_sprites.add(expl)
                creatmod()
        elif hit.mob_type == 'enemy3_n1.png':
            if hit.hp >= 0:
                hit.hp -= 1
            else:
                hit.kill()
                score += 300
                expl = Explosion(hit.rect.center, 'mob3')
                all_sprites.add(expl)
                creatmod()

    hits = pygame.sprite.spritecollide(player, goods, True, pygame.sprite.collide_rect_ratio(0.7))
    for hit in hits:
        if hit.goods_type == 'speed.png':
            player.speed -= 2
            player.speed_level += 1
        if hit.goods_type == 'bullet_supply.png':
            if player.level < 5:
                player.level += 1
        if hit.goods_type == 'bomb_supply.png':
            player.bomb_num += 1  # 数量加1
        if hit.goods_type == 'hp.png':
            player.lifes += 1
    all_sprites.draw(screen)

    now_str = str(now)
    if now_str[:-3] == '':
        now_str = '0.' + now_str[-3:] + 's'
    else:
        now_str = now_str[:-3] + '.' + now_str[-3:] + 's'
    draw_text(screen, now_str, 18, WIDTH / 2, 28)
    draw_text(screen, 'Score:' + str(score), 18, WIDTH / 2, 10)
    draw_text(screen, 'X ' + str(player.lifes), 18, WIDTH / 10 + 57, HEIGHT - 40)
    draw_text(screen, 'X ' + str(player.bomb_num), 18, WIDTH / 10 + 57, HEIGHT - 110)
    draw_text(screen, ': ' + str(player.speed_level), 18, WIDTH - 30, HEIGHT - 85)
    draw_text(screen, ': ' + str(player.level), 18, WIDTH - 30, HEIGHT - 40)
    pygame.display.flip()
    count += 1
pygame.quit()
