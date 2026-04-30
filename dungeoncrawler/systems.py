import arcade
import math

from player import (
    update_player_movement,
    update_camera,
    update_crosshair
)

from combat import (
    handle_bullet_enemy_collisions,
    resolve_enemy_damage_and_death,
    handle_player_enemy_collisions
)

from entities import spawn_wave


def update_game(game, dt):

    if game.game_over:
        return

    # =========================
    # PLAYER + CAMERA
    # =========================
    update_player_movement(game, dt)
    update_camera(game)
    update_crosshair(game)

    # =========================
    # WORLD BOUNDS
    # =========================
    game.player.center_x = max(0, min(game.world_width, game.player.center_x))
    game.player.center_y = max(0, min(game.world_height, game.player.center_y))

    # =========================
    # MASK FOLLOWS PLAYER
    # =========================
    game.mask.center_x = game.player.center_x
    game.mask.center_y = game.player.center_y

    # =========================
    # BULLETS
    # =========================
    for bullet in list(game.bullet_list):
        bullet.center_x += bullet.change_x * dt
        bullet.center_y += bullet.change_y * dt

        if (
            bullet.center_x < 0 or bullet.center_x > game.world_width or
            bullet.center_y < 0 or bullet.center_y > game.world_height
        ):
            bullet.remove_from_sprite_lists()

    # =========================
    # ENEMY MOVEMENT
    # =========================
    for enemy in game.enemy_list:

        # safety check (prevents crashes from broken enemies)
        if not hasattr(enemy, "speed"):
            continue

        dx = game.player.center_x - enemy.center_x
        dy = game.player.center_y - enemy.center_y

        angle = math.atan2(dy, dx)

        enemy.center_x += math.cos(angle) * enemy.speed * dt
        enemy.center_y += math.sin(angle) * enemy.speed * dt

    # =========================
    # COMBAT
    # =========================
    handle_bullet_enemy_collisions(game, game.knockback_force)
    resolve_enemy_damage_and_death(game, dt)
    handle_player_enemy_collisions(game, force=10)

    # =========================
    # PARTICLES
    # =========================
    for p in list(game.particle_list):
        p.center_x += p.change_x
        p.center_y += p.change_y

        p.change_x *= 0.95
        p.change_y *= 0.95

        p.alpha -= 5

        if p.alpha <= 0:
            p.remove_from_sprite_lists()

    # =========================
    # WAVE SYSTEM (FIXED)
    # =========================
    if len(game.enemy_list) == 0:
        game.wave += 1
        spawn_wave(
            game.enemy_list,
            game.player.center_x,
            game.player.center_y,
            game.wave,
            game.world_width,
            game.world_height
        )

    # =========================
    # TIMER / GAME OVER
    # =========================
    if game.invincible_timer > 0:
        game.invincible_timer -= dt

    if game.health <= 0:
        game.game_over = True
