import random
import pygame
import matplotlib
import matplotlib.pyplot as plt

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
        scaling_factor = 0.5
        if self.type == predator.type:
            scaling_factor = 0.05 #cannibalism is less efficient
        transferred_energy = self.food_value * scaling_factor
        if predator.energy <= 100 - transferred_energy:
            predator.energy += transferred_energy
        elif predator.energy <= 100:
            predator.energy = 100
    
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
        reproduction_cost = 0.7
        self.energy -= reproduction_cost * self.reproductive_urge
        partner.energy -= reproduction_cost * partner.reproductive_urge
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
        scaling_factor = 0.2
        transferred_energy = self.food_value * scaling_factor
        if predator.energy <= 100 - transferred_energy:
            predator.energy += transferred_energy
        elif predator.energy <= 100:
            predator.energy = 100

def initialise_ecosystem(num_rabbits, num_foxes, num_food, x_size, y_size):
    foxes = []
    rabbits = []
    food = []
    ecosystem = []

    for r in range(num_rabbits):
        type = "rabbit"
        rabbits.append(init_animal(type=type))
    
    for f in range(num_foxes):
        type = "fox"
        foxes.append(init_animal(type=type))

    for n in range(num_food):
        position = (random.randint(0, x_size), random.randint(0, y_size))
        food_value = random.randint(10, 100)
        food.append(Food(food_value, position))

    ecosystem = [rabbits, foxes, food, x_size, y_size]
    return ecosystem

def init_animal(pos = (-1, -1), type="", x_size=4096, y_size=4096):
    rabbit_min_food_value = 10
    rabbit_min_efficiency = 10
    rabbit_min_move_distance = 10
    rabbit_min_reproductive_urge = 10

    fox_min_food_value = 10
    fox_min_efficiency = 10
    fox_min_move_distance = 10
    fox_min_reproductive_urge = 10

    if pos == (-1, -1):
        pos = (random.randint(0, x_size), random.randint(0, y_size))

    genes = []
    genes.append(type)
    if type == "rabbit":
        genes.append(random.randint(rabbit_min_food_value, 100)) #food value
        genes.append(random.randint(rabbit_min_efficiency, 100)) #efficiency
        genes.append(random.randint(rabbit_min_move_distance, 100)) #move distance
        genes.append(random.randint(rabbit_min_reproductive_urge, 100)) #reproductive urge
    elif type == "fox":
        genes.append(random.randint(fox_min_food_value, 100)) #food value
        genes.append(random.randint(fox_min_efficiency, 100)) #efficiency
        genes.append(random.randint(fox_min_move_distance, 100)) #move distance
        genes.append(random.randint(fox_min_reproductive_urge, 100)) #reproductive urge
    return Animal(genes, pos)

