import os, datetime, numpy, pdb

class Generalizer:
	def __init__(self):
		self.load_initial_weights()
		self.mu = 0.05
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


	def adjust_mu(self,result,filename):
		file = open(filename, 'r')
		sum_error = 0
		sample_size = 0
		for line in file:
			sample_size += 1
			values = line.split('|')
			values[len(values)-1].replace('\n','')
			
			tuple = list(map(lambda x: float(x), values)) # all values
			difference = numpy.power(result-tuple[0],2)
			
			i = 1
			norm = 0
			for i in range(len(tuple)):
				norm += numpy.power(tuple[i],2)
			norm = numpy.sqrt(norm)

			sum_error += difference / norm
		file.close()

		final_error = sum_error / sample_size
		if (final_error < 0,3):
			return 0.003
		elif (final_error < 0,6):
			return 0.006
		else:
			return 0.009


	def adjust_weights(self,result):
		mu_values = []
		for r in result:
			mu_values.append(self.adjust_mu(r[0],r[1]))

		if (mu_values):
			self.mu = sum(mu_values)/len(mu_values)

		games = [0, 0]
		for r in result:
			file = open(r[1], 'r')
			if (int(r[0]) == 1):
				games[0] += 1
			else:
				games[1] += 1
			for line in file:
				values = line.split('|')
				values[len(values)-1].replace('\n','')
				b = list(map(lambda x: float(x), values))
				for i in range(0, len(self.weights)):
					# w(i) <- w(i) + mu(V_train_(b) - V_aprox_(b))x(i)
					if i > 0: 
						self.weights[i] = self.weights[i] + self.mu*(r[0] - b[0])*b[i]
					else:
						self.weights[i] = self.weights[i] + self.mu*(r[0] - b[0]) #w0
			norm = 0
			for w in self.weights:
				norm += numpy.power(w,2)
			norm = numpy.sqrt(norm)

			for i in range(len(self.weights)):
				self.weights[i] /= norm

			file.close()
		self.persist_metrics(games)
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
