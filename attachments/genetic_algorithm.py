import random
import game
import matplotlib.pyplot as plt
import os


def initialize_population(population_size, chromosome_length):
    population = []
    choices = [0, 1, 2]
    
    for _ in range(population_size):
        chromosome = random.choices(choices, k=chromosome_length)
        population.append(chromosome)
    
    return population


def fitness(chromosome, game, method):
    fitness = game.get_score(chromosome, method)
    return fitness




def choose_best_chromosome(population, fitness_values, num_selection):
        best_chromosomes = []
        sorted_indices = sorted(range(len(fitness_values)), key=lambda k: fitness_values[k], reverse=True)
        for i in range(num_selection):
            best_chromosomes.append(population[sorted_indices[i]])
        return best_chromosomes

def roulette_wheel_selection(population, fitness_values):
        total_fitness = sum(fitness_values)
        probabilities = [fitness / total_fitness for fitness in fitness_values]
        selected_parents = []
        for _ in range(2): 
            rand_val = random.random() 
            cumulative_prob = 0
            for i, prob in enumerate(probabilities):
                cumulative_prob += prob
                if rand_val <= cumulative_prob:
                    selected_parents.append(population[i])
                    break

        return selected_parents



def two_point_crossover(parent1, parent2):
        point1 = random.randint(0, len(parent1) - 1)
        point2 = random.randint(point1 + 1, len(parent1))

        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

        return child1, child2

def one_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)

    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2

def mutate(individual, mutation_rate):
    mutated_individual = individual.copy()

    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            mutated_individual[i] = random.randint(0, 2)

    return mutated_individual



def replace(population, childList, the_game):
    combined = population + childList 
    if method == 1:
        combined.sort(key=lambda individual: fitness(individual, the_game, 1), reverse=True)
    elif method == 2:
        combined.sort(key=lambda individual: fitness(individual, the_game, 2), reverse=True)
    new_population = combined[:len(population)]
    return new_population


def genetic_algorithm(chromosome_length, num_generations, method, the_game):
    
    if method == 1:
        population = initialize_population(200, chromosome_length)
        parents_size = 200
    elif method == 2:
        population = initialize_population(500, chromosome_length)
        parents_size = 200

    avg_fit =[]
    min_fit =[]
    max_fit =[]

    for generation in range(num_generations):
        fitness_scores = [fitness(chromosome, the_game, method) for chromosome in population]

        if method == 1:
            parents = choose_best_chromosome(population, fitness_scores, parents_size)
        elif method == 2:
            parents = roulette_wheel_selection(population, fitness_scores)
        childList = []
        for i in range(0, len(parents) - 2, 2):
            if method == 1:
                child1, child2 = one_point_crossover(parents[i], parents[i + 1])
                childList.extend([child1, child2])
            elif method == 2:
                child1, child2 = two_point_crossover(parents[i], parents[i + 1])
                childList.extend([child1, child2])

        if method == 1:
            childList = [mutate(chromosome, 0.1) for chromosome in childList]
        elif method == 2:
            childList = [mutate(chromosome, 0.5) for chromosome in childList]

        population = replace(population, childList, the_game)
        max_fit.append(max(fitness_scores))
        min_fit.append(min(fitness_scores))
        avg_fit.append(sum(fitness_scores) / len(fitness_scores))


    return max_fit, min_fit, avg_fit, population[0]



def create_game():
    levels_directory = './levels/level'
    levels = []
    for i in range(1, 11):
        with open(levels_directory + str(i) + '.txt', 'r') as file:
            file_contents = file.read()
            levels.append(file_contents)
    return game.Game(levels)


def plot_fitness(type, fitness, level, directory):
    X = "Generation"
    Y = type + " Fitness"
    title = type + " Fitness per Generation in level " + str(level)
    file_path = os.path.join(directory, title + ".png")
    generations = range(1, len(fitness) + 1)
    plt.plot(generations, fitness)
    plt.xlabel(X)
    plt.ylabel(Y)
    plt.title(title)
    plt.show()
    plt.savefig(file_path)
    plt.close()


method = 1
print("method", method)
print()
game_sample = create_game()
for index in range(len(game_sample.levels)):
    level_index = index + 1
    game_sample.load_next_level()
    chromosome_len = game_sample.current_level_len
    max_fit, min_fit, avg_fit, best_individual = genetic_algorithm(chromosome_len, 500, method, game_sample)
    print("level:", level_index)
    print("fitness:" ,fitness(best_individual, game_sample, method))
    print("Feasibility:", game_sample.is_solvable(game_sample.levels[index],best_individual))
    print()
    plot_fitness("MAX", max_fit, level_index,'./output_plots/method_1/max_fit')
    plot_fitness("Avg", avg_fit, level_index,'./output_plots/method_1/avg_fit')
    plot_fitness("MIN", min_fit, level_index,'./output_plots/method_1/min_fit')
    plot_fitness("MAX", max_fit, level_index,'./output_plots/method_2/max_fit')
    plot_fitness("Avg", avg_fit, level_index,'./output_plots/method_2/avg_fit')
    plot_fitness("MIN", min_fit, level_index,'./output_plots/method_2/min_fit')
