from minescript import *
player = player_position()
px = int(player[0])
py = int(player[1])
pz = int(player[2])

for x in range(px-3, px+3):
    for y in range(py-3, py+3):
        for z in range(pz-3, pz+3):
            b = get_block(x, y, z)
            if b and b != 'minecraft:air' and b != 'minecraft:grass_block' and b != 'minecraft:dirt':
                echo(b)

