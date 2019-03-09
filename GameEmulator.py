import random
import pdb
import datetime

class Game:
	GAME_OVER = False

	PLAYER_ONE = 1
	PLAYER_TWO = 2

	EMPTY = 0
	INVALID = -1
	PIECES = 10

	X_MAX = 17
	X_MIN = -1
	Y_MAX = 9
	Y_MIN = -1

	def __init__(self):
		now = datetime.datetime.now()
		name = "snapshots-" + str(now).replace(':','_') + ".txt"
		
		self.name = name 
		self.player_turn = 1
		self.board = self.create_board()
		self.players_pieces = self.initialize_players_pieces()

		self.player1_done_pieces = 0
		self.player1_advanced_pieces = 0
		self.player1_middle_pieces = 0
		self.player1_far_pieces = 10

		self.player2_done_pieces = 0
		self.player2_advanced_pieces = 0
		self.player2_middle_pieces = 0
		self.player2_far_pieces = 10

		print(self.board)

	def initialize_players_pieces(self):
		players_pieces = []
		players_pieces.append([])
		players_pieces.append([[0,6], [1,6], [1,7], [2,5], [2,6], [2,7], [3,5], [3,6], [3,7], [3,8]])
		players_pieces.append([[16,6], [15,6], [15,7], [14,5], [14,6], [14,7], [13,5], [13,6], [13,7], [13,8]])
		return players_pieces

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
		board.append(self.create_board_line(6, 6, self.PLAYER_ONE))
		board.append(self.create_board_line(6, 7, self.PLAYER_ONE))
		board.append(self.create_board_line(5, 7, self.PLAYER_ONE))
		board.append(self.create_board_line(5, 8, self.PLAYER_ONE))
		board.append(self.create_board_line(4, 8, self.EMPTY))
		board.append(self.create_board_line(4, 9, self.EMPTY))
		board.append(self.create_board_line(3, 9, self.EMPTY))
		board.append(self.create_board_line(3, 10, self.EMPTY))
		board.append(self.create_board_line(2, 10, self.EMPTY))
		board.append(self.create_board_line(3, 10, self.EMPTY))
		board.append(self.create_board_line(3, 9, self.EMPTY))
		board.append(self.create_board_line(4, 9, self.EMPTY))
		board.append(self.create_board_line(4, 8, self.EMPTY))
		board.append(self.create_board_line(5, 8, self.PLAYER_TWO))
		board.append(self.create_board_line(5, 7, self.PLAYER_TWO))
		board.append(self.create_board_line(6, 7, self.PLAYER_TWO))
		board.append(self.create_board_line(6, 6, self.PLAYER_TWO))
		return board

	def start_game(self):
		while not self.GAME_OVER:
			self.move_weighted()
			
			if self.game_over():
				self.save_state()
				break
			
			self.move_randomly()
			if self.game_over():
				self.save_state()	
				break
			self.save_state() # save state once, after both players have played
		
	def add(self, var_player1, var_player2):
		if (self.player_turn == self.PLAYER_ONE):
			var_player1 += 1
		else:
			var_player2 += 1

	def sub(self, var_player1, var_player2):
		if (self.player_turn == self.PLAYER_ONE):
			var_player1 -= 1
		else:
			var_player2 -= 1				

	def update_var(self, old_pos, new_pos):
		#pdb.set_trace()
		if (new_pos[0] > 12):
			self.add(self.player1_done_pieces, self.player2_far_pieces)
		elif (new_pos[0] > 9):
			self.add(self.player1_advanced_pieces, self.player2_far_pieces)
		elif (new_pos[0] > 6):
			self.add(self.player1_middle_pieces, self.player2_middle_pieces)
		elif (new_pos[0] > 4):
			self.add(self.player1_far_pieces, self.player2_advanced_pieces)
		else:
			self.add(self.player1_far_pieces, self.player2_done_pieces)

		if (old_pos[0] > 12):
			self.sub(self.player1_done_pieces, self.player2_far_pieces)
		elif (old_pos[0] > 9):
			self.sub(self.player1_advanced_pieces, self.player2_far_pieces)
		elif (old_pos[0] > 6):
			self.sub(self.player1_middle_pieces, self.player2_middle_pieces)
		elif (old_pos[0] > 4):
			self.sub(self.player1_far_pieces, self.player2_advanced_pieces)
		else:
			self.sub(self.player1_far_pieces, self.player2_done_pieces)

	def execute_move(self, id_piece, new_pos):
		old_pos = self.players_pieces[self.player_turn][id_piece]
		self.board[old_pos[0]][old_pos[1]] = self.EMPTY

		self.players_pieces[self.player_turn][id_piece] = new_pos
		self.board[new_pos[0]][new_pos[1]] = self.player_turn

		self.update_var(old_pos, new_pos)

		self.player_turn = self.player_turn % 2 + 1

	def move_randomly(self):
		id_piece = random.randint(0, self.PIECES - 1)
		possibilities = self.calculate_moves(self.players_pieces[self.player_turn][id_piece])
		if possibilities:
			new_pos = possibilities[random.randint(0,len(possibilities)- 1)]
		else:
			self.move_randomly()

	def move_weighted(self):
		greatest_profit = 0.0
		piece = 0
		move = [0,0]
		stop = False
		i = 1

		while (not stop and i in range(self.PIECES+1)):
			possibilities = self.calculate_moves(self.players_pieces[self.PLAYER_ONE][i])
			for possible_move in possibilities:
				current_profit = self.simulate_state(i, possible_move)
				if (current_profit > 0,79):
					piece = i
					move = possible_move
					stop = True
					break
				elif (current_profit > greatest_profit):
					piece = i
					move = possible_move
			i += 1
		self.execute_move(piece, move)

	def simulate_state(self, id_piece, move_to_test):
		old_pos = self.players_pieces[self.player_turn][id_piece]
		self.update_var(old_pos, move_to_test)

		independent_var = 0
		player_one_weight = self.player1_done_pieces*0.1 + self.player1_advanced_pieces*0.07 + self.player1_middle_pieces*0.06 + self.player1_far_pieces*0.05
		player_two_weight = self.player1_done_pieces*(-0.1) + self.player1_advanced_pieces*(-0.07) + self.player1_middle_pieces*(-0.06) + self.player1_far_pieces*(-0.05)
		
		self.update_var(move_to_test, old_pos) # undo 'fake' movement

		return (player_one_weight + player_two_weight + independent_var)

	def game_over(self):
		i = 0
		if (self.player_turn == self.PLAYER_ONE):
			while (i < self.PIECES and self.players_pieces[self.PLAYER_ONE][i][0] > 13):
				i += 1
		else:
			while (i < self.PIECES and self.players_pieces[self.PLAYER_TWO][i][0] < 4):
				i += 1
		self.GAME_OVER = i == self.PIECES
		return self.GAME_OVER

	def save_state(self):
		file = open(self.name, "a")
		
		line = ""
		line += str(self.player1_done_pieces) + "-"  + str(self.player2_done_pieces) + "-"
		line += str(self.player1_advanced_pieces) + "-" + str(self.player2_advanced_pieces) + "-"
		line += str(self.player1_middle_pieces) + "-" + str(self.player2_middle_pieces) + "-"
		line += str(self.player1_far_pieces) + "-" + str(self.player2_far_pieces)
		line += "\n"
		file.write(line)
		
		if self.GAME_OVER:
			winner = self.player_turn % 2
			line = str(winner) + "\n"
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
		return position[0] in range(self.X_MIN,self.X_MAX) and position[1] in range(self.Y_MIN,self.Y_MAX) and self.board[position[0]][position[1]] == self.EMPTY

if __name__== "__main__":
	Test = Game()

	Test.start_game() 
