from minescript import *
import json
import time
import math

trees = [
    'minecraft:oak_log',
    'minecraft:birch_log'
]

player = player_position()
px = int(player[0])
py = int(player[1])
pz = int(player[2])

def minelogs(x, y, z, trees):
    player_look_at(x + 0.5, y + 1.0, z + 0.5)
    player_press_attack(True)
    while any(get_block(x,y,z).startswith(t) for t in trees):
        time.sleep(0.1)
    player_press_attack(False)


def walk_to(x, y, z, walktime):
    player_look_at(x, y, z)
    player_press_jump(True)
    player_press_forward(True)
    time.sleep(walktime)
    player_press_jump(False)
    player_press_forward(False)

def scan_trees(px, py, pz):
    found_logs = []
    region = get_block_region([px-10, py-1, pz-10], [px+10, py+6, pz+10])

    for x in range(region.min_pos[0], region.max_pos[0]):

        for y in range(region.min_pos[1], region.max_pos[1]):

            for z in range(region.min_pos[2], region.max_pos[2]):

                block = region.get_block(x, y, z)

                if block is None:
                    continue

                if any(block.startswith(t) for t in trees):
                    #echo(f"found: {block}")
                    found_logs.append({"x": x, "y": y, "z": z})
    return found_logs


while True:
    player = player_position()
    px = int(player[0])
    py = int(player[1])
    pz = int(player[2])
    found_logs = scan_trees(px, py, pz)
    trees_grouped = {}
    for log in found_logs:
        key = (log['x'], log['z'])
        if key not in trees_grouped:
            trees_grouped[key] = []
        trees_grouped[key].append(log['y'])

    f = open("trees.json", "w")
    json.dump(found_logs, f)
    echo(f"scan complete found {len(found_logs)} logs")
    if not found_logs:
        echo("no trees found, done!")
        break

    sorted_trees = sorted(trees_grouped.items(), key=lambda item: math.sqrt((item[0][0] - px)**2 + (item[0][1] - pz)**2))
    for (tx, tz), y_values in sorted_trees:

        dist = math.sqrt((tx - px) ** 2 + (tz - pz) ** 2)
        walk_time = dist / 5
        walk_to(tx, sorted(y_values)[0], tz, walk_time)

        for ty in sorted(y_values):

            player = player_position()

            px = int(player[0])
            py = int(player[1])
            pz = int(player[2])
            horiz_dist = math.sqrt((tx - px) ** 2 + (tz - pz) ** 2)
            if horiz_dist > 4:
                walk_to(tx, ty, tz, horiz_dist / 5)
            if abs(ty - py) > 6:
                continue
            minelogs(tx, ty, tz, trees)
        echo('collecting the goods')
        time.sleep(2)
        player_press_forward(True)
        player_press_jump(True)
        time.sleep(1)
        player_press_forward(False)
        player_press_jump(False)
        player_set_orientation(0,0)
        player_press_forward(True)
        time.sleep(0.5)
        player_press_forward(False)
        player_set_orientation(90,0)
        player_press_forward(True)
        time.sleep(0.5)
        player_press_forward(False)
        player_set_orientation(180,0)
        player_press_forward(True)
        time.sleep(0.5)
        player_press_forward(False)
        player_set_orientation(270,0)
        player_press_forward(True)
        time.sleep(0.5)
        player_press_forward(False)
        echo('switching target')