from minescript import *
player = player_position()
px = int(player[0])
py = int(player[1])
pz = int(player[2])

ores = [
    #'minecraft:iron_ore',
    #'minecraft:deepslate_iron_ore',
    'minecraft:ancient_debris',
    'minecraft:emerald_ore',
    'minecraft:deepslate_diamond_ore',
    'minecraft:deepslate_emerald_ore',
    'minecraft:diamond_ore',
    'minecraft:lapis_lazuli_ore',
    'minecraft:deepslate_lapis_lazuli_ore'
]

region = get_block_region([px-50, py-50, pz-50], [px+50, py+50, pz+50])

for x in range(region.min_pos[0], region.max_pos[0]):

    for y in range(region.min_pos[1], region.max_pos[1]):

        for z in range(region.min_pos[2], region.max_pos[2]):

            block = region.get_block(x, y, z)

            if block is None:
                continue

            if block in ores:
                echo(f"{block} at {x}, {y}, {z}")

