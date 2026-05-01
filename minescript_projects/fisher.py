from minescript import *
import time




#main loop
while True:
    #cast that mf out
    player_press_use(True)
    time.sleep(0.1)
    player_press_use(False)

    #wait for that fish bite
    while True:
        fish = entities()
        for thing in fish:
            if thing.name and "!!" in thing.name:
                player_press_use(True)
                time.sleep(0.1)
                player_press_use(False)
                break
        else:
            time.sleep(0.5)
            continue
        break
