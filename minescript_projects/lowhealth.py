from minescript import *
import time

health = player_health()

while True:
    health = player_health()
    if health <= 10.0:
        echo(f"health low, heal up. Health; {health}")
    time.sleep(2)