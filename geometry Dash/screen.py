


def move_screen_right(moved, player, blocks, Player, world_width, win, Finish):

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
    return moved, player, win


def move_screen_left(moved, player, blocks, Player, world_width, win):
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
    return moved, player, win

