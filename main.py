import getopt, sys
import curses, ui
from cryptosystems import rsa

#/ - - - - - - - - - - - - - - - - - - - - UI functions- - - - - - - - - - - - - - - - - - - - -
def usage():
	print("\tScript to present and play cryptosystems.\n--p0: \'n\': set first prime to p0, otherwise 19.\n")

def get_options(job):
	if len(job)<1: job.append(0)
	if len(job)<2: job.append(19)

	try:
		opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "p0="])
	except getopt.GetoptError:
		return 0

	job[0] = 1
	for opt, arg in opts:
		if opt in ("--p0"):
			job[0] = 1
			try:
				job[1]=int(arg)
			except Exception:
				print(" Wrong argument after p0. Please type the decimal number!")
				job[0] = 0
			if job[0] != 0 and job[1] > 20000:
				print(" The value of p0 is too big; upper limit is 20000.")
				job[0] = 0
		elif opt in ("-h", "--help"):
			usage()
			job[0] = 0

	return job[0]
# end
#/ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def main(stdscr, job):
	if not job[0]:
		return

	stdscr = curses.initscr()

	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)


	rsa.run(stdscr, job)


	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()

	curses.endwin()
#

if __name__ == '__main__':
	job = [0,19]
	get_options(job)
	curses.wrapper(main, job)

