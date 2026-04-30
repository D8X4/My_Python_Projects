#!/usr/bin/env python3
import arcade

WIDTH = 800
HEIGHT = 600
TITLE = "step 2 - drawing"


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_rect_filled(arcade.XYWH(100, 100, 80, 80), arcade.color.ELECTRIC_CYAN)
        arcade.draw_circle_filled(400, 100, 40, arcade.color.YELLOW)
        arcade.draw_line(0, 0, 800, 600, arcade.color.RED, 3)
        arcade.draw_triangle_filled(700, 100, 650, 200, 750, 200, arcade.color.ORANGE)

    def on_update(self, delta_time):
        pass


game = Game()
arcade.run()
