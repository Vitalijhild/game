import pygame
pygame.init()

#? створення констант для роботи гри
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
LIGHT_BLUE = (50, 50, 220)
RED = (200, 0, 0)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)
BROWN = (116, 79, 0)
BG_COLOR = (0, 0, 100)
WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 40

#? створення вікна з потрібними розмірами та ігрового годинника
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

#? створення забраження для заднього фону в меню
menu_bg_image = pygame.image.load('images\\menu_bg.png')
menu_bg_image = pygame.transform.scale(menu_bg_image, (WIN_WIDTH, WIN_HEIGHT))

#? створення зображення назви гри в меню гри
menu_name = pygame.image.load('images\\menu_name.png')
menu_name = pygame.transform.scale(menu_name, (WIN_HEIGHT - 75, 75))

#? створення зображення для заднього фону гри
bg_image = pygame.image.load('images//images.jpg')
bg_image = pygame.transform.scale(bg_image, (WIN_WIDTH, WIN_HEIGHT))

#? свторення зображення для перемоги
win_image = pygame.image.load('images//thumb.jfif')
win_image = pygame.transform.scale(win_image, (WIN_WIDTH, WIN_HEIGHT))

#? створення забраження для програшу
gg_image = pygame.image.load('images//game-over_1.png')
gg_image = pygame.transform.scale(gg_image, (WIN_WIDTH, WIN_HEIGHT))

#? створення фонової музики
pygame.mixer.music.load("music\\bg_song.wav")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

#? створення звуку перемоги
music_win = pygame.mixer.Sound("music\\win-song.wav")
music_win.set_volume(0.08)

#? створення звуку пострілу
music_shot = pygame.mixer.Sound("music\\sgot.wav")

#TODO свторуння класу кнопки
class Button():
    #! створення методу конструктора
    def __init__(self, x, y, width, height, text, font, color, bg_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.txt = pygame.font.SysFont("Arial", font).render(text, True, color)
        self.color = bg_color

    #! створення методу показу кнопки
    def show(self, x, y):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.txt, (x + 10, y))

#TODO створення класу для іконка соціальної мережі
class Image_Botton(pygame.sprite.Sprite):
    #! створення методу конструктора
    def __init__(self, x, y, width, heigth, image, txt_for_text):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, heigth))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.show_txt = False
        self.text = Button(self.rect.x + 40, self.rect.y, 140, 30, txt_for_text, 18, BLACK, BROWN)

    #! створення методу показу кнопки
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        if self.show_txt == True:
            self.text.show(self.rect.x + 35, self.rect.y)
#TODO створення класу ігрового спрайту який є наслідком класа pygame.sprite.Sprite
class GameSprite(pygame.sprite.Sprite):
    #! створення методу конструктора
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    #! створення методу показу кнопки
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#TODO створення класу гравця який є наслідком класу GameSprite
class Player(GameSprite):
    #! створення методу конструктора
    def __init__(self, x, y, widht, height, image, speed_x, speed_y):
        super().__init__(x, y, widht, height, image)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image_l = pygame.transform.flip(self.image, True, False)
        self.image_r = self.image
        self.image_up = pygame.image.load('images\\hero_up.png')
        self.image_down = pygame.image.load('images\\hero_down.png')
        self.diretion = 'right'

    #! створення методу руху
    def update(self):
        if self.rect.left > 0 and self.speed_x < 0 or self.rect.right < WIN_WIDTH and self.speed_x > 0:
            self.rect.x += self.speed_x

        #! перевірка зіткнення гравця та стін або країв украну
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        if self.speed_x < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)
        if self.rect.top > 0 and self.speed_y < 0 or self.rect.bottom < WIN_HEIGHT and self.speed_y > 0:
            self.rect.y += self.speed_y
        
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_y < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        if self.speed_y > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
    #! створення методу для пострілу
    def fire(self):
        if self.diretion == 'left':
            bullet = Bullet(self.rect.left, self.rect.centery, 30, 30, 'images\\bullet.png', 'left', -20)
        elif self.diretion == 'right':
            bullet = Bullet(self.rect.right, self.rect.centery, 30, 30, 'images\\bullet.png', 'right', 20)
        elif self.diretion == 'up':
            bullet = Bullet(self.rect.right, self.rect.centery, 30, 30, 'images\\bullet.png', 'up', -20)
        elif self.diretion == 'down':
            bullet = Bullet(self.rect.right, self.rect.centery, 30, 30, 'images\\bullet.png', 'down', 20)

        bullet.add(bullets)

