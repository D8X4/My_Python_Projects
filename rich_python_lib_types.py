from click import style
from rich import print

from rich.console import Console
c = Console()

#simple panel
from rich.panel import Panel
c.print(Panel('first rich project'))
c.print(Panel('[bold green] scan complete[/bold green]',title='results'))
c.print(Panel.fit('Fits to content width'))

#complicated panel
from rich.panel import Panel
from rich.align import Align
from rich import box

box_styles = {'box.DOUBLE',          # ╔══╗ double line
'box.ROUNDED',        # ╭──╮ rounded corners
'box.HEAVY',           # ┏━━┓ thick lines
'box.SQUARE',          # ┌──┐ normal square
'box.MINIMAL',         # no corners, just lines
'box.SIMPLE',        # very minimal
'box.HORIZONTALS',    # only horizontal lines
'box.ASCII'           # +--+ pure ASCII]
              }
c.print(Panel(Align.center("Network Recon Tool v1.0"), box=box.DOUBLE))

from rich.table import Table
t = Table(title='results test')
#simple table
t.add_column('host', style='cyan')
t.add_column('port', style='green')
t.add_column('rtt', style='blue')

t.add_row('8.8.8.8', "UP", '4.1ms')
t.add_row('1.1.1.1', "UP", '100ms')
t.add_row('192.168.1.254', '[red]DOWN[/red]', 'n/a')



c.print(t)

#rule header
from rich.rule import Rule
c.print(Rule('network scanner'))
c.print(Rule())

#progress bar automatic
from rich.progress import track
import time
for item in track(range(100), description='scanning...'):
    time.sleep(0.01)

#manual progress control
from rich.progress import Progress
with Progress() as progress:
    task = progress.add_task('scanning...', total=100)
    for i in range(100):
        progress.update(task, advance=1)
        time.sleep(0.01)

c.print(Panel('[green]scan complete[/green]'))

colors = [
    # standard
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    # bright
    "bright_black", "bright_red", "bright_green", "bright_yellow",
    "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
    # named
    "aquamarine1", "aquamarine3", "blue_violet", "cadet_blue",
    "chartreuse1", "chartreuse2", "chartreuse3", "chartreuse4",
    "cornflower_blue", "cornsilk1", "dark_blue", "dark_cyan",
    "dark_goldenrod", "dark_green", "dark_khaki", "dark_magenta",
    "dark_olive_green1", "dark_olive_green2", "dark_olive_green3",
    "dark_orange", "dark_orange3", "dark_red", "dark_sea_green",
    "dark_sea_green1", "dark_sea_green2", "dark_sea_green3", "dark_sea_green4",
    "dark_slate_gray1", "dark_slate_gray2", "dark_slate_gray3",
    "dark_turquoise", "dark_violet", "deep_pink1", "deep_pink2",
    "deep_pink3", "deep_pink4", "deep_sky_blue1", "deep_sky_blue2",
    "deep_sky_blue3", "deep_sky_blue4", "dodger_blue1", "dodger_blue2",
    "dodger_blue3", "gold1", "gold3", "green1", "green3", "green4",
    "green_yellow", "grey0", "grey100", "grey11", "grey15", "grey19",
    "grey23", "grey27", "grey3", "grey30", "grey35", "grey37", "grey39",
    "grey42", "grey46", "grey50", "grey53", "grey54", "grey58", "grey62",
    "grey63", "grey66", "grey69", "grey7", "grey70", "grey74", "grey78",
    "grey82", "grey84", "grey85", "grey89", "grey93", "hot_pink",
    "hot_pink2", "hot_pink3", "indian_red", "indian_red1", "khaki1",
    "khaki3", "light_coral", "light_cyan1", "light_cyan3",
    "light_goldenrod1", "light_goldenrod2", "light_goldenrod3",
    "light_pink1", "light_pink3", "light_pink4", "light_salmon1",
    "light_salmon3", "light_sea_green", "light_sky_blue1", "light_sky_blue3",
    "light_sky_blue4", "light_slate_blue", "light_slate_grey",
    "light_steel_blue", "light_steel_blue1", "light_steel_blue3",
    "light_yellow3", "magenta1", "magenta2", "magenta3",
    "medium_orchid", "medium_orchid1", "medium_orchid3",
    "medium_purple", "medium_purple1", "medium_purple2",
    "medium_purple3", "medium_purple4", "medium_spring_green",
    "medium_turquoise", "medium_violet_red", "misty_rose1", "misty_rose3",
    "navajo_white1", "navajo_white3", "navy_blue", "orange1", "orange3",
    "orange4", "orange_red1", "orchid", "orchid1", "orchid2",
    "pale_green1", "pale_green3", "pale_turquoise1", "pale_turquoise4",
    "pale_violet_red1", "pink1", "pink3", "plum1", "plum2", "plum3", "plum4",
    "purple", "purple3", "purple4", "red1", "red3", "rosy_brown",
    "royal_blue1", "salmon1", "sandy_brown", "sea_green1", "sea_green2",
    "sea_green3", "sky_blue1", "sky_blue2", "sky_blue3", "slate_blue1",
    "slate_blue3", "spring_green1", "spring_green2", "spring_green3",
    "spring_green4", "steel_blue", "steel_blue1", "steel_blue3",
    "tan", "thistle1", "thistle3", "turquoise2", "turquoise4",
    "violet", "wheat1", "wheat4", "yellow1", "yellow2", "yellow3",
    "yellow4", "yellow_green"
]
