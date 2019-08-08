import curses

def print_menu(stdscr, menu_items, print_choose, which=-1, row_begin=2):
	stdscr.move(row_begin, 0)
	stdscr.clrtobot()

	PRINTABLE = 1

	row = row_begin
	row_bold = None
	i = 0
	while i < len(menu_items):
		p_c = 3 # default value for printing and choosing state;
		if i < len(print_choose) and type(print_choose[i]) == int:
			p_c = print_choose[i]

		if not p_c&PRINTABLE:
			i += 1
			continue

		if i == which:
			row_bold = row
		stdscr.addstr(row, 1, menu_items[i])
		row += 1
		i += 1

	if row_bold != None:
		stdscr.addstr(row_bold, 1, menu_items[which], curses.A_BOLD)
#

def scr_print(stdscr, row, col, message, bold=False):
	if bold:
		stdscr.addstr(row, col, message, curses.A_BOLD)
	else:
		stdscr.addstr(row, col, message)
#

def input_select(stdscr, print_choose, which):
	CHOOSABLE = 2

	result = [0, which, 0]
	len_1 = len(print_choose) - 1

	c = stdscr.getch()

	if c == curses.KEY_UP and which > 0:
		i = which - 1
		while i > 0 and (print_choose[i]&CHOOSABLE) == 0:
			i -= 1

		if print_choose[i]&CHOOSABLE:
			result[1] = i
	elif c==curses.KEY_DOWN and which < len_1:
		i = which + 1
		while i < len_1 and (print_choose[i]&CHOOSABLE) == 0:
			i += 1

		if print_choose[i]&CHOOSABLE:
			result[1] = i
	elif c==curses.KEY_RIGHT:
		result[2] = 1
	elif c==curses.KEY_LEFT:
		result[2] = -1
	elif c==curses.KEY_ENTER or c==10:
		result[0] = ord('\n')
	elif c==curses.KEY_BACKSPACE:
		result[0] = ord('\b')
	else:
		result[0] = c

	return result
#

def show_dict(stdscr, title, dict_object, row_begin=2):
	stdscr.move(row_begin, 0)
	stdscr.clrtobot()

	stdscr.addstr( row_begin , 1, title)
	stdscr.addstr(row_begin+1, 2, "(press enter to exit)")

	(scr_h, c) = stdscr.getmaxyx()
	scr_h -= 2
	row = row_begin + 2
	for key,val in dict_object.items():
		stdscr.addstr(row, 1, "{}: {}".format(key, val) )
		row += 1
		if row == scr_h: break

	stdscr.addstr(row, 1, "Exit ", curses.A_BOLD)

	run = True
	while run:
		c = stdscr.getch()
		if c==curses.KEY_ENTER or c==10:
			run = False
#

def print_table(stdscr, array, row_begin, i_selected, table_cols=6):
	(scr_h, n) = stdscr.getmaxyx()
	scr_h = (scr_h - row_begin - 2)//2 #

	i_begin = (i_selected//table_cols)*table_cols
	i_begin = max(i_begin - (scr_h - 2)*table_cols, 0)

	n = min(i_begin + scr_h*table_cols, len(array))


	stdscr.move(row_begin, 0)
	stdscr.clrtobot()

	number_len = len(str(array[n-1]))
	row = row_begin
	if i_begin < table_cols:
		i = min(table_cols, len(array))*(number_len + 3) - 1
		stdscr.addstr(row, 1, "/")
		stdscr.addstr("-"*i)
		stdscr.addstr("\\")
		row += 1

	i = i_begin
	while i < n:
		stdscr.addstr(row, 1, "|")
		low_border = "|" if i < n - table_cols else "\\"
		j = 0
		while j < table_cols and i < n:
			if i == i_selected:
				stdscr.addstr(" {1:{0}d}".format(number_len, array[i]), curses.A_BOLD)
			else:
				stdscr.addstr(" {1:{0}d}".format(number_len, array[i]) )

			stdscr.addstr(" |")
			low_border += "-"*(number_len+3)
			j += 1
			i += 1
		row += 1
		if i < n - table_cols:
			low_border = low_border[:-1] + "|"
		else:
			low_border = low_border[:-1] + "/"
		stdscr.addstr(row, 1, low_border)
		row += 1
#

def select_navigate_list(stdscr, array, selected, title, message, skip=None, row_begin=2):
	stdscr.move(row_begin, 0)
	stdscr.clrtobot()

	stdscr.addstr(row_begin, 1, title)

	if skip == None:
		list_cp = array
	else:
		list_cp = array[:]
		list_cp.remove(skip)

	i_selected = 0
	while i_selected < len(list_cp):
		if list_cp[i_selected] == selected:
			break
		i_selected += 1

	if i_selected >= len(list_cp): i_selected = 0

	TABLE_COLS = 6
	run = True

	while run:
		stdscr.addstr(row_begin+1, 1, message.format(list_cp[i_selected]) )

		print_table(stdscr, list_cp, row_begin+2, i_selected, TABLE_COLS)


		c = stdscr.getch()

		if c == curses.KEY_UP and i_selected > 0:
			i_selected -= TABLE_COLS
			if i_selected < 0: i_selected = 0
		elif c==curses.KEY_DOWN and i_selected < len(list_cp) - 1:
			i_selected += TABLE_COLS
			if i_selected >= len(list_cp): i_selected = len(list_cp) - 1
		elif c == curses.KEY_LEFT and i_selected > 0:
			i_selected -= 1
		elif c==curses.KEY_RIGHT and i_selected < len(list_cp) - 1:
			i_selected += 1
		elif c==curses.KEY_ENTER or c==10:
			run = False
	#

	return list_cp[i_selected]
#

