import pygame
from setting.setting import Setting


class Ship():
    def __init__(self, screen, ai_setting):
        # 初始化飞船的位置
        self.screen = screen
        self.setting = ai_setting

        # 加载飞船的图像并取其外接矩形
        self.image = pygame.image.load('res/ship_b.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_bottom = False

    def update(self):
        if self.moving_right and self.screen_rect.right > self.rect.right:
            self.center += self.setting.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.setting.ship_speed
        if self.moving_up and  self.rect.d > 0:
            self.center += self.setting.ship_speed
        if self.moving_bottom and self.screen.bottom > self.rect.bottom:
            self.center -= self.setting.ship_speed

        self.rect.centerx = self.center

    def blitme(self):
        """ 在指定位置绘制飞船 """
        self.screen.blit(self.image, self.rect)
