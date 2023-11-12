
from graphics import _root as root
from keyboard import is_pressed

from blocks_classes import *
from map import *


def move_screen_right():
    for item in win.items:
        item.move(-20, 0)


def move_screen_left():
    for item in win.items:
        item.move(20, 0)


def save_world(level_name):
    with open(f"levels/{level_name}.dash", "w") as world:
        for line in blocks:
            for block in line:
                if type(block) is Air:
                    world.write("A")
                elif type(block) is Block:
                    world.write("B")
                elif type(block) is Spike:
                    world.write("S")
                elif type(block) is Finish:
                    world.write("F")
                elif type(block) is Start:
                    world.write("P")
                elif type(block) is Walk_through_block:
                    world.write("W")
                elif type(block) is Double_jump:
                    world.write("D")
            world.write("\n")



TARGETED_FRAME_RATE = 60
blocks = []
BLOCK_TYPES = [Air, Block, Spike, Walk_through_block, Double_jump, Finish, Start]
level_name = "level1"

if __name__ == "__main__":
    start_block = None

    world_width = 0
    world_height = 0

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    win = GraphWin("geometry dash", width, height, autoflush=False)
    win.master.geometry('%dx%d+%d+%d' % (width, height, 0, 0))
    win.setBackground("#333")

    blocks, world_width, world_height, start_block, win = create_map("level1", world_width, world_height, win, True)
    blocks = change_finish_line_states(blocks, Finish, world_height)

    screen_offset = 0

    start = time.time()
    while True:
        fElapsedTime = time.time() - start

        sleep_time = 1 / TARGETED_FRAME_RATE - fElapsedTime
        if sleep_time < 0:
            sleep_time = 0

        mouse = win.checkMouse()

        if mouse:
            x = int(mouse.getX()/Block.WIDTH)
            y = int(mouse.getY()/Block.HEIGHT)

            x += screen_offset

            try:
                blocks[y][x].undraw()

                block = blocks[y][x]
                t = type(block)

                types_index = BLOCK_TYPES.index(t)
                change_to = BLOCK_TYPES[(types_index + 1) % len(BLOCK_TYPES)]

                if t is Start:
                    start_block = None

                if change_to is Air:
                    block = Air()
                elif change_to is Start:
                    if start_block is None:
                        block = Start(Point((x - screen_offset + 1) * Block.WIDTH - Block.WIDTH / 2,
                                                 y * Block.HEIGHT + Block.HEIGHT / 2))
                        block.draw(win)
                        start_block = block
                    else:
                        block = Air()
                else:
                    block = change_to(Point((x - screen_offset + 1) * Block.WIDTH - Block.WIDTH / 2,
                                             y * Block.HEIGHT + Block.HEIGHT / 2))
                    block.draw(win)

                blocks[y][x] = block
                blocks = change_finish_line_states(blocks, Finish, world_height)

            except IndexError as e:
                pass
            except AttributeError as e:
                if type(blocks[y][x]) is Air:
                    block = Block(Point((x - screen_offset + 1) * Block.WIDTH - Block.WIDTH / 2,
                                         y * Block.HEIGHT + Block.HEIGHT / 2))
                    block.draw(win)
                    blocks[y][x] = block


        if is_pressed('right'):
            move_screen_right()
            screen_offset += 1

        if is_pressed("Left"):
            move_screen_left()
            screen_offset -= 1

        if is_pressed("Esc"):
            save_world(level_name)
            print("saved")


        win.update()

        time.sleep(sleep_time)
        start = time.time()