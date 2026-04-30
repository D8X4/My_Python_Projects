import arcade
import random
import math

ENEMY_TYPES = ["normal", "fast", "tank"]

def create_enemy(enemy_type, x, y):

    if enemy_type == "normal":
        texture = "imgs4game/enemy.png"
        speed = 100
        health = 2

    elif enemy_type == "fast":
        texture = "imgs4game/enemy_fast.png"
        speed = 230
        health = 1

    elif enemy_type == "tank":
        texture = "imgs4game/enemy_tank.png"
        speed = 50
        health = 3

    enemy = arcade.Sprite(texture, scale=0.5)

    enemy.center_x = x
    enemy.center_y = y

    enemy.type = enemy_type
    enemy.speed = speed
    enemy.health = health

    enemy.hit_timer = 0
    enemy.was_hit = False
    enemy.knockback_x = 0
    enemy.knockback_y = 0

    return enemy


def spawn_wave(enemy_list, player_x, player_y, wave, world_width=2400, world_height=1800):
    num_to_spawn = max(1, int(5 + wave * 2))

    for _ in range(num_to_spawn):
        while True:
            x = random.randint(0, world_width)
            y = random.randint(0, world_height)

            dx = x - player_x
            dy = y - player_y

            if dx * dx + dy * dy > 300 * 300:
                enemy = create_enemy("normal", x, y)
                enemy_list.append(enemy)
                break

    return enemy_list
