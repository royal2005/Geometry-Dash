from src.game_features.blocks_classes import *
from src.game_features.screen import *
import math


class Player(Image):
    WIDTH, HEIGHT = 40, 40
    VEL = 15

    def __init__(self, p):
        super().__init__(p, r"game_features\images\player.png")
        self.x = int(self.getAnchor().x / Block.WIDTH)
        self.y = int(self.getAnchor().y / Block.HEIGHT)

        self.grav = 0
        self.count = 0

        self.last_moved_dir = None

    def __repr__(self):
        return "Player"

    def check_gravity(self, world_width, moved, blocks):

        offset_jump_y = 2
        if self.getAnchor().y % 1 != 0:
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
            exit(f"you lost you completed {int(100 / (world_width / moved))}% of the level ")

        self.move(0, grav_move)

    def check_inside_block(self, blocks, moved, Player, world_width, win, Finish):
        while True:
            inside = False

            real_y = math.ceil(self.getAnchor().y / 20)
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
                    self.move(0, -1)
                elif self.last_moved_dir == "right":
                    moved, self, win = move_screen_left(moved, self, blocks, Player, world_width, win)
                elif self.last_moved_dir == "left":
                    moved, self, win = move_screen_right(moved, self, blocks, Player, world_width, win, Finish)
            else:
                self.move(0, 1)
                break
        return moved, self, win

    def check_spikes(self, blocks, world_width, moved):

        y = round(self.getAnchor().y / Block.HEIGHT)

        bottom_right = False
        bottom_left = False

        block_state = blocks[y][self.x]
        if block_state.KILLS:
            bottom_right = True

        block_state = blocks[y][self.x - 1]
        if block_state.KILLS:
            bottom_left = True

        if bottom_right or bottom_left:
            exit(f"you lost you completed {int(100 / (world_width / moved))}% of the level ")

    def jump(self, blocks):
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
        super().move(dx, dy)
        self.y = int(self.getAnchor().y / Block.HEIGHT)

    def screen_move(self, dx, dy):
        super().move(dx, dy)
