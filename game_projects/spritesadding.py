#!/usr/bin/env python3
import arcade

WIDTH = 800
HEIGHT = 600
TITLE = "step 3 - sprites"


class Game(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.player = arcade.Sprite("shh.png", scale=0.1)
        self.player.center_x = WIDTH / 2
        self.player.center_y = HEIGHT / 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player.center_x += 200 * delta_time
        self.player.angle += 2
        if self.player.center_x > WIDTH:
            self.player.center_x = 0
        if self.player.center_y > HEIGHT:
            self.player.center_y = 0


game = Game()
arcade.run()
