from graphics import *
from graphics import _root as root
from keyboard import is_pressed
import time
import math
import tkinter


class Block(Image):
    WIDTH, HEIGHT = 20, 20
    SOLID = True
    KILLS = False
    JUMP_ABLE = True

    def __init__(self, p):
        super().__init__(p, "images/block.png")

    def __repr__(self):
        return "block"


class Air:
    WIDTH, HEIGHT = 20, 20
    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __repr__(self):
        return "Air"


class Finish(Image):
    WIDTH, HEIGHT = 20, 20
    STATES = {0: "images/Finish_middle.png",
              1: "images/Finish_bottom.png",
              2: "images/Finish_top.png"}

    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __init__(self, p):
        super().__init__(p, "images/Finish_middle.png")
        self.state = 0

    def __repr__(self):
        return "Finish line"

    def change_state(self, new_state):
        #states:
        # 0: middle, 1: bottom, 2: top

        canvas = self.canvas
        self.undraw()
        super().__init__(self.getAnchor(), self.STATES[new_state])
        self.draw(canvas)

        self.state = new_state


class Spike(Image):
    SOLID = False
    KILLS = True
    JUMP_ABLE = False

    def __init__(self, p):
        super().__init__(p, "images/Spike.png")


class Start(Circle):
    RADIUS = 10
    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __init__(self, center):
        super().__init__(center, self.RADIUS)
        self.setFill("blue")
        self.setOutline("#555")


class Double_jump(Image):
    WIDTH, HEIGHT = 20, 20
    SOLID = False
    KILLS = False
    JUMP_ABLE = True

    def __init__(self, p):
        super().__init__(p, "images/double_jump_block.png")


class Walk_through_block(Image):
    WIDTH, HEIGHT = 20, 20
    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __init__(self, p):
        super().__init__(p, "images/walk_through_block.png")


def create_map(level_name):
    global blocks, world_width, world_height, start_block
    blocks.clear()

    try:
        with open(f"levels/{level_name}.dash", "r") as level:
            y = -1
            while True:
                line = level.readlines(1)
                if world_width == 0:
                    world_width = len(line[0])
                if len(line) > 0:
                    line = line[0]
                else:
                    break

                y += 1

                blocks_col = []
                x = 0
                for char in line:
                    x += 1
                    if char == "A":
                        block = Air()
                    elif char == "B":
                        block = Block(Point(x*Block.WIDTH-Block.WIDTH/2, y*Block.HEIGHT+Block.HEIGHT/2))
                        block.draw(win)
                    elif char == "F":
                        block = Finish(Point(x*Block.WIDTH-Block.WIDTH/2, y*Block.HEIGHT+Block.HEIGHT/2))
                        block.draw(win)
                    elif char == "S":
                        block = Spike(Point(x*Block.WIDTH-Block.WIDTH/2, y*Block.HEIGHT+Block.HEIGHT/2))
                        block.draw(win)
                    elif char == "P":
                        block = Start(Point(x*Block.WIDTH-Block.WIDTH/2, y*Block.HEIGHT+Block.HEIGHT/2))
                        start_block = block
                        block.draw(win)
                    elif char == "W":
                        block = Walk_through_block(Point(x*Block.WIDTH-Block.WIDTH/2, y*Block.HEIGHT+Block.HEIGHT/2))
                        block.draw(win)
                    elif char == "D":
                        block = Double_jump(Point(x*Block.WIDTH-Block.WIDTH/2, y*Block.HEIGHT+Block.HEIGHT/2))
                        block.draw(win)
                    else:
                        block = None

                    if not block is None:
                        blocks_col.append(block)

                world_height += 1
                blocks.append(blocks_col)

    except Exception as e:
        print(f"created a blank level due to {e}")
        blocks = [[Air() for i in range(0, win.getWidth(), Block.WIDTH)] for ii in range(0, win.getHeight(), Block.HEIGHT)]


def move_screen_right():
    for item in win.items:
        item.move(-20, 0)


def move_screen_left():
    for item in win.items:
        item.move(20, 0)


def change_finish_line_states():
    global blocks

    for y, line in enumerate(blocks):
        for x, block in enumerate(line):
            if type(block) is Finish:
                state = 0
                if y == 0:
                    state = 2
                elif y == world_height:
                    state = 1

                block.change_state(state)


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

    create_map(level_name)
    change_finish_line_states()

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
                change_finish_line_states()

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