def move_animals(ecosystem):
    #print("moving animals")
    rabbits = ecosystem[0]
    foxes = ecosystem[1]

    # Iterate over a copy of the list to avoid index errors when removing
    for rabbit in rabbits:
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

    for fox in foxes:
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
                    if len(ecosystem[1]) > 1:
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
    num_rabbits = 24
    num_foxes = 12
    num_food = 4096
    x_size = 4096
    y_size = 4096
    screen_x_size = 1024
    screen_y_size = 1024
    d_x = 0
    d_y = 0
    centre_x = x_size // 2
    centre_y = y_size // 2

    move_x = 20
    move_y = 20

    rabbit_nums = []
    fox_nums = []
    food_nums = []

    avg_r_reproductive_urge = 0
    avg_f_reproductive_urge = 0
    avg_r_food_value = 0
    avg_r_move_distance = 0
    avg_f_move_distance = 0
    avg_r_efficiency = 0
    avg_f_efficiency = 0

    avg_r_reproductive_urges = []
    avg_f_reproductive_urges = []
    avg_r_food_values = []
    avg_r_move_distances = []
    avg_f_move_distances = []
    avg_r_efficiencies = []
    avg_f_efficiencies = []

    num_r = 0
    num_f = 0
    num_fd = 0
    
    ecosystem = initialise_ecosystem(num_rabbits, num_foxes, num_food, x_size, y_size)
    
    pygame.init()
    screen = pygame.display.set_mode((screen_x_size, screen_y_size))
    pygame.display.set_caption("Ecosystem Simulation")
    
    count = 0
    running = True
    while running:
        count += 1
        d_x = 0
        d_y = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    d_x = -move_x
                elif event.key == pygame.K_RIGHT:
                    d_x = move_x
                elif event.key == pygame.K_UP:
                    d_y = -move_y
                elif event.key == pygame.K_DOWN:
                    d_y = move_y
                elif event.key == pygame.K_r:
                    # Find the nearest rabbit to the current centre and set centre_x, centre_y to its position
                    alive_rabbits = [r for r in ecosystem[0] if r.alive]
                    if alive_rabbits:
                        nearest_rabbit = min(alive_rabbits, key=lambda r: distance((centre_x, centre_y), r.position))
                        centre_x, centre_y = int(nearest_rabbit.position[0]), int(nearest_rabbit.position[1])
                elif event.key == pygame.K_f:
                    # Find the nearest fox to the current centre and set centre_x, centre_y to its position
                    alive_foxes = [f for f in ecosystem[1] if f.alive]
                    if alive_foxes:
                        nearest_fox = min(alive_foxes, key=lambda f: distance((centre_x, centre_y), f.position))
                        centre_x, centre_y = int(nearest_fox.position[0]), int(nearest_fox.position[1])
                elif event.key == pygame.K_p:
                    running = False
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_MIDDLE:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Convert mouse position to ecosystem coordinates
                    centre_x = mouse_x + (centre_x - screen_x_size // 2)
                    centre_y = mouse_y + (centre_y - screen_y_size // 2)
                if event.button == pygame.BUTTON_LEFT:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Convert mouse position to ecosystem coordinates
                    f_x = mouse_x + (centre_x - screen_x_size // 2)
                    f_y = mouse_y + (centre_y - screen_y_size // 2)
                    pos = (f_x, f_y)
                    type = "fox"
                    fox = init_animal(pos=pos, type=type)
                    ecosystem[1].append(fox)
                if event.button == pygame.BUTTON_RIGHT:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Convert mouse position to ecosystem coordinates
                    r_x = mouse_x + (centre_x - screen_x_size // 2)
                    r_y = mouse_y + (centre_y - screen_y_size // 2)
                    pos = (r_x, r_y)
                    type = "rabbit"
                    rabbit = init_animal(pos=pos, type=type)
                    ecosystem[0].append(rabbit)
        centre_x += d_x
        centre_y += d_y
        #print(f"Centre: ({centre_x}, {centre_y})")
        #print(count)
        food_respawn_rate = 32  # Number of food items to respawn each iteration
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
        
        total_r_reproductive_urge = 0
        total_r_food_value = 0
        total_r_move_distance = 0
        total_r_efficiency = 0
        c_r = 0
        c_f = 0

        for rabbit in ecosystem[0]:
            if rabbit.alive:
                total_r_reproductive_urge += rabbit.reproductive_urge
                total_r_food_value += rabbit.food_value
                total_r_move_distance += rabbit.move_distance
                total_r_efficiency += rabbit.efficiency
                c_r += 1
                pos_x = int(rabbit.position[0]) 
                pos_y = int(rabbit.position[1])
                # Check if rabbit is within the visible screen area centered on (centre_x, centre_y)
                screen_left = centre_x - screen_x_size // 2
                screen_right = centre_x + screen_x_size // 2
                screen_top = centre_y - screen_y_size // 2
                screen_bottom = centre_y + screen_y_size // 2
                if pos_x < screen_left or pos_x >= screen_right or pos_y < screen_top or pos_y >= screen_bottom:
                    continue
                else:
                    # Draw rabbit at its position relative to the screen center
                    draw_x = pos_x - screen_left
                    draw_y = pos_y - screen_top
                    pygame.draw.circle(screen, (255, 255, 0), (draw_x, draw_y), 10)
        avg_r_reproductive_urge = total_r_reproductive_urge / c_r if c_r > 0 else 0
        avg_r_food_value = total_r_food_value / c_r if c_r > 0 else 0
        avg_r_move_distance = total_r_move_distance / c_r if c_r > 0 else 0
        avg_r_efficiency = total_r_efficiency / c_r if c_r > 0 else 0
        avg_r_reproductive_urges.append(avg_r_reproductive_urge)
        avg_r_food_values.append(avg_r_food_value)
        avg_r_move_distances.append(avg_r_move_distance)
        avg_r_efficiencies.append(avg_r_efficiency)

        total_f_reproductive_urge = 0
        total_f_move_distance = 0
        total_f_efficiency = 0
        c_f = 0

        for fox in ecosystem[1]:
            if fox.alive:
                total_f_reproductive_urge += fox.reproductive_urge
                total_f_move_distance += fox.move_distance
                total_f_efficiency += fox.efficiency
                c_f += 1
                pos_x = int(fox.position[0])
                pos_y = int(fox.position[1])
                # Check if fox is within the visible screen area centered on (centre_x, centre_y)
                screen_left = centre_x - screen_x_size // 2
                screen_right = centre_x + screen_x_size // 2
                screen_top = centre_y - screen_y_size // 2
                screen_bottom = centre_y + screen_y_size // 2
                if pos_x < screen_left or pos_x >= screen_right or pos_y < screen_top or pos_y >= screen_bottom:
                    continue
                else:
                    # Draw fox at its position relative to the screen center
                    draw_x = pos_x - screen_left
                    draw_y = pos_y - screen_top
                    pygame.draw.circle(screen, (255, 0, 0), (draw_x, draw_y), 10)
        avg_f_reproductive_urge = total_f_reproductive_urge / c_f if c_f > 0 else 0
        avg_f_move_distance = total_f_move_distance / c_f if c_f > 0 else 0
        avg_f_efficiency = total_f_efficiency / c_f if c_f > 0 else 0
        avg_f_reproductive_urges.append(avg_f_reproductive_urge)
        avg_f_move_distances.append(avg_f_move_distance)
        avg_f_efficiencies.append(avg_f_efficiency)

        for food in ecosystem[2]:
            if food.alive:
                pos_x = int(food.position[0])
                pos_y = int(food.position[1])
                # Check if food is within the visible screen area centered on (centre_x, centre_y)
                screen_left = centre_x - screen_x_size // 2
                screen_right = centre_x + screen_x_size // 2
                screen_top = centre_y - screen_y_size // 2
                screen_bottom = centre_y + screen_y_size // 2
                if pos_x < screen_left or pos_x >= screen_right or pos_y < screen_top or pos_y >= screen_bottom:
                    continue
                else:
                    # Draw food at its position relative to the screen center
                    draw_x = pos_x - screen_left
                    draw_y = pos_y - screen_top
                    pygame.draw.circle(screen, (0, 255, 0), (draw_x, draw_y), 6)

        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(f"Rabbits: {num_r}  Foxes: {num_f}  Food: {num_fd}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))
        
        pygame.time.delay(50)
        pygame.display.flip()
    return ((rabbit_nums, fox_nums, food_nums), (avg_r_reproductive_urges, avg_f_reproductive_urges, avg_r_food_values, avg_r_move_distances, avg_f_move_distances, avg_r_efficiencies, avg_f_efficiencies))

(rabbit_nums, fox_nums, food_nums), (avg_r_reproductive_urges, avg_f_reproductive_urges, avg_r_food_values, avg_r_move_distances, avg_f_move_distances, avg_r_efficiencies, avg_f_efficiencies) = display_ecosystem()

plt.figure(figsize=(16, 9))

# Plot populations
plt.subplot(2, 1, 1)
ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.plot(range(len(rabbit_nums)), rabbit_nums, label='Rabbits', color='tab:blue')
#ax1.plot(range(len(food_nums)), food_nums, label='Food', color='tab:green')
ax2.plot(range(len(fox_nums)), fox_nums, label='Foxes', color='tab:orange')

ax1.set_xlabel('Time Steps')
ax1.set_ylabel('Rabbit Population', color='tab:blue')
ax2.set_ylabel('Fox Population', color='tab:orange')

ax1.set_title('Ecosystem Simulation - Populations')

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

# Plot average values
plt.subplot(2, 1, 2)
plt.plot(range(len(avg_r_reproductive_urges)), avg_r_reproductive_urges, label='Avg R Rep Urge')
plt.plot(range(len(avg_f_reproductive_urges)), avg_f_reproductive_urges, label='Avg F Rep Urge')
plt.plot(range(len(avg_r_food_values)), avg_r_food_values, label='Avg R Fd Val')
plt.plot(range(len(avg_r_move_distances)), avg_r_move_distances, label='Avg R Mv Dis')
plt.plot(range(len(avg_f_move_distances)), avg_f_move_distances, label='Avg F Mv Dis')
plt.plot(range(len(avg_r_efficiencies)), avg_r_efficiencies, label='Avg R Eff')
plt.plot(range(len(avg_f_efficiencies)), avg_f_efficiencies, label='Avg F Eff')
plt.xlabel('Time Steps')
plt.ylabel('Average Values')
plt.title('Ecosystem Simulation - Average Values')
plt.legend()

plt.tight_layout()
plt.show()
pygame.quit()
exit()