import ui

class Crypto:
	def __init__(self, number0=19, number1=500):
		self.p_index = None
		self.q_index = None
		self.carmichaels_t = None
		self.d_rev = None # d*e = 1 mod lambda(n)
		self.n_mply = None
		self.e = None
		self.primes_in_range(number0, number1)
	#

	def sieve_of_Eratosthenes(self, number1=500):
		sieve = [True]*(number1+1)
		p_square = 4
		p = 2
		while p_square <= number1:
			i = p_square
			while i <= number1:
				sieve[i] = False
				i += p

			p += 1
			p_square = p*p
		return sieve
	#
	def primes_in_range(self, number0=19, number1=500):
		sieve = self.sieve_of_Eratosthenes(number1)

		self.primes = []
		p = number0 if number0 > 3 else 3
		while p <= number1:
			if sieve[p]: self.primes.append(p)
			p += 1
	#
	def primes_tab(self):
		return self.primes
	#
	def set_p_q(self, p_new=None, q_new=None):
		if p_new != None: self.p_index = p_new
		if q_new != None: self.q_index = q_new

		if self.p_index != None and self.q_index != None:
			self.n_mply = self.p_index * self.q_index
			self.set_carmichaels_t_by_LCM()
			if self.e != None and self.gcd(self.e, self.carmichaels_t) != 1:
				self.e = None
	#
	def set_carmichaels_t_by_LCM(self): # carmichaels_lambda - carmichaels totient function = LCM(p-1, q-1);
		self.carmichaels_t = (self.p_index-1) * (self.q_index-1) // self.gcd(self.p_index-1, self.q_index-1)
	#
	def set_e(self, e_new):
		if e_new != None:
			self.e = e_new
			self.d_rev = self.modular_inverse(e_new, self.carmichaels_t)
	#
	def all_set(self):
		if self.p_index != None and self.q_index != None and self.carmichaels_t != None and \
			self.d_rev != None and self.n_mply != None and self.e != None:
			return True
		return False
	#
	def get_p(self):
		return self.p_index
	#
	def get_q(self):
		return self.q_index
	#
	def get_e(self):
		return self.e
	#
	def modular_inverse(self, exp, modulus):
		if modulus == 1: return 0

		inverse = 0
		new_inv = 1
		r = modulus
		new_r = exp
		while new_r != 0:
			quotient = r // new_r
			# (inverse, new_inv) := (new_inv, inverse - quotient * new_inv);
			temp = new_inv
			new_inv = inverse - quotient*new_inv
			inverse = temp
			# (r, new_r) := (new_r, r - quotient * new_r);
			temp = new_r
			new_r = r - quotient*new_r
			r = temp
		if r > 1:
			self.d_rev = None # "exp is not invertible";
			return False
		if inverse < 0: inverse = inverse + modulus
		return inverse
	#
	def modular_pow(self, base, exp, modulus): # base^exponent (mod modulus)
		if modulus == 1: return 0
		# Assert :: (modulus - 1) * (modulus - 1) does not overflow base
		result = 1
		base = base % modulus
		while exp > 0:
			if exp % 2 == 1:
				result = (result * base) % modulus
			exp = exp >> 1
			base = (base*base) % modulus
		return result
	#
	def gcd(self, n1, n2):
		val = 0
		while True:
			if n2!=0:
				val = n1%n2
				n1 = n2
				n2 = val
			elif n2==0:
				val = n1
				break
		return val
	#
	def options_4_e(self, last=1000):
		limit = min(last, self.carmichaels_t)
		sieve = self.sieve_of_Eratosthenes(limit)

		limited_primes = []
		p = 7
		while p < limit:
			gcd2 = self.gcd(p, self.carmichaels_t)
			if sieve[p] and gcd2 == 1: limited_primes.append(p)
			p += 1
		return limited_primes
	#
	def show_public(self):
		pub = {"n":self.n_mply, "e":self.e}
		return pub
	#
	def show_private(self):
		priv = {"p":self.p_index, "q":self.q_index, "lambda (Carmichael's t)":None, "d (secret private key exponent)":None}
		priv["lambda (Carmichael's t)"] = self.carmichaels_t
		priv["d (secret private key exponent)"] = self.d_rev
		return priv
	#
	def encrypt(self, m):
		if self.all_set()  == False:
			raise ValueError("Crypto class is not set to do encryption yet.")
		if m >= self.n_mply or m < 0:
			raise ValueError("Encryption value has to be in range [0, "+str(self.n_mply)+")")

		return self.modular_pow(m, self.e, self.n_mply) # c = m^e (mod n_mply)
	#
	def decrypt(self, c):
		if self.all_set()  == False:
			raise ValueError("Crypto class is not set to do encryption yet.")

		return self.modular_pow(c, self.d_rev, self.n_mply) # m = c^d (mod n_mply)
	#
	def brute_force_hack(self, encrypted):
		if self.n_mply == None or self.e == None:
			raise ValueError("Crypto class is not set to do brute force hack yet.")

		result = []
		m = 0
		while m < self.n_mply:
			c = self.modular_pow(m, self.e, self.n_mply)
			if c == encrypted:
				result.append(m)
			m += 1

		return result
	#
"""
def __iter__(self):
def __next__(self):
"""
#


