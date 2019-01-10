import math

from aco import ACO, Graph
from plot import plot
import matplotlib.pyplot as plt
import numpy as np


def distance(loc1: dict, loc2: dict):
    return math.sqrt((loc1['x'] - loc2['x']) ** 2 + (loc1['y'] - loc2['y']) ** 2)


def main():
    cities = []
    points = []

    """
    :param ant_count:
    :param generations:
    :param alpha: relative importance of pheromone
    :param beta: relative importance of heuristic information
    :param rho: pheromone residual coefficient
    :param q: pheromone intensity
    :param strategy: pheromone update strategy. 0 - ant-cycle, 1 - ant-quality, 2 - ant-density
    """

    num_ants = 30
    generations = 100
    alpha = 1.0
    beta = 9
    rho = 2  
    q = 0.2 
    strategy = 2
    

    with open('./data/berlin.txt') as f:
        for line in f.readlines():
            city = line.split(' ')
            cities.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
            points.append((int(city[1]), int(city[2])))
    cost_matrix = []
    rank = len(cities)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)
    aco = ACO(num_ants, generations, alpha, beta, rho, q, strategy)
    graph = Graph(cost_matrix, rank)
    #path, cost, all_costs, all_paths, all_best_costs, all_best_paths, all_gen_best_costs = aco.solve(graph)
    path, cost, all_converge, total_converge = aco.solve(graph)
    print('cost: {}, path: {}'.format(cost, path))

    f, (ax1, ax2) = plt.subplots(1, 2,sharey=True)

    ax1.plot(range(num_ants), np.mean(all_converge,axis=0), 'r-', alpha=1, label="mean")

    for i in range(generations):
        ax1.plot( range(len(all_converge[i])), all_converge[i], '#82848c', alpha=0.3)

    ax1.set_title('Generations')
    ax2.set_title('Convergence (lowest cost found)')
    
    ax1.set(xlabel="Ants", ylabel="Cost (Distance)")
    ax2.set(xlabel="Ants * Generations",)

    ax2.plot(range(len(total_converge)), total_converge)
    
    #plt.xlabel('Ants')
    #plt.ylabel('Cost (Distance)')
    #plt.legend(['mean','iteration'])
    plt.show()


#    plot(points, path)

if __name__ == '__main__':
    main()
