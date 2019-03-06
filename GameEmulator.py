import random

class Game:
	PLAYER_ONE = 1
	PLAYER_TWO = 2
	EMPTY = 0
	LENGTH = 12
	INVALID = -1
	PIECES = 10
	def __init__(self):
		self.board = create_board()
		self.player_turn = 1
		self.player_one_pieces = __initialize_pieces(PLAYER_ONE)
		self.player_two_pieces = __initialize_pieces(PLAYER_TWO)
	def __initialize_pieces(self, player_id):
		pieces = []
		if (player_id == PLAYER_ONE):
			pieces = [ [0, 6], [1, 6], [1, 7], [2, 5],[2,6],[2,7],[3,5], [3,6], [3,7], [3,8]]
		else:
			pieces = [[16,6],[15,6],[15,7],[14,5],[14,6],[14,7],[13,5],[13,6],[13,7],[13,8]]
		return pieces
	def create_board_line(start, end, value):
		row = []
		for i in LENGTH:
			if i in range(start, end):
				row[i] = value
			else:
				row[i] = INVALID
		return row
	def create_board:
		board = []
		board[0] = create_board_line(6,6,PLAYER_ONE)
		board[1] = create_board_line(6,7, PLAYER_ONE)
		board[2] = create_board_line(5,7,PLAYER_ONE)
		board[3] = create_board_line(5,8,PLAYER_ONE)
		board[4] = create_board_line(0,12, EMPTY)
		board[5] = create_board_line(1,12, EMPTY)
		board[6] = create_board_line(1,11, EMPTY)
		board[7] = create_board_line(2,11, EMPTY)
		board[8] = create_board_line(2,10, EMPTY)
		board[9] = board[7]
		board[10] = board[6]
		board[11] = board[5]
		board[12] = board[4]
		board[13] = create_board_line(5,6, PLAYER_TWO)
		board[14] = create_board_line(5,7, PLAYER_TWO)
		board[15] = create_board_line(6,7, PLAYER_TWO)
		board[16] = create_board_line(6,6, PLAYER_TWO)
		return board
	def start_game(self):
		while not __game_over():
			__move()
			__save_state()

	def __move(self):
		id_piece, new_pos = __calculate_random_move()
		if (player_turn == PLAYER_ONE):
			old_pos = self.player_one_pieces[id_piece]
			self.player_one_pieces[id_piece] = new_pos

		else:
			old_pos = self.player_two_pieces[id_piece]
			self.player_two_pieces[id_piece] = new_pos

		self.board[new_pos[0]][new_pos[1]] = player_turn
		self.board[old_pos[0]][old_pos[1]] = EMPTY

		player_turn = player_turn % 2 + 1

	def __game_over(self):
		i = 0
		if (self.player_turn = PLAYER_ONE):
			while (i < PIECES and self.player_one_pieces[i][0] > 13):
				i += 1
		else:
			while (i < PIECES and self.player_two_pieces[i][0] < 4):
				i += 1
		return i == PIECES
	def __save_state():
		
	def __calculate_random_move(self):
  		piece = random.randint(0,9)

  		if self.player_turn == PLAYER_ONE:
  			actual_pos = self.player_one_pieces[piece]
  		else:
  			actual_pos = self.player_two_pieces[piece]

  		possible_moves = 0

  		for i in range(actual_pos[0] -1,actual_pos[0] -1):
  				for j in range(actual_pos[1] -1, actual_pos[1]-1):
  					if (self.board[i][j] == EMPTY and j != actual_pos[1]):
  						possible_moves += 1

  		selected_move = random.randint(1,possible_moves)
  		
  		if self.player_turn == PLAYER_ONE:
  			new_pos = self.player_one_pieces[piece]
  		else:
  			new_pos = self.player_two_pieces[piece]

  		if selected_move == 1:
  			new_pos = [new_pos[0] - 1, new_pos[1] - 1]
  		elif selected_move == 2:
  			new_pos = [new_pos[0] - 1, new_pos[1] + 1]
  		elif selected_move == 3:
  			new_pos = [new_pos[0], new_pos[1] - 1]
  		elif selected_move == 4:
  			new_pos = [new_pos[0], new_pos[1] + 1]
  		elif selected_move == 5:
  			new_pos = [new_pos[0] + 1, new_pos[1] - 1]
  		elif selected_move == 6:
  			new_pos = [new_pos[0] + 1, new_pos[1] + 1]
  		return (pos, new_pos)




















