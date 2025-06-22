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
        self.energy = 50

    def get_eaten(self, predator):
        self.alive = False
        if predator.energy <= 100 - self.food_value * 0.1:
            predator.energy += self.food_value * 0.1
    
    def eat(self, food):
        food.get_eaten(self)
    
    def move(self, new_position):
        distance_moved = distance(self.position, new_position)
        self.energy -= (1 / self.efficiency) * distance_moved
        #print(self.energy)
        if new_position != self.position: #and self.energy > 0:
            self.position = new_position

    def reproduce(self, partner):
        if self.type == partner.type:
            new_genes = [self.type]
            for i in range(1, len(self.genes)):
                if random.random() < MUTATION_RATE:
                    new_genes.append(random.randint(5, 100))
                else:
                    new_genes.append((self.genes[i] + partner.genes[i]) // 2)
        offspring = Animal(new_genes, self.position)
        self.energy -= self.reproductive_urge
        partner.energy -= partner.reproductive_urge
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

    rabbit_min_food_value = 20
    rabbit_min_efficiency = 50
    rabbit_min_move_distance = 50
    rabbit_min_reproductive_urge = 20

    fox_min_food_value = 50
    fox_min_efficiency = 50
    fox_min_move_distance = 50
    fox_min_reproductive_urge = 10

    for r in range(num_rabbits):
        genes = []
        genes.append("rabbit")
        genes.append(random.randint(rabbit_min_food_value, 100)) #food value
        genes.append(random.randint(rabbit_min_efficiency, 100)) #efficiency
        genes.append(random.randint(rabbit_min_move_distance, 100)) #move distance
        genes.append(random.randint(rabbit_min_reproductive_urge, 100)) #reproductive urge
        position = (random.randint(0, x_size), random.randint(0, y_size))
        rabbits.append(Animal(genes, position))
    
    for f in range(num_foxes):
        genes = []
        genes.append("fox")
        genes.append(random.randint(fox_min_food_value, 100)) #food value
        genes.append(random.randint(fox_min_efficiency, 100)) #efficiency
        genes.append(random.randint(fox_min_move_distance, 100)) #move distance
        genes.append(random.randint(fox_min_reproductive_urge, 100)) #reproductive urge
        position = (random.randint(0, x_size), random.randint(0, y_size))
        foxes.append(Animal(genes, position))

    for n in range(num_food):
        position = (random.randint(0, x_size), random.randint(0, y_size))
        food_value = random.randint(10, 100)
        food.append(Food(food_value, position))

    ecosystem = [rabbits, foxes, food, x_size, y_size]
    return ecosystem

def move_animals(ecosystem):
    #print("moving animals")
    rabbits = ecosystem[0]
    foxes = ecosystem[1]

    # Iterate over a copy of the list to avoid index errors when removing
    for rabbit in rabbits[:]:
        i = rabbits.index(rabbit)
        #print(f"Moving rabbit {i}")
        if rabbit.energy <= 0:
            rabbit.alive = False
        if not rabbit.alive:
            rabbits.remove(rabbit)
            #print(f"Rabbit {i} died")
        else:
            rabbit.energy -= 1  # Decrease energy for each move
            action = "eat"
            if rabbit.energy < 100 - rabbit.reproductive_urge:
                action = "eat"
            elif rabbit.energy > 100 - rabbit.reproductive_urge and len(rabbits) > 1:
                action = "reproduce"
            #print(f"Rabbit energy: {rabbit.energy}, action: {action}")

            if action == "eat":
                #print("rabbit eating")
                alive_food = [f for f in ecosystem[2] if f.alive]
                if len(alive_food) == 0:
                    new_position = (rabbit.position[0] + random.randint(-rabbit.move_distance, rabbit.move_distance),
                                    rabbit.position[1] + random.randint(-rabbit.move_distance, rabbit.move_distance))
                    rabbit.move(new_position)
                else:
                    closest_food = min(alive_food, key=lambda f: distance(rabbit.position, f.position))
                    #print(closest_food.position)
                    if distance(rabbit.position, closest_food.position) <= rabbit.move_distance:
                        rabbit.move(closest_food.position)
                        rabbit.eat(closest_food)
                        ecosystem[2].remove(closest_food)
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
                other_rabbits = [r for r in rabbits if r is not rabbit and r.alive]
                if not other_rabbits:
                    continue
                closest_rabbit = min(other_rabbits, key=lambda r: distance(rabbit.position, r.position))
                if distance(rabbit.position, closest_rabbit.position) <= rabbit.move_distance:
                    rabbit.move(closest_rabbit.position)
                    # Attempt to reproduce if close enough
                    offspring = rabbit.reproduce(closest_rabbit)
                    rabbits.append(offspring)
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
    ecosystem[0] = rabbits  # Update the ecosystem with the remaining rabbits

    for fox in foxes[:]:
        j = foxes.index(fox)
        #print(f"fox {j} energy {fox.energy}")
        #print(f"Moving fox {j}")
        if fox.energy <= 0:
            fox.alive = False
        if not fox.alive:
            foxes.remove(fox)
            #print(f"Fox {j} died")
        else:
            fox.energy -= 1  # Decrease energy for each move
            action = "eat"
            if fox.energy < 100 - fox.reproductive_urge:
                action = "eat"
            elif fox.energy > 100 - fox.reproductive_urge and len(foxes) > 1:
                action = "reproduce"

            #print(f"Fox energy: {fox.energy}, action: {action}")

            if action == "eat":
                alive_rabbits = [r for r in rabbits if r.alive]
                if len(alive_rabbits) == 0:
                    if len(ecosystem[1] > 1):
                        # Foxes can eat other foxes if no rabbits are available
                        alive_foxes = [f for f in foxes if f is not fox and f.alive]
                        if alive_foxes:
                            closest_fox = min(alive_foxes, key=lambda f: distance(fox.position, f.position))
                            if distance(fox.position, closest_fox.position) <= fox.move_distance and closest_fox.alive:
                                fox.move(closest_fox.position)
                                fox.eat(closest_fox)
                                if closest_fox in foxes:
                                    foxes.remove(closest_fox)
                            else:
                                dx = closest_fox.position[0] - fox.position[0]
                                dy = closest_fox.position[1] - fox.position[1]
                                dist = distance(fox.position, closest_fox.position)
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
                        else:
                            new_position = (fox.position[0] + random.randint(-fox.move_distance, fox.move_distance),
                                            fox.position[1] + random.randint(-fox.move_distance, fox.move_distance))
                            fox.move(new_position)
                    else:
                        new_position = (fox.position[0] + random.randint(-fox.move_distance, fox.move_distance),
                                        fox.position[1] + random.randint(-fox.move_distance, fox.move_distance))
                        fox.move(new_position)
                else:
                    closest_rabbit = min(alive_rabbits, key=lambda r: distance(fox.position, r.position))
                    if distance(fox.position, closest_rabbit.position) <= fox.move_distance and closest_rabbit.alive:
                        fox.move(closest_rabbit.position)
                        fox.eat(closest_rabbit)
                        if closest_rabbit in rabbits:
                            rabbits.remove(closest_rabbit)  # Remove the rabbit from the ecosystem
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
                other_foxes = [f for f in foxes if f is not fox and f.alive]
                if not other_foxes:
                    continue
                closest_fox = min(other_foxes, key=lambda f: distance(fox.position, f.position))
                if distance(fox.position, closest_fox.position) <= fox.move_distance:
                    fox.move(closest_fox.position)
                    # Attempt to reproduce if close enough
                    offspring = fox.reproduce(closest_fox)
                    foxes.append(offspring)
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
    ecosystem[1] = foxes  # Update the ecosystem with the remaining foxes

def display_ecosystem():
    num_rabbits = 30
    num_foxes = 2
    num_food = 75
    x_size = 1024
    y_size = 1024

    rabbit_nums = []
    fox_nums = []
    food_nums = []
    
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
        food_respawn_rate = 1  # Number of food items to respawn each iteration
        for i in range(food_respawn_rate):
            position = (random.randint(0, x_size), random.randint(0, y_size))
            food_value = random.randint(10, 100)
            ecosystem[2].append(Food(food_value, position))

        screen.fill((0, 0, 0))
        move_animals(ecosystem)
        num_r = len([r for r in ecosystem[0] if r.alive])
        num_f = len([f for f in ecosystem[1] if f.alive])
        num_fd = len([f for f in ecosystem[2] if f.alive])
        #print(f"Rabbits: {num_r}, Foxes: {num_f}, Food: {num_fd}")
        rabbit_nums.append(num_r)
        fox_nums.append(num_f)
        food_nums.append(num_fd)
        
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
        
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(f"Rabbits: {num_r}  Foxes: {num_f}  Food: {num_fd}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))
        
        pygame.time.delay(300)
        pygame.display.flip()

display_ecosystem()