#!/usr/bin/env python3
import arcade
import math
import random

WIDTH = 1920
HEIGHT = 1080
TITLE = "dungeon crawl"

PLAYER_SPEED = 200
CROSSHAIR_RADIUS = 80
ENEMY_SPEED = 100
ENEMY_HEALTH = 3

WORLD_WIDTH = 2400
WORLD_HEIGHT = 1800


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, resizable=True)
        arcade.set_background_color(arcade.color.BLACK)

        # player stats
        self.player = arcade.Sprite('imgs4game/player.png', scale=0.5)
        self.player.center_x = WORLD_WIDTH / 2
        self.player.center_y = WORLD_HEIGHT / 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # flashlight stats
        self.mask = arcade.Sprite('imgs4game/mask.png')
        self.mask_list = arcade.SpriteList()
        self.mask_list.append(self.mask)

        # bullet stats
        self.bullet_list = arcade.SpriteList()
        self.max_bullets = 10
        self.bullet_count = 0
        self.reloading = False
        self.reload_timer = 0

        # crosshair initualization
        self.crosshair = arcade.Sprite('imgs4game/crosshair.png', scale=1)
        self.crosshair.center_x = self.player.center_x + 5
        self.crosshair.center_y = self.player.center_y + 5
        self.crosshair_list = arcade.SpriteList()
        self.crosshair_list.append(self.crosshair)

        # floor shit
        self.floor_list = arcade.SpriteList()
        self.tile_size = 64
        for x in range(0, WORLD_WIDTH, self.tile_size):
            for y in range(0, WORLD_HEIGHT, self.tile_size):
                tile = arcade.Sprite('imgs4game/floor.png')
                tile.left = x
                tile.bottom = y
                self.floor_list.append(tile)

        self.particle_list = arcade.SpriteList()

        # movement booleans
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        # health
        self.health = 3

        # iframe timer
        self.invincible_timer = 0

        # shake init things
        self.shake_timer = 0
        self.shake_intensity = 10

        # random score counter
        self.score = 0

        # random score multiplier
        self.multiplier = 1
        self.combo_timer = 0
        self.max_combo = 4.0

        # enemy colors and player colors
        self.WHITE = arcade.color.WHITE
        self.ORIGINAL_COLOR = arcade.color.WHITE

        # game state
        self.game_over = False

        # wave number
        self.wave = 0

        # camera thing for hud
        self.setup_cameras()

        # mouse x and y things
        self.mouse_x = 0
        self.mouse_y = 0

        # spawn enemies
        self.spawn_enemies()
        self.hit_timer = 0
        # sound init
        self.music = arcade.load_sound('sounds/game_music.wav')
        self.shoot_sound = arcade.load_sound('sounds/shooting_sound.wav')
        self.death_sound = arcade.load_sound('sounds/death_sound.wav')
        self.damage_sound = arcade.load_sound('sounds/damaga_sound.mp3')

        arcade.play_sound(self.music, volume=0.35, loop=True)

    def setup_cameras(self):
        self.camera = arcade.Camera2D()

    def on_resize(self, width, height):
        super().on_resize(width, height)

    def spawn_enemies(self):
        # enemy stats
        types = ['normal', 'fast', 'tank']
        self.enemy_list = arcade.SpriteList()
        self.wave += 1
        num_to_spawn = 10 + (self.wave * 5)
        for _ in range(num_to_spawn):
            self.enemy = arcade.Sprite('imgs4game/enemy.png', scale=0.5)
            enemy_type = random.choice(types)
            self.enemy.type = enemy_type
            if self.enemy.type == 'normal':
                self.enemy.speed = 100
                self.enemy.health = 2
            if self.enemy.type == 'fast':
                self.enemy.texture = arcade.load_texture('imgs4game/enemy_fast.png')
                self.enemy.speed = 230
                self.enemy.health = 1
            if self.enemy.type == 'tank':
                self.enemy.texture = arcade.load_texture('imgs4game/enemy_tank.png')
                self.enemy.speed = 50
                self.enemy.health = 3
            while True:
                xspawn = random.randint(0, WORLD_WIDTH)
                yspawn = random.randint(0, WORLD_HEIGHT)
                x_diff = xspawn - self.player.center_x
                y_diff = yspawn - self.player.center_y
                dist = math.sqrt(x_diff**2 + y_diff**2)
                if dist > 400:
                    self.enemy.center_x = xspawn
                    self.enemy.center_y = yspawn
                    self.enemy.hit_timer = 0
                    self.enemy.was_hit = False
                    self.enemy_list.append(self.enemy)
                    break

    def reset_game(self):
        arcade.set_background_color(arcade.color.BLACK)

        # player stats
        self.player = arcade.Sprite('imgs4game/player.png', scale=0.5)
        self.player.center_x = WORLD_WIDTH / 2
        self.player.center_y = WORLD_HEIGHT / 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # flashlight stats
        self.mask = arcade.Sprite('imgs4game/mask.png')
        self.mask_list = arcade.SpriteList()
        self.mask_list.append(self.mask)

        # bullet stats
        self.bullet_list = arcade.SpriteList()
        self.max_bullets = 10
        self.bullet_count = 0
        self.reloading = False
        self.reload_timer = 0

        # crosshair initualization
        self.crosshair = arcade.Sprite('imgs4game/crosshair.png', scale=1)
        self.crosshair.center_x = self.player.center_x + 5
        self.crosshair.center_y = self.player.center_y + 5
        self.crosshair_list = arcade.SpriteList()
        self.crosshair_list.append(self.crosshair)

        # floor shit
        self.floor_list = arcade.SpriteList()
        self.tile_size = 64
        for x in range(0, WORLD_WIDTH, self.tile_size):
            for y in range(0, WORLD_HEIGHT, self.tile_size):
                tile = arcade.Sprite('imgs4game/floor.png')
                tile.left = x
                tile.bottom = y
                self.floor_list.append(tile)

        self.particle_list = arcade.SpriteList()

        # movement booleans
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        # iframe timer
        self.invincible_timer = 0

        # shake init things
        self.shake_timer = 0
        self.shake_intensity = 10

        # random score multiplier
        self.multiplier = 1
        self.combo_timer = 0
        self.max_combo = 4.0

        # enemy colors and player colors
        self.WHITE = arcade.color.WHITE
        self.ORIGINAL_COLOR = arcade.color.WHITE

        # game state
        self.game_over = False

        # wave number
        self.wave = 0

        # camera thing for hud
        self.setup_cameras()

        # mouse x and y things
        self.mouse_x = 0
        self.mouse_y = 0

        # spawn enemies
        self.spawn_enemies()
        self.hit_timer = 0

        self.game_over = False
        self.health = 3
        self.score = 0
        self.bullet_count = 0
        self.reloading = False
        self.reload_timer = 0

    def on_draw(self):
        self.clear()

        # =========================
        # GAME OVER
        # =========================
        if self.game_over:

            # IMPORTANT: reset camera so UI is not affected by world transform
            self.camera.use()  # safe reset step
            self.camera.position = (self.width / 2, self.height / 2)

            cx = self.width * 0.5
            cy = self.height * 0.5

            arcade.draw_text(
                "GAME OVER",
                cx,
                cy + 60,
                arcade.color.WHITE,
                60,
                anchor_x="center",
                anchor_y="center"
            )

            arcade.draw_text(
                f"Score: {int(self.score)}",
                cx,
                cy,
                arcade.color.WHITE,
                28,
                anchor_x="center",
                anchor_y="center"
            )

            arcade.draw_text(
                "Press R to Restart",
                cx,
                cy - 60,
                arcade.color.WHITE,
                22,
                anchor_x="center",
                anchor_y="center"
            )

            return

        # =========================
        # WORLD RENDER
        # =========================
        self.camera.use()

        self.floor_list.draw()

        arcade.draw_lrbt_rectangle_outline(
            0, WORLD_WIDTH, 0, WORLD_HEIGHT,
            arcade.color.WHITE, 10
        )

        self.enemy_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.particle_list.draw()
        self.crosshair_list.draw()
        self.mask_list.draw()

        # =========================
        # CAMERA-ATTACHED HUD
        # =========================

        cam_x, cam_y = self.camera.position

        left = cam_x - self.width / 2
        right = cam_x + self.width / 2
        bottom = cam_y - self.height / 2
        top = cam_y + self.height / 2

        arcade.draw_text(
            f"HP: {self.health}",
            left + 20,
            bottom + 20,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            f"Wave {self.wave} - Enemies: {len(self.enemy_list)}",
            left + 20,
            top - 40,
            arcade.color.WHITE,
            18
        )

        ammo_display = (
            "RELOADING..."
            if self.reloading
            else f"Ammo: {self.max_bullets - self.bullet_count}"
        )

        arcade.draw_text(
            ammo_display,
            right - 20,
            top - 40,
            arcade.color.WHITE,
            18,
            anchor_x="right"
        )

        arcade.draw_text(
            f"Score: {int(self.score)}",
            right - 20,
            top - 70,
            arcade.color.WHITE,
            18,
            anchor_x="right"
        )

        if self.combo_timer > 0:
            arcade.draw_text(
                f"COMBO x{self.multiplier:.1f}",
                right - 20,
                top - 100,
                arcade.color.YELLOW,
                10,
                anchor_x="right"
            )

    def on_update(self, delta_time):
        if self.game_over:
            return
        # move player
        if self.up:
            self.player.center_y += PLAYER_SPEED * delta_time
        if self.down:
            self.player.center_y -= PLAYER_SPEED * delta_time
        if self.left:
            self.player.center_x -= PLAYER_SPEED * delta_time
        if self.right:
            self.player.center_x += PLAYER_SPEED * delta_time

        # camera position things
        self.camera.position = (self.player.center_x, self.player.center_y)

        if self.shake_timer > 0:
            shake_x = random.uniform(-self.shake_intensity, self.shake_intensity)
            shake_y = random.uniform(-self.shake_intensity, self.shake_intensity)
            self.camera.position = (self.player.center_x + shake_x,
                                    self.player.center_y + shake_y)
            self.shake_timer -= delta_time

        # torch mask logic
        self.mask.center_x = self.player.center_x
        self.mask.center_y = self.player.center_y

        # player border clamping
        if self.player.left < 0:
            self.player.left = 0
        elif self.player.right > WORLD_WIDTH:
            self.player.right = WORLD_WIDTH
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.top > WORLD_HEIGHT:
            self.player.top = WORLD_HEIGHT

        # move bullets
        self.bullet_list.update()
        for bullet in self.bullet_list:
            bullet.center_x += bullet.change_x * delta_time
            bullet.center_y += bullet.change_y * delta_time
            if bullet.center_x < 0 or bullet.center_x > WORLD_WIDTH:
                bullet.remove_from_sprite_lists()
            if bullet.center_y < 0 or bullet.center_y > WORLD_HEIGHT:
                bullet.remove_from_sprite_lists()

        # bullet things continued
        if self.reloading:
            self.reload_timer -= delta_time
            if self.reload_timer <= 0:
                self.bullet_count = 0
                self.reloading = False

        # COMBO TIMER UPDATE
        if self.combo_timer > 0:
            self.combo_timer -= delta_time

            if self.combo_timer <= 0:
                self.combo_timer = 0
                self.multiplier = 1
        # update enemies
        for enemy in self.enemy_list:
            angle = math.atan2(self.player.center_y - enemy.center_y, self.player.center_x - enemy.center_x)
            enemy.change_x = math.cos(angle) * enemy.speed
            enemy.change_y = math.sin(angle) * enemy.speed

            # actually move the enemies
            enemy.center_x += enemy.change_x * delta_time
            enemy.center_y += enemy.change_y * delta_time

        # move crosshair to follow mouse but locked to CROSSHAIR_RADIUS around player
        angle = math.atan2(self.mouse_y - self.player.center_y, self.mouse_x - self.player.center_x)
        self.crosshair.center_x = self.player.center_x + math.cos(angle) * CROSSHAIR_RADIUS
        self.crosshair.center_y = self.player.center_y + math.sin(angle) * CROSSHAIR_RADIUS

        # iframe timer update
        self.invincible_timer -= delta_time

        # =========================
        # BULLET → ENEMY COLLISION
        # =========================
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            for enemy in hit_list:
                # mark hit (only once per bullet hit)
                if not hasattr(enemy, "was_hit") or not enemy.was_hit:
                    enemy.was_hit = True
                    enemy.hit_timer = 0.1

                    # knockback
                    enemy.center_x += bullet.change_x * 0.2
                    enemy.center_y += bullet.change_y * 0.2

                    bullet.remove_from_sprite_lists()
                    self.camera.zoom = 1.05

        # =========================
        # ENEMY STATE UPDATE
        # =========================
        for enemy in list(self.enemy_list):

            # hit flash timer
            if enemy.hit_timer > 0:
                enemy.hit_timer -= delta_time
                enemy.color = arcade.color.LIGHT_BLUE
                continue
            else:
                enemy.color = self.ORIGINAL_COLOR

            # only process damage once per hit cycle
            if hasattr(enemy, "was_hit") and enemy.was_hit:

                enemy.was_hit = False
                enemy.health -= 1

                # =========================
                # ENEMY DEATH
                # =========================
                if enemy.health <= 0:

                    self.enemy_list.remove(enemy)

                    arcade.play_sound(self.death_sound)
                    self.combo_timer = self.max_combo
                    self.multiplier += 0.5

                    # =========================
                    # BLOOD PARTICLES (FIXED)
                    # =========================
                    for _ in range(8):
                        blood = arcade.Sprite('imgs4game/blood.png')
                        blood.center_x = enemy.center_x
                        blood.center_y = enemy.center_y

                        blood.change_x = random.uniform(-5, 5)
                        blood.change_y = random.uniform(-5, 5)

                        blood.alpha = 255

                        self.particle_list.append(blood)

                    self.score += 1 * self.multiplier

        # =========================
        # PARTICLE UPDATE (IMPORTANT FIX)
        # =========================
        for blood in self.particle_list:

            blood.center_x += blood.change_x
            blood.center_y += blood.change_y

            blood.change_x *= 0.95
            blood.change_y *= 0.95

            blood.alpha -= 5

            if blood.alpha <= 0:
                blood.remove_from_sprite_lists()

        # =========================
        # WAVE CHECK
        # =========================
        if len(self.enemy_list) == 0:
            self.spawn_enemies()

        # =========================
        # CAMERA RESET ZOOM
        # =========================
        if self.camera.zoom > 1.0:
            self.camera.zoom += (1.0 - self.camera.zoom) * 0.1
            if self.camera.zoom < 1.01:
                self.camera.zoom = 1.0

        # ENEMY PLAYER COLLISION
        for enemy in self.enemy_list:

            if arcade.check_for_collision_with_list(enemy, self.player_list):

                if self.invincible_timer <= 0:

                    # knockback
                    dx = self.player.center_x - enemy.center_x
                    dy = self.player.center_y - enemy.center_y

                    if abs(dx) > abs(dy):
                        self.player.center_x += 40 if dx > 0 else -40
                    else:
                        self.player.center_y += 40 if dy > 0 else -40

                    # clamp
                    self.player.center_x = max(0, min(WORLD_WIDTH, self.player.center_x))
                    self.player.center_y = max(0, min(WORLD_HEIGHT, self.player.center_y))

                    # damage
                    self.health -= 1
                    self.invincible_timer = 1.5
                    self.shake_timer = 0.6

                    arcade.play_sound(self.damage_sound)

                    if self.health <= 0:
                        self.health = 0
                        self.game_over = True

    def on_key_press(self, key, modifiers):
        if self.game_over:
            if key == arcade.key.R:
                self.reset_game()
            return
        if key == arcade.key.W:
            self.up = True
        if key == arcade.key.S:
            self.down = True
        if key == arcade.key.A:
            self.left = True
        if key == arcade.key.D:
            self.right = True
        if key == arcade.key.ESCAPE:
            self.reset_game()
        if key == arcade.key.R and not self.reloading:
            self.reloading = True
            self.reload_timer = 3.0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.up = False
        if key == arcade.key.S:
            self.down = False
        if key == arcade.key.A:
            self.left = False
        if key == arcade.key.D:
            self.right = False

    def on_mouse_motion(self, x, y, dx, dy):
        # this is where mouse position comes in
        self.mouse_x = self.camera.position[0] + (x - self.width / 2)
        self.mouse_y = self.camera.position[1] + (y - self.height / 2)

    def on_mouse_press(self, x, y, button, modifiers):
        # left click = shoot
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.bullet_count >= self.max_bullets or self.reloading:
                return
            bullet = arcade.Sprite('imgs4game/bullet.png', scale=0.5)
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y
            dx = self.crosshair.center_x - self.player.center_x
            dy = self.crosshair.center_y - self.player.center_y
            angle = math.atan2(dy, dx)
            bullet_speed = 30
            bullet.change_x = math.cos(angle) * bullet_speed
            bullet.change_y = math.sin(angle) * bullet_speed
            self.bullet_list.append(bullet)
            self.bullet_count += 1
            arcade.play_sound(self.shoot_sound, volume=1.2)


game = Game()
arcade.run()

