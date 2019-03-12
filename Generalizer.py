class Generalizer:
	def __init__(self):
		#self.independent_weight = 0.001

		#self.player1_start_weight = 0.01
		#self.player1_far_weight = 0.025
		#self.player1_middle_weight = 0.05
		#self.player1_near_weight = 0.075
		#self.player1_end_weight = 0.1

		#self.player2_start_weight = 0.02
		#self.player2_far_weight = 0.01
		#self.player2_middle_weight = -0.04
		#self.player2_near_weight = -0.06
		#self.player2_end_weight = -0.1

		self.weights = [0.001, 0.01, 0.025, 0.05, 0.075, 0.1, 0.02, 0.01, -0.04, -0.06, -0.1]

		self.mu = 0.05

		self.print()

	def get_independent_weight(self):
		return self.weights[0]

	def get_player1_start_weight(self):
		return self.weights[1]

	def get_player1_far_weight(self):
		return self.weights[2]

	def get_player1_middle_weight(self):
		return self.weights[3]

	def get_player1_near_weight(self):
		return self.weights[4]

	def get_player1_end_weight(self):
		return self.weights[5]

	def get_player2_start_weight(self):
		return self.weights[6]

	def get_player2_far_weight(self):
		return self.weights[7]

	def get_player2_middle_weight(self):
		return self.weights[8]

	def get_player2_near_weight(self):
		return self.weights[9]

	def get_player2_end_weight(self):
		return self.weights[10]

	def set_independent_weight(self, value):
		self.weights[0] = value

	def set_player1_start_weight(self, value):
		self.weights[1] = value

	def set_player1_far_weight(self, value):
		self.weights[2] = value

	def set_player1_middle_weight(self, value):
		self.weights[3] = value

	def set_player1_near_weight(self, value):
		self.weights[4] = value

	def set_player1_end_weight(self, value):
		self.weights[5] = value

	def set_player2_start_weight(self, value):
		self.weights[6] = value

	def set_player2_far_weight(self, value):
		self.weights[7] = value

	def set_player2_middle_weight(self, value):
		self.weights[8] = value

	def set_player2_near_weight(self, value):
		self.weights[9] = value

	def set_player2_end_weight(self, value):
		self.weights[10] = value

	def parse_number(s):
		return int(s)

	def adjust_weights(self):
		file = open('test.txt', 'r')
		tuplas_resultado = []
		tuplas_resultado.append([])
		for line in file:
			values = line.split('-')
			values[len(values)-1].replace('\n','')
			if (len(values) > 1):
				tuplas_resultado.append(list(map(self.parse_number(),values)))
			else:
				tuplas_resultado[0] = [int(values[0])]

		for i in range(1, len(tuplas_resultado)):
			for j in range(0, len(tuplas_resultado[i])):
				self.weights[j] = self.weights[j] + mu*(tuplas_resultado[0][0] - 1)*tuplas_resultado[i][j]
 

		self.print()

	def print(self):
		print("Independent weight:\t", self.weights[0])
		print()
		print("P1 | Start weight:\t", self.weights[1])
		print("P1 | Far weight:\t", self.weights[2])
		print("P1 | Middle weight:\t", self.weights[3])
		print("P1 | Near weight:\t", self.weights[4])
		print("P1 | End weight:\t", self.weights[5])
		print()
		print("P2 | Start weight:\t", self.weights[6])
		print("P2 | Far weight:\t", self.weights[7])
		print("P2 | Middle weight:\t", self.weights[8])
		print("P2 | Near weight:\t", self.weights[9])
		print("P2 | End weight:\t", self.weights[10])
		print()
