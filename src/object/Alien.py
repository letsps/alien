import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_setting, screen):
        super(Alien, self).__init__()
        # 初始化外星人的位置
        self.screen = screen
        self.setting = ai_setting

        # 加载外星人的图像并取其外接矩形
        self.image = pygame.image.load('res/alien_d.png')
        self.rect = self.image.get_rect()

        # 每个外星人的起始位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精准位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # self.moving_right = False
        # self.moving_left = False
        # self.moving_up = False
        # self.moving_down = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.setting.alien_speed_factor * self.setting.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
