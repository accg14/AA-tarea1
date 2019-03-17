import os, datetime, numpy, pdb

class Generalizer:
	def __init__(self):
		self.load_initial_weights()
		self.mu = 0.1


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

			sum_error += difference #/ norm
		file.close()

		final_error = sum_error / sample_size
		if (final_error < 0,3):
			return 0.03
		elif (final_error < 0,6):
			return 0.06
		else:
			return 0.09


	def adjust_weights(self,result):
		self.old_weights = list(map(lambda x : x, self.weights))

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
				
				self.weights[0] = self.weights[0] + self.mu*(b[1] - b[0]) #w0
				
				for i in range(2, len(self.weights)):
					# w(i) <- w(i) + mu(V_train_(b) - V_aprox_(b))x(i)
					self.weights[i] = self.weights[i] + self.mu*(b[1] - b[0])*b[i]

			norm = 0
			for w in self.weights:
				norm += numpy.power(w, 2)
			norm = numpy.sqrt(norm)

			for i in range(len(self.weights)):
				self.weights[i] /= norm

			file.close()
		self.persist_metrics(games)
		self.persist_new_weights()

