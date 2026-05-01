from minescript import *
import time
import math

# ============================================================
#  AUTO MINER - Full Script
#  Order of operations:
#  1. Scan 50-block radius for ores -> save to file
#  2. Switch to pickaxe
#  3. Dig down to Y = -12
#  4. For each saved ore:
#       match_y -> match_x -> match_z -> mine_ore
# ============================================================

ORES_FILE = 'ores'
MAX_DEPTH = -55  # never go below this Y level

# ── Mining speed ───────────────────────────────────────────────
# Uncomment the one that matches your pickaxe situation.
# Efficiency pickaxe (~0.6s per deepslate block):
MINE_TIME = 0.6
# No efficiency (~2.0s per deepslate block):
#MINE_TIME = 2.0

ORE_LIST = [
    #'minecraft:ancient_debris',
    #'minecraft:emerald_ore',
    'minecraft:deepslate_diamond_ore',
    #'minecraft:deepslate_emerald_ore',
    'minecraft:diamond_ore',
    #'minecraft:lapis_lazuli_ore',
    #'minecraft:deepslate_lapis_lazuli_ore',
    #'minecraft:coal_ore'
    # Uncomment below to also collect iron:
    # 'minecraft:iron_ore',
    # 'minecraft:deepslate_iron_ore',
]

# ============================================================
#  STEP 1 — Scan for ores and save coords to file
# ============================================================
echo("Scanning for ores...")

player = player_position()
px = int(player[0])
py = int(player[1])
pz = int(player[2])

SCAN_RADIUS = 25  # reduce if you want even tighter targeting

region = get_block_region(
    [px - SCAN_RADIUS, py - SCAN_RADIUS, pz - SCAN_RADIUS],
    [px + SCAN_RADIUS, py + SCAN_RADIUS, pz + SCAN_RADIUS]
)

# Collect all ore coords first, then sort by distance before saving
ore_coords = []
for x in range(region.min_pos[0], region.max_pos[0]):
    for y in range(region.min_pos[1], region.max_pos[1]):
        for z in range(region.min_pos[2], region.max_pos[2]):
            block = region.get_block(x, y, z)
            if block is None:
                continue
            if block in ORE_LIST:
                if y < MAX_DEPTH:
                    continue  # skip anything below max depth
                dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                ore_coords.append((dist, x, y, z))

# Sort closest first
ore_coords.sort(key=lambda e: e[0])

# Write sorted list to file
with open(ORES_FILE, 'w') as f:
    for entry in ore_coords:
        _, x, y, z = entry
        f.write(f"{x},{y},{z}\n")

echo(f"Scan complete — {len(ore_coords)} ore blocks saved, sorted closest first.")

# ============================================================
#  STEP 2 — Switch to pickaxe
# ============================================================
def pickaxeswitcher():
    items = player_inventory()
    for item in items:
        if "pickaxe" in item.item:
            player_inventory_select_slot(item.slot)
            echo(f"Switched to {item.item}")
            return
    echo("WARNING: No pickaxe found in inventory!")

# ============================================================
#  STEP 3 — Dig straight down to Y = -12
# ============================================================
def digdown():
    echo("Digging down to Y=-55...")
    player_set_orientation(0, 90)
    player_press_attack(True)
    while True:
        py = int(player_position()[1])
        if py <= -12:
            break
        if py <= MAX_DEPTH:
            echo(f"Hit max depth during digdown, stopping.")
            break
        if get_block(int(player_position()[0]), py - 1, int(player_position()[2])) == "minecraft:bedrock":
            echo("Bedrock detected below, stopping digdown.")
            break
        time.sleep(0.1)
    player_press_attack(False)
    echo("Reached target depth!")

# ============================================================
#  HELPERS — Lava / void safety check
# ============================================================
def is_safe(px, py, pz):
    # Hard depth limit — stop immediately if at or below max depth
    if py <= MAX_DEPTH:
        echo(f"STOP: At max depth {py}, refusing to go deeper.")
        player_press_forward(False)
        player_press_attack(False)
        return False

    block_below = get_block(px, py - 1, pz)
    block_at    = get_block(px, py,     pz)

    BEDROCK = "minecraft:bedrock"
    if block_below in ("minecraft:lava", "minecraft:flowing_lava"):
        echo("DANGER: Lava below! Stopping.")
        player_press_forward(False)
        return False
    if block_at in ("minecraft:lava", "minecraft:flowing_lava"):
        echo("DANGER: Lava at feet! Stopping.")
        player_press_forward(False)
        return False
    if block_below == BEDROCK:
        echo("DANGER: Bedrock below! Stopping.")
        player_press_forward(False)
        player_press_attack(False)
        return False
    if block_at == BEDROCK:
        echo("DANGER: Standing on bedrock! Stopping.")
        player_press_forward(False)
        player_press_attack(False)
        return False
    return True

