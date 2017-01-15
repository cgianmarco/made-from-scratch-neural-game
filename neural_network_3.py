import math

from random import randint, random, uniform

import sys

import pygame

from simplenn import *


############# constants ###############

"""
Environment constants

"""

size_y = 80

size_x = 640

spaceship_radius = 10

meteor_radius = 10

counter = 0



"""
Genetic algorithm constants

"""

population_size = 200 # MUST BE EVEN!

gene_size = 10

mutation_rate = 0.01

crossover_rate = 0.7

target_score = 20000000








############## classes ################

class spaceship:

	

	def __init__(self):

		self.y = randint(spaceship_radius, size_y - spaceship_radius)

		self.x = 50

		self.v = 0

		self.old_v = 0

		self.distance_to_border = size_y - self.y

		self.destroyed = 0

		self.last_side = 0


	def move(self):

			if self.y + spaceship_radius + self.v > size_y:

				self.y = size_y - spaceship_radius

				# self.y = self.y - self.v

			if self.y - spaceship_radius + self.v < 0:

				self.y = spaceship_radius

				# self.y = self.y - self.v

			else:

				self.y = self.y + self.v

			self.distance_to_border = size_y - self.y


	def y_distance_to_meteor(self, meteor):

		return meteor.y - self.y


	def x_distance_to_meteor(self, meteor):

		return meteor.x - self.x


	def print_spaceship(self):

		print "spaceship.x = " + str(self.x)

		print "spaceship.y = " + str(self.y)

		print "spaceship.v = " + str(self.v)


	def get_closest_meteor(self, meteor1, meteor2):

		distance_to_meteor_1 = math.sqrt( self.x_distance_to_meteor(meteor1)**2 + self.y_distance_to_meteor(meteor1)**2 )

		distance_to_meteor_2 = math.sqrt( self.x_distance_to_meteor(meteor2)**2 + self.y_distance_to_meteor(meteor2)**2 )

		if distance_to_meteor_1 > distance_to_meteor_2:

			return meteor2

		else:

			return meteor1


class meteor:

	
	def __init__(self):

		self.x = 0

		self.y = randint(0, size_y)

		self.v = -4



	def move(self):

		if self.x > 0:

			self.x = self.x + self.v

		else:

			self.x = size_x

			self.y = randint(0, size_y)


	def print_meteor(self):

		print "meteor.x = " + str(self.x)

		print "meteor.y = " + str(self.y)

		print "meteor.v = " + str(self.v)



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



############ genetic algorithm #############




def create_population():

	return [ create_gene(gene_size) for i in range(population_size) ]


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



def initialize_fitness_scores():

		return [ 0 for i in range(population_size) ]



def crossover(father, mother):

	crossover_index = randint(1, gene_size - 1)

	sum_father = 0

	sum_mother = 0

	for i in range(gene_size):

		sum_father = sum_father + father[i]

	for i in range(gene_size):

		father[i] = father[i] / sum_father

	for i in range(gene_size):

		sum_mother = sum_mother + mother[i]

	for i in range(gene_size):

		mother[i] = mother[i] / sum_mother



	if random() < crossover_rate:

		child_one = father[:crossover_index] + mother[crossover_index:]

		

		child_two = mother[:crossover_index] + father[crossover_index:]

		

	else:

		child_one = father

		child_two = mother

	# print "child one is " + str(child_one) + "\n"

	# print "child two is " + str(child_two) + "\n"


	return [child_one, child_two]



def get_gene_sum(gene):

	sum = 0

	for i in range(gene_size):

		sum = sum + gene[i]

	return sum



def mutate(gene):

	if random() < mutation_rate:

		if random() > 0.5:

			gene[ randint(0, gene_size - 1) ] = uniform(0, max(gene))

		else:

			gene[ randint(0, gene_size - 1) ] = -uniform(0, max(gene))

	return gene



def getBestIndividuals(population, fitness_scores):

	first_best = 0;

	second_best = 0;

	for i in range(len(population)):

		if fitness_scores[i] > fitness_scores[first_best]:

			first_best = i

	for j in range(len(population)):

		if j != first_best:

			if fitness_scores[j] > fitness_scores[second_best]:

				second_best = j

			if second_best == first_best:

				second_best = second_best + 1

	return [population[first_best], population[second_best]]


def roulette_wheel_selection(population, fitness_scores):

	# fitness_scores_max = max(fitness_scores)

	# roulette_value = uniform(0, fitness_scores_max)

	fitness_scores_sum = 0

	for i in range(population_size):

		fitness_scores_sum = fitness_scores_sum + fitness_scores[i]

	roulette_value = uniform(0, fitness_scores_sum)

	current = 0

	for i in range(population_size):

		current = current + fitness_scores[i]

		if current  > roulette_value:

			return population[i]

	if current == 0 :

		return population[randint(0, population_size - 1)]



