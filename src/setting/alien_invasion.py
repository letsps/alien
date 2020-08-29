import pygame
import game_function as gf
from setting.setting import Setting
from object.Ship import Ship
from pygame.sprite import Group


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_setting = Setting()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(screen, ai_setting)
    bullets = Group()

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_setting, screen, ship, bullets)
        ship.update()
        gf.update_bullet(bullets)
        gf.update_screen(ai_setting, screen, ship, bullets)
