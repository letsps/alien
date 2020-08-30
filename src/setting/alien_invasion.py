import pygame
import game_function as gf
from object.Alien import Alien
from object.GameStats import GameStats
from setting.setting import Setting
from object.Ship import Ship
from pygame.sprite import Group


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_setting = Setting()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("Alien Invasion")

    stats = GameStats(ai_setting)

    ship = Ship(screen, ai_setting)
    alien = Alien(ai_setting, screen)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(ai_setting, screen, ship, aliens)

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_setting, screen, ship, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullet(ai_setting, screen, ship,  aliens, bullets)
            gf.update_aliens(ai_setting, screen, stats, ship, aliens, bullets)
        gf.update_screen(ai_setting, screen, ship, aliens, bullets)
