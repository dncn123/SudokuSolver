import numpy as np
from GeneticAlgorithm import GeneticAlgorithm


ii = 200
quizzes = np.load("quizzes.npy")[:ii]

gens = []

for i in range(ii):
	GA = GeneticAlgorithm(quizzes[0], 100)
	GA.run(1000)
	gens.append(len(GA.fitness_avg))

gens = np.array(gens)
print(gens.mean())