def update_fitness_scores():

	global counter

	population_score_sum = 0

	for i in range(population_size):

		# print i

		s = spaceship()

		s.y = size_y/2

		m = meteor()

		m2 = meteor()

		# m3 = meteor()

		m.x = randint(size_x, size_x + 300)

		m2.x = randint(size_x + 300, size_x + 700)

		# m3.x = randint(size_x, size_x + 200)

		m.y = randint(meteor_radius, size_y - meteor_radius)

		m2.y = randint(meteor_radius, size_y - meteor_radius)

		# m3.y = randint(meteor_radius, size_y - meteor_radius)

		fitness_scores[i] = 0

		

		counter = counter + 1

		# print counter

		while s.destroyed != 1:

			# if counter > 1000:

			# msElapsed = clock.tick(100)

			# else:

			msElapsed = clock.tick(100)

			screen.fill(white)



			# inputs = [ s.y, w1,  s.distance_to_border, s.x_distance_to_meteor(m), w2, s.y_distance_to_meteor(m) ]



			# inputs_first_layer = [ s.y, s.distance_to_border, -1, s.x_distance_to_meteor(m), s.y_distance_to_meteor(m), -1, s.x_distance_to_meteor(m2), s.y_distance_to_meteor(m2), -1]

			# inputs = [s.y, s.distance_to_border, s.x_distance_to_meteor(m), s.y_distance_to_meteor(m), s.x_distance_to_meteor(m2), s.y_distance_to_meteor(m2)]

			inputs = [s.y, s.distance_to_border, s.x_distance_to_meteor(s.get_closest_meteor(m, m2)), s.y_distance_to_meteor(s.get_closest_meteor(m, m2))]

			network_inputs = [ inputs for j in range(2) ]

			# weights_first_layer = [population[i][0], population[i][1], population[i][2], population[i][4], population[i][5], population[i][6], population[i][8], population[i][9], population[i][10]]

			weights_first_neuron = [population[i][0], population[i][1], population[i][2], population[i][3]]

			# weights_first_neuron = [population[i][0], population[i][1], population[i][2], population[i][3]]

			weights_second_neuron = [population[i][5], population[i][6], population[i][7], population[i][8]]

			# weights_third_neuron = [population[i][14], population[i][15], population[i][16], population[i][17], population[i][18], population[i][19]]

			# weights_forth_neuron = [population[i][6], population[i][13], population[i][20]]

			weights_forth_neuron = [population[i][4], population[i][9]]

			# print weights_first_layer



			n1 = neuron(4)

			n2 = neuron(4)

			# n3 = neuron(6)

			n4 = neuron(2)




			l1 = layer()

			l2 = layer()


			l1.add_neuron(n1)

			l1.add_neuron(n2)

			# l1.add_neuron(n3)

			l2.add_neuron(n4)



			nn = network()

			nn.add_layer(l1)

			nn.add_layer(l2)

			# print weights_first_neuron


			n1.set_weights(weights_first_neuron)

			n2.set_weights(weights_second_neuron)

			# n3.set_weights(weights_third_neuron)

			n4.set_weights(weights_forth_neuron)


			nn.set_inputs(network_inputs)



			s.old_v = s.v

			s.v =  4 * nn.feedforward()

			# print s.v

			s.move()

			m.move()

			m2.move()

			check_collisions(s, m, m2)

			pygame.draw.circle(screen, red, (int(s.x), int(s.y)), 10, 2)

			pygame.draw.circle(screen, blue, (int(m.x), int(m.y)), 10, 2)

			pygame.draw.circle(screen, blue, (int(m2.x), int(m2.y)), 10, 2)

			pygame.display.update()

			# ((s.old_v > 0 and s.v <= 0) or (s.old_v <= 0 and s.v > 0)) and 
				
			# if s.y_distance_to_meteor(s.get_closest_meteor(m, m2)) > 40 and s.y_distance_to_meteor(s.get_closest_meteor(m, m2)) < 45:
			

			# fitness_scores[i] = fitness_scores[i] + 0.01

			if s.y > spaceship_radius and s.y < spaceship_radius + 5 and s.last_side == 1:

				fitness_scores[i] = fitness_scores[i] + 1

				s.last_side = -1

			if s.y < size_y - spaceship_radius and s.y > size_y - spaceship_radius - 5 and s.last_side == -1:

				fitness_scores[i] = fitness_scores[i] + 1

				s.last_side = 1

			if s.y == size_y - spaceship_radius:

				s.last_side == 1

			if s.y == spaceship_radius:

				s.last_side = -1 

			# if s.y < size_y/2 + 10 and s.y > size_y/2 - 10:

			# fitness_scores[i] = fitness_scores[i] + 1

		population_score_sum = population_score_sum + fitness_scores[i]

		# print "gene number " + str(i) + "got fitness score " + str(fitness_scores[i])

	print "Average population fitness is " + str(population_score_sum/200.0)

	for i in range(population_size):

		if fitness_scores[i] == max(fitness_scores):

			print population[i]




