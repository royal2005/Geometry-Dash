
from graphics import *
from graphics import _root as root
from keyboard import is_pressed
import time
import math
import tkinter


class Player ( Image ):
    WIDTH, HEIGHT = 40, 40
    VEL = 15

    def __init__(self, p):
        super ().__init__ ( p, "images/player.png" )
        self.x = int ( self.getAnchor ().x / Block.WIDTH )
        self.y = int ( self.getAnchor ().y / Block.HEIGHT )

        self.grav = 0
        self.count = 0

        self.last_moved_dir = None

    def __repr__(self):
        return "Player"

    def check_gravity(self): 
        global blocks
        global world_width
        global moved

        offset_jump_y = 2
        if self.getAnchor ().y % 1!=0:
            offset_jump_y = 1

        # check collision with lower half
        bottom_right = False
        bottom_left = False

        # check collision with higher half
        top_right = False
        top_left = False

        block_state = blocks[self.y + 1][self.x]
        if not block_state.SOLID:
            bottom_right = True

        block_state = blocks[self.y + 1][self.x - 1]
        if not block_state.SOLID:
            bottom_left = True

        block_state = blocks[self.y - offset_jump_y][self.x]
        if block_state.SOLID:
            top_right = True

        block_state = blocks[self.y - offset_jump_y][self.x - 1]
        if block_state.SOLID:
            top_left = True

        if not (bottom_right and bottom_left):
            if self.count > 0:
                self.count = 0
        else:
            self.count += 1 / 60

        if self.count < 0:
            # up
            grav_move = self.count ** 2 * self.VEL / 2 * -1 * 100

        else:
            # down
            grav_move = self.count ** 2 * self.VEL / 2 * 120
        if grav_move > 14:
            grav_move = 14

        if grav_move < 0 and (top_left or top_right):
            exit ( f"you lost you completed {int ( 100 / (world_width / moved) )}% of the level " )

        self.move ( 0, grav_move )

    def check_inside_block(self):
        while True:
            inside = False

            real_y = math.ceil ( self.getAnchor ().y / 20 )
            y = self.y

            for virtual_y in [y, real_y]:
                block_state = blocks[virtual_y][self.x]
                if block_state.SOLID:
                    inside = True

                block_state = blocks[virtual_y - 1][self.x]
                if block_state.SOLID:
                    inside = True

                block_state = blocks[virtual_y][self.x - 1]
                if block_state.SOLID:
                    inside = True

                block_state = blocks[virtual_y - 1][self.x - 1]
                if block_state.SOLID:
                    inside = True

            if inside:
                if self.last_moved_dir is None:
                    player.move ( 0, -1 )
                elif self.last_moved_dir=="right":
                    move_screen_left ()
                elif self.last_moved_dir=="left":
                    move_screen_right ()
            else:
                player.move ( 0, 1 )
                break

    def check_spikes(self):
        global blocks

        y = round ( self.getAnchor ().y / Block.HEIGHT )

        bottom_right = False
        bottom_left = False

        block_state = blocks[y][self.x]
        if block_state.KILLS:
            bottom_right = True

        block_state = blocks[y][self.x - 1]
        if block_state.KILLS:
            bottom_left = True

        if bottom_right or bottom_left:
            exit ( f"you lost you completed {int ( 100 / (world_width / moved) )}% of the level " )

    def jump(self):
        can_jump = False

        block_state = blocks[self.y + 1][self.x]
        if block_state.JUMP_ABLE:
            can_jump = True

        block_state = blocks[self.y + 1][self.x - 1]
        if block_state.JUMP_ABLE:
            can_jump = True

        if can_jump:
            self.count = -1 / 6

    def move(self, dx, dy):
        super ().move ( dx, dy )
        self.y = int ( self.getAnchor ().y / Block.HEIGHT )

    def screen_move(self, dx, dy):
        super ().move ( dx, dy )


class Block ( Image ):
    WIDTH, HEIGHT = 20, 20
    SOLID = True
    KILLS = False
    JUMP_ABLE = True

    def __init__(self, p):
        super ().__init__ ( p, "images/block.png" )

    def __repr__(self):
        return "block"


class Air:
    WIDTH, HEIGHT = 20, 20
    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __repr__(self):
        return "Air"


class Finish ( Image ):
    WIDTH, HEIGHT = 20, 20
    STATES = {0: "images/Finish_middle.png",
              1: "images/Finish_bottom.png",
              2: "images/Finish_top.png"}

    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __init__(self, p):
        super ().__init__ ( p, "images/Finish_middle.png" )
        self.state = 0

    def __repr__(self):
        return "Finish line"

    def change_state(self, new_state):
        # states:
        # 0: middle, 1: bottom, 2: top

        canvas = self.canvas
        self.undraw ()
        super ().__init__ ( self.getAnchor (), self.STATES[new_state] )
        self.draw ( canvas )

        self.state = new_state


class Spike ( Image ):
    SOLID = False
    KILLS = True
    JUMP_ABLE = False

    def __init__(self, p):
        super ().__init__ ( p, "images/Spike.png" )


