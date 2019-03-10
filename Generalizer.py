class Generalizer:
	def __init__(self):
		self.independent_weight = 0.001

		self.player1_start_weight = 0.015
		self.player1_far_weight = 0.035
		self.player1_middle_weight = 0.055
		self.player1_near_weight = 0.075
		self.player1_end_weight = 0.1

		self.player2_start_weight = 0.0015
		self.player2_far_weight = -0.02
		self.player2_middle_weight = -0.04
		self.player2_near_weight = -0.06
		self.player2_end_weight = -0.1

		self.print()

	def get_independent_weight(self):
		return self.independent_weight

	def get_player1_start_weight(self):
		return self.player1_start_weight

	def get_player1_far_weight(self):
		return self.player1_far_weight

	def get_player1_middle_weight(self):
		return self.player1_middle_weight

	def get_player1_near_weight(self):
		return self.player1_near_weight

	def get_player1_end_weight(self):
		return self.player1_end_weight

	def get_player2_start_weight(self):
		return self.player2_start_weight

	def get_player2_far_weight(self):
		return self.player2_far_weight

	def get_player2_middle_weight(self):
		return self.player2_middle_weight

	def get_player2_near_weight(self):
		return self.player2_near_weight

	def get_player2_end_weight(self):
		return self.player2_end_weight

	def set_independent_weight(self, value):
		self.independent_weight = value

	def set_player1_start_weight(self, value):
		self.player1_start_weight = value

	def set_player1_far_weight(self, value):
		self.player1_far_weight = value

	def set_player1_middle_weight(self, value):
		self.player1_middle_weight = value

	def set_player1_near_weight(self, value):
		self.player1_near_weight = value

	def set_player1_end_weight(self, value):
		self.player1_end_weight = value

	def set_player2_start_weight(self, value):
		self.player2_start_weight = value

	def set_player2_far_weight(self, value):
		self.player2_far_weight = value

	def set_player2_middle_weight(self, value):
		self.player2_middle_weight = value

	def set_player2_near_weight(self, value):
		self.player2_near_weight = value

	def set_player2_end_weight(self, value):
		self.player2_end_weight = value

	def adjust_weights(self):
		
		self.print()

	def print(self):
		print("Independent weight:\t", self.independent_weight)
		print()
		print("P1 | Start weight:\t", self.player1_start_weight)
		print("P1 | Far weight:\t", self.player1_far_weight)
		print("P1 | Middle weight:\t", self.player1_middle_weight)
		print("P1 | Near weight:\t", self.player1_near_weight)
		print("P1 | End weight:\t", self.player1_end_weight)
		print()
		print("P2 | Start weight:\t", self.player2_start_weight)
		print("P2 | Far weight:\t", self.player2_far_weight)
		print("P2 | Middle weight:\t", self.player2_middle_weight)
		print("P2 | Near weight:\t", self.player2_near_weight)
		print("P2 | End weight:\t", self.player2_end_weight)
		print()
