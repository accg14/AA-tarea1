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
	Y_MAX = 13
	Y_MIN = -1

	def __init__(self):
		now = datetime.datetime.now()
		name = "snapshots-" + str(now) + ".txt"
		
		self.name = name 
		self.board = self.create_board()
		self.player_turn = 1
		self.players_pieces = self.initialize_players_pieces()

		self.player1_in = 0
		self.player2_in = 0

		self.movimientos_temporal = 0

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
		board.append(self.create_board_line(0, 12, self.EMPTY))
		board.append(self.create_board_line(1, 12, self.EMPTY))
		board.append(self.create_board_line(1, 11, self.EMPTY))
		board.append(self.create_board_line(2, 11, self.EMPTY))
		board.append(self.create_board_line(2, 10, self.EMPTY))
		board.append(self.create_board_line(2, 11, self.EMPTY))
		board.append(self.create_board_line(1, 11, self.EMPTY))
		board.append(self.create_board_line(1, 12, self.EMPTY))
		board.append(self.create_board_line(0, 12, self.EMPTY))
		board.append(self.create_board_line(5, 8, self.PLAYER_TWO))
		board.append(self.create_board_line(5, 7, self.PLAYER_TWO))
		board.append(self.create_board_line(6, 7, self.PLAYER_TWO))
		board.append(self.create_board_line(6, 6, self.PLAYER_TWO))
		return board

	def start_game(self):
		self.save_state();
		while not self.game_over():
			self.move()
			self.save_state()
		self.GAME_OVER = True
		self.save_state()

	def move(self):
		id_piece = random.randint(0, self.PIECES - 1)
		#
		#pdb.set_trace()
		possibilities = self.calculate_moves(self.players_pieces[self.player_turn][id_piece])
		#print(possibilities)
		if possibilities:
			new_pos = possibilities[random.randint(0,len(possibilities)- 1)]

			old_pos = self.players_pieces[self.player_turn][id_piece]
			self.players_pieces[self.player_turn][id_piece] = new_pos
			#pdb.set_trace()
			self.board[new_pos[0]][new_pos[1]] = self.player_turn
			self.board[old_pos[0]][old_pos[1]] = self.EMPTY
			self.player_turn = self.player_turn % 2 + 1
		else:
			self.move()

	def game_over(self):
		i = 0
		if (self.player_turn == self.PLAYER_ONE):
			while (i < self.PIECES and self.players_pieces[1][i][0] > 13):
				i += 1
		else:
			while (i < self.PIECES and self.players_pieces[2][i][0] < 4):
				i += 1
		return i == self.PIECES

	def save_state(self):	
		file = open(self.name, "a")

		if self.movimientos_temporal < 10:
			self.movimientos_temporal += 1
			for i in range(len(self.board)):
				file.write(str(self.board[i]) + "\n")
			file.write("-------------------------------\n")
		#file.write(line)
		#if self.GAME_OVER:
		#	winner = self.player_turn % 2
		#	line = str(winner) + "\n"
		#	file.write(line)
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

		# Tercer movimiento posible | arriba
		if (self.X_MIN < position_X_sub):
			if (self.board[position_X_sub][position[1]] == 0):
				possibilities.append([position_X_sub,position[1]])
			elif (self.board[position_X_sub][position[1]] != self.INVALID):
				if(self.verify_jump([position_X_sub - 2,position[1]])):
					possibilities.append([position_X_sub - 2,position[1]])

		# Cuarto movimiento posible | abajo
		if (position_X_add < self.X_MAX):
			if (self.board[position_X_add][position[1]] == 0):
				possibilities.append([position_X_add,position[1]])
			elif (self.board[position_X_add][position[1]] != self.INVALID):
				if(self.verify_jump([position_X_add + 2,position[1]])):
					possibilities.append([position_X_add + 2,position[1]])

		# Quinto movimiento posible | izquierda arriba
		if (self.X_MIN < position_X_sub and self.Y_MIN < position_Y_sub):
			if (self.board[position_X_sub][position_Y_sub] == 0):
				possibilities.append([position_X_sub,position_Y_sub])
			elif (self.board[position_X_sub][position_Y_sub] != self.INVALID):
				if(self.verify_jump([position_X_sub - 1,position_Y_sub - 2])):
					possibilities.append([position_X_sub - 1,position_Y_sub - 2])

		# Sexto movimiento posible | derecha abajo
		if (position_X_add < self.X_MAX and position_Y_add < self.Y_MAX):
			if (self.board[position_X_add][position_Y_add] == 0):
				possibilities.append([position_X_add,position_Y_add])
			elif (self.board[position_X_add][position_Y_add] != self.INVALID):
				if(self.verify_jump([position_X_add + 1,position_Y_add + 2])):
					possibilities.append([position_X_add + 1,position_Y_add + 2])

		return possibilities

	def verify_jump(self, position):
		return position[0] in range(self.X_MIN,self.X_MAX) and position[1] in range(self.Y_MIN,self.Y_MAX) and self.board[position[0]][position[1]] == self.EMPTY



if __name__== "__main__":
	Test = Game()

	Test.start_game() 