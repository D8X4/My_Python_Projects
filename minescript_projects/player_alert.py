from minescript import *
import math
import time

player = player_position()
#entity.minecraft.player
mob_list = entities()
while True:
    player = player_position()
    mob_list = entities()
    for mob in mob_list:
        if mob.type == "entity.minecraft.player":
            px = player[0]
            py = player[2]
            ex = mob.position[0]
            ey = mob.position[2]

            nx = ex - px
            ny = ey - py

            distance = math.sqrt(nx ** 2 + ny ** 2)
            if distance <= 50:
                echo(f"player: {mob.name} is {distance:.1f} away")


    time.sleep(3)