class Start ( Circle ):
    RADIUS = 10
    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __init__(self, center):
        super ().__init__ ( center, self.RADIUS )
        self.setFill ( "blue" )
        self.setOutline ( "#555" )


class Walk_through_block ( Image ):
    WIDTH, HEIGHT = 20, 20
    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __init__(self, p):
        super ().__init__ ( p, "images/block.png" )


class Double_jump ( Image ):
    WIDTH, HEIGHT = 20, 20
    SOLID = False
    KILLS = False
    JUMP_ABLE = True

    def __init__(self, p):
        super ().__init__ ( p, "images/double_jump_block.png" )


def create_map(level_name):
    global blocks, world_width, world_height, start_block
    blocks.clear ()

    try:
        with open ( f"levels/{level_name}.dash", "r" ) as level:
            y = -1
            while True:
                line = level.readlines ( 1 )
                if world_width==0:
                    world_width = len ( line[0] )
                if len ( line ) > 0:
                    line = line[0]
                else:
                    break

                y += 1

                blocks_col = []
                x = 0
                for char in line:
                    x += 1
                    if char=="A":
                        block = Air ()
                    elif char=="B":
                        block = Block (
                            Point ( x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2 ) )
                        block.draw ( win )
                    elif char=="F":
                        block = Finish (
                            Point ( x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2 ) )
                        block.draw ( win )
                    elif char=="S":
                        block = Spike (
                            Point ( x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2 ) )
                        block.draw ( win )
                    elif char=="P":
                        block = Start (
                            Point ( x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2 ) )
                        start_block = block
                    elif char=="W":
                        block = Walk_through_block (
                            Point ( x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2 ) )
                        block.draw ( win )
                    elif char=="D":
                        block = Double_jump (
                            Point ( x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2 ) )
                        block.draw ( win )
                    else:
                        block = None

                    if not block is None:
                        blocks_col.append ( block )

                world_height += 1
                blocks.append ( blocks_col )

    except Exception as e:
        print ( f"created a blank level due to {e}" )
        blocks = [[Air () for i in range ( 0, win.getWidth (), Block.WIDTH )] for ii in
                  range ( 0, win.getHeight (), Block.HEIGHT )]


def move_screen_right():
    global player, blocks
    global moved
    moved += 1

    bottom_right = False
    top_right = False

    block_state = blocks[player.y][player.x + 1]
    if not block_state.SOLID:
        bottom_right = True
    elif type ( block_state ) is Finish:
        print ( exit ( "You finished the level" ) )

    block_state = blocks[player.y - 1][player.x + 1]
    if not block_state.SOLID:
        top_right = True
    elif type ( block_state ) is Finish:
        print ( exit ( "You finished the level" ) )

    if bottom_right and top_right:
        player.last_moved_dir = "right"
        for item in win.items:
            if not type ( item ) is Player:
                item.move ( -20, 0 )
            else:
                item.x += 1
    else:
        exit ( f"you lost you completed {int ( 100 / (world_width / moved) )}% of the level " )


def move_screen_left():
    global player, blocks
    global moved
    moved -= 1

    bottom_left = False
    top_left = False

    block_state = blocks[player.y][player.x - 2]
    if not block_state.SOLID:
        bottom_left = True

    block_state = blocks[player.y - 1][player.x - 2]
    if not block_state.SOLID:
        top_left = True

    if bottom_left and top_left:
        player.last_moved_dir = "left"
        for item in win.items:
            if not type ( item ) is Player:
                item.move ( 20, 0 )
            else:
                item.x -= 1
    else:
        exit ( f"you lost you completed {int ( 100 / (world_width / moved) )}% of the level " )


def change_finish_line_states():
    global blocks

    for y, line in enumerate ( blocks ):
        for x, block in enumerate ( line ):
            if type ( block ) is Finish:
                state = 0
                if y==0:
                    state = 2
                elif y==world_height:
                    state = 1

                block.change_state ( state )


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
if __name__=="__main__":
    moved = 0
    world_width = 0
    world_height = 0
    start_block = None

    width = root.winfo_screenwidth ()
    height = root.winfo_screenheight ()

    win = GraphWin ( "geometry dash", width, height, autoflush=False )
    win.master.geometry ( '%dx%d+%d+%d' % (width, height, 0, 0) )
    win.setBackground ( "#333" )

    create_map ( "level1" )
    change_finish_line_states ()

    player = Player (
        Point ( start_block.getCenter ().x - Block.WIDTH / 2, start_block.getCenter ().y - Block.HEIGHT / 2 ) )
    player.draw ( win )

    start = time.time ()
    while True:
        fElapsedTime = time.time () - start

        sleep_time = 1 / TARGETED_FRAME_RATE - fElapsedTime
        if sleep_time < 0:
            sleep_time = 0

        if autoMove + AUTO_MOVE_COOL <= time.time ():
            move_screen_right ()
            autoMove = time.time ()

        player.last_moved_dir = None

        player.check_gravity ()
        player.check_spikes ()

        if is_pressed ( "Space" ):
            player.jump ()

        player.check_inside_block ()

        win.update ()

        time.sleep ( sleep_time )
        start = time.time ()