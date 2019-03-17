import os, datetime, numpy, pdb

class Generalizer:
	def __init__(self):
		self.load_initial_weights()
		self.mu = 2
		self.print_weights()


	def load_initial_weights(self):
		file = open('weights.txt', 'r')
		all_lines = file.readlines()
		file.close()

		last = all_lines[-1]
		values = last.split('|')
		self.weights = (list(map(lambda x: float(x), values)))

		last = all_lines[-2]
		values = last.split('|')
		self.old_weights = (list(map(lambda x: float(x), values)))


	def get_weights_for_player1(self):
		return self.weights

	def get_weights_for_player2(self):
		return self.old_weights


	def get_independent_weight(self):
		return self.weights[0]

	def get_player1_end_weight(self):
		return self.weights[1]

	def get_player2_end_weight(self):
		return self.weights[2]

	def get_player1_near_weight(self):
		return self.weights[3]

	def get_player2_near_weight(self):
		return self.weights[4]

	def get_player1_middle_weight(self):
		return self.weights[5]

	def get_player2_middle_weight(self):
		return self.weights[6]

	def get_player1_far_weight(self):
		return self.weights[7]

	def get_player2_far_weight(self):
		return self.weights[8]

	def get_player1_start_weight(self):
		return self.weights[9]

	def get_player2_start_weight(self):
		return self.weights[10]


	def set_independent_weight(self, value):
		self.weights[0] = value

	def set_player1_end_weight(self, value):
		self.weights[1] = value

	def set_player2_end_weight(self, value):
		self.weights[2] = value

	def set_player1_near_weight(self, value):
		self.weights[3] = value

	def set_player2_near_weight(self, value):
		self.weights[4] = value

	def set_player1_middle_weight(self, value):
		self.weights[5] = value

	def set_player2_middle_weight(self, value):
		self.weights[6] = value

	def set_player1_far_weight(self, value):
		self.weights[7] = value

	def set_player2_far_weight(self, value):
		self.weights[8] = value

	def set_player1_start_weight(self, value):
		self.weights[9] = value

	def set_player2_start_weight(self, value):
		self.weights[10] = value


	def persist_new_weights(self):
		file = open('weights.txt', 'a')
		weights_str = list(map(lambda x: str(x), self.weights))
		line = '|'.join(weights_str) + '\n'
		file.write(line)
		file.close()


	def persist_metrics(_, games):
		file = open('metric_results.txt', 'a')
		metric_str = list(map(lambda x: str(x), games))
		line = '|'.join(metric_str) + '\n'
		file.write(line)
		file.close()		


	def adjust_weights(self, results):
		self.old_weights = list(map(lambda x : x, self.weights))

		win_lose_games = [0, 0]
		for result in results:
			game_result = result[0]
			file_name = result[1]

			if(game_result == 1):
				mu = 0.0000001
			else:
				mu = 0.0001

			file = open(file_name, 'r')

			if (int(game_result) == 1):
				win_lose_games[0] += 1
			else:
				win_lose_games[1] += 1

			for line in file:
				values = line.split('|')
				values[len(values) - 1].replace('\n','')
				b = list(map(lambda x: float(x), values))
				self.weights[0] = self.weights[0] + mu*(b[1] - b[0]) #w0

				for i in range(2, len(self.weights)):
					# w(i) <- w(i) + mu(V_train_(b) - V_aprox_(b))x(i)
					self.weights[i] = self.weights[i] + mu*(b[1] - b[0])*b[i]

			norm = 0
			for w in self.weights:
				norm += numpy.power(w, 2)
			norm = numpy.sqrt(norm)

			for i in range(len(self.weights)):
				self.weights[i] /= norm

			file.close()
		self.persist_metrics(win_lose_games)
		self.persist_new_weights()


	def print_weights(self):
		print("Independent weight:\t", self.get_independent_weight())
		print()
		print("P1 | Start weight:\t", self.get_player1_start_weight())
		print("P1 | Far weight:\t", self.get_player1_far_weight())
		print("P1 | Middle weight:\t", self.get_player1_middle_weight())
		print("P1 | Near weight:\t", self.get_player1_near_weight())
		print("P1 | End weight:\t", self.get_player1_end_weight())
		print()
		print("P2 | Start weight:\t", self.get_player2_start_weight())
		print("P2 | Far weight:\t", self.get_player2_far_weight())
		print("P2 | Middle weight:\t", self.get_player2_middle_weight())
		print("P2 | Near weight:\t", self.get_player2_near_weight())
		print("P2 | End weight:\t", self.get_player2_end_weight())
		print()
