
# # Algoritmo génetico


# - Nombre: Alfredo Vanegas Arcega
# - Expediente: 297121
# - Grupo: 35


import string
from typing import Literal
import numpy as np


ALPHABET = string.ascii_lowercase
total_best_genotipes = 100
total_genotipes = 400
rng = np.random.default_rng(seed=69)
# Va en orden de las ciudades
PATHS = [
    [0,15,8,23,5,9,14,23,3,18,7,8,11,20,8],
    [15,0,17,28,24,28,16,23,15,12,17,20,33,21,17],
    [8,17,0,27,9,21,13,21,11,9,3,11,18,14,4],
    [23,28,27,0,20,25,34,51,19,30,24,17,27,18,28],
    [5,24,9,20,0,7,23,39,4,19,13,13,10,5,17],
    [9,28,21,25,7,0,26,38,8,22,17,12,5,9,21],
    [14,16,13,34,23,26,0,13,18,6,11,12,35,22,11],
    [23,23,21,51,39,38,13,0,26,21,20,27,36,31,19],
    [3,15,11,19,4,8,18,26,0,14,8,4,11,4,12],
    [18,12,9,30,19,22,6,21,14,0,8,15,29,19,6],
    [7,17,3,24,13,17,11,20,8,8,0,9,23,13,5],
    [8,20,11,17,9,12,12,27,4,15,9,0,17,5,15],
    [11,33,18,27,10,5,35,36,11,29,23,17,0,17,20],
    [20,21,14,18,5,9,22,31,4,19,13,5,17,0,16],
    [8,17,4,28,17,21,11,19,12,6,5,15,20,16,0],
]
np.random.seed(69)

def get_initial_genotipes(total_genotipes):
    generated_genotipes = [] 
    for _ in range(0, total_genotipes):
        genotipe = []
        # La lista inicial consiste de todas las ciudades disponibles
        available_choices = [x for x in range(len(PATHS))]
        for _ in range(0, len(PATHS)):
            letter_index = np.random.randint(0, len(available_choices))
            letter = available_choices[letter_index]
            # Se quita la ciudad para que no se repita de nuevo
            available_choices.remove(letter)
            genotipe.append(letter) 
        generated_genotipes.append({'alleles': genotipe, 'fitness': 0})
    generated_genotipes = evaluate_genotipes(generated_genotipes)
    return generated_genotipes


def evaluate_genotipes(genotipes):
    for genotipe in genotipes:
        total_score = 0
        alleles = genotipe['alleles']
        for i in range(len(alleles)-1):
            cost = PATHS[alleles[i]][alleles[i+1]]
            total_score += cost
        total_score += PATHS[alleles[len(alleles)-1]][alleles[0]]
        genotipe['fitness'] = total_score
    return genotipes

def get_best_genotipes(genotipes, best_genotipes_kept):
    best_genotipes = []
    scores = [genotipe['fitness'] for genotipe in genotipes]
    scores.sort(reverse=False)
    best_scores = list(set(scores[:best_genotipes_kept])) 
    for i in range(0, len(genotipes)):
        if len(best_genotipes) == best_genotipes_kept:
            break
        if genotipes[i]['fitness'] in best_scores:
            best_genotipes.append(genotipes[i])
    return best_genotipes


def inversion_mutation(genotipes):
    for genotipe in genotipes:
        ran_start = np.random.randint(0, len(genotipe['alleles']) - 1)
        ran_end = np.random.randint(ran_start + 2, len(genotipe['alleles']) + 1)
        mutation = genotipe['alleles'][ran_start:ran_end]
        mutation.reverse()
        genotipe['alleles'][ran_start:ran_end] = mutation
    return genotipes


def displacement_mutation(genotipes):
    for genotipe in genotipes:
        ran_start = np.random.randint(0, len(genotipe['alleles']) - 1)
        ran_end = np.random.randint(ran_start + 1, len(genotipe['alleles']))
        unavailable_choices = [x for x in range(ran_start, ran_end+1)]
        choices = [x for x in range(0, len(genotipe['alleles'])) if not x in unavailable_choices]
        if not len(choices) == 0:
            ran_pos = np.random.choice(choices)
            choices.remove(ran_pos)
        else:
            continue
        #selection = genotipe['alleles'][ran_start:ran_end+1]
        #displacement = genotipe['alleles'][ran_pos:ran_start]
        genotipe['alleles'][ran_start:ran_end+1], genotipe['alleles'][ran_pos:ran_start] = genotipe['alleles'][ran_pos:ran_start], genotipe['alleles'][ran_start:ran_end+1]
    return genotipes



def exchange_mutation(genotipes):
    mutations = []
    for genotipe in genotipes:
        ran_pos1, ran_pos2 = np.sort(rng.choice(np.arange(len(genotipe['alleles'])), size=2, replace=False))
        aux = genotipe['alleles'][ran_pos1]
        genotipe['alleles'][ran_pos1] = genotipe['alleles'][ran_pos2]
        genotipe['alleles'][ran_pos2] = aux
        mutations.append(genotipe)
    return mutations


def insertion_mutation(genotipes):
    for genotipe in genotipes:
        ran_index = np.random.randint(0, len(genotipe['alleles']))
        ran_pos = np.random.randint(0, len(genotipe['alleles']))
        letter = genotipe['alleles'][ran_index]
        aux = genotipe['alleles'][ran_pos]
        genotipe['alleles'][ran_pos] = letter
        genotipe['alleles'][ran_index] = aux
    return genotipes


