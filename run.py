import os
import io
import json
import random
import argparse
import matplotlib.pyplot as plt
from plotRoute import plot_route

random.seed(0)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default="./data/Input_Data.json", required=False,
                        help="Enter the input Json file name")
    parser.add_argument('--pop_size', type=int, default=50, required=False,
                        help="Enter the population size")
    parser.add_argument('--mute_prob', type=float, default=0.5, required=False,
                        help="Mutation Probabilty")
    parser.add_argument('--iterations', type=int, default=5000, required=False,
                        help="Number of iterations to run")

    return parser.parse_args()


def load_instance(json_file):
    """
    Inputs: path to json file
    Outputs: json file object if it exists, or else returns NoneType
    """
    if os.path.exists(path=json_file):
        with io.open(json_file, 'rt', newline='') as file_object:
            return json.load(file_object)
    return None


def initialize_population(n_customers, n_population):
    population = []
    while len(population) < n_population:
        chromosome = random.sample([i for i in range(1, n_customers+1)], n_customers)
        if chromosome not in population:
            population.append(chromosome)
    return population


def evaluate(chromosome, distance_matrix, demand, cap_vehicle, return_subroute=False):
    total_distance = 0
    cur_load = 0
    n_vehicle = 0
    route = []
    sub_route = []
    for customer in chromosome:
        cur_load += demand[customer]
        if cur_load > cap_vehicle:
            if return_subroute:
                sub_route.append(route[:])
            total_distance += calculate_distance(route, distance_matrix)
            n_vehicle += 1
            cur_load = demand[customer]
            route = [customer]
        else:
            route.append(customer)

    total_distance += calculate_distance(route, distance_matrix)
    n_vehicle += 1
    if return_subroute:
        sub_route.append(route[:])
        return sub_route
    return total_distance + n_vehicle


def calculate_distance(route, distance_matrix):
    distance = 0
    distance += distance_matrix[0][route[0]]
    distance += distance_matrix[route[-1]][0]
    for i in range(0, len(route)-1):
        distance += distance_matrix[route[i]][route[i+1]]
    return distance


def get_chromosome(population, func, *params, reverse=False, k=1):
    scores = []
    for chromosome in population:
        scores.append([func(chromosome, *params), chromosome])
    scores.sort(reverse=reverse)
    if k == 1:
        return scores[0]
    elif k > 1:
        return scores[:k]
    else:
        raise Exception("invalid k")


def ordered_crossover(chromo1, chromo2):
    # Modifying this to suit our needs
    #  If the sequence does not contain 0, this throws error
    #  So we will modify inputs here itself and then
    #       modify the outputs too

    ind1 = [x-1 for x in chromo1]
    ind2 = [x-1 for x in chromo2]
    size = min(len(ind1), len(ind2))
    a, b = random.sample(range(size), 2)
    if a > b:
        a, b = b, a

    holes1, holes2 = [True] * size, [True] * size
    for i in range(size):
        if i < a or i > b:
            holes1[ind2[i]] = False
            holes2[ind1[i]] = False

    # We must keep the original values somewhere before scrambling everything
    temp1, temp2 = ind1, ind2
    k1, k2 = b + 1, b + 1
    for i in range(size):
        if not holes1[temp1[(i + b + 1) % size]]:
            ind1[k1 % size] = temp1[(i + b + 1) % size]
            k1 += 1

        if not holes2[temp2[(i + b + 1) % size]]:
            ind2[k2 % size] = temp2[(i + b + 1) % size]
            k2 += 1

    # Swap the content between a and b (included)
    for i in range(a, b + 1):
        ind1[i], ind2[i] = ind2[i], ind1[i]

    # Finally adding 1 again to reclaim original input
    ind1 = [x+1 for x in ind1]
    ind2 = [x+1 for x in ind2]
    return ind1, ind2


def mutate(chromosome, probability):
    if random.random() < probability:
        index1, index2 = random.sample(range(len(chromosome)), 2)
        chromosome[index1], chromosome[index2] = chromosome[index2], chromosome[index1]
        index1, index2 = sorted(random.sample(range(len(chromosome)), 2))
        mutated = chromosome[:index1] + list(reversed(chromosome[index1:index2+1]))
        if index2 < len(chromosome) - 1:
            mutated += chromosome[index2+1:]
        return mutated
    return chromosome


def replace(population, chromo_in, chromo_out):
    population[population.index(chromo_out)] = chromo_in


def check_validity(chromosome, length):
    for i in range(1, length+1):
        if i not in chromosome:
            raise Exception("invalid chromosome")


if __name__ == '__main__':

    # get input
    # initialize population
    # calculate cost
    # if terminal -> finish
    # repeat iteration
    # -> select chromosomes
    # -> mutate chromosomes
    # -> replace
    # -> calculate cost
    args = get_parser()
    instance = load_instance(args.input_path)
    n_customers = instance['Number_of_customers']
    demand = {}
    for i in range(1, n_customers+1):
        demand[i] = instance["customer_" + str(i)]['demand']

    distance_matrix = instance['distance_matrix']
    cap_vehicle = instance['vehicle_capacity']
    depart = instance['depart']
    n_population = args.pop_size
    iteration = args.iterations
    cur_iter = 1
    mutate_prob = args.mute_prob

    population = initialize_population(n_customers, n_population)
    prev_score, chromosome = get_chromosome(population, evaluate, distance_matrix, demand, cap_vehicle)

    score_history = [prev_score]

    while cur_iter <= iteration:
        chromosomes = get_chromosome(population, evaluate, distance_matrix, demand, cap_vehicle, k=2)
        chromosome1 = chromosomes[0][1]
        chromosome2 = chromosomes[1][1]
        offspring1, offspring2 = ordered_crossover(chromosome1, chromosome2)
        offspring1 = mutate(offspring1, mutate_prob)
        offspring2 = mutate(offspring2, mutate_prob)
        score1 = evaluate(offspring1, distance_matrix, demand, cap_vehicle)
        score2 = evaluate(offspring2, distance_matrix, demand, cap_vehicle)
        score, chromosome = get_chromosome(population, evaluate, distance_matrix, demand, cap_vehicle, reverse=True)

        if score1 < score:
            replace(population, chromo_in=offspring1, chromo_out=chromosome)

        score, chromosome = get_chromosome(population, evaluate, distance_matrix, demand, cap_vehicle, reverse=True)

        if score2 < score:
            replace(population, chromo_in=offspring2, chromo_out=chromosome)

        score, chromosome = get_chromosome(population, evaluate, distance_matrix, demand, cap_vehicle)
        score_history.append(score)
        prev_score = score
        cur_iter += 1

    print(score, chromosome)
    subroutes = evaluate(chromosome, distance_matrix, demand, cap_vehicle, return_subroute=True)
    title = "SSGA for CVRP, mute_prob={}".format(mutate_prob)
    plot_route(subroutes, instance, title)
    plt.cla()
    plt.plot(score_history)
    plt.xlabel("Iterations")
    plt.ylabel("Cost")
    plt.title(title)
    plt.savefig('figure/cost.png')
    plt.show()

