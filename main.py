import curses

# modes

def movement(key, mode, y, x, maxy, maxx, scr) -> (int, int, curses.window, str):
    if key == curses.KEY_BACKSPACE:
        mode = "text"
    key = chr(key)
    if key == 'q':
        return
    elif key == 'h':
        y, x = inc_dim((0, -1), y, x, maxy, maxx)
    elif key == 'j':
        y, x = inc_dim((1, 0), y, x, maxy, maxx)
    elif key == 'l':
        y, x = inc_dim((0, 1), y, x, maxy, maxx)
    elif key == 'k':
        y, x = inc_dim((-1, 0), y, x, maxy, maxx)
    # cool functions
    elif key in 'x ':
        scr.addstr(y, x, ' ', curses.color_pair(1))
        y, x = inc_dim((0, 1), y, x, maxy, maxx)
    elif key == 'X':
        scr.addstr(y, x, ' ', curses.color_pair(1))
        y, x = inc_dim((0, -1), y, x, maxy, maxx)
    return y, x, scr, mode

def text(key, mode, y, x, maxy, maxx, scr) -> (int, int, curses.window):
    if key == curses.KEY_BACKSPACE:
        mode = "movement"
    elif key == curses.KEY_LEFT:
        y, x = inc_dim((0, -1), y, x, maxy, maxx)
    elif key == curses.KEY_DOWN:
        y, x = inc_dim((1, 0), y, x, maxy, maxx)
    elif key == curses.KEY_RIGHT:
        y, x = inc_dim((0, 1), y, x, maxy, maxx)
    elif key == curses.KEY_UP:
        y, x = inc_dim((-1, 0), y, x, maxy, maxx)
    key = chr(key)
    if key.lower() in "qwertyuiopasdfghjklzxcvbnm[]{}\\;':\",.<>/?0123456789!@#$%^&*()-_+*| ":
        scr.addstr(y, x, key, curses.color_pair(1))
        y, x = inc_dim((0, 1), y, x, maxy, maxx)
    elif key == '\n':
        y, x = inc_dim((1, -1), y, x, maxy, maxx)
    return y, x, scr, mode

modes = {
    "movement": movement,
    "text": text
}

def inc_dim(inc, y, x, maxy, maxx) -> (int, int):
    # dec y
    if inc[0] == -1:
        y -= 1 if y > 0 else 0
    # inc y
    elif inc[0] == 1:
        y += 1 if y < maxy else 0
    # dec x
    if inc[1] == -1:
        x -= 1 if x > 0 else 0
    # inc x
    elif inc[1] == 1:
        x += 1 if x < maxx else 0
    return y, x

colors = [
    (curses.COLOR_WHITE, curses.COLOR_BLACK),
    (curses.COLOR_BLUE,  curses.COLOR_BLACK)
]

def main(scr: curses.window):
    mode = "movement"
    for n, pair in enumerate(colors):
        curses.init_pair(n+1, *pair)

    y, x = 0, 0
    while True:
        # maxy/x
        maxy, maxx = [n-1 for n in scr.getmaxyx()]
        maxy -= 1

        # output mode
        scr.move(maxy+1, 1)
        scr.clrtobot()
        scr.addstr(maxy+1, 1, mode)

        # move cursor to proper position
        scr.move(y, x)

        # get user input
        key = scr.getch()
        # try:
        y, x, scr, mode = modes[mode](key, mode, y, x, maxy, maxx, scr)
        # except ValueError:
            # pass

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
