import arcade
import math

CROSSHAIR_RADIUS = 80
PLAYER_SPEED = 200


def update_player_movement(game, dt):

    dx = 0
    dy = 0

    if game.up:
        dy += 1
    if game.down:
        dy -= 1
    if game.left:
        dx -= 1
    if game.right:
        dx += 1

    length = math.sqrt(dx * dx + dy * dy)

    if length > 0:
        dx /= length
        dy /= length

    game.player.center_x += dx * PLAYER_SPEED * dt
    game.player.center_y += dy * PLAYER_SPEED * dt

    # knockback (proper decay + dt)
    game.player.center_x += game.player.knockback_x * dt
    game.player.center_y += game.player.knockback_y * dt

    game.player.knockback_x *= 0.85
    game.player.knockback_y *= 0.85

    # stop tiny jitter forever
    if abs(game.player.knockback_x) < 0.01:
        game.player.knockback_x = 0
    if abs(game.player.knockback_y) < 0.01:
        game.player.knockback_y = 0

def update_camera(game):
    game.camera.position = game.player.position

def update_mouse(game, x, y):
    cam_x, cam_y = game.camera.position

    screen_center_x = game.width / 2
    screen_center_y = game.height / 2

    # convert screen → world
    world_mouse_x = cam_x + (x - screen_center_x)
    world_mouse_y = cam_y + (y - screen_center_y)

    game.mouse_x = world_mouse_x
    game.mouse_y = world_mouse_y

def update_crosshair(game):
    import math

    dx = game.mouse_x - game.player.center_x
    dy = game.mouse_y - game.player.center_y

    angle = math.atan2(dy, dx)

    game.crosshair.center_x = game.player.center_x + math.cos(angle) * CROSSHAIR_RADIUS
    game.crosshair.center_y = game.player.center_y + math.sin(angle) * CROSSHAIR_RADIUS

def shoot(game):
    if game.reloading:
        return

    if game.bullet_count >= game.max_bullets:
        game.reloading = True
        game.reload_timer = 2.5
        return

    bullet = arcade.Sprite("imgs4game/bullet.png", scale=0.5)
    bullet.center_x = game.player.center_x
    bullet.center_y = game.player.center_y

    dx = game.crosshair.center_x - game.player.center_x
    dy = game.crosshair.center_y - game.player.center_y

    angle = math.atan2(dy, dx)

    speed = 500
    bullet.change_x = math.cos(angle) * speed
    bullet.change_y = math.sin(angle) * speed

    game.bullet_list.append(bullet)
    game.bullet_count += 1

    arcade.play_sound(game.shoot_sound)
