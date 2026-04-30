import arcade

# --- HUD LAYOUT CONSTANTS ---
HUD_PADDING = 20
FONT_SIZE = 18
LINE_HEIGHT = 22

# -------------------------
# IN-GAME HUD
# -------------------------


def draw_hud(game):
    x = HUD_PADDING
    y = game.height - HUD_PADDING

    # Top-left stack layout
    arcade.draw_text(
        f"HP: {game.health}",
        x,
        y,
        arcade.color.WHITE,
        FONT_SIZE
    )

    arcade.draw_text(
        f"Enemies: {len(game.enemy_list)}",
        x,
        y - LINE_HEIGHT,
        arcade.color.WHITE,
        FONT_SIZE
    )

    arcade.draw_text(
        f"Ammo: {game.max_bullets - game.bullet_count} / {game.max_bullets}",
        x,
        y - LINE_HEIGHT * 2,
        arcade.color.WHITE,
        FONT_SIZE
    )

# -------------------------
# GAME OVER SCREEN
# -------------------------
def draw_game_over(game):
    cx = game.width * 0.5
    cy = game.height * 0.5

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
        f"Score: {int(game.score)}",
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