#TODO створення класу для ворогів
class Enemy(GameSprite):
    #! створення методу конструктора
    def __init__(self, x, y, widht, height, image, speed, directional, min_coord, max_coord):
        super().__init__(x, y, widht, height, image)
        self.speed = speed
        self.directional = directional
        self.min_coord = min_coord
        self.max_coord = max_coord
        self.x = x
        self.y = y
    #! створення методу руху
    def update(self):
        if self.directional == 'left' or self.directional == 'right':
            if self.rect.right >= self.max_coord:
                self.directional = 'left'
            elif self.rect.left <= self.min_coord:
                self.directional = 'right'

            if self.directional == 'left':
                self.rect.x -= self.speed
            elif self.directional == 'right':
                self.rect.x += self.speed
        elif self.directional == 'up' or self.directional == 'down':
            if self.rect.top <= self.min_coord:
                self.directional = 'down'
            elif self.rect.bottom >= self.max_coord:
                self.directional = 'up'
            
            if self.directional == 'up':
                self.rect.y -= self.speed
            if self.directional == 'down':
                self.rect.y += self.speed

#TODO створення класу пуль
class Bullet(GameSprite):
    def __init__(self, x, y, widht, height, image, diretion, speed):
        super().__init__(x, y, widht, height, image)
        self.speed = speed
        self.diretion = diretion
    def update(self):
        if self.diretion == 'right' or self.diretion == 'left':
            self.rect.x += self.speed
        elif self.diretion == 'up' or self.diretion == 'down':
            self.rect.y += self.speed
        if self.rect.right >= WIN_WIDTH or self.rect.left <= 0:
            self.kill()
class Gun(GameSprite):
    def __init__(self, x, y, widht, height, image):
        super().__init__(x, y, widht, height, image)
        self.gun_up = False
        self.rect.x = x
        self.rect.y = y
    def update(self):
        if self.gun_up == True:
            self.rect.x = player.rect.right
            self.rect.y = player.rect.right
class Bust(GameSprite):
    def __init__(self, x, y, widht, height, image):
        super().__init__(x, y, widht, height, image)
        self.use_bust = False

#? створення групи пуль
bullets = pygame.sprite.Group()

#? створення ігрових об'єктів гравця та ворогів
player = Player(100, 50, 30, 50, 'images//hero.png', 0, 0)
gun = Gun(200, 80, 40, 20, 'images\\gun.png')
speed_up = Bust(20, 300, 50, 60, 'images\\speed_up.png')
enemys = pygame.sprite.Group()
enemy1 = Enemy(440, 50, 60, 50, 'images//cyborg.png', 5, 'right', 440, 570)
enemys.add(enemy1)
enemy2 = Enemy(430, 160, 60, 50, 'images//cyborg.png', 5, 'down', 160, 380)
enemys.add(enemy2)
enemy3 = Enemy(580, 180, 60, 50, 'images//cyborg.png', 5, 'left', 440, 690)
enemys.add(enemy3)
enemy4 = Enemy(100, 430, 60, 50, 'images//cyborg.png', 5, 'right', 10, 690)
enemys.add(enemy4)

#? створення групи стін
walls = pygame.sprite.Group()

#? створення стін
wall1 = GameSprite(600, 0 , 20, 150, 'images//platform2_v.png')
walls.add(wall1)
wall2 = GameSprite(400, 0 , 20, 400, 'images//platform2_v.png')
walls.add(wall2)
wall3 = GameSprite(420, 130, 60, 20, 'images//platform2_v.png')
walls.add(wall3)
wall4 = GameSprite(540, 130, 60, 20, 'images//platform2_v.png')
walls.add(wall4)
wall5 = GameSprite(0, 130, 300, 20, 'images//platform2_v.png')
walls.add(wall5)
wall6 = GameSprite(170, 70, 20, 60, 'images//platform2_v.png')
walls.add(wall6)
wall7 = GameSprite(100, 230, 300, 20, 'images//platform2_v.png')
walls.add(wall7)
wall8 = GameSprite(0, 375, 300, 20, 'images//platform2_v.png')
walls.add(wall8)
wall9 = GameSprite(550, 230, 150, 20, 'images//platform2_v.png')
walls.add(wall9)
wall10 = GameSprite(550, 380, 150, 20, 'images//platform2_v.png')
walls.add(wall10)
coin = GameSprite(620, 30, 90, 90, 'images//coin.png')

