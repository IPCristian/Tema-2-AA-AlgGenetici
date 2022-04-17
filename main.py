import copy
import math
import random


def write_population():
    for i in range(len(population)):
        output.write(str(i + 1) + ": ")
        for bit in population[i]:
            output.write(str(bit))
        x = get_x(population[i])
        output.write(" x = " + str(x) + " f = " + str(get_f(x)) + "\n")
    output.write("\n")


def get_x(chromosome):
    decimal = int(str("".join(chromosome)), 2)
    return ((dom_def[1] - dom_def[0]) / (math.pow(2, cromosome_len) - 1)) \
           * decimal + dom_def[0]                                                               # Formula from Course 5


def get_f(x):
    return param_fct[0] * math.pow(x, 2) + param_fct[1] * x + param_fct[2]


def function_values():
    fct_values = []
    for chromosome in population:
        fct_values.append(get_f(get_x(chromosome)))
    return fct_values


def selection_probability(fct_values):
    sum_values = sum(fct_values)
    select_prob = []
    for value in fct_values:
        select_prob.append(value / sum_values)

    if not iteration_counter:
        output.write("Selection probabilities:\n\n")
        for i in range(pop_len):
            output.write("Cromosome: " + str(i+1) + " , Probability: " + str(select_prob[i]) + "\n")
        output.write("\n\n")

    select_intervs = []
    total = 0
    for prob in select_prob:
        select_intervs.append(total)
        total += prob
    select_intervs.append(1)

    return select_intervs


def binary_search(low, high, select_intervs, u):
    mid = int((high + low) / 2)
    if select_intervs[mid] < u <= select_intervs[mid + 1]:
        return mid
    elif (u < select_intervs[mid]):
        return binary_search(low, mid, select_intervs, u)
    else:
        return binary_search(mid + 1, high, select_intervs, u)


def roulette_selection(select_intervs):
    global population
    new_population = []

    for i in range(pop_len):
        u = random.random()
        if u == 0:
            j = 1
        else:
            j = binary_search(0, len(select_intervs)-1, select_intervs, u)
        new_population.append(population[j])
        if not iteration_counter:
            output.write("u = " + str(u) + ", We select Chromosome " + str(j + 1) + "\n")

    output.write("\n\n")
    population = copy.deepcopy(new_population)
    return

def recomb_participants():
    recomb_croms = []
    if not iteration_counter:
        output.write("Recombination Probability: " + str(recomb_prob) + "\n\n")
        for i in range(pop_len):
            output.write(str(i+1) + ": ")
            for bit in population[i]:
                output.write(str(bit))
            x = random.random()
            output.write(" u = " + str(x))
            if x < recomb_prob:
                recomb_croms.append(i)
                output.write(" < " + str(recomb_prob) + " -> Participates")
            output.write("\n")
    else:
        for i in range(pop_len):
            x = random.random()
            if x < recomb_prob:
                recomb_croms.append(i)

    output.write("\n")
    return recomb_croms

def recombination(participants):

    while len(participants) > 3:
        a,b = random.sample(participants,2)
        participants.remove(a)
        participants.remove(b)

        break_point = random.randint(1,20)

        if not iteration_counter:
            output.write("Recombination between chromosome " + str(a+1) + " and " + str(b+1) + "\n")

        new_a = population[a[:break_point]] + b[break_point:]
        # --------------- #



# ------------------------------------------------------ Main -------------------------------------------------------- #

input = open("input.txt", "r")
output = open("output.txt", "w")

lines = input.readlines()
pop_len = int(lines[0])                                                                         # Population Size
dom_def = (int(lines[1].split()[0]), int(lines[1].split()[1]))                                  # [A,B]
param_fct = (int(lines[2].split()[0]), int(lines[2].split()[1]), int(lines[2].split()[2]))      # Ax^2 + Bx + C
precision = int(lines[3])                                                                       # Precision Number
recomb_prob = float(lines[4])                                                                   # Recombination Probability
mutate_prob = float(lines[5])                                                                   # Mutation Probability
iterations = int(lines[6])                                                                      # Number of iterations
cromosome_len = math.floor(math.log((dom_def[1] - dom_def[0]) * math.pow(10, precision), 2))    # Formula from Course 5

population = []                                                                                 # Initial randomly
for i in range(pop_len):                                                                        # generated population
    population.append([])
    for j in range(cromosome_len):
        bit = random.random()
        if bit > 0.5:
            population[i].append(str(1))
        else:
            population[i].append(str(0))

output.write("Initial population:\n\n")
write_population()

for iteration_counter in range(iterations):

    # Selection Probability
    select_intervs = selection_probability(function_values())
    if not iteration_counter:
        output.write("Selection Probability Intervals: ")
        for interv in select_intervs:
            output.write(str(interv) + " ")
        output.write("\n\n")

    # Roulette Selection Method
    roulette_selection(select_intervs)
    if not iteration_counter:
        output.write("After selection:\n\n")
        write_population()

    # Recombination
    recombination(recomb_participants())

    iteration_counter += 1

# -------------------------------------------------------------------------------------------------------------------- #
