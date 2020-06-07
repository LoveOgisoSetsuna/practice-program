# 初始模块导入
import pygame
import random
import sys
from pygame import *

# 相关参数初始化
width = 800
height = 600
gray = (230, 230, 230)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
dark_green = (0, 100, 0)
bright_green = (0, 200, 0)
dark_red = (100,0,0)
bright_red = (200,0,0)
blue = (0, 0, 255)
HEAD = 0
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
cell_size = 20
map_width = int(width / cell_size)
map_height = int(height / cell_size)
file='大鱼.mp3'#音乐路径
pygame.mixer.init()#初始化
track=pygame.mixer.music.load(file)#加载音乐文件



# 主函数
def main():
    pygame.init()
    size = width, height = 800, 600
    snake_speed_clock = pygame.time.Clock()  # pygame时钟
    screen = pygame.display.set_mode((map_width, map_height))  #
    pygame.display.set_caption("贪吃蛇小游戏")
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen.fill(white)
    show_start_info(screen)  # 欢迎信息
    screen.fill(white)
    pygame.display.update()
    mode = [0, 1]
    menu(screen, snake_speed_clock, mode)

def menu(screen, snake_speed_clock, mode):
    font = pygame.font.Font('myfont.ttf', 40)
    tip1 = font.render('贪吃蛇小游戏', True, (65, 105, 225))
    screen.blit(tip1, (310, 100))
    tip1 = font.render('请选择模式："a":生存模式 "s":标准模式', True, (65, 105, 225))
    screen.blit(tip1, (130, 300))
    pygame.display.update()
    while True:
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()  # 终止程序
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:  # 终止程序
                    terminate()  # 终止程序
                elif event.key == K_a:#生存模式
                    while True:
                        food_time_control = [80, 60, 40, 30]
                        speed_setting = [4, 7, 11, 15]
                        pygame.mixer.music.play()  # 开始播放音乐
                        running_game(screen, snake_speed_clock, food_time_control, speed_setting, mode[0])
                        show_gameover_info(screen)
                elif event.key == K_s:#标准模式
                    screen.fill(white)
                    pygame.display.update()
                    font = pygame.font.Font('myfont.ttf', 40)
                    tip1 = font.render('标准模式', True, (65, 105, 225))
                    screen.blit(tip1, (330, 100))
                    tip1 = font.render('请按键选择难度："z":简单 "x":普通  "c":困难', True, (65, 105, 225))
                    screen.blit(tip1, (80, 300))
                    pygame.display.update()
                    while True:
                        for event in pygame.event.get():  # event handling loop
                            if event.type == QUIT:
                                terminate()  # 终止程序
                            elif event.type == KEYDOWN:
                                if event.key == K_ESCAPE or event.key == K_q:  # 终止程序
                                    terminate()  # 终止程序
                                elif event.key == K_z:
                                    while True:
                                        food_time_control = [80, 80, 80, 80]
                                        speed_setting = [5, 5, 5, 5]
                                        pygame.mixer.music.play()  # 开始播放音乐
                                        running_game(screen, snake_speed_clock, food_time_control, speed_setting, mode[1])
                                        show_gameover_info(screen)
                                elif event.key == K_x:
                                    while True:
                                        food_time_control = [60, 60, 60, 60]
                                        speed_setting = [10, 10, 10, 10]
                                        pygame.mixer.music.play()  # 开始播放音乐
                                        running_game(screen, snake_speed_clock, food_time_control, speed_setting, mode[1])
                                        show_gameover_info(screen)
                                elif event.key == K_c:
                                    while True:
                                        food_time_control = [40, 40, 40, 40]
                                        speed_setting = [15, 15, 15, 15]
                                        pygame.mixer.music.play()  # 开始播放音乐
                                        running_game(screen, snake_speed_clock, food_time_control, speed_setting, mode[1])
                                        show_gameover_info(screen)
                    return  # 结束此函数, 重新开始游戏


