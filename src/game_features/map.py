from src.game_features.blocks_classes import *


def create_map(world_width, world_height, win, edit):
    blocks = []
    try:
        with open(r"game_features\levels\level1.txt", "r") as level:
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
                        block = Block(
                            Point(x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2))
                        block.draw(win)
                    elif char == "F":
                        block = Finish(
                            Point(x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2))
                        block.draw(win)
                    elif char == "S":
                        block = Spike(
                            Point(x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2))
                        block.draw(win)
                    elif char == "P":
                        block = Start(
                            Point(x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2))
                        start_block = block
                        if edit:
                            block.draw(win)
                    elif char == "W":
                        block = Walk_through_block(
                            Point(x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2))
                        block.draw(win)
                    elif char == "D":
                        block = Double_jump(
                            Point(x * Block.WIDTH - Block.WIDTH / 2, y * Block.HEIGHT + Block.HEIGHT / 2))
                        block.draw(win)
                    else:
                        block = None

                    if not block is None:
                        blocks_col.append(block)

                world_height += 1
                blocks.append(blocks_col)

    except Exception as e:
        print(f"created a blank level due to {e}")

    return blocks, world_width, world_height, start_block, win


def change_finish_line_states(blocks, Finish, world_height):
    for y, line in enumerate(blocks):
        for x, block in enumerate(line):
            if type(block) is Finish:
                state = 0
                if y == 0:
                    state = 2
                elif y == world_height:
                    state = 1

                block.change_state(state)
    return blocks