def inverted_exchange_mutation(genotipes):
    for genotipe in genotipes:
        ran_start, ran_end = np.sort(rng.choice(np.arange(len(genotipe['alleles'])), size=2, replace=False))
        selection = genotipe['alleles'][ran_start:ran_end]
        selection.reverse()
        genotipe['alleles'][ran_start:ran_end] = selection
        ran_ex1 = np.random.randint(0, len(selection))
        ran_ex2 = np.random.randint(0, len(genotipe['alleles']))
        aux = genotipe['alleles'][ran_ex1]
        genotipe['alleles'][ran_ex1] = genotipe['alleles'][ran_ex2]
        genotipe['alleles'][ran_ex2] = aux
    return genotipes


def inverted_displacement_mutation(genotipes):
    for genotipe in genotipes:
        ran_start, ran_end = np.sort(rng.choice(np.arange(len(genotipe['alleles'])), size=2, replace=False))
        ran_pos = np.random.randint(0, ran_end - ran_start)
        genotipe['alleles'][ran_start:ran_end].reverse() #selection
        #displacement = genotipe['alleles'][ran_pos:ran_start]
        genotipe['alleles'][ran_start:ran_end], genotipe['alleles'][ran_pos:ran_start] =  genotipe['alleles'][ran_pos:ran_start], genotipe['alleles'][ran_start:ran_end]
    return genotipes


def pmx_offspring(parent1, parent2):
    cut1, cut2 = np.sort(rng.choice(np.arange(len(parent1)+1), size=2, replace=False))
    offspring = ['' for x in range(0, len(parent1))]

    offspring[cut1:cut2] = parent1[cut1:cut2]
    rest_index = np.concatenate([np.arange(0, cut1), np.arange(cut2, len(parent1))])
    for i in rest_index:
        candidate = parent2[i]
        while candidate in parent1[cut1:cut2]:
            candidate = parent2[np.where(parent1 == candidate)[0][0]]

        offspring[i] = candidate
    return offspring


def pmx_crossing(genotipes, total_offspring):
    childs = []
    for _ in range(0, int(np.floor(total_offspring / 2))):
        p1, p2 = np.sort(rng.choice(np.arange(len(genotipes)), size=2, replace=False))
        parent1, parent2 = np.array(genotipes[p1]['alleles']), np.array(genotipes[p2]['alleles'])
        offspring0 = pmx_offspring(parent1, parent2)
        offspring1 = pmx_offspring(parent2, parent1)
        childs.append({'alleles': offspring0, 'fitness': 0})
        childs.append({'alleles': offspring1, 'fitness': 0})
    return childs 

def insert_random_letter(genotipes):
    for genotipe in genotipes:
        available_letters = [x for x in ALPHABET if x not in genotipe['alleles']]
        ran_pos = np.random.randint(0, len(genotipe['alleles']))
        ran_letter = np.random.randint(0, len(available_letters))
        letter = available_letters[ran_letter]
        genotipe['alleles'][ran_pos] = letter
    return genotipes


def get_perfect_genotipe(genotipes, max_score):
    for genotipe in genotipes:
        if genotipe['fitness'] == max_score:
            return genotipe
    return None


def has_perfect_genotipe(genotipes, max_score):
    for genotipe in genotipes:
        if genotipe['fitness'] == max_score:
            return True
    return False


def get_best_genotipe(genotipes):
    best_score = genotipes[0]['fitness']
    best_genotipe = genotipes[0]
    for genotipe in genotipes:
        if genotipe['fitness'] < best_score:
            best_score = genotipe['fitness']
            best_genotipe = genotipe
    return best_genotipe


def evolution_loop(
    total_genotipes: int, 
    best_genotipes_kept: int, 
    total_generations: int, 
    operator: Literal['inversion', 
                      'displacement', 
                      'exchange', 
                      'insertion', 
                      'inverted_exchange', 
                      'inverted_displacement']
):
    mutation_operator = inversion_mutation
    if operator == "inversion":
        mutation_operator = inversion_mutation
    elif operator == "displacement":
        mutation_operator = displacement_mutation
    elif operator == "exchange":
        mutation_operator = exchange_mutation
    elif operator == "insertion":
        mutation_operator = insertion_mutation
    elif operator == "inverted_exchange":
        mutation_operator = inverted_exchange_mutation
    elif operator == "inverted_displacement":
        mutation_operator = inverted_displacement_mutation

    # Initial variables
    generations_count = 0
    genotipes = get_initial_genotipes(total_genotipes)
    for _ in range(total_generations):
        best_genotipes = get_best_genotipes(genotipes, best_genotipes_kept)
        genotipes = pmx_crossing(best_genotipes, total_genotipes - len(best_genotipes))
        genotipes.extend(best_genotipes)
        genotipes = mutation_operator(genotipes) 
        genotipes = evaluate_genotipes(genotipes)
        best_genotipe = get_best_genotipe(genotipes)
        generations_count += 1
        print("Generación: " , generations_count)
        print("Mejor: ", best_genotipe)

evolution_loop(
    total_genotipes=800,
    best_genotipes_kept=50,
    total_generations=100,
    operator="inversion"
)