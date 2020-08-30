import sys
from time import sleep

import pygame

from object.Alien import Alien
from object.Bullet import Bullet


def get_number_aliens_x(ai_setting, alien_width):
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_row(ai_setting, ship_height, alien_height):
    available_space_y = ai_setting.screen_height - 3 * alien_height - ship_height
    number_row = int(available_space_y / (2 * alien_height))
    return number_row


def create_alien(ai_setting, screen, alien_width, aliens, alien_number, row_number):
    alien = Alien(ai_setting, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_setting, screen, ship, aliens):
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_setting, alien_width)
    number_row = get_number_row(ai_setting, ship.rect.height, alien.rect.height)

    for row_number in range(number_row):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting, screen, alien_width, aliens, alien_number, row_number)


def check_bullets_aliens_collision(ai_setting, screen, ship, aliens, bullets):
    # 检测碰撞
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_setting, screen, ship, aliens)


def update_bullet(ai_setting, screen, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        # bullet.update(ai_setting, screen, ship, bullets)
        print("容器中的子弹"+str(len(bullets))+"坐标" + str(bullet.y))
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullets_aliens_collision(ai_setting, screen, ship, aliens, bullets)


def ship_hit(ai_setting, screen, stats, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False


def update_aliens(ai_setting, screen,stats, ship, aliens, bullets):
    check_fleet_edges(ai_setting, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, screen, stats, ship, aliens, bullets)
    check_aliens_bottom(ai_setting, screen, stats, ship, aliens, bullets)


def fire_bullet(ai_setting, screen, ship, bullets):
    # if len(bullets) < ai_setting.bullet_allowed and ai_setting.down_bullet:
    if len(bullets) < ai_setting.bullet_allowed:
        new_bullet = Bullet(ai_setting, screen, ship)
        print("初始坐标"+str(new_bullet.y))
        bullets.add(new_bullet)
        print("创建子弹:"+"坐标"+str(new_bullet.y))
    # draw_bullets(bullets)


def check_keydown_event(event, ai_setting, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        # ai_setting.down_bullet = True
        fire_bullet(ai_setting, screen, ship, bullets)


def check_keyup_event(event, ai_setting, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_SPACE:
        ai_setting.down_bullet = False
    elif event.key == pygame.K_q:
        sys.exit()


def check_events(ai_setting, screen, ship, bullets):
    """ 响应按键和鼠标事件 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_setting, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ai_setting, ship, bullets)


def update_screen(ai_setting, screen, ship, aliens, bullets):
    screen.fill(ai_setting.bg_color)
    draw_bullets(bullets)
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()


def draw_bullets(bullets):
    for bullet in bullets.sprites():
        bullet.draw_bullet()


def check_fleet_edges(ai_setting, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break


def change_fleet_direction(ai_setting, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1


def check_aliens_bottom(ai_setting, screen,stats, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, screen,stats, ship, aliens, bullets)
            break