# ============================================================
#  HELPER — Escape corners and re-center on block
# ============================================================
_last_pos = [None, None]  # [position, unchanged_count]

def recenter():
    """
    Detects when the player is genuinely stuck (position hasn't changed
    across multiple iterations) and shuffles them toward open space.
    Only triggers on actual stuck situations, not normal tunneling.
    """
    global _last_pos
    pos = player_position()
    px, py, pz = round(pos[0], 1), round(pos[1], 1), round(pos[2], 1)
    AIR = ("minecraft:air", "minecraft:cave_air", "minecraft:void_air")

    # Track how many iterations the position has been unchanged
    if _last_pos[0] == (px, py, pz):
        _last_pos[1] += 1
    else:
        _last_pos[0] = (px, py, pz)
        _last_pos[1] = 0

    # Only act if we've been stuck in the same spot for 3+ iterations
    if _last_pos[1] >= 3:
        echo("Stuck detected, finding escape direction...")
        ipx, ipy, ipz = int(pos[0]), int(pos[1]), int(pos[2])
        sides = [
            (0,   ipx,     ipz + 1),
            (180, ipx,     ipz - 1),
            (-90, ipx + 1, ipz    ),
            (90,  ipx - 1, ipz    ),
        ]
        for yaw, nx, nz in sides:
            if (get_block(nx, ipy + 1, nz) in AIR and
                    get_block(nx, ipy, nz) in AIR):
                player_set_orientation(yaw, 0)
                player_press_forward(True)
                time.sleep(0.4)
                player_press_forward(False)
                time.sleep(0.1)
                _last_pos[1] = 0  # reset counter after escape
                return

        # All sides blocked — try jumping
        player_press_jump(True)
        time.sleep(0.4)
        player_press_jump(False)
        _last_pos[1] = 0

    # Basic wall-hug nudge (independent of stuck detection)
    off_x = abs((pos[0] % 1.0) - 0.5)
    off_z = abs((pos[2] % 1.0) - 0.5)
    if off_x > 0.35 or off_z > 0.35:
        player_set_orientation(180, 0)
        player_press_forward(True)
        time.sleep(0.2)
        player_press_forward(False)
        time.sleep(0.1)
        player_set_orientation(0, 0)
        player_press_forward(True)
        time.sleep(0.15)
        player_press_forward(False)
        time.sleep(0.1)

# ============================================================
#  HELPER — Pillar up one block using offhand blocks
# ============================================================
def has_offhand_blocks():
    """Returns True if the offhand slot has any placeable block."""
    items = player_inventory()
    for item in items:
        # Offhand slot is slot 40 in Minecraft's inventory numbering
        if item.slot == 40 and item.item != "minecraft:air" and item.count > 0:
            return True
    return False


def pillar_step_up():
    """
    ULTRA-SPEED Vertical Pillar Logic:
    Minimizes delays between mining, jumping, and placing.
    """
    p = player_position()
    # Floor coordinates to ensure we stay centered on the pillar
    px, py, pz = int(p[0]), int(p[1]), int(p[2])

    # 1. Clear Headroom (Flick Up)
    # Start mining immediately as the camera moves to the ceiling
    player_set_orientation(0, -90)
    player_press_attack(True)

    # Tightened mining window for 2 blocks above
    # Assuming Efficiency pickaxe based on current MINE_TIME
    time.sleep(MINE_TIME * 1.05)
    player_press_attack(False)

    # 2. Position for Placement (Flick Down)
    player_set_orientation(0, 90)

    # 3. The Rapid Pillar Maneuver
    player_press_jump(True)
    # Placements occur at the very start of the jump arc for speed
    time.sleep(0.12)

    player_press_use(True)
    time.sleep(0.02)  # Micro-press for block placement
    player_press_use(False)

    player_press_jump(False)

    # 4. Minimal Recovery
    # Quick hand-off back to the match_y loop
    time.sleep(0.05)
    return True

