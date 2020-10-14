import pygame
import random
import math

#初始化
pygame.init()
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption('飞机大战')
icon = pygame.image.load('feiji/ufo.png')
pygame.display.set_icon(icon)
bgImg = pygame.image.load('feiji/bg.png')


#分数模块
score = 0
over = 0
font = pygame.font.Font('freesansbold.ttf',30)

def show_score():
    text = f"Score:{score}"
    score_render = font.render(text,True,(255,255,255))
    screen.blit(score_render, (10,10))

over_font = pygame.font.Font('freesansbold.ttf',64)
def over_game():
    if over == 1:
        text = "GAME OVER"
        render = over_font.render(text,True,(255,0,0))
        screen.blit(render,(200,400))


#添加飞机
playerImg = pygame.image.load('feiji/player1.jpg')
playerX = 400
playerY = 500
playerMove = 0

def move_player():
    global playerX
    playerX += playerMove
    # 防止飞机出界
    if playerX > 740:
        playerX = 740
    if playerX < 10:
        playerX = 10

#添加敌人
number_enemies = 5
class Enemy():
    def __init__(self):
        self.img = pygame.image.load('feiji/enemy.png')
        self.x = random.randint(100,700)
        self.y = random.randint(50,200)
        self.step = random.randint(2,4)
    def reset(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(50, 200)
enemies = []

for i in range(number_enemies):
    enemies.append(Enemy())

#两个点之间的距离
def distance(bx,by,ex,ey):
    a = bx - by
    b = ex - ey
    return math.sqrt(a*a + b*b)
#print(distance())


#添加子弹
class Bullet():
    def __init__(self):
        self.img = pygame.image.load('feiji/bullet.png')
        self.x = playerX
        self.y = playerY
        self.step = 6

    #检测击中
    def hit(self):
        global score
        for e in enemies:
            if(distance(self.x,self.y,e.x,e.y) < 20):
                score += 1
                bullets.remove(self)
                e.reset()

bullets = []


#显示敌人并移动
def show_enemy():
    global over
    for e in enemies:
        screen.blit(e.img,(e.x,e.y))
        e.x += e.step
        if(e.x > 760 or e.x <0):
            e.step *= -1
            e.y += 25
            if e.y > 460:
                over = 1
                print("Game Over")
                enemies.clear()

#显示子弹并移动
def show_bullet():
    for b in bullets:
        screen.blit(b.img,(b.x,b.y))
        b.hit()
        b.x = playerX + 16
        b.y -= b.step
        if b.y < 0:
            bullets.remove(b)



#游戏主循环
running = True
while running:
    screen.blit(bgImg,(0,0))
    show_score()
    for event in pygame.event.get():  # 从队列中获取事件
        if event.type == pygame.QUIT:
            running = False
        # 检测到键盘按下时
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerMove = 5
            elif event.key == pygame.K_LEFT:
                playerMove = -5
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet())

            # if event.key == pygame.K_LEFT+pygame.K_RIGHT
            # playerMove =0
        if event.type == pygame.KEYUP:
            playerMove = 0
    screen.blit(playerImg, (playerX,playerY))
    move_player()
    show_enemy()
    show_bullet()
    over_game()

    pygame.display.update()
