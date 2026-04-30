#!/usr/bin/env python3
# imports
import arcade
import random
# width of Windows
WIDTH = 800
# height of window
HEIGHT = 600
# title of the game
TITLE = "step 5 - sprite lists"

# SPEED of player and enemy count for area
SPEED = 200
ENEMY_COUNT = 5


class Game(arcade.Window):
    def __init__(self):
        # initialization of game
        super().__init__(WIDTH, HEIGHT, TITLE)
        # sets background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        # gets player.png
        self.player = arcade.Sprite("patrick.png", scale=0.05)
        self.player.center_x = WIDTH / 2
        self.player.center_y = HEIGHT / 2
        # adds player to a list
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.enemy_list = arcade.SpriteList()
        # gets enemy and spawns them and makes them move
        for i in range(ENEMY_COUNT):
            enemy = arcade.Sprite("shh.png", scale=0.03)
            enemy.center_x = random.randint(0, WIDTH)
            enemy.center_y = random.randint(0, HEIGHT)
            enemy.change_x = random.uniform(-2, 2)
            enemy.change_y = random.uniform(-2, 2)
            self.enemy_list.append(enemy)

        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def on_draw(self):
        # draws player and enemy
        self.clear()
        self.enemy_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        # how the movement moves
        if self.up:
            self.player.center_y += SPEED * delta_time
        if self.down:
            self.player.center_y -= SPEED * delta_time
        if self.left:
            self.player.center_x -= SPEED * delta_time
        if self.right:
            self.player.center_x += SPEED * delta_time
        # off screen logic for PLAYER
        if self.player.center_x > WIDTH:
            self.player.center_x = 0
        elif self.player.center_x < 0:
            self.player.center_x = WIDTH
        if self.player.center_y > HEIGHT:
            self.player.center_y = 0
        elif self.player.center_y < 0:
            self.player.center_y = HEIGHT
        # off screen ogic for ENEMY
        for enemy in self.enemy_list:
            if enemy.center_x > WIDTH:
                enemy.center_x = 0
            elif enemy.center_x < 0:
                enemy.center_x = WIDTH
            if enemy.center_y > HEIGHT:
                enemy.center_y = 0
            elif enemy.center_y < 0:
                enemy.center_y = HEIGHT
        self.enemy_list.update()

    def on_key_press(self, key, modifiers):
        # movement keys for player
        if key == arcade.key.UP or key == arcade.key.W:
            self.up = True
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down = True
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left = True
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right = True

    def on_key_release(self, key, modifiers):
        # detect is key is let go
        if key == arcade.key.UP or key == arcade.key.W:
            self.up = False
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down = False
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left = False
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right = False


# runs game
game = Game()
arcade.run()
