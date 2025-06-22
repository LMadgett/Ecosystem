import random
import pygame

MUTATION_RATE = 0.1

class Animal:
    def __init__(self, genes, position):
        self.type = genes[0]
        self.food_value = genes[1]
        self.efficiency = genes[2]
        self.move_distance = genes[3]
        self.reproductive_urge = genes[4]
        self.genes = genes
        self.position = position
        self.alive = True
        self.energy = 10

    def get_eaten(self, predator):
        self.alive = False
        if predator.energy <= 100 - self.food_value * 0.1:
            predator.energy += self.food_value * 0.1
    
    def eat(self, food):
        food.get_eaten(self)
    
    def move(self, new_position):
        self.position = new_position
        #self.energy -= (100 / self.efficiency) * distance_moved

    def reproduce(self, partner):
        if self.type == partner.type:
            new_genes = [self.type]
            for i in range(1, len(self.genes)):
                if random.random() < MUTATION_RATE:
                    new_genes.append(random.randint(5, 100))
                else:
                    new_genes.append((self.genes[i] + partner.genes[i]) // 2)
        offspring = Animal(new_genes, self.position)
        return offspring

def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

class Food:
    def __init__(self, food_value, position):
        self.food_value = food_value
        self.position = position
        self.alive = True

    def get_eaten(self, predator):
        self.alive = False
        if predator.energy <= 100 - self.food_value * 0.1:
            predator.energy += self.food_value * 0.1

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
        genes.append(random.randint(5, 100)) #reproductive urge
        position = (random.randint(0, x_size), random.randint(0, y_size))
        rabbits.append(Animal(genes, position))
    
    for f in range(num_foxes):
        genes = []
        genes.append("fox")
        genes.append(random.randint(50, 100)) #food value
        genes.append(random.randint(25, 100)) #efficiency
        genes.append(random.randint(10, 100)) #move distance
        genes.append(random.randint(5, 100)) #reproductive urge
        position = (random.randint(0, x_size), random.randint(0, y_size))
        foxes.append(Animal(genes, position))

    for n in range(num_food):
        position = (random.randint(0, x_size), random.randint(0, y_size))
        food_value = random.randint(10, 100)
        food.append(Food(food_value, position))

    ecosystem = [rabbits, foxes, food, x_size, y_size]
    return ecosystem

def move_animals(ecosystem):
    for rabbit in ecosystem[0]:
        if not rabbit.alive:
            continue
        else:
            action = ""
            if rabbit.energy < 100 - rabbit.reproductive_urge:
                action = "eat"
            elif rabbit.energy > 100 - rabbit.reproductive_urge:
                action = "reproduce"
            
            if action == "eat":
                closest_food = min(ecosystem[2], key=lambda f: distance(rabbit.position, f.position))
                #print(closest_food.position)
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
    for fox in ecosystem[1]:
        if not fox.alive:
            continue
        else:
            action = ""
            if fox.energy < 100 - fox.reproductive_urge:
                action = "eat"
            elif fox.energy > 100 - fox.reproductive_urge:
                action = "reproduce"
            
            if action == "eat":
                closest_rabbit = min(ecosystem[0], key=lambda r: distance(fox.position, r.position) if r.alive else float('inf'))
                if distance(fox.position, closest_rabbit.position) <= fox.move_distance and closest_rabbit.alive:
                    fox.move(closest_rabbit.position)
                    fox.eat(closest_rabbit)
                else:
                    # Move towards the closest rabbit by up to move_distance
                    dx = closest_rabbit.position[0] - fox.position[0]
                    dy = closest_rabbit.position[1] - fox.position[1]
                    dist = distance(fox.position, closest_rabbit.position)
                    if dist == 0:
                        ratio = 0
                    else:
                        ratio = fox.move_distance / dist
                    if ratio > 1:
                        ratio = 1
                    new_x = fox.position[0] + dx * ratio
                    new_y = fox.position[1] + dy * ratio
                    new_position = (new_x, new_y)
                    fox.move(new_position)
            elif action == "reproduce":
                # Find the closest other fox to reproduce with
                other_foxes = [f for f in ecosystem[1] if f is not fox and f.alive]
                if not other_foxes:
                    return
                closest_fox = min(other_foxes, key=lambda f: distance(fox.position, f.position))
                if distance(fox.position, closest_fox.position) <= fox.move_distance:
                    fox.move(closest_fox.position)
                    # Attempt to reproduce if close enough
                    offspring = fox.reproduce(closest_fox)
                    ecosystem[1].append(offspring)
                else:
                    # Move towards the closest fox by up to move_distance
                    dx = closest_fox.position[0] - fox.position[0]
                    dy = closest_fox.position[1] - fox.position[1]
                    dist = distance(fox.position, closest_fox.position)
                    ratio = fox.move_distance / dist
                    if ratio > 1:
                        ratio = 1
                    new_x = fox.position[0] + dx * ratio
                    new_y = fox.position[1] + dy * ratio
                    new_position = (new_x, new_y)
                    fox.move(new_position)
    
def display_ecosystem():
    num_rabbits = 2
    num_foxes = 2
    num_food = 20
    x_size = 800
    y_size = 600
    
    ecosystem = initialise_ecosystem(num_rabbits, num_foxes, num_food, x_size, y_size)
    
    pygame.init()
    screen = pygame.display.set_mode((ecosystem[3], ecosystem[4]))
    pygame.display.set_caption("Ecosystem Simulation")
    
    count = 0
    running = True
    while running:
        count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #print(count)

        screen.fill((0, 0, 0))
        move_animals(ecosystem)
        
        for rabbit in ecosystem[0]:
            #print(rabbit.position)
            if rabbit.alive:
                pygame.draw.circle(screen, (255, 255, 0), (int(rabbit.position[0]), int(rabbit.position[1])), 10)
        
        for fox in ecosystem[1]:
            if fox.alive:
                pygame.draw.circle(screen, (255, 0, 0), (int(fox.position[0]), int(fox.position[1])), 10)
                #print(fox.position)
        
        for food in ecosystem[2]:
            if food.alive:
                pygame.draw.circle(screen, (0, 255, 0), (int(food.position[0]), int(food.position[1])), 6)
        
        pygame.display.flip()

display_ecosystem()