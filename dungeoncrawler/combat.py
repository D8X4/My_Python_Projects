import arcade
import random
import math


# =========================
# BULLET -> ENEMY COLLISION
# =========================
def handle_bullet_enemy_collisions(game, force):

    for bullet in list(game.bullet_list):

        hit_list = arcade.check_for_collision_with_list(
            bullet,
            game.enemy_list
        )

        for enemy in hit_list:

            # prevent double-processing same bullet
            if getattr(enemy, "hit_by_bullet", False):
                continue

            enemy.hit_by_bullet = True
            enemy.hit_timer = 0.1

            # directions
            dx = enemy.center_x - game.player.center_x
            dy = enemy.center_y - game.player.center_y

            # normalization of dx and dy
            length = math.sqrt(dx*dx + dy*dy)
            if length == 0:
                continue
            dx /= length
            dy /= length

            # knockback

            enemy.knockback_x += dx * force
            enemy.knockback_y += dy * force

            enemy.knockback_x = max(min(enemy.knockback_x, 15), -15)
            enemy.knockback_y = max(min(enemy.knockback_y, 15), -15)

            bullet.remove_from_sprite_lists()


# =========================
# ENEMY DAMAGE + DEATH LOGIC
# =========================
def resolve_enemy_damage_and_death(game, dt):

    for enemy in list(game.enemy_list):

        # flash effect timer
        if enemy.hit_timer > 0:
            enemy.hit_timer -= dt
            enemy.color = arcade.color.LIGHT_BLUE
            continue
        else:
            enemy.color = arcade.color.WHITE

        # only apply damage once per hit cycle
        if getattr(enemy, "hit_by_bullet", False):

            enemy.hit_by_bullet = False
            enemy.health -= 1

            # =========================
            # ENEMY DIED
            # =========================
            if enemy.health <= 0:

                # SCORE + COMBO ONLY ON DEATH
                game.combo_timer = game.max_combo
                game.multiplier += 0.5
                game.score += 1 * game.multiplier

                arcade.play_sound(game.death_sound)

                # particles
                for _ in range(8):
                    blood = arcade.Sprite("imgs4game/blood.png")
                    blood.center_x = enemy.center_x
                    blood.center_y = enemy.center_y

                    blood.change_x = random.uniform(-5, 5)
                    blood.change_y = random.uniform(-5, 5)

                    blood.alpha = 255

                    game.particle_list.append(blood)

                game.enemy_list.remove(enemy)


def handle_player_enemy_collisions(game, force):
    for enemy in list(game.enemy_list):

        if arcade.check_for_collision(enemy, game.player):

            if game.invincible_timer <= 0:

                game.health -= 1
                arcade.play_sound(game.death_sound)
                game.invincible_timer = 0.5

                # direction of knockback
                dx = game.player.center_x - enemy.center_x
                dy = game.player.center_y - enemy.center_y

                length = math.sqrt(dx*dx + dy*dy)
                if length == 0:
                    continue

                dx /= length
                dy /= length

                # knockback
                force = 10
                game.player.knockback_x = dx * force
                game.player.knockback_y = dy * force
