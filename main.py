import numpy as np
import math
import time
import random
import pygame
from random import randint


class Dot():
  def __init__(self, inputs, hiddenlayer, outputs):
    self.start_position = [0, 200]

    self.position = self.start_position[:]

    self.weights_1 = 0.10 * np.random.randn(inputs, hiddenlayer)
    self.weights_2 = 0.10 * np.random.randn(hiddenlayer, outputs)
    self.biases_1 = np.zeros((1, hiddenlayer))
    self.biases_2 = np.zeros((1, outputs))

  def reset(self):
    self.position = self.start_position[:]


  def move_xy(self, x, y, speed):
    self.position[0] += (x-0.5)*speed 
    self.position[1] += (y-0.5)*speed 
    

  def sigmoid(self, x):
    return 1 / (1 + np.exp(-x))
  def ReLU(self, x):
    return max(0.0, x)
  

  def mutate(self, chance, mutate_rate):
    for i in range(len(self.weights_1)):
      for k in range(len(self.weights_1[i])):
        if (randint(0,chance) == 1):
          self.weights_1[i][k] += random.uniform(-1, 1) * mutate_rate
    for i in range(len(self.biases_1[0])):
      if (randint(0,chance) == 1):
        self.biases_1[0][i] += random.uniform(-1, 1) * mutate_rate

    for i in range(len(self.weights_2)):
      for k in range(len(self.weights_2[i])):
        if (randint(0,chance) == 1):
          self.weights_2[i][k] += random.uniform(-1, 1) * mutate_rate
    for i in range(len(self.biases_2[0])):
      if (randint(0,chance) == 1):
        self.biases_2[0][i] += random.uniform(-1, 1) * mutate_rate
  
  def think(self, inputs):
    self.output_layer1 = self.sigmoid(np.dot(inputs, self.weights_1) + self.biases_1)
    self.output = np.dot(self.output_layer1, self.weights_2) + self.biases_2

class Goal():
  def __init__(self, speed):
    self.reset()
  def reset(self):
    self.start_position = [380, random.uniform(0, 400)]
    self.caught = False

    self.position = self.start_position[:]
    self.direction = [random.uniform(-1, 0), random.uniform(-0.5, 0.5)]

  def move(self, speed):

    self.position[0] += self.direction[0] *speed
    self.position[1] += self.direction[1] *speed


class Population():
  def __init__(self,size):
    self.population = size
    self.dots = list()
    for i in range(size):
      self.dots.append(Dot(4, 6, 2))
    self.goal = Goal(15)

  def runday(self, steps):
    self.goal.reset()
    for i in range(self.population):
      self.dots[i].steps = 0
    for i in range(steps):
      for i in range(self.population):
        self.dots[i].distance_x = self.goal.position[0] - self.dots[i].position[0]
        self.dots[i].distance_y = self.goal.position[1] - self.dots[i].position[1]
        self.dots[i].senses = [self.dots[i].distance_x, self.dots[i].distance_y, abs(self.dots[i].position[0] - 125), abs(self.dots[i].position[1] - 240)]
        # self.dots[i].senses = [self.dots[i].position[0], self.dots[i].position[1], self.goal.position[0], self.goal.position[1]]
      
      for i in range(self.population):
        self.dots[i].think(self.dots[i].senses)

      for i in range(self.population):
        self.dots[i].distance = (math.sqrt((self.goal.position[0] - self.dots[i].position[0])**2 + (self.goal.position[1] - self.dots[i].position[1])**2))
        self.dots[i].within_wall = False
        if (self.dots[i].position[0] > 120 and self.dots[i].position[0] < 130):
          if (self.dots[i].position[1] > 40 and self.dots[i].position[1] < 240):
            self.dots[i].within_wall =  True
            self.dots[i].steps+=1
            
        if (self.dots[i].distance > 10 and self.dots[i].within_wall == False):
          self.dots[i].move_xy((self.dots[i].output[0][0]), (self.dots[i].output[0][1]), 4)
          self.dots[i].steps +=1
        if(self.dots[i].distance < 10):
          self.goal.caught = True
      
      if (self.goal.caught == False):
        self.goal.move(1)
      

      screen.fill(background_color)
      if (True):#self.generation == 0):
        for i in range(self.population):
          pygame.draw.rect(screen, BLACK, (self.dots[i].position[0], self.dots[i].position[1], 3, 3))
      else:
        pygame.draw.rect(screen, BLACK, (self.dots[self.highest_fitness_index].position[0], self.dots[self.highest_fitness_index].position[1], 3, 3))
      pygame.draw.rect(screen, RED, (self.goal.position[0], self.goal.position[1], 5, 5))
      pygame.draw.rect(screen, BLACK, (120, 40, 10, 200))
      
      pygame.display.flip()
      # time.sleep(0.001)


    
    for i in range(self.population):
      self.dots[i].fitness =  self.dots[i].distance + (self.dots[i].steps /30)
      if(self.dots[i].within_wall == True):
        self.dots[i].fitness += 300

    self.best_fitness = 10000000
    self.added_fitness = 0
    self.highest_fitness_index = 0
    for i in range(self.population):
      self.added_fitness += self.dots[i].fitness
      if (self.dots[i].fitness < self.best_fitness):
        self.best_fitness = self.dots[i].fitness
        self.highest_fitness_index = i

    for i in range(self.population):
      if (self.dots[i].fitness > self.added_fitness / (self.population)):
        self.dots[i].weights_1[:] = self.dots[self.highest_fitness_index].weights_1[:]
        self.dots[i].biases_1[:] = self.dots[self.highest_fitness_index].biases_1[:]

        self.dots[i].weights_2[:] = self.dots[self.highest_fitness_index].weights_2[:]
        self.dots[i].biases_2[:] = self.dots[self.highest_fitness_index].biases_2[:]

      if (self.dots[i].fitness != self.best_fitness):
        self.dots[i].mutate(8, 0.2)

    for i in range (self.population):
      if (i == self.highest_fitness_index):
        self.dots[i].color = "green"
      else:
        self.dots[i].color = 'black'
        

    for i in range(self.population):
      self.dots[i].reset()
    
    print(self.dots[0].weights_1)
    print(self.dots[0].weights_2)
    print('steps: ', self.dots[self.highest_fitness_index].steps)
    print('distance: ', self.dots[self.highest_fitness_index].distance)
    print('highest_fitness: ', self.best_fitness)
    

print('------------------New Trial-------------------------')


pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('machine learning')
clock = pygame.time.Clock()


background_color = 0, 255, 0
RED = 255, 0, 0
BLACK = 0, 0, 0
dot_thickness = 5

pop = Population(50)
crash = False
while crash == False:
  for i in range(1000):
    pop.generation = i
    print('----New day, generation-----', pop.generation)
    pop.runday(235)
    # pygame.draw.rect(screen, RED, (random.randint(5, 6), 25, 100, 50), 5)
    # pygame.display.flip()
    # time.sleep(0.05)
    # time.sleep(10 / 1000)
  crash = True
