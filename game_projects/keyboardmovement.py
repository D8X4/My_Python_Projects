#!/usr/bin/env python3
import arcade

WIDTH = 800
HEIGHT = 600
TITLE = 'step 4 - keyboard input'

SPEED = 200


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.player = arcade.Sprite("shh.png", scale=0.05)
        self.player.center_x = WIDTH / 2
        self.player.center_y = HEIGHT / 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):
        if self.up:
            self.player.center_y += SPEED * delta_time
        if self.down:
            self.player.center_y -= SPEED * delta_time
        if self.left:
            self.player.center_x -= SPEED * delta_time
        if self.right:
            self.player.center_x += SPEED * delta_time
        if self.player.center_x > WIDTH:
            self.player.center_x = 0
        elif self.player.center_x < 0:
            self.player.center_x = WIDTH
        if self.player.center_y > HEIGHT:
            self.player.center_y = 0
        elif self.player.center_y < 0:
            self.player.center_y = HEIGHT

# for full wrap arround logic


# if self.player.center_x > WIDTH + self.player.width / 2:
#     self.player.center_x = -self.player.width / 2
# elif self.player.center_x < -self.player.width / 2:
#     self.player.center_x = WIDTH + self.player.width / 2

# if self.player.center_y > HEIGHT + self.player.height / 2:
#     self.player.center_y = -self.player.height / 2
# elif self.player.center_y < -self.player.height / 2:
#     self.player.center_y = HEIGHT + self.player.height / 2

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


game = Game()
arcade.run()
