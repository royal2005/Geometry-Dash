from graphics import *


class Block(Image):
    WIDTH, HEIGHT = 20, 20
    SOLID = True
    KILLS = False
    JUMP_ABLE = True

    def __init__(self, p):
        super().__init__(p, "game_features/images/block.png")

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
    STATES = {0: r"game_features\images\Finish_middle.png",
              1: r"game_features\images\Finish_bottom.png",
              2: r"game_features\images\Finish_top.png"}

    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __init__(self, p):
        super().__init__(p, r"game_features\images\Finish_middle.png")
        self.state = 0

    def __repr__(self):
        return "Finish line"

    def change_state(self, new_state):
        # states:
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
        super().__init__(p, r"game_features\images\Spike.png")


class Start(Circle):
    RADIUS = 10
    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __init__(self, center):
        super().__init__(center, self.RADIUS)
        self.setFill("blue")
        self.setOutline("#555")


class Walk_through_block(Image):
    WIDTH, HEIGHT = 20, 20
    SOLID = False
    KILLS = False
    JUMP_ABLE = False

    def __init__(self, p):
        super().__init__(p, r"game_features\images\block.png")


class Double_jump(Image):
    WIDTH, HEIGHT = 20, 20
    SOLID = False
    KILLS = False
    JUMP_ABLE = True

    def __init__(self, p):
        super().__init__(p, r"game_features\images\double_jump_block.png")
