#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygame
from sys import exit
import random
import math


class Bullet:
    def __init__(self):
        self.screen_height, self.screen_width = (800, 494)
        x, y = pygame.mouse.get_pos()
        self.image = pygame.image.load('img/bullet.png').convert_alpha()
        self.bullet_height, self.bullet_width = (self.image.get_height(), self.image.get_width())
        self.bullet_x, self.bullet_y = (x - self.bullet_width / 2, y - self.bullet_height / 2)
        self.active = True  #子弹的状态

    def shot(self):
        if self.active:
            self.bullet_y -= 1.5
        else:
            self.bullet_y = self.screen_height + 100
        if self.bullet_y <= 0 - self.image.get_height():
            self.active = False

    def restart(self):
        x, y = pygame.mouse.get_pos()
        self.bullet_x, self.bullet_y = (x - self.image.get_width() / 2, y - self.image.get_height() / 2)
        #激活子弹

class Plane:
    def __init__(self):
        self.screen_height, self.screen_width = (800, 494)

        self.image = pygame.image.load('img/plane.png').convert_alpha()
        self.plane_height, self.plane_width = (self.image.get_height(), self.image.get_width())
        self.plane_x, self.plane_y = (self.screen_width / 2 - self.plane_width / 2, self.screen_height - self.plane_height - 20)
    def move(self):
        x, y = pygame.mouse.get_pos()
        self.plane_x, self.plane_y = (x - self.image.get_width() / 2, y - self.image.get_height() / 2)

class Boss:
    def __init__(self):
        self.screen_height, self.screen_width = (800, 494)
        self.image = pygame.image.load('img/boss.png').convert_alpha()
        self.boss_height, self.boss_width = (self.image.get_height(), self.image.get_width())
        self.boss_x, self.boss_y = (random.uniform(0, self.screen_width - self.boss_width), 0 - self.boss_height)
        self.active = False
        self.speed = 0
    def attack(self):
        if self.active:
            self.boss_y += self.speed
        else:
            self.boss_y = 0 - self.boss_height
        if self.boss_y >= self.screen_height:
            self.active = False
    def restart(self):
        self.boss_x, self.boss_y = (random.uniform(0, self.screen_width - self.boss_width), 0)

pygame.init()
pygame.mixer.init()

backgroundMusic = pygame.mixer.Sound('./yinyue/battle.ogg')
backgroundMusic.play()
boom = pygame.mixer.Sound("./yinyue/boom.wav")
boom.set_volume(0.4)
planeBoom = pygame.mixer.Sound("./yinyue/planeBoom.wav")
planeBoom.set_volume(0.2)
screen = pygame.display.set_mode((494, 800), 0, 32)
pygame.display.set_caption("飞机大战")
background = pygame.image.load('img/bg.png').convert()
#把背景画上去
plane = Plane()
#飞机



bullets = []
bullet = Bullet()
#子弹
for i in range(5):     #添加5颗子弹
    bullets.append(Bullet())
bulletNum = len(bullets)

bosses = []
boss = Boss()
#大Boss
for k in range(5):
    bosses.append(Boss())
bossNum = len(bosses)

interval_bullet = 0
#子弹发射剩余
indexA = 0
#累加
indexC = 0


score = 0
my_font = pygame.font.SysFont('SimHei', 30)
#创建字体对象
font_area = my_font.render("得分: 0", True, (255, 0, 0))
area = font_area.get_rect()
area.center = (70, 30)
#得分

clock = pygame.time.Clock()


while True:

    interval_bullet -= 1

    if interval_bullet <= 0:
        interval_bullet = 200

        indexB = math.floor(indexA / bossNum)
        if not bosses[indexB % bossNum].active:
            bosses[indexB % bossNum].active = True
            if score <= 1000:
                speed_x = 0.01
                speed_y = 0.04
            elif score <= 2000:
                speed_x = 0.03
                speed_y = 0.1
            elif score <= 4000:
                speed_x = 0.05
                speed_y = 0.12
            else:
                speed_x = 0.08
                speed_y = 0.15
            bosses[indexB % bossNum].speed = round(random.uniform(speed_x, speed_y), 2)
            bosses[indexB % bossNum].boss_x, bosses[indexB % bossNum].boss_y = (random.uniform(0, bosses[indexB % bossNum].screen_width - bosses[indexB % bossNum].boss_width), 0 - bosses[indexB % bossNum].boss_height)

        indexA += 1
    #发射多颗子弹 和 多个Boss


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not bullets[indexC % bulletNum].active:

                bullets[indexC % bulletNum].active = True
                x, y = pygame.mouse.get_pos()
                bullets[indexC % bulletNum].bullet_x, bullets[indexC % bulletNum].bullet_y = (
                x - bullets[indexC % bulletNum].bullet_width / 2, y - bullets[indexC % bulletNum].bullet_height / 2)
                indexC += 1

    #千万注意 这儿有个图层概念
    screen.blit(background, (0, 0))
    #画上背景

    for j in bullets:
        j.shot()
        screen.blit(j.image, (j.bullet_x, j.bullet_y))
    # 画上子弹


        for k in bosses:
            k.attack()
            screen.blit(k.image, (k.boss_x, k.boss_y))
        # 画上Boss

            if (not ((k.boss_x + k.boss_width < j.bullet_x) or (
                k.boss_x > j.bullet_x + j.bullet_width))) and (not (
                (k.boss_y + k.boss_height < j.bullet_y) or (
                k.boss_y > j.bullet_y + j.bullet_height))):
                score += int(k.speed * 1000)

                font_area = my_font.render("得分: " + str(score), True, (255, 0, 0))
                boom.play()
                k.active = False
                j.active = False
                print(k.speed)
            #判断爆炸

            if (not ((k.boss_x + k.boss_width < plane.plane_x) or (
                        k.boss_x > plane.plane_x + plane.plane_width))) and (
                    not ((k.boss_y + k.boss_height < plane.plane_y) or (
                        k.boss_y > plane.plane_y + plane.plane_height))):
                planeBoom.play()
                print('死了')
                clock.tick(15)
    plane.move()
    screen.blit(plane.image, (plane.plane_x, plane.plane_y))
    #画上飞机


    screen.blit(font_area, area)
    #把分数写上

    pygame.display.update()
    #刷新画面