def match_x(ox):
    while True:
        pos = player_position()
        px  = int(pos[0])
        py  = int(pos[1])
        pz  = int(pos[2])

        if not is_safe(px, py, pz):
            break

        recenter()

        if ox - px > 1:
            # Need to go East (negative X direction = yaw -90)
            player_set_orientation(-90, 0)
            player_press_attack(True)
            time.sleep(MINE_TIME)
            player_press_attack(False)
            player_set_orientation(-90, 30)
            player_press_attack(True)
            time.sleep(MINE_TIME)
            player_press_attack(False)
            player_press_forward(True)
            time.sleep(0.5)
            player_press_forward(False)

        elif px - ox > 1:
            # Need to go West (yaw 90)
            player_set_orientation(90, 0)
            player_press_attack(True)
            time.sleep(MINE_TIME)
            player_press_attack(False)
            player_set_orientation(90, 30)
            player_press_attack(True)
            time.sleep(MINE_TIME)
            player_press_attack(False)
            player_press_forward(True)
            time.sleep(0.5)
            player_press_forward(False)

        else:
            echo("X matched.")
            break

# ============================================================
#  STEP 4b — Match Z axis (mine north/south)
# ============================================================
def match_z(oz):
    while True:
        pos = player_position()
        px  = int(pos[0])
        py  = int(pos[1])
        pz  = int(pos[2])

        if not is_safe(px, py, pz):
            break

        recenter()

        if oz - pz > 1:
            # Need to go South (yaw 0)
            player_set_orientation(0, 0)
            player_press_attack(True)
            time.sleep(MINE_TIME)
            player_press_attack(False)
            player_set_orientation(0, 30)
            player_press_attack(True)
            time.sleep(MINE_TIME)
            player_press_attack(False)
            player_press_forward(True)
            time.sleep(0.5)
            player_press_forward(False)

        elif pz - oz > 1:
            # Need to go North (yaw 180)
            player_set_orientation(180, 0)
            player_press_attack(True)
            time.sleep(MINE_TIME)
            player_press_attack(False)
            player_set_orientation(180, 30)
            player_press_attack(True)
            time.sleep(MINE_TIME)
            player_press_attack(False)
            player_press_forward(True)
            time.sleep(0.5)
            player_press_forward(False)

        else:
            echo("Z matched.")
            break

# ============================================================
#  STEP 4c — Match Y axis (staircase up or down)
# ============================================================
def match_y(oy):
    AIR   = ("minecraft:air", "minecraft:cave_air", "minecraft:void_air")
    LAVA  = ("minecraft:lava", "minecraft:flowing_lava")

    while True:
        pos = player_position()
        px  = int(pos[0])
        py  = int(pos[1] - 1)
        pz  = int(pos[2])

        if not is_safe(px, py, pz):
            break

        recenter()

        if oy - py > 1:
            # ── NEED TO GO UP — pillar straight up ─────────────────────
            pillar_step_up()
            continue

        elif py - oy > 1:
            # ── NEED TO GO DOWN — dig straight down ────────────────────
            if py <= MAX_DEPTH:
                echo(f"At max depth ({MAX_DEPTH}), stopping.")
                break

            # Lava check — don't mine into lava below
            block_below = get_block(px, py - 1, pz)
            if block_below in LAVA:
                echo("Lava below! Cannot go down here, skipping.")
                break

            # Cave/void check — if it's already a big drop, don't just fall in
            if block_below in AIR:
                # Look down into the void and count how far the drop is
                drop = 0
                for i in range(1, 10):
                    if get_block(px, py - i, pz) not in AIR:
                        break
                    drop += 1
                if drop >= 4:
                    echo(f"Cave detected below ({drop} block drop), skipping.")
                    break
                else:
                    # Small drop, safe to fall
                    echo("Short drop, falling...")
                    player_press_forward(False)
                    time.sleep(0.8)
            else:
                # Solid block below — mine straight down
                echo("Digging down...")
                player_set_orientation(0, 90)
                player_press_attack(True)
                time.sleep(MINE_TIME)
                player_press_attack(False)
                time.sleep(0.1)
            continue

        else:
            echo("Y matched.")
            break


# ============================================================
#  STEP 4d — Mine the ore (scan small radius, look-at and attack)
# ============================================================

MAX_REACH = 3.5  # stay well inside Minecraft's 4.5 block reach limit

# player_look_at aims at the corner of a block by default.
# Adding 0.5 to each axis centers the crosshair on the block face.
def look_at_center(bx, by, bz):
    player_look_at(bx + 0.5, by + 0.5, bz + 0.5)

