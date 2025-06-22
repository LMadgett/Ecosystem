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
    alive = True
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
    ecosystem = []

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

    ecosystem = [rabbits, foxes, food]

def move_animals(ecosystem):
    for rabbit in ecosystem[0]:
        if not rabbit.alive:
            continue
        else:
            action = ""
            if rabbit.energy > rabbit.reproductive_urge:
                action = "eat"
            elif rabbit.energy < rabbit.reproductive_urge:
                action = "reproduce"
            
            if action == "eat":
                closest_food = min(ecosystem[2], key=lambda f: distance(rabbit.position, f.position))
                if distance(rabbit.position, closest_food.position) <= rabbit.move_distance:
                    rabbit.move(closest_food.position)
                    rabbit.eat(closest_food)
                else:
                    # Move towards the closest food by up to move_distance
                    dx = closest_food.position[0] - rabbit.position[0]
                    dy = closest_food.position[1] - rabbit.position[1]
                    dist = distance(rabbit.position, closest_food.position)
                    ratio = rabbit.move_distance / dist
                    if ratio > 1:
                        ratio = 1
                    new_x = rabbit.position[0] + dx * ratio
                    new_y = rabbit.position[1] + dy * ratio
                    new_position = (new_x, new_y)
                    rabbit.move(new_position)
            elif action == "reproduce":
                # Find the closest other rabbit to reproduce with
                other_rabbits = [r for r in ecosystem[0] if r is not rabbit and r.alive]
                if not other_rabbits:
                    return
                closest_rabbit = min(other_rabbits, key=lambda r: distance(rabbit.position, r.position))
                if distance(rabbit.position, closest_rabbit.position) <= rabbit.move_distance:
                    rabbit.move(closest_rabbit.position)
                    # Attempt to reproduce if close enough
                    offspring = rabbit.reproduce(closest_rabbit)
                    ecosystem[0].append(offspring)
                else:
                    # Move towards the closest rabbit by up to move_distance
                    dx = closest_rabbit.position[0] - rabbit.position[0]
                    dy = closest_rabbit.position[1] - rabbit.position[1]
                    dist = distance(rabbit.position, closest_rabbit.position)
                    ratio = rabbit.move_distance / dist
                    if ratio > 1:
                        ratio = 1
                    new_x = rabbit.position[0] + dx * ratio
                    new_y = rabbit.position[1] + dy * ratio
                    new_position = (new_x, new_y)
                    rabbit.move(new_position)