#!/usr/bin/env python3
import arcade
import random

WIDTH = 800
HEIGHT = 600
TITLE = "step 2 - drawing"


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.x = 0
        self.y = 0

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(self.x, self.y, 40, arcade.color.YELLOW)

    def on_update(self, delta_time):
        self.x += 3
        self.y += 3
        if self.x > WIDTH:
            self.x = 0
        if self.y > HEIGHT:
            self.y = 0


game = Game()
arcade.run()
