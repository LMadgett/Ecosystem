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
            predator.energy += self.food_value
    
    def eat(self, food):
        food.get_eaten(self)
    
    def move(self, new_position):
        distance_moved = distance(self.position, new_position)
        if distance_moved < self.move_distance:
            self.position = new_position
            self.energy -= (1 / self.efficiency) * distance_moved

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

    def __init__(self, position):
        self.position = position
    
    def get_eaten(self, predator):
        self.alive = False
        if predator.energy <= 100 - self.food_value:
            predator.energy += self.food_value

def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5