def dist_to(bx, by, bz):
    pos = player_position()
    return math.sqrt((bx - pos[0])**2 + (by - pos[1])**2 + (bz - pos[2])**2)

def walk_closer(bx, by, bz):
    """Face the block and walk toward it until within reach."""
    echo(f"Too far ({dist_to(bx,by,bz):.1f} blocks), walking closer...")
    dx = bx - int(player_position()[0])
    dz = bz - int(player_position()[2])
    yaw = math.degrees(math.atan2(-dx, dz))
    player_set_orientation(yaw, 0)
    # Walk in short steps until close enough
    for _ in range(6):
        if dist_to(bx, by, bz) <= MAX_REACH:
            break
        player_press_forward(True)
        time.sleep(0.3)
        player_press_forward(False)
        time.sleep(0.1)

def mine_block_safe(bx, by, bz, timeout=4):
    """Walk closer if needed, then look at center and mine until gone or timeout."""
    if dist_to(bx, by, bz) > MAX_REACH:
        walk_closer(bx, by, bz)
    look_at_center(bx, by, bz)
    player_press_attack(True)
    start = time.time()
    while time.time() - start < timeout:
        if get_block(bx, by, bz) not in ORE_LIST:
            break
        time.sleep(0.1)
    player_press_attack(False)

def find_nearby_ore(cx, cy, cz, radius=3):
    """Scan a cube radius around coords, return list of all ore blocks found."""
    found = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                bx, by, bz = cx + dx, cy + dy, cz + dz
                if get_block(bx, by, bz) in ORE_LIST:
                    found.append((bx, by, bz))
    return found

def pickup_loop():
    """Walk a star pattern to collect all nearby item drops."""
    pos = player_position()
    cx, cz = pos[0], pos[2]
    for yaw, dur in [(0, 0.5), (180, 1.0), (90, 0.5), (270, 1.0), (0, 0.5)]:
        player_set_orientation(yaw, 0)
        player_press_forward(True)
        time.sleep(dur)
        player_press_forward(False)
        time.sleep(0.1)

def mine_ore(ox, oy, oz):
    echo(f"Mining ore at {ox}, {oy}, {oz}...")

    # Mine the initial target block
    mine_block_safe(ox, oy, oz, timeout=5)

    # Keep scanning until the entire vein is cleared
    # Use a wider 3-block radius and reposition toward blocks that are out of reach
    no_ore_rounds = 0
    while no_ore_rounds < 2:  # require 2 clean scans before giving up
        pos = player_position()
        px, py, pz = int(pos[0]), int(pos[1]), int(pos[2])

        ore_blocks = find_nearby_ore(px, py, pz, radius=3)

        if not ore_blocks:
            no_ore_rounds += 1
            time.sleep(0.2)
            continue

        no_ore_rounds = 0  # reset if we found something
        for bx, by, bz in ore_blocks:
            if get_block(bx, by, bz) not in ORE_LIST:
                continue  # already mined since we built the list
            d = dist_to(bx, by, bz)
            if d > MAX_REACH:
                # Walk toward it before mining
                walk_closer(bx, by, bz)
            mine_block_safe(bx, by, bz, timeout=4)

    # Final check — if original block somehow still exists hit it again
    if get_block(ox, oy, oz) in ORE_LIST:
        echo("Original ore still there, mining again...")
        mine_block_safe(ox, oy, oz, timeout=5)

    # Walk a proper pickup loop so no drops get left on the ground
    echo("Collecting drops...")
    pickup_loop()
    echo("Ore vein cleared, moving on.")


# ============================================================
#  MAIN — Run everything
# ============================================================
pickaxeswitcher()
digdown()

echo("Starting ore navigation...")

with open(ORES_FILE, 'r') as f:
    ore_lines = f.readlines()

for line in ore_lines:
    line = line.strip()
    if not line:
        continue

    coords = line.split(',')
    ox = int(coords[0])
    oy = int(coords[1])
    oz = int(coords[2])

    # Skip if already mined or never existed
    if get_block(ox, oy, oz) not in ORE_LIST:
        echo(f"Skipping {ox},{oy},{oz} — already mined.")
        continue

    # Refresh player position for each ore target
    pos = player_position()
    px  = int(pos[0])
    py  = int(pos[1])
    pz  = int(pos[2])

    echo(f"Heading to ore at {ox}, {oy}, {oz} | Current: {px}, {py}, {pz}")

    match_y(oy)
    match_x(ox)
    match_z(oz)
    mine_ore(ox, oy, oz)

echo("All ores mined! Script complete.")