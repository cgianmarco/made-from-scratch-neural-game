


import math

from random import randint, random, uniform


########### overall methods ############


def erf(x):
	"""
	Approximation of error function

	"""
	# save the sign of x
	sign = 1 if x >= 0 else -1

	x = abs(x)

	# constants
	a1 =  0.254829592

	a2 = -0.284496736

	a3 =  1.421413741

	a4 = -1.453152027

	a5 =  1.061405429

	p  =  0.3275911

	# A&S formula 7.1.26
	t = 1.0/(1.0 + p*x)

	y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)

	return sign*y


############## classes ################


class neuron:


	def __init__ (self, number_of_inputs):

		self.inputs = []

		self.weights = []

		self.number_of_inputs = number_of_inputs


	def set_inputs(self, inputs):

		self.inputs = inputs


	def set_weights(self, weights):

		self.weights = weights

	def get_inputs(self):

		return self.inputs


	def get_weights(self):

		return self.weights

	def process(self):

		"""
		Returns neuron output

		"""

		sum = 0

		for i in range(len(self.inputs)):

			sum = sum + self.inputs[i] * self.weights[i]

		# if sum < -700:

		# 	sum = -700

		return  erf(sum)



	# def generate_v(self):


	# 	sum = 0

	# 	sum_weights = 0

	# 	for i in range(len(self.inputs) - 1):

	# 		sum = sum + self.inputs[i] * self.weights[i]

	# 		sum_weights = sum_weights + self.weights[i]

	# 	if sum < -700:

	# 		sum = -700

	# 	if sum_weights != 0:

	# 		return 1/(1 + math.e ** (-sum)) - self.weights[len(self.weights) - 1]

	# 	else:

	# 		return 1/(1 + math.e ** (-sum))



class layer:


	def __init__(self):

		self.number_of_neurons = 0

		self.neurons = []

		self.number_of_inputs = 0


	def add_neuron(self, n):

		self.neurons.append(n)

		self.number_of_neurons = self.number_of_neurons + 1

		self.number_of_inputs = self.number_of_inputs + n.number_of_inputs

	def get_neurons(self):

		return self.neurons

	def feed(self, inputs):

		"""
		Feeds the inputs to each neuron

		"""

		for i in range(self.number_of_neurons):

			self.neurons[i].set_inputs(inputs[i])

	def forward(self, next_layer):

		"""
		Returns list of outputs of each neuron of the layer

		"""

		outputs = []

		if next_layer == None:

			return self.neurons[0].process()



		if next_layer.number_of_neurons != 1:

			for i in range(self.number_of_neurons):

				small_output = []

				for j in range(next_layer.number_of_inputs/next_layer.number_of_neurons):

					small_output.append(self.neurons[i].process())

				outputs.append(small_output)

			return outputs

		else:

			small_output = []

			for i in range(self.number_of_neurons):	

				small_output.append(self.neurons[i].process())

			outputs.append(small_output)

			return outputs


class network:

	def __init__(self):

		self.number_of_layers = 0

		self.layers = []

		self.inputs = []

	def add_layer(self, l):

		self.layers.append(l)

		self.number_of_layers = self.number_of_layers + 1

	def get_layers(self):

		return self.layers


	def set_inputs(self, inputs):

		self.inputs = inputs

		self.layers[0].feed(inputs)


	def feedforward(self):

		"""
		Returns output of the network

		"""

		for i in range(self.number_of_layers - 1):

			self.layers[i].feed(self.inputs)

			self.inputs = self.layers[i].forward(self.layers[i + 1])

			# print self.inputs

		self.layers[self.number_of_layers - 1].feed(self.inputs)

		self.inputs = self.layers[self.number_of_layers - 1].forward(None)


		return self.inputs






############ genetic algorithm #############




def create_gene(gene_size):

	"""
	Returns array of weights

	"""
	weights = []

	for i in range(gene_size):

		if(random() > 0.5):

			weights.append(-random())

		else:

			weights.append(random())


	return weights