def evolve(population, fitness_scores):

	new_population = []

	while len(new_population) < population_size:

		selected_gene_one = roulette_wheel_selection(population, fitness_scores)

		selected_gene_two = roulette_wheel_selection(population, fitness_scores)

		# print "gene one is : " + str(selected_gene_one) + "\n\n"

		# print "gene two is : " + str(selected_gene_two) + "\n\n"

		new_population.append(mutate(crossover(selected_gene_one, selected_gene_two)[0]))

		new_population.append(mutate(crossover(selected_gene_one, selected_gene_two)[1]))

		# print "child one is : " + str(crossover(selected_gene_one, selected_gene_two)[0]) + "\n\n"

		# print "child two is : " + str(crossover(selected_gene_one, selected_gene_two)[1]) + "\n\n"

	return new_population


	# return [ mutate( crossover ( getBestIndividuals(population, fitness_scores)[0], getBestIndividuals(population, fitness_scores)[1] ) ) for i in range(population_size)]


############## general methods ###############

def check_collisions(spaceship, meteor1, meteor2):

	distance_to_meteor_1 = math.sqrt( spaceship.x_distance_to_meteor(meteor1)**2 + spaceship.y_distance_to_meteor(meteor1)**2 )

	distance_to_meteor_2 = math.sqrt( spaceship.x_distance_to_meteor(meteor2)**2 + spaceship.y_distance_to_meteor(meteor2)**2 )

	if distance_to_meteor_1 < spaceship_radius + meteor_radius or distance_to_meteor_2 < spaceship_radius + meteor_radius:

		spaceship.destroyed = 1




################## tests ####################


pygame.init()

clock = pygame.time.Clock()

red = (255,0,0)
blue = (0,255,0)
white = (255,255,255)

counter = 0

screen = pygame.display.set_mode((660,500))

     



population = create_population()

# population = [[-0.00680879185833967, 0.14963507340904908, 0.03255125827714044, -0.06480309394748807, -0.006162988766075966, -0.23217942675974462, 0.9477039520768346, -0.15940510828385066, -2.5921377834130097, 2.9316069092654846] for i in range(population_size)]

population = [[-0.004200868032921885, 0.09047105445532605, 0.5234182684015307, 0.8271533403127935, -0.42044401736308484, 0.2903291183706598, -0.0622041198455559, -0.0648503553616526, 0.5289123919655885, -0.772651139750606] for i in range(population_size)]

fitness_scores = initialize_fitness_scores()

print max(fitness_scores)

while max(fitness_scores) < target_score:

	update_fitness_scores()

	# population = evolve(population, fitness_scores)

	# print max(fitness_scores)

print population



# population = create_population()

# print population

# i = 0

# while i < 10:

# 	gene1 = roulette_wheel_selection(population, fitness_scores)

# 	gene2 = roulette_wheel_selection(population, fitness_scores)

# 	print "parents: "

# 	print str(gene1) + "\n\n"

# 	print str(gene2) + "\n\n"

# 	print "crossover results: "

# 	print crossover(gene1, gene2)[0]

# 	print crossover(gene1, gene2)[1]


# 	i = i + 1




# print "Father gene is " + str(population[0])

# print "Mother gene is " + str(population[1])

# child = crossover(population[0], population[1])

# print "Child gene is " + str(child)

# mutate(child)

# print "Mutated child gene is " + str(child)

# print population

# print evolve(population, fitness_scores)





################## setup ####################



# fitness_scores = initialize_fitness_scores()

# population = create_population()

# s.v = 1

# s.print_spaceship()

# s.move()

# s.print_spaceship()

# print s.x_distance_to_meteor(m)
# print s.y_distance_to_meteor(m)

# m.move()

# print s.x_distance_to_meteor(m)
# print s.y_distance_to_meteor(m)

# print population[0]

# inputs = [ s.y,  s.x_distance_to_meteor(m),  s.y_distance_to_meteor(m) ]

# n = neuron(inputs, population[0])

# s.v = n.generate_v()

# s.move()


# for i in range(population_size):

# 	s = spaceship()

# 	m = meteor()

# 	while s.destroyed != 1:

# 		inputs = [ s.y,  s.x_distance_to_meteor(m),  s.y_distance_to_meteor(m) ]

# 		n = neuron(inputs, population[0])

# 		s.v = n.generate_v()

# 		s.move()

# 		m.move()

# 		check_collisions(s, m)

# 		fitness_scores[i] = fitness_scores[i] + 1

# 	print "Fitness score of gene number " + str(i) + " is equal to " + str(fitness_scores[i])