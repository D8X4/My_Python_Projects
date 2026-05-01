from minescript import *
import time
import math

#list of hostile mobs
hostile_mobs = [
    'entity.minecraft.zombie',
    'entity.minecraft.skeleton',
    'entity.minecraft.creeper',
    'entity.minecraft.slime',
    'entity.minecraft.spider',
    'entity.minecraft.witch',
    'entity.minecraft.pillager',
    'entity.minecraft.ravager',
    'entity.minecraft.vindicator',
    'entity.minecraft.evoker',
    'entity.minecraft.blaze',
    'entity.minecraft.ghast',
    'entity.minecraft.magma_cube',
    'entity.minecraft.zombified_piglin',
    'entity.minecraft.wither_skeleton',
    'entity.minecraft.enderman',
    'entity.minecraft.endermite',
    'entity.minecraft.silverfish',
    'entity.minecraft.guardian',
    'entity.minecraft.elder_guardian',
    'entity.minecraft.phantom',
    'entity.minecraft.drowned',
    'entity.minecraft.husk',
    'entity.minecraft.stray',
    'entity.minecraft.cave_spider',
    'entity.minecraft.piglin_brute',
    'entity.minecraft.warden',
    'entity.minecraft.ender_dragon',
    'entity.minecraft.wither',
    'entity.minecraft.shulker',
    'entity.minecraft.hoglin',
    'entity.minecraft.zoglin',
    'entity.minecraft.piglin',
]
while True:
    # gets tje emtities
    mob_list = entities()


    #gets player position
    player = player_position()
    x = player[0]
    y = player[2]
    pc = x, y



#main logic
#gathers all mobs in entities()
    for mob in mob_list:
        #scrolls through list
        if mob.type in hostile_mobs:
            #gets entity position
            mx = mob.position[0]
            my = mob.position[2]
            #calculation for distance
            nx = mx - x
            ny = my - y
            # gets radius
            distance = math.sqrt(nx**2 + ny**2)
            #prints to me the name, health, distance
            if distance <= 30:
                echo(f"name: {mob.name} health: {mob.health} distance: x:{nx:.1f}, y:{ny:.1f}")
    time.sleep(5)