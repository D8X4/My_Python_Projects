from minescript import *
import time
structure_blocks = [
    # Village
    'minecraft:dirt_path',
    'minecraft:bell',
    'minecraft:hay_block',
    'minecraft:composter',
    'minecraft:blast_furnace',
    'minecraft:smoker',
    'minecraft:cartography_table',
    'minecraft:fletching_table',
    'minecraft:grindstone',
    'minecraft:lectern',
    'minecraft:loom',
    'minecraft:smithing_table',
    'minecraft:stonecutter',

    # Dungeon
    'minecraft:mossy_cobblestone',
    'minecraft:spawner',

    # Stronghold
    'minecraft:stone_bricks',
    'minecraft:mossy_stone_bricks',
    'minecraft:cracked_stone_bricks',
    'minecraft:chiseled_stone_bricks',
    'minecraft:iron_bars',
    'minecraft:end_portal_frame',

    # Desert Temple
    'minecraft:orange_terracotta',
    'minecraft:blue_terracotta',
    'minecraft:chiseled_sandstone',
    'minecraft:cut_sandstone',

    # Jungle Temple
    'minecraft:dispenser',
    'minecraft:tripwire_hook',
    'minecraft:vine',

    # Ocean Monument
    'minecraft:prismarine',
    'minecraft:prismarine_bricks',
    'minecraft:dark_prismarine',
    'minecraft:sea_lantern',

    # Nether Fortress
    'minecraft:nether_bricks',
    'minecraft:nether_brick_fence',
    'minecraft:nether_wart',

    # Bastion Remnant
    'minecraft:blackstone',
    'minecraft:gilded_blackstone',
    'minecraft:polished_blackstone',
    'minecraft:polished_blackstone_bricks',

    # End City
    'minecraft:purpur_block',
    'minecraft:purpur_pillar',
    'minecraft:end_stone_bricks',
    'minecraft:chorus_plant',

    # Deep Dark / Ancient City
    'minecraft:sculk',
    'minecraft:sculk_catalyst',
    'minecraft:sculk_sensor',
    'minecraft:sculk_shrieker',
    'minecraft:sculk_vein',
    'minecraft:reinforced_deepslate',
    'minecraft:deepslate_tiles',
    'minecraft:deepslate_tile_stairs',
    'minecraft:deepslate_bricks',
    'minecraft:soul_lantern',
    'minecraft:soul_sand',

    # Woodland Mansion
    'minecraft:dark_oak_log',
    'minecraft:dark_oak_planks',
    'minecraft:dark_oak_stairs',
    'minecraft:dark_oak_slab',
    'minecraft:cobblestone',
    'minecraft:gray_wool',
    'minecraft:white_wool',
    'minecraft:birch_planks',

    # Pillager Outpost
    'minecraft:dark_oak_log',
    'minecraft:dark_oak_planks',
    'minecraft:mossy_cobblestone',
    'minecraft:iron_bars',

    # Shipwreck
    'minecraft:spruce_planks',
    'minecraft:spruce_log',
    'minecraft:spruce_stairs',
    'minecraft:spruce_slab',
    'minecraft:oak_planks',
    'minecraft:oak_log',

    # Ruined Portal
    'minecraft:obsidian',
    'minecraft:crying_obsidian',
    'minecraft:netherrack',
    'minecraft:magma_block',

    # Mineshaft
    'minecraft:oak_planks',
    'minecraft:oak_fence',
    'minecraft:rail',
    'minecraft:chain',
    'minecraft:cobweb',

    # Igloo
    'minecraft:snow_block',
    'minecraft:ice',
    'minecraft:packed_ice',
    'minecraft:blue_ice',
    'minecraft:white_carpet',
    'minecraft:red_carpet',
    'minecraft:spruce_trapdoor',

    # Trail Ruins
    'minecraft:mud_bricks',
    'minecraft:packed_mud',
    'minecraft:suspicious_gravel',
    'minecraft:suspicious_sand',
    'minecraft:terracotta',

    # Trial Chambers
    'minecraft:tuff',
    'minecraft:tuff_bricks',
    'minecraft:chiseled_tuff',
    'minecraft:trial_spawner',
    'minecraft:vault',
    'minecraft:copper_block',
    'minecraft:exposed_copper',
    'minecraft:oxidized_copper',
    'minecraft:copper_grate',
]

#while True:
player = player_position()

px = int(player[0])
py = int(player[1])
pz = int(player[2])

region = get_block_region([px-100, py-100, pz-100], [px+100, py+100, pz+100])
empty = set()

for x in range(region.min_pos[0], region.max_pos[0]):
    for y in range(region.min_pos[1], region.max_pos[1]):
        for z in range(region.min_pos[2], region.max_pos[2]):
            block = region.get_block(x, y, z)
            if block is None:
                continue
            if block in structure_blocks or block.startswith('minecraft:end_portal_frame') or block.startswith('minecraft:nether_portal') or block.startswith('minecraft:iron_bars') or block.startswith('minecraft:trial_spawner') or block.startswith('minecraft:tripwire_hook'):
                base_block = block.split('[')[0]
                if base_block not in empty:
                    empty.add(base_block)
                    if block == 'minecraft:spawner':
                        echo(f"spawner at {x}, {y}, {z}")
                    elif block.startswith('minecraft:trial_spawner'):
                        echo(f"trial chamber at {x}, {y}, {z}")
                    elif block == 'minecraft:packed_mud':
                        echo(f"trial ruins spotted at {x}, {y}, {z}")
                    elif block == "minecraft:white_carpet":
                        echo(f"igloo at {x}, {y}, {z}")
                    elif block == 'minecraft:cobweb':
                        echo(f"mineshaft at {x}, {y}, {z}")
                    elif block == 'minecraft:crying_obsidian':
                        echo(f'ruined portal at {x}, {y}, {z}')
                    elif block == 'minecraft:spruce_slab':
                        echo(f"shipwreck spotted at {x}, {y}, {z}")
                    elif block.startswith('minecraft:iron_bars'):
                        echo(f"pillager outpost at {x}, {y}, {z}")
                    elif block == 'minecraft:gray_wool':
                        echo(f"woodland mansion at {x}, {y}, {z}")
                    elif block == 'minecraft:sculk':
                        echo(f"deep dark at {x}, {y}, {z}")
                    elif block == 'minecraft:end_stone_bricks':
                        echo(f"end city at {x}, {y}, {z}")
                    elif block == 'minecraft:blackstone':
                        echo(f"Bastion at {x}, {y}, {z}")
                    elif block == 'minecraft:nether_bricks':
                        echo(f"nether fortress at {x}, {y}, {z}")
                    elif block == 'minecraft:prismarine':
                        echo(f"ocean monument at {x}, {y}, {z}")
                    elif block.startswith('minecraft:tripwire_hook'):
                        echo(f"jungle temple at {x}, {y}, {z}")
                    elif block == 'minecraft:orange_terracotta':
                        echo(f"desert temple at {x}, {y}, {z}")
                    elif block.startswith('minecraft:end_portal_frame'):
                        echo(f"stronghold at {x}, {y}, {z}")
                    elif block.startswith('minecraft:nether_portal'):
                        echo(f"nether portal at {x}, {y}, {z}")
                    elif block == 'minecraft:dirt_path':
                        echo(f"villiage at {x}, {y}, {z}")

    #time.sleep(10)