def run_crypt(stdscr, crypto, value, do_encrypt=True):
	messages_rows = ["Number to {}: {}",
					"No result yet.",
					"Exit"]
	print_choice = [3,1,3]

	if do_encrypt:
		ui.print_menu(stdscr, ["Encrypt typed number.", "\tPress enter on number to do encryption."], [])
		job = "encrypt"
	else:
		ui.print_menu(stdscr, ["Decrypt typed number.", "\tPress enter on number to do decryption."], [])
		job = "decrypt"


	limit = crypto.show_public()
	limit = limit['n'] if type(limit['n']) == int else 10

	result = 0
	cmd = 0
	run = True
	while run:
		messages_rows[0] = "Number to {}: {}".format(job, value)
		ui.print_menu(stdscr, messages_rows, print_choice, cmd, 4)


		(c, cmd, n) = ui.input_select(stdscr, print_choice, cmd)

		if c >= ord('0') and c <= ord('9') and cmd == 0:
			value = value*10 + int(c-ord('0'))
			if value >= limit:
				value = limit-1
		elif c == ord('\b') and cmd == 0:
			value = value//10
		elif c == ord('\n') and cmd == 0:
			try:
				if do_encrypt:
					result = crypto.encrypt(value)
					messages_rows[1] = "Encrypted value is: {}".format(result)
				else:
					result = crypto.decrypt(value)
					messages_rows[1] = "Decrypted value is: {}".format(result)
			except ValueError as e:
				if hasattr(e, 'message'):
					messages_rows[1] = e.message
				else:
					messages_rows[1] = str(e)
		elif c == ord('\n') and cmd == 2:
			run = False
	#

	return result
#

def run(stdscr, options):
	if len(options) < 2:
		c = 19
	else:
		c = options[1]

	crypto = Crypto(c, c+1200)

	value_2_encrypt = 0
	encrypted_value = 0

	ui.scr_print(stdscr, 0, 0, "\t RSA encrypt / decrypt presentation.")
	messages_rows = ["Select 1st prime (current value {}) ".format(crypto.get_p()),
					"Select 2nd prime (current value {}) ".format(crypto.get_q()),
					"Select parameter 'e' (current value {}) ".format(crypto.get_e()),
					"Encrypt number (~ message)",
					"Decrypt number (~ message)",
					"Brute force guess",
					"Show public values",
					"Show private values", "Exit"]
	print_choice = [3]*len(messages_rows)

	cmd = 0
	run = True
	while run:
		messages_rows[0] = "Select 1st prime (current value {}) ".format(crypto.get_p())
		messages_rows[1] = "Select 2nd prime (current value {}) ".format(crypto.get_q())
		messages_rows[2] = "Select parameter 'e' (current value {}) ".format(crypto.get_e())
		if crypto.get_p() == None or crypto.get_q() == None:
			print_choice[2] = 0
		else:
			print_choice[2] = 3

		ui.print_menu(stdscr, messages_rows, print_choice, cmd)

		(c, cmd, n) = ui.input_select(stdscr, print_choice, cmd)

		if c != ord('\n'):
			pass
		elif cmd == 0:
			n = ui.select_navigate_list(stdscr, crypto.primes_tab(), crypto.get_p(), "Select number from table below.", "Step on table to select one, press enter to choose it, {}  ", crypto.get_q() )
			crypto.set_p_q(n)
		elif cmd == 1:
			n = ui.select_navigate_list(stdscr, crypto.primes_tab(), crypto.get_q(), "Select number from table below.", "Step on table to select one, press enter to choose it, {}  ", crypto.get_p() )
			crypto.set_p_q(None, n)
		elif cmd == 2:
			n = ui.select_navigate_list(stdscr, crypto.options_4_e(), crypto.get_e(), "Select number 'e' from table below.", "Step on table to select one, press enter to choose it, {}  ")
			crypto.set_e(n)
		elif cmd == 3:
			encrypted_value = run_crypt(stdscr, crypto, value_2_encrypt)
		elif cmd == 4:
			value_2_encrypt = run_crypt(stdscr, crypto, encrypted_value, False)
		elif cmd == 5:
			try:
				ui.print_menu(stdscr, ["Hacking by brute force ..."], [1], 0)
				hacked = crypto.brute_force_hack(encrypted_value)

				n = crypto.show_public()
				if len(hacked) > 1:
					message = "Solutions for c = m^e (mod n): {} = {}^{} (mod {})".format(encrypted_value, "{}", crypto.get_e(), n["n"])
				else:
					message = "Solution for c = m^e (mod n): {} = {}^{} (mod {})".format(encrypted_value, "{}", crypto.get_e(), n["n"])

				ui.select_navigate_list(stdscr, hacked, None, "Options for unencrypted value solved by brute force.", message)
			except ValueError as e:
				message = ["", "Press any key to exit."]
				if hasattr(e, 'message'):
					message[0] = e.message
				else:
					message[0] = str(e)
				ui.print_menu(stdscr, message, [1, 3], 1)
				ui.input_select(stdscr, [], 0)
		elif cmd == 6:
			n = crypto.show_public()
			ui.show_dict(stdscr, "Public values", n, 2)
		elif cmd == 7:
			n = crypto.show_private()
			ui.show_dict(stdscr, "Private values", n, 2)
		elif cmd == 8:
			run = False

#
