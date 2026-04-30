#!/usr/bin/env python3
import arcade
import random

WIDTH = 800
HEIGHT = 600
TITLE = "step 6 - collision"

SPEED = 200
ENEMY_COUNT = 5


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.player = arcade.Sprite("patrick.png", scale=0.05)
        self.player.center_x = WIDTH / 2
        self.player.center_y = HEIGHT / 2

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.spawn_enemies()
        self.game_over = False
        self.score = 0
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def spawn_enemies(self):
        self.enemy_list = arcade.SpriteList()
        for i in range(ENEMY_COUNT):
            enemy = arcade.Sprite("shh.png", scale=0.03)
            enemy.center_x = random.randint(0, WIDTH)
            enemy.center_y = random.randint(0, HEIGHT)
            enemy.change_x = random.uniform(-2, 2)
            enemy.change_y = random.uniform(-2, 2)
            self.enemy_list.append(enemy)

    def on_draw(self):
        self.clear()
        if self.game_over:
            arcade.draw_text(f'game over score: {self.score}', WIDTH/2, HEIGHT/2, arcade.color.WHITE, 48, anchor_x='center')
        else:
            self.enemy_list.draw()
            self.player_list.draw()
            arcade.draw_text(f"score: {self.score}", 10, HEIGHT - 30,
                             arcade.color.WHITE, 20)

    def on_update(self, delta_time):
        if not self.game_over:
            self.score += 1
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

        # collision check
        hit_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for enemy in hit_list:
            self.game_over = True
            # enemy.remove_from_sprite_lists()
            # self.score += 1
        if len(self.enemy_list) == 0:
            self.spawn_enemies()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up = True
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down = True
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left = True
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right = True
        if key == arcade.key.R:
            arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

            self.player = arcade.Sprite("patrick.png", scale=0.05)
            self.player.center_x = WIDTH / 2
            self.player.center_y = HEIGHT / 2

            self.player_list = arcade.SpriteList()
            self.player_list.append(self.player)

            self.spawn_enemies()
            self.game_over = False
            self.score = 0
            self.up = False
            self.down = False
            self.left = False
            self.right = False

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
