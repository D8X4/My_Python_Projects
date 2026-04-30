#!/usr/bin/env python3
import arcade
WIDTH = 800
HEIGHT = 600
TITLE = "step 1"


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.timer = 0
        self.show_second = False

    def on_draw(self):
        self.clear()
        if self.show_second:
            arcade.draw_text("new text after 3 seconds", WIDTH/2, HEIGHT/2,
                             arcade.color.RASPBERRY, 24, anchor_x="center")
        else:
            arcade.draw_text("it works", WIDTH/2, HEIGHT/2,
                             arcade.color.WHITE, 24, anchor_x="center")

    def on_update(self, delta_time):
        self.timer += delta_time
        if self.timer >= 3:
            self.show_second = True


game = Game()
arcade.run()
