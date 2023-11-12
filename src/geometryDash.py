from graphics import _root as root
from keyboard import is_pressed

from src.game_features.player import Player
from src.game_features.screen import *
from src.game_features.map import *

TARGETED_FRAME_RATE = 60
blocks = []

# DEBUG ONLY - CREATE A FLOOR
# FLOOR_HEIGHT = 5*Block.HEIGHT
# for y in range(win.getHeight(), win.getHeight()-FLOOR_HEIGHT, -Block.HEIGHT):
#     blocksCol = []
#     for x in range(0, win.getWidth(), Block.WIDTH):
#         block = Block(Point(x+Block.WIDTH/2, y-Block.HEIGHT/2))
#         block.draw(win)
#         blocksCol.append(block)
#     blocks[int(y/Block.HEIGHT)-1] = blocksCol

autoMove = 0
AUTO_MOVE_COOL = 0.05
if __name__ == "__main__":
    moved = 0
    world_width = 0
    world_height = 0
    start_block = None

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    win = GraphWin("geometry dash", width, height, autoflush=False)
    win.master.geometry('%dx%d+%d+%d' % (width, height, 0, 0))
    win.setBackground("#333")

    blocks, world_width, world_height, start_block, win = create_map(world_width, world_height, win, False)
    blocks = change_finish_line_states(blocks, Finish, world_height)

    player = Player(
        Point(start_block.getCenter().x - Block.WIDTH / 2, start_block.getCenter().y - Block.HEIGHT / 2))
    player.draw(win)

    start = time.time()
    while True:
        fElapsedTime = time.time() - start

        sleep_time = 1 / TARGETED_FRAME_RATE - fElapsedTime
        if sleep_time < 0:
            sleep_time = 0

        if autoMove + AUTO_MOVE_COOL <= time.time():
            moved, player, win = move_screen_right(moved, player, blocks, Player, world_width, win, Finish)
            autoMove = time.time()

        player.last_moved_dir = None

        player.check_gravity(world_width, moved, blocks)
        player.check_spikes(blocks, world_width, moved)

        if is_pressed("Space"):
            player.jump(blocks)

        moved, player, win = player.check_inside_block(blocks, moved, Player, world_width, win, Finish)

        win.update()

        time.sleep(sleep_time)
        start = time.time()
