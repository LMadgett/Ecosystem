import random

MUTATION_RATE = 0.1

class Animal:
    type = ""
    food_value = 0
    efficiency = 0
    move_distance = 0
    reproductive_urge = 0
    position = (0, 0)
    alive = True
    energy = 100

    def __init__(self, genes, position):
        self.type = genes[0]
        self.food_value = genes[1]
        self.efficiency = genes[2]
        self.move_distance = genes[3]
        self.reproductive_urge = genes[4]
        self.position = position

    def get_eaten(self, predator):
        self.alive = False
        if predator.energy <= 100 - self.food_value:
            predator.energy += self.food_value * 0.1
    
    def eat(self, food):
        food.get_eaten(self)
    
    def move(self, new_position):
        distance_moved = distance(self.position, new_position)
        if distance_moved < self.move_distance:
            self.position = new_position
            self.energy -= (100 / self.efficiency) * distance_moved

    def reproduce(self, partner):
        if self.type == partner.type:
            new_genes = [self.type]
            for i in range(len(self.genes)):
                if random.random() < MUTATION_RATE:
                    new_genes.append(random.randint(0, 100))
                else:
                    new_genes.append((self.genes[i] + partner.genes[i]) // 2)
        offspring = Animal(new_genes, self.position)
        return offspring

class Food:
    position = (0, 0)
    food_value = 0

    def __init__(self, food_value, position):
        self.food_value = food_value
        self.position = position
    
    def get_eaten(self, predator):
        self.alive = False
        if predator.energy <= 100 - self.food_value:
            predator.energy += self.food_value

def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def initialise_ecosystem(num_rabbits, num_foxes, num_food, x_size, y_size):
    foxes = []
    rabbits = []
    food = []

    for r in range(num_rabbits):
        genes = []
        genes.append("rabbit")
        genes.append(random.randint(50, 100)) #food value
        genes.append(random.randint(25, 100)) #efficiency
        genes.append(random.randint(10, 100)) #move distance
        genes.append(random.randint(0, 100)) #reproductive urge
        position = (random.randint(0, x_size), random.randint(0, y_size))
        rabbits.append(Animal(genes, position))
    
    for f in range(num_foxes):
        genes = []
        genes.append("fox")
        genes.append(random.randint(50, 100)) #food value
        genes.append(random.randint(25, 100)) #efficiency
        genes.append(random.randint(10, 100)) #move distance
        genes.append(random.randint(0, 100)) #reproductive urge
        position = (random.randint(0, x_size), random.randint(0, y_size))
        foxes.append(Animal(genes, position))

    for n in range(num_food):
        position = (random.randint(0, x_size), random.randint(0, y_size))
        food_value = random.randint(10, 100)
        food.append(Food(food_value, position))