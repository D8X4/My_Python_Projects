#!/usr/bin/env python3

import arcade
import random

WIDTH = 800
HEIGHT = 600
TITLE = "step 7 - camera"

SPEED = 200
WORLD_WIDTH = 900
WORLD_HEIGHT = 700

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.gui_camera = arcade.Camera2D()
        self.player = arcade.Sprite("patrick.png", scale=0.05)
        self.player.center_x = WORLD_WIDTH / 2
        self.player.center_y = WORLD_HEIGHT / 2

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.score = 0
        self.coin_list = arcade.SpriteList()
        self.camera = arcade.Camera2D()

        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def spawn_coins(self):
        self.coin_list = arcade.SpriteList()
        for i in range(20):
            coin = arcade.Sprite("player.png", scale=0.5)
            coin.center_x = random.randint(0, WORLD_WIDTH)
            coin.center_y = random.randint(0, WORLD_HEIGHT)
            self.coin_list.append(coin)


    def on_draw(self):
        self.clear()
        self.camera.use()
        self.coin_list.draw()
        self.player_list.draw()
        arcade.draw_rect_outline(arcade.XYWH(WORLD_WIDTH/2, WORLD_HEIGHT/2, WORLD_WIDTH, WORLD_HEIGHT), arcade.color.RED, 5)
        self.gui_camera.use()
        arcade.draw_text(f"score: {self.score}", 10, HEIGHT - 30,
                                     arcade.color.WHITE, 20)

    def on_update(self, delta_time):
        if self.up:
            self.player.center_y += SPEED * delta_time
        if self.down:
            self.player.center_y -= SPEED * delta_time
        if self.left:
            self.player.center_x -= SPEED * delta_time
        if self.right:
            self.player.center_x += SPEED * delta_time

        self.camera.position = (
            self.player.center_x,
            self.player.center_y
        )
        hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in hit_list:
            self.score += 1
            coin.remove_from_sprite_lists()
        if len(self.coin_list) == 0:
            self.spawn_coins()
        if self.up:
            self.player.center_y += SPEED * delta_time
        if self.down:
            self.player.center_y -= SPEED * delta_time
        if self.left:
            self.player.center_x -= SPEED * delta_time
        if self.right:
            self.player.center_x += SPEED * delta_time
        
        if self.player.center_x > WORLD_WIDTH:
            self.player.center_x = WORLD_WIDTH
        elif self.player.center_x < 0:
            self.player.center_x = 0
        
        if self.player.center_y > WORLD_HEIGHT:
            self.player.center_y = WORLD_HEIGHT
        elif self.player.center_y < 0:
            self.player.center_y = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up = True
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down = True
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left = True
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up = False
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down = False
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left = False
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right = False

game = Game()
arcade.run()