#? створення кнопок та нипису в меню
btn1 = Button(250, 150, 200, 100, "Start", 30, BLACK, BLUE)
btn2 = Button(250, 300, 200, 100, "Quit", 30, BLACK, BLACK)
subs = Button(25, 375, 130, 25, 'Subscribe pls:', 20, RED, GREEN)

#? створення іконок соціальніх мереж
tt_icon = Image_Botton(30, 410, 30, 30, 'images\\tt_image.png', '@hildgame')
inst_icon = Image_Botton(30, 450, 30, 30, 'images\\inst_image.jfif', '@vitalijmedvede2')


game = True
level = 0
#TODO створення ігрового циклу
while game:
    #? обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if level == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if btn1.rect.collidepoint(x, y):
                    btn1.color = LIGHT_BLUE
                elif btn2.rect.collidepoint(x, y):
                    btn2.color = LIGHT_BLUE
                elif tt_icon.rect.collidepoint(x, y):
                     tt_icon.show_txt = True
                elif inst_icon.rect.collidepoint(x, y):
                    inst_icon.show_txt = True
                else:
                    btn1.color = BLUE
                    btn2.color = BLUE
                    inst_icon.show_txt = False
                    tt_icon.show_txt = False
                            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn1.rect.collidepoint(x, y):
                    level = 1
                if btn2.rect.collidepoint(x, y):
                    level = 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.speed_x = 5
                player.image = player.image_r
                player.diretion = 'right'
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.speed_x = -5
                player.image = player.image_l
                player.diretion = 'left'
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.speed_y = -5
                player.image = player.image_up
                player.diretion = 'up'
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.speed_y = 5
                player.image = player.image_down
                player.diretion = 'down'
            if event.key == pygame.K_SPACE and gun.gun_up:
                player.fire()
                music_shot.play()
                music_shot.set_volume(0.05)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.speed_x = 0
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.speed_x = 0
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.speed_y = 0
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.speed_y = 0

    if level == 0:
        window.blit(menu_bg_image, (0, 0))
        window.blit(menu_name, (125, 50))
        btn1.show(btn1.rect.x + 70, btn1.rect.y + 30)
        btn2.show(btn2.rect.x + 70, btn2.rect.y + 30)
        subs.show(subs.rect.x, subs.rect.y)
        tt_icon.show()
        inst_icon.show()

    elif level == 1:
        window.blit(bg_image, (0, 0))

        player.reset()
        player.update()
        enemys.draw(window)
        enemys.update()
        walls.draw(window)
        bullets.draw(window)
        bullets.update()
        coin.reset()
        if speed_up.use_bust == False:
            speed_up.reset()
        if gun.gun_up == False:
            gun.reset()

        if pygame.sprite.collide_rect(player, coin):
            play = False
            window.blit(win_image, (0, 0))
            
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.play(1)
            music_win.play()

        if pygame.sprite.spritecollide(player, enemys, False):
            play = False
            level = 0
            window.blit(gg_image, (0, 0))
        if pygame.sprite.collide_rect(player, gun):
            gun.gun_up = True
        if pygame.sprite.collide_rect(player, speed_up):
            speed_up = True
            player.speed_x += 2
            player.speed_y += 2

        pygame.sprite.groupcollide(bullets, walls, True, False)
        pygame.sprite.groupcollide(bullets, enemys, True, True)

    elif level == 2:
        game = False    
    elif level == 3:
        tt_text.show(subs.rect.x + 35, subs.rect.bottom + 10)
    
    
    clock.tick(40)
    pygame.display.update()