# 运行主体
def running_game(screen, snake_speed_clock, food_time_control, speed_setting, mode):
    start_x = random.randint(4, map_width - 10)
    start_y = random.randint(3, map_height - 5)  # 随机生成一个起始位置
    snake_array = [{'x': start_x, 'y': start_y},  # 生成初始贪吃蛇
                   {'x': start_x - 1, 'y': start_y},
                   {'x': start_x - 2, 'y': start_y}]
    direction = RIGHT
    food = food_position()
    if(mode == 0):
        drug = drug_position(food)  # 检查毒药生成位置是否与食物重叠
        food_new = food_position_check(food, drug)#检查食物生成位置是否与毒药重叠
    else:
        drug = {'a': 1, 'b': 1}
        food_new = food_position_check(food, drug)
    food_time_default = 100
    food_time = food_time_default
    while True:
        # ----------------坐标数据处理与逻辑判断部分--------------------
        for event in pygame.event.get():  # 蛇方向的操控
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_a or event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_d or event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_w or event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_s or event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        move_snake(direction, snake_array)  # 进行蛇的移动
        if(mode == 0):
            judge = alive_judge_survive(snake_array,drug)  # 判断蛇是否活着
        else:
            judge = alive_judge_normal(snake_array)
        if not judge:
            record_scores(len(snake_array) - 3)
            pygame.mixer.music.pause()#音乐暂停
            break  # 如果蛇判断死亡，跳出循环
        food_time = food_time_judge(snake_array, food, food_time, food_time_default)#判断当前难度等级
        snake_grow(snake_array, food, len(snake_array)-3, drug, mode)  # 如果没死，就判断是否吃到食物，同时根据分数控制毒药
        # ------------------图像绘制部分------------------------
        screen.fill(gray)
        draw_snake(screen, snake_array)
        draw_food(screen, food_new)
        if(mode == 0):
            draw_drug(screen, drug)
        draw_score(screen, len(snake_array)-3)
        snake_speed=control_speed(len(snake_array) - 3, food_time_default, food_time_control, speed_setting)[0]
        food_time_default=control_speed(len(snake_array) - 3, food_time_default, food_time_control, speed_setting)[1]
        snake_speed_clock.tick(snake_speed)  # 控制fps
        pygame.display.update()  # 刷新屏幕

def control_speed(score,food_time_default,food_time_control,speed_setting):#分数梯度控制难度
    if score >= 0 and score <= 2:
         food_time_default = food_time_control[0]
         snake_speed = speed_setting[0]
    elif score > 2 and score <= 10:
        food_time_default = food_time_control[1]
        snake_speed = speed_setting[1]
    elif score > 10 and score <= 18:
        food_time_default = food_time_control[2]
        snake_speed = speed_setting[2]
    elif score > 18 :
        food_time_default = food_time_control[3]
        snake_speed = speed_setting[3]
    Hard_or_Easy = [snake_speed, food_time_default]
    return Hard_or_Easy

def drug_position(food):  # 随机生成毒药的位置
    drug = {'a': random.randint(5, map_width - 5), 'b': random.randint(5, map_height - 5)}
    while (drug['a'] == food['x'] and drug['a'] == food['x']):
        drug = {'a': random.randint(5, map_width - 5), 'b': random.randint(5, map_height - 5)}
    return drug

def move_snake(direction, snake_array):  # 移动蛇
    if direction == UP:
        new_head = {'x': snake_array[HEAD]['x'], 'y': snake_array[HEAD]['y'] - 1}
    elif direction == DOWN:
        new_head = {'x': snake_array[HEAD]['x'], 'y': snake_array[HEAD]['y'] + 1}
    elif direction == LEFT:
        new_head = {'x': snake_array[HEAD]['x'] - 1, 'y': snake_array[HEAD]['y']}
    elif direction == RIGHT:
        new_head = {'x': snake_array[HEAD]['x'] + 1, 'y': snake_array[HEAD]['y']}
    snake_array.insert(0, new_head)

def draw_snake(screen, snake_array):  # 画出蛇
    for array in snake_array:
        x = array['x'] * cell_size
        y = array['y'] * cell_size
        snake_draw_out = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, bright_green, snake_draw_out)


def draw_food(screen, food):  # 画出食物
    x = food['x'] * cell_size
    y = food['y'] * cell_size
    food_draw_out = pygame.Rect(x, y, cell_size, cell_size)
    pygame.draw.rect(screen, yellow, food_draw_out)

def draw_drug(screen, drug):  # 画出毒药
    x = drug['a'] * cell_size
    y = drug['b'] * cell_size
    drug_draw_out = pygame.Rect(x, y, cell_size, cell_size)
    pygame.draw.rect(screen, dark_green, drug_draw_out)


def food_position():  # 随机生成食物位置
    return {'x': random.randint(3, map_width - 3), 'y': random.randint(3, map_height - 3)}

def food_position_check(food, drug):
    while (food['x'] == drug['a'] and food['y'] == drug['b']):
        food= {'x': random.randint(5, map_width - 5), 'y': random.randint(5, map_height - 5)}
    return food

def alive_judge_survive(snake_array,drug):  # 判断蛇是否还活着
    judge = True
    if snake_array[HEAD]['x'] == -1 or snake_array[HEAD]['x'] == map_width or snake_array[HEAD]['y'] == -1 or \
            snake_array[HEAD]['y'] == map_height or (snake_array[HEAD]['x'] == drug['a'] and snake_array[HEAD]['y'] == drug['b']):
        judge = False
    for snake_body in snake_array[1:]:
        if snake_body['x'] == snake_array[HEAD]['x'] and snake_body['y'] == snake_array[HEAD]['y']:
            judge = False
    return judge

def alive_judge_normal(snake_array):  # 判断蛇是否还活着
    judge = True
    if snake_array[HEAD]['x'] == -1 or snake_array[HEAD]['x'] == map_width or snake_array[HEAD]['y'] == -1 or \
            snake_array[HEAD]['y'] == map_height :
        judge = False
    for snake_body in snake_array[1:]:
        if snake_body['x'] == snake_array[HEAD]['x'] and snake_body['y'] == snake_array[HEAD]['y']:
            judge = False
    return judge

def snake_grow(snake_array, food, score, drug, mode):  # 判断是否吃到了食物
    if snake_array[HEAD]['x'] == food['x'] and snake_array[HEAD]['y'] == food['y']:
        food['x'] = random.randint(3, map_width - 3)
        food['y'] = random.randint(3, map_height - 3)
        if (score % 5 == 0 and mode == 0):
            drug['a'] = random.randint(5, map_width - 5)
            drug['b'] = random.randint(5, map_height - 5)
            while (drug['a'] == food['x'] and drug['a'] == food['x']):
                drug['a'] = random.randint(5, map_width - 5)
                drug['b'] = random.randint(5, map_height - 5)
    else:
        del snake_array[-1]

def food_time_judge(snake_array, food,food_time , food_time_default):
    if snake_array[HEAD]['x'] == food['x'] and snake_array[HEAD]['y'] == food['y']:
        food_time=food_time_default
    else:
        food_time = food_time-1
        if (food_time == 0):
            food['x'] = random.randint(3, map_width - 3)
            food['y'] = random.randint(3, map_height - 3)
            food_time = food_time_default
    return food_time



#开始信息显示
def show_start_info(screen):
	font = pygame.font.Font('myfont.ttf', 40)
	tip = font.render('按任意键开始游戏~~~', True, (65, 105, 225))
	gamestart = pygame.image.load('结束.jpg')
	screen.blit(gamestart, (140, 30))
	screen.blit(tip, (240, 550))
	pygame.display.update()

	while True:  #键盘监听事件
		for event in pygame.event.get():  # event handling loop
			if event.type == QUIT:
				terminate()     #终止程序
			elif event.type == KEYDOWN:
				if (event.key == K_ESCAPE):  #终止程序
					terminate() #终止程序
				else:
					return #结束此函数, 开始游戏
#游戏结束信息显示
def show_gameover_info(screen):
    font = pygame.font.Font('myfont.ttf', 40)
    tip = font.render('按Q或者ESC退出游戏, 按任意键重新开始游戏~', True, (65, 105, 225))
    gamestart = pygame.image.load('贪吃蛇开头.jpg')
    screen.blit(gamestart, (148, 0))
    screen.blit(tip, (80, 300))
    tip = font.render('按Z查看排行榜', True, (65, 105, 225))
    screen.blit(tip, (150, 400))
    pygame.display.update()
    while True:
        for event in pygame.event.get():  # event handling loo
            if event.type == QUIT:
                terminate()  # 终止程序
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:  # 终止程序
                    terminate()  # 终止程序
                elif event.key == K_z:
                    while True:
                        with open("排行榜积分.txt", "r") as f:
                            for line in f:  # 遍历每一行
                                wordlist = line.split()  # 将每一行的数字分开放在列表中
                        grade=wordlist[0:5]
                        screen.fill(yellow)
                        pygame.display.update()
                        font = pygame.font.Font('myfont.ttf', 40)
                        tip1 = font.render('第一名的成绩为:%s'%grade[0], True, (65, 105, 225))
                        screen.blit(tip1, (330, 100))
                        tip1 = font.render('第二名的成绩为:%s'%grade[1], True, (65, 105, 225))
                        screen.blit(tip1, (330, 170))
                        tip1 = font.render('第三名的成绩为:%s'%grade[2], True, (65, 105, 225))
                        screen.blit(tip1, (330, 240))
                        tip1 = font.render('第四名的成绩为:%s'%grade[3], True, (65, 105, 225))
                        screen.blit(tip1, (330, 310))
                        tip1 = font.render('第五名的成绩为:%s'%grade[4], True, (65, 105, 225))
                        screen.blit(tip1, (330, 380))
                        tip1 = font.render('按任意键返回主菜单', True, (65, 105, 225))
                        screen.blit(tip1, (270, 450))
                        pygame.display.update()
                        while True:
                            for event in pygame.event.get():  # event handling loo
                                if event.type == QUIT:
                                    terminate()  # 终止程序
                                elif event.type == KEYDOWN:
                                    if event.key == K_ESCAPE or event.key == K_q:  # 终止程序
                                        terminate()  # 终止程序
				else:
					main()
                                    
                else:
                    return #结束此函数, 重新开始游戏
#画成绩
def draw_score(screen,score):
	font = pygame.font.Font('myfont.ttf', 30)#这个代表图片存放的路径
	scoreSurf = font.render('得分: %s' % (score*10), True, blue)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (width - 120, 10)
	screen.blit(scoreSurf, scoreRect)


def text_save(data):#filename为写入文件的路径，data为要写入数据列表.
  file = open('排行榜积分.txt','a')
  for i in range(len(data)):
    s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
    s = s.replace(',','') +' '  #去除单引号，逗号，每行末尾追加空格
    file.write(s)
  file.close()
  print("保存文件成功")
# 记录成绩
def record_scores(score):
    with open("排行榜积分.txt", "r") as f:
        for line in f:  # 遍历每一行
            wordlist = line.split()  # 将每一行的数字分开放在列表中
            wordlist = list(map(int, wordlist))
            wordlist.sort()
            wordlist.reverse()
            wordlist.append(str((score - 1)*10))
            wordlist = list(map(int, wordlist))
            wordlist.sort()
            wordlist.reverse()
            print(wordlist[0:5])
    with open('排行榜积分.txt', 'w') as f:
        text_save(wordlist[0:5])
    f.close()
#程序终止
def terminate():
	pygame.quit()
	sys.exit()


main()
