import random

queens = [1, 1, 1, 1, 1, 1, 1, 1]

def fitness(queens):
    horizontal_collisions = sum([queens.count(queen)-1 for queen in queens]) / 2

    diagonal_collisions = 0

    n = len(queens)
    left_diagonal = [0] * (2*n - 1)
    right_diagonal = [0] * (2*n - 1)

    for i in range(n):
        left_diagonal[i + queens[i] - 1] += 1
        right_diagonal[n - i + queens[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2*n - 1):
        if left_diagonal[i] > 1:
            diagonal_collisions += (left_diagonal[i] * (left_diagonal[i] - 1)) / 2
        if right_diagonal[i] > 1:
            diagonal_collisions += (right_diagonal[i] * (right_diagonal[i] - 1)) / 2

    return int(maxFitness - (horizontal_collisions + diagonal_collisions))

maxFitness = (len(queens) * (len(queens) - 1)) / 2

print("=" * 60)
print("8-QUEENS-PROBLEM - GENETISCHER ALGORITHMUS")
print("=" * 60)
print(f"Initialkonfiguration: {queens}")
print(f"Fitness der Initialkonfiguration: {fitness(queens)}/{int(maxFitness)}")
print(f"Maximale Fitness (konfliktfrei): {int(maxFitness)}")
print("=" * 60)

def select_mating_pool(population, fitnesses, num_parents):
    parents = []
    for _ in range(num_parents):
        max_fitness_idx = fitnesses.index(max(fitnesses))
        parents.append(population[max_fitness_idx])
        fitnesses[max_fitness_idx] = -1  # Exclude this individual from being selected again
    return parents

def crossover(parents, offspring_size):
    offspring = []
    crossover_point = len(parents[0]) // 2

    for k in range(offspring_size):
        parent1_idx = k % len(parents)
        parent2_idx = (k + 1) % len(parents)
        child = parents[parent1_idx][:crossover_point] + parents[parent2_idx][crossover_point:]
        offspring.append(child)
    return offspring

def mutate(offspring):
    for idx in range(len(offspring)):
        gene_idx = random.randint(0, len(offspring[idx]) - 1)
        new_value = random.randint(1, len(offspring[idx]))
        offspring[idx][gene_idx] = new_value
    return offspring

# Example usage
population_size = 20
num_generations = 1000

# Initialize population
population = [queens for _ in range(population_size)]

print(f"\nStarte genetischen Algorithmus...")
print(f"Populationsgröße: {population_size}")
print(f"Maximale Generationen: {num_generations}")
print(f"Anzahl Eltern pro Generation: 5")
print("=" * 60)
print()

best_solution = None
best_solution_generation = 0

for generation in range(num_generations):
    fitnesses = [fitness(individual) for individual in population]
    parents = select_mating_pool(population, fitnesses.copy(), num_parents=5)
    offspring = crossover(parents, offspring_size=population_size - len(parents))
    offspring = mutate(offspring)
    population = parents + offspring
    
    best_fitness = max(fitnesses)
    avg_fitness = sum(fitnesses) / len(fitnesses)
    worst_fitness = min(fitnesses)
    best_individual = population[fitnesses.index(best_fitness)]
    
    # Zeige nur jede 10. Generation oder wenn sich die beste Fitness verbessert
    if generation % 10 == 0 or best_fitness > (best_solution[1] if best_solution else 0):
        print(f"Generation {generation:3d} | Beste: {best_fitness:2.0f} | Durchschnitt: {avg_fitness:5.2f} | Schlechteste: {worst_fitness:2.0f}")
    
    if best_solution is None or best_fitness > best_solution[1]:
        best_solution = (best_individual.copy(), best_fitness, generation)
        best_solution_generation = generation
    
    if best_fitness == maxFitness:
        print("=" * 60)
        print(f"✓ LÖSUNG GEFUNDEN in Generation {generation}!")
        print(f"Konfiguration: {best_individual}")
        print(f"Fitness: {best_fitness}/{int(maxFitness)} (konfliktfrei)")
        print("=" * 60)
        break
else:
    print("=" * 60)
    print(f"Maximale Generationen ({num_generations}) erreicht.")
    if best_solution:
        print(f"\nBeste gefundene Lösung:")
        print(f"  Generation: {best_solution_generation}")
        print(f"  Konfiguration: {best_solution[0]}")
        print(f"  Fitness: {best_solution[1]}/{int(maxFitness)}")
        print(f"  Verbleibende Konflikte: {int(maxFitness - best_solution[1])}")
    print("=" * 60)

