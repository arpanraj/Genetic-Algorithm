#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 15 08:34:24 2022

@author: arpanrajpurohit
"""
import random
import itertools
import matplotlib.pyplot as plt

QUEENS = 8
NUM_CHESS_COLS = 8
POPULATION_SIZE = 10
NUM_ITERATIONS = 100000
MUTATION_PCT = 0.4
COMBINATIONS = 56
MIXING_NUMBER = 2
PARENT_COUNT = 2
MAX_FITNESS = 28

def create_population():
    population = []

    for chromosome in range(POPULATION_SIZE):
        new = [random.randrange(QUEENS) for col_nu in range(QUEENS)]
        population.append(new)
    
    return population

def fitness(parent):
    fitness = 0
    for col_nu in range(NUM_CHESS_COLS):
        par_col = parent[col_nu]
        
        for other_col_nu in range(NUM_CHESS_COLS):    
            par_other_col = parent[other_col_nu]
            
            if other_col_nu == col_nu:
                continue
            if par_other_col == par_col:
                continue
            if other_col_nu + par_other_col == col_nu + par_col:
                continue
            if other_col_nu - par_other_col == col_nu - par_col:
                continue
            
            fitness += 1
    return fitness/2

def selection(population):
    parents = []
    print("Population")
    for chromosome in population:
        fit = fitness(chromosome)
        if random.randrange(COMBINATIONS) < fit:
            parents.append(chromosome)    
        print(f'{chromosome}. Fitness: {fit}')
    return parents

def crossover(parents):
    random_spots = random.sample(range(QUEENS), PARENT_COUNT - 1)
    children = []
    parent_combos = list(itertools.permutations(parents, PARENT_COUNT))
    print("Children")
    for parent_combo in parent_combos:
        child1 = []
        child2 = []
        div_start = 0
        for parent_ind, random_spot in enumerate(random_spots):
            first_part_by1st_parent = parent_combo[parent_ind][div_start:random_spot]
            first_part_by2nd_parent = parent_combo[-1][div_start:random_spot]
            child1.append(first_part_by1st_parent)
            child2.append(first_part_by2nd_parent)
            div_start = random_spot
            second_part_by1st_parent = parent_combo[parent_ind][random_spot:]
            second_part_by2nd_parent = parent_combo[-1][random_spot:]
            child1.append(second_part_by2nd_parent)
            child2.append(second_part_by1st_parent)
        flat_child1 = list(itertools.chain(*child1))
        flat_child2 = list(itertools.chain(*child2))
        fit_child1  = fitness(flat_child1)
        fit_child2  = fitness(flat_child2)
        print(f'Child-1: {flat_child1}. Fitness: {fit_child1}')
        print(f'Child-2: {flat_child2}. Fitness: {fit_child2}')
        children.append(flat_child1)
        children.append(flat_child2)
    return children
            
        
def mutate(child):
    child_size = len(child)
    for row in range(child_size):
        if random.random() < MUTATION_PCT:
            child[row] = random.randrange(QUEENS)
    return child

def genetic_algo(population):
    
    parents = selection(population)

    children = crossover(parents)

    children = list(map(mutate, children))

    new_gen = children

    for ind in population:
        new_gen.append(ind)

    new_gen = sorted(new_gen, key=lambda ind: fitness(ind), reverse=True)[:POPULATION_SIZE]

    return new_gen

def get_avg(population): 
    fitnesses = []
    for chromosome in population: 
        fit = fitness(chromosome)
        fitnesses.append(fit)
    return sum(fitnesses) / len(fitnesses)

if __name__ == "__main__":
    gen = 0
    population = create_population()
    generations = []
    avg_fitnesses = []
    while fitness(population[0]) != MAX_FITNESS or gen > NUM_ITERATIONS:
        avg_fitness = get_avg(population)
        print('Generation: '+ str(gen))
        population = genetic_algo(population)
        generations.append(gen)
        avg_fitnesses.append(avg_fitness)
        gen += 1
    plt.plot(generations,avg_fitnesses)
    plt.title('Genetic Algorithm')
    plt.xlabel('generation')
    plt.ylabel('fitness')
    plt.show()
    