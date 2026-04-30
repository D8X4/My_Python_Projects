#!/usr/bin/env python3
import arcade
import math
import random

from entities import spawn_wave, create_enemy
from combat import (
    handle_bullet_enemy_collisions,
    resolve_enemy_damage_and_death
)
from ui import draw_hud, draw_game_over
from player import (
    update_player_movement,
    update_camera,
    update_mouse,
    update_crosshair,
    shoot
)
from systems import update_game


WIDTH = 2400
HEIGHT = 1800
TITLE = "dungeon crawl"


class Game(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, resizable=True)
        arcade.set_background_color(arcade.color.BLACK)

        # =========================
        # WORLD SIZE
        # =========================
        self.world_width = WIDTH
        self.world_height = HEIGHT

        # =========================
        # PLAYER
        # =========================
        self.player = arcade.Sprite("imgs4game/player.png", scale=0.5)
        self.player.center_x = self.world_width / 2
        self.player.center_y = self.world_height / 2
        self.player.health = 3
        self.player.knockback_x = 0
        self.player.knockback_y = 0
        self.knockback_force = 8
        self.max_combo = 4.0
        self.shoot_sound = arcade.load_sound("sounds/shooting_sound.wav")
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # =========================
        # sounds and shit
        # =========================
        self.music = arcade.load_sound("sounds/game_music.wav")
        self.shoot_sound = arcade.load_sound("sounds/shooting_sound.wav")
        self.death_sound = arcade.load_sound("sounds/death_sound.wav")
        self.damage_sound = arcade.load_sound("sounds/damaga_sound.mp3")

        arcade.play_sound(self.music, volume=0.35, loop=True)

        # =========================
        # WORLD
        # =========================
        self.mask = arcade.Sprite("imgs4game/mask.png")
        self.mask_list = arcade.SpriteList([self.mask])
        self.mask.center_x = self.player.center_x
        self.mask.center_y = self.player.center_y
        self.floor_list = arcade.SpriteList()

        tile_size = 64

        for x in range(0, self.world_width, tile_size):
            for y in range(0, self.world_height, tile_size):
                tile = arcade.Sprite("imgs4game/floor.png")
                tile.left = x
                tile.bottom = y
                self.floor_list.append(tile)

        # =========================
        # COMBAT
        # =========================
        self.bullet_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()

        self.max_bullets = 10
        self.bullet_count = 0
        self.reloading = False
        self.reload_timer = 0

        # =========================
        # INPUT
        # =========================
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.mouse_x = 0
        self.mouse_y = 0

        # =========================
        # GAME STATE
        # =========================
        self.health = 3
        self.invincible_timer = 0

        self.score = 0
        self.multiplier = 1
        self.combo_timer = 0

        self.game_over = False
        self.wave = 0

        # =========================
        # CAMERA
        # =========================
        self.setup_cameras()
        self.gui_camera = arcade.Camera2D()

        # =========================
        # CROSSHAIR
        # =========================
        self.crosshair = arcade.Sprite("imgs4game/crosshair.png", scale=1)
        self.crosshair_list = arcade.SpriteList([self.crosshair])

        self.mask_list = arcade.SpriteList([self.mask])

        # =========================
        # ENEMIES
        # =========================
        self.enemy_list = arcade.SpriteList()
        spawn_wave(
            self.enemy_list,
            self.player.center_x,
            self.player.center_y,
            self.wave,
            self.world_width,
            self.world_height
        )
    # =========================
    # CAMERA
    # =========================
    def setup_cameras(self):
        self.camera = arcade.Camera2D()

    # =========================
    # UPDATE
    # =========================
    def on_update(self, dt):
        if self.game_over:
            return

        update_game(self, dt)

        # camera must always follow player
        update_camera(self)

    # =========================
    # DRAW
    # =========================
    def on_draw(self):
        self.clear()

        self.camera.use()

        self.floor_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.particle_list.draw()
        self.mask_list.draw()
        self.crosshair_list.draw()

        self.gui_camera.use()
        draw_hud(self)

        if self.game_over:
            draw_game_over(self)
    # =========================
    # INPUT
    # =========================
    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.up = True
        if key == arcade.key.S:
            self.down = True
        if key == arcade.key.A:
            self.left = True
        if key == arcade.key.D:
            self.right = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.up = False
        if key == arcade.key.S:
            self.down = False
        if key == arcade.key.A:
            self.left = False
        if key == arcade.key.D:
            self.right = False

        if key == arcade.key.R and self.game_over:
            self.reset_game()

    def on_mouse_motion(self, x, y, dx, dy):
        update_mouse(self, x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            shoot(self)

    # =========================
    # RESET
    # =========================
    def reset_game(self):

        self.player.center_x = self.world_width / 2
        self.player.center_y = self.world_height / 2

        self.health = 3
        self.invincible_timer = 0
        self.player.knockback_x = 0
        self.player.knockback_y = 0
        self.score = 0
        self.multiplier = 1
        self.combo_timer = 0

        self.game_over = False
        self.wave = 0

        self.bullet_list.clear()
        self.particle_list.clear()

        self.bullet_count = 0
        self.reloading = False
        self.reload_timer = 0

        self.enemy_list.clear()
        spawn_wave(self.enemy_list, self.player.center_x, self.player.center_y, self.wave)


game = Game()
arcade.run()
