import datetime, pdb, random, sys
from Generalizer import Generalizer

class Game:
	PLAYER_ONE = 1
	PLAYER_TWO = 2

	EMPTY = 0
	INVALID = -1
	PIECES = 10

	X_MAX = 17
	X_MIN = -1
	Y_MAX = 9
	Y_MIN = -1

	REAL_MIN = 0

	PLAYER_1_X_WIN = 12
	PLAYER_2_X_WIN = 4

	LIMIT_MOVE = 200000

	FILE_NAME = "result"
	FILE_EXTENSION = ".txt"


	def __init__(self, limit_game, update_frequency, game_type):
		self.generalizer = Generalizer()

		self.LIMIT_GAME = limit_game + 1
		self.UPDATE_FREQUENCY = update_frequency
		self.GAME_TYPE = game_type


	def create_board_line(self, start, end, value):
		row = []
		for i in range(self.Y_MAX):
			if i in range(start, end + 1):
				row.append(value)
			else:
				row.append(self.INVALID)
		return row


	def create_board(self):
		board = []
		board.append(self.create_board_line(4, 4, self.PLAYER_ONE))
		board.append(self.create_board_line(4, 5, self.PLAYER_ONE))
		board.append(self.create_board_line(3, 5, self.PLAYER_ONE))
		board.append(self.create_board_line(3, 6, self.PLAYER_ONE))
		board.append(self.create_board_line(2, 6, self.EMPTY))
		board.append(self.create_board_line(2, 7, self.EMPTY))
		board.append(self.create_board_line(1, 7, self.EMPTY))
		board.append(self.create_board_line(1, 8, self.EMPTY))
		board.append(self.create_board_line(0, 8, self.EMPTY))
		board.append(self.create_board_line(1, 8, self.EMPTY))
		board.append(self.create_board_line(1, 7, self.EMPTY))
		board.append(self.create_board_line(2, 7, self.EMPTY))
		board.append(self.create_board_line(2, 6, self.EMPTY))
		board.append(self.create_board_line(3, 6, self.PLAYER_TWO))
		board.append(self.create_board_line(3, 5, self.PLAYER_TWO))
		board.append(self.create_board_line(4, 5, self.PLAYER_TWO))
		board.append(self.create_board_line(4, 4, self.PLAYER_TWO))
		return board


	def initialize_pieces_position(self):
		self.profit_reached = 0
		self.player1_end_pieces = self.EMPTY
		self.player2_end_pieces = self.EMPTY
		self.player1_near_pieces = self.EMPTY
		self.player2_near_pieces = self.EMPTY
		self.player1_middle_pieces = self.EMPTY
		self.player2_middle_pieces = self.EMPTY
		self.player1_far_pieces = self.EMPTY
		self.player2_far_pieces = self.EMPTY
		self.player1_start_pieces = self.PIECES
		self.player2_start_pieces = self.PIECES


	def initialize_players_pieces(self):
		players_pieces = []
		players_pieces.append([])
		players_pieces.append([[0,4], [1,4], [1,5], [2,3], [2,4], [2,5], [3,3], [3,4], [3,5], [3,6]])
		players_pieces.append([[16,4], [15,4], [15,5], [14,3], [14,4], [14,5], [13,3], [13,4], [13,5], [13,6]])
		return players_pieces


	def start_game(self):
		self.adjust_array = []
		self.game_identifier = 1

		while (self.game_identifier < self.LIMIT_GAME):
			self.file_name = self.FILE_NAME + str(self.game_identifier) + self.FILE_EXTENSION
			self.board = self.create_board()
			self.initialize_pieces_position()
			self.players_pieces = self.initialize_players_pieces()

			self.GAME_OVER = False

			self.player_turn = self.PLAYER_ONE

			self.move_identifier = 0

			if (self.GAME_TYPE):
				while not self.GAME_OVER:
					self.move_weighted()
					self.move_identifier += 1
					self.save_state()
					self.game_over()

					if (not self.GAME_OVER):
						self.move_weighted_outdated()
						self.move_identifier += 1
						self.game_over()
			else:
				while not self.GAME_OVER:
					self.move_weighted()
					self.move_identifier += 1
					self.save_state()
					self.game_over()

					if (not self.GAME_OVER):
						self.move_randomly()
						self.move_identifier += 1
						self.game_over()

			self.game_identifier += 1


	def update_var(self, old_pos, new_pos):
		if (self.player_turn == self.PLAYER_ONE):
			if (old_pos[0] < 4):
				self.player1_start_pieces -= 1
			elif (old_pos[0] < 7):
				self.player1_far_pieces -= 1
			elif (old_pos[0] < 10):
				self.player1_middle_pieces -= 1
			elif (old_pos[0] < 13):
				self.player1_near_pieces -= 1
			else:
				self.player1_end_pieces -= 1

			if (new_pos[0] < 4):
				self.player1_start_pieces += 1
			elif (new_pos[0] < 7):
				self.player1_far_pieces += 1
			elif (new_pos[0] < 10):
				self.player1_middle_pieces += 1
			elif (new_pos[0] < 13):
				self.player1_near_pieces += 1
			else:
				self.player1_end_pieces += 1

		else:
			if (12 < old_pos[0]):
				self.player2_start_pieces -= 1
			elif (9 < old_pos[0]):
				self.player2_far_pieces -= 1
			elif (6 < old_pos[0]):
				self.player2_middle_pieces -= 1
			elif (3 < old_pos[0] ):
				self.player2_near_pieces -= 1
			else:
				self.player2_end_pieces -= 1

			if (12 < new_pos[0]):
				self.player2_start_pieces += 1
			elif (9 < new_pos[0]):
				self.player2_far_pieces += 1
			elif (6 < new_pos[0]):
				self.player2_middle_pieces += 1
			elif (3 < new_pos[0] ):
				self.player2_near_pieces += 1
			else:
				self.player2_end_pieces += 1


	def execute_move(self, id_piece, new_pos):
		old_pos = self.players_pieces[self.player_turn][id_piece]
		self.board[old_pos[0]][old_pos[1]] = self.EMPTY

		self.players_pieces[self.player_turn][id_piece] = new_pos
		self.board[new_pos[0]][new_pos[1]] = self.player_turn

		self.update_var(old_pos, new_pos)

		self.player_turn = self.player_turn % 2 + 1


	def verify_stuck(self, player, position):
		stuck = True
		index = 0
		if (player == self.PLAYER_ONE):
			row = position[0] + 1
		else:
			row = position[0] - 1

		while (stuck and index < self.Y_MAX):
			value = self.board[row][index]
			if(value == self.EMPTY or value == player):
				stuck = False
			index += 1

		return stuck


	def move_randomly(self):
		stuck = False
		index = 0
		while (not stuck and index < self.PIECES):
			if (self.PLAYER_1_X_WIN < self.players_pieces[self.PLAYER_TWO][index][0] and self.verify_stuck(self.PLAYER_TWO, self.players_pieces[self.PLAYER_TWO][index])):
				stuck = True
			index += 1

		if (stuck):
			self.GAME_OVER = True
		else:
			id_piece = random.randint(0, self.PIECES - 1)
			possibilities = self.calculate_moves(self.players_pieces[self.player_turn][id_piece])
			if possibilities:
				new_pos = possibilities[random.randint(0, len(possibilities)- 1)]
				self.execute_move(id_piece, new_pos)
			else:
				self.move_randomly()


	def move_weighted_outdated():
		print('hola')


	def move_weighted(self):
		stuck = False
		index = 0
		while (not stuck and index < self.PIECES):
			if (self.players_pieces[self.PLAYER_ONE][index][0] < self.PLAYER_2_X_WIN and self.verify_stuck(self.PLAYER_ONE, self.players_pieces[self.PLAYER_ONE][index])):
				stuck = True
			index += 1

		if (stuck):
			self.GAME_OVER = True
		else:
			init = False
			base = random.randint(0, self.PIECES - 1)
			moves = []

			for i in range(0, self.PIECES):
				selected_piece = (base + i) % self.PIECES
				possibilities = self.calculate_moves(self.players_pieces[self.PLAYER_ONE][selected_piece])
				for possible_move in possibilities:
					current_profit = self.simulate_state(selected_piece, possible_move)
					if (not init):
						init = True
						greatest_profit = current_profit
						moves.append([selected_piece, possible_move])

					elif (current_profit > greatest_profit):
						greatest_profit = current_profit
						moves = [[selected_piece, possible_move]]

					elif (current_profit == greatest_profit):
						moves.append([selected_piece, possible_move])

			self.print_board()

			self.profit_reached = greatest_profit
			
			print(moves)

			if (1 < len(moves)):
				chosen = random.randint(0, len(moves) - 1)
				self.execute_move(moves[chosen][0], moves[chosen][1])
				print("PIECE: ", moves[chosen][0], " MOVE: ", moves[chosen][1])
			elif (1 == len(moves)):
				self.execute_move(moves[0][0], moves[0][1])
			else:
				self.GAME_OVER = True


	def print_board(self):
		print("----------")
		printable = ""
		for x in range(self.REAL_MIN, self.X_MAX):
			if(x % 2 == 0):
				printable += " ["
			else:
				printable += "["
			for y in range(self.REAL_MIN, self.Y_MAX):
				if(self.board[x][y] == self.INVALID):
					printable += "9,"
				else:
					printable += str(self.board[x][y])
					printable += ","
			printable += "]\n"
		print(printable)


	def simulate_state(self, id_piece, move_to_test):
		old_pos = self.players_pieces[self.player_turn][id_piece]

		# Simulates 'fake' movement
		self.update_var(old_pos, move_to_test)

		if (self.player1_end_pieces == self.PIECES):
			player_one_weight = 1
			player_two_weight = 0
		elif (self.player2_end_pieces == self.PIECES):
			player_one_weight = 0
			player_two_weight = -1
		else:
			player_one_weight = self.player1_end_pieces*self.generalizer.get_player1_end_weight() + self.player1_near_pieces*self.generalizer.get_player1_near_weight() + self.player1_middle_pieces*self.generalizer.get_player1_middle_weight() + self.player1_far_pieces*self.generalizer.get_player1_far_weight() + self.player1_start_pieces*self.generalizer.get_player1_start_weight()
			
			player_two_weight = self.player2_end_pieces*self.generalizer.get_player2_end_weight() + self.player2_near_pieces*self.generalizer.get_player2_near_weight() + self.player2_middle_pieces*self.generalizer.get_player2_middle_weight() + self.player2_far_pieces*self.generalizer.get_player2_far_weight() + self.player2_start_pieces*self.generalizer.get_player2_start_weight()

		# Undo 'fake' movement
		self.update_var(move_to_test, old_pos)

		if(player_one_weight == 1 or player_two_weight == -1):
			return (player_one_weight + player_two_weight)
		else:
			return (player_one_weight + player_two_weight + self.generalizer.get_independent_weight())

	def game_over(self):
		if(self.player1_end_pieces == self.PIECES or self.player2_end_pieces == self.PIECES or self.LIMIT_MOVE < self.move_identifier):
			self.GAME_OVER = True
			self.save_state()

			if (self.player1_end_pieces == self.PIECES):
				self.adjust_array.append([1,self.file_name])
			else:
				self.adjust_array.append([-1,self.file_name])

			if not (self.game_identifier % self.UPDATE_FREQUENCY):
				self.generalizer.adjust_weights(self.adjust_array)
				self.adjust_array = []


	def save_state(self):
		split = "|"

		file = open(self.file_name, "a")

		line = str(self.profit_reached) + split
		line += str(self.player1_end_pieces) + split
		line += str(self.player2_end_pieces) + split
		line += str(self.player1_near_pieces) + split
		line += str(self.player2_near_pieces) + split
		line += str(self.player1_middle_pieces) + split
		line += str(self.player2_middle_pieces) + split
		line += str(self.player1_far_pieces) + split
		line += str(self.player2_far_pieces) + split
		line += str(self.player1_start_pieces) + split
		line += str(self.player2_start_pieces) + "\n"

		file.write(line)
		file.close()


	def calculate_moves(self, position):
		possibilities = []

		position_X_sub = position[0] - 1
		position_X_add = position[0] + 1
		position_Y_sub = position[1] - 1
		position_Y_add = position[1] + 1

		# Primer movimiento posible | izquierda
		if (self.Y_MIN < position_Y_sub):
			if (self.board[position[0]][position_Y_sub] == 0):
				possibilities.append([position[0],position_Y_sub])
			elif (self.board[position[0]][position_Y_sub] != self.INVALID):
				if(self.verify_jump([position[0],position_Y_sub - 1])):
					possibilities.append([position[0],position_Y_sub - 1])

		# Segundo movimiento posible | derecha
		if (position_Y_add < self.Y_MAX):
			if (self.board[position[0]][position_Y_add] == 0):
				possibilities.append([position[0],position_Y_add])
			elif (self.board[position[0]][position_Y_add] != self.INVALID):
				if(self.verify_jump([position[0],position_Y_add + 1])):
					possibilities.append([position[0],position_Y_add + 1])

		# Si la fila es multiplo de 2
		if (position[0] % 2 == 0):
			if not (self.player_turn == self.PLAYER_ONE and self.PLAYER_1_X_WIN < position[0]):
				# Tercer movimiento posible | izquierda arriba
				if (self.X_MIN < position_X_sub):
					if (self.board[position_X_sub][position[1]] == 0):
						possibilities.append([position_X_sub,position[1]])
					elif (self.board[position_X_sub][position[1]] != self.INVALID):
						if(self.verify_jump([position_X_sub - 1,position_Y_sub])):
							possibilities.append([position_X_sub - 1,position_Y_sub])

				# Cuarto movimiento posible | derecha arriba
				if (self.X_MIN < position_X_sub and position_Y_add < self.Y_MAX):
					if (self.board[position_X_sub][position_Y_add] == 0):
						possibilities.append([position_X_sub,position_Y_add])
					elif (self.board[position_X_sub][position_Y_add] != self.INVALID):
						if(self.verify_jump([position_X_sub - 1,position_Y_add])):
							possibilities.append([position_X_sub - 1,position_Y_add])

			if not (self.player_turn == self.PLAYER_TWO and position[0] < self.PLAYER_2_X_WIN):
				# Quinto movimiento posible | izquierda abajo
				if (position_X_add < self.X_MAX):
					if (self.board[position_X_add][position[1]] == 0):
						possibilities.append([position_X_add,position[1]])
					elif (self.board[position_X_add][position[1]] != self.INVALID):
						if(self.verify_jump([position_X_add + 1,position_Y_sub])):
							possibilities.append([position_X_add + 1,position_Y_sub])

				# Sexto movimiento posible | derecha abajo
				if (position_X_add < self.X_MAX and position_Y_add < self.Y_MAX):
					if (self.board[position_X_add][position_Y_add] == 0):
						possibilities.append([position_X_add,position_Y_add])
					elif (self.board[position_X_add][position_Y_add] != self.INVALID):
						if(self.verify_jump([position_X_add + 1,position_Y_add])):
							possibilities.append([position_X_add + 1,position_Y_add])

		# Si la fila no es multiplo de 2
		else:
			if not (self.player_turn == self.PLAYER_ONE and self.PLAYER_1_X_WIN < position[0]):
				# Tercer movimiento posible | izquierda arriba
				if (self.X_MIN < position_X_sub and self.Y_MIN < position_Y_sub):
					if (self.board[position_X_sub][position_Y_sub] == 0):
						possibilities.append([position_X_sub,position_Y_sub])
					elif (self.board[position_X_sub][position_Y_sub] != self.INVALID):
						if(self.verify_jump([position_X_sub - 1,position_Y_sub])):
							possibilities.append([position_X_sub - 1,position_Y_sub])

				# Cuarto movimiento posible | derecha arriba
				if (self.X_MIN < position_X_sub):
					if (self.board[position_X_sub][position[1]] == 0):
						possibilities.append([position_X_sub,position[1]])
					elif (self.board[position_X_sub][position[1]] != self.INVALID):
						if(self.verify_jump([position_X_sub - 1,position_Y_add])):
							possibilities.append([position_X_sub - 1,position_Y_add])

			if not (self.player_turn == self.PLAYER_TWO and position[0] < self.PLAYER_2_X_WIN):
				# Quinto movimiento posible | izquierda abajo
				if (position_X_add < self.X_MAX and self.Y_MIN < position_Y_sub):
					if (self.board[position_X_add][position_Y_sub] == 0):
						possibilities.append([position_X_add,position_Y_sub])
					elif (self.board[position_X_add][position_Y_sub] != self.INVALID):
						if(self.verify_jump([position_X_add + 1,position_Y_sub])):
							possibilities.append([position_X_add + 1,position_Y_sub])

				# Sexto movimiento posible | derecha abajo
				if (position_X_add < self.X_MAX):
					if (self.board[position_X_add][position[1]] == 0):
						possibilities.append([position_X_add,position[1]])
					elif (self.board[position_X_add][position[1]] != self.INVALID):
						if(self.verify_jump([position_X_add + 1,position_Y_add])):
							possibilities.append([position_X_add + 1,position_Y_add])

		return possibilities


	def verify_jump(self, position):
		return position[0] in range(self.REAL_MIN,self.X_MAX) and position[1] in range(self.REAL_MIN,self.Y_MAX) and self.board[position[0]][position[1]] == self.EMPTY


if __name__== "__main__":
	Test = Game(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
	Test.start_game()
