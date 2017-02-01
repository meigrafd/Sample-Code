import curses
stdscr = curses.initscr()

finished = False

try:
	while not finished:
		c = stdscr.getch()
		if c == curses.CRTL:
			print("Pressed: CTRL")

except (KeyboardInterrupt, SystemExit):
	finished = True

curses.endwin()