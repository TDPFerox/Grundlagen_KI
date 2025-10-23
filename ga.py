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

def run_single_ga(population_size, num_generations, num_parents, initial_config, verbose=False):
    """
    Führt einen einzelnen GA-Lauf durch und gibt Erfolgsstatus und Generationen zurück.
    
    Returns:
        (success, generations_to_solution, evaluations_to_solution, best_fitness)
        - success: True wenn optimale Lösung gefunden
        - generations_to_solution: Generation bei der Lösung gefunden wurde (oder None)
        - evaluations_to_solution: Anzahl Fitness-Evaluationen bis zur Lösung
        - best_fitness: Beste erreichte Fitness
    """
    # Initialize population
    population = [initial_config[:] for _ in range(population_size)]
    
    evaluations = 0
    
    for generation in range(num_generations):
        # Fitness für alle Individuen berechnen
        fitnesses = [fitness(individual) for individual in population]
        evaluations += len(population)
        
        parents = select_mating_pool(population, fitnesses.copy(), num_parents=num_parents)
        offspring = crossover(parents, offspring_size=population_size - len(parents))
        offspring = mutate(offspring)
        population = parents + offspring
        
        best_fitness = max(fitnesses)
        
        if verbose and generation % 10 == 0:
            avg_fitness = sum(fitnesses) / len(fitnesses)
            worst_fitness = min(fitnesses)
            print(f"Generation {generation:3d} | Beste: {best_fitness:2.0f} | Durchschnitt: {avg_fitness:5.2f} | Schlechteste: {worst_fitness:2.0f}")
        
        # Optimale Lösung gefunden (Fitness = 28, konfliktfrei)
        if best_fitness == maxFitness:
            best_individual = population[fitnesses.index(best_fitness)]
            if verbose:
                print(f"  LÖSUNG GEFUNDEN in Generation {generation}!")
                print(f"  Konfiguration: {best_individual}")
                print(f"  Evaluationen: {evaluations}")
            return True, generation, evaluations, best_fitness
    
    # Keine optimale Lösung gefunden
    final_fitnesses = [fitness(individual) for individual in population]
    evaluations += len(population)
    best_fitness = max(final_fitnesses)
    
    if verbose:
        print(f"✗ Keine optimale Lösung gefunden. Beste Fitness: {best_fitness}/{int(maxFitness)}")
    
    return False, None, evaluations, best_fitness

def run_multiple_experiments(num_runs, population_size, num_generations, num_parents, initial_config):
    """
    Führt mehrere GA-Läufe durch und berechnet SR und AES Metriken.
    
    SR (Success Rate) = Anzahl erfolgreicher Läufe / Anzahl aller Läufe
    AES (Average Evaluations to Solution) = Durchschnitt der Evaluationen bei erfolgreichen Läufen
    AES_Gen = Durchschnitt der Generationen bei erfolgreichen Läufen
    """
    print("=" * 70)
    print(f"EXPERIMENTELLE ANALYSE - {num_runs} LÄUFE")
    print("=" * 70)
    print(f"Parameter:")
    print(f"  Populationsgröße: {population_size}")
    print(f"  Max. Generationen: {num_generations}")
    print(f"  Anzahl Eltern: {num_parents}")
    print(f"  Optimaldefinition: Fitness = {int(maxFitness)} (konfliktfrei)")
    print("=" * 70)
    print()
    
    successful_runs = 0
    total_generations_to_solution = 0
    total_evaluations_to_solution = 0
    best_fitness_values = []
    
    for run in range(num_runs):
        # print(f"Lauf {run + 1}/{num_runs}...", end=" ")
        success, gen_to_solution, eval_to_solution, best_fitness = run_single_ga(
            population_size, num_generations, num_parents, initial_config, verbose=False
        )
        
        best_fitness_values.append(best_fitness)
        
        if success:
            successful_runs += 1
            total_generations_to_solution += gen_to_solution
            total_evaluations_to_solution += eval_to_solution
            # print(f"Erfolg in Generation {gen_to_solution} ({eval_to_solution} Evaluationen)")
        # else:
            # print(f"Fehlgeschlagen (Beste Fitness: {best_fitness}/{int(maxFitness)})")
    
    print()
    print("=" * 70)
    print("ERGEBNISSE:")
    print("=" * 70)
    
    # Success Rate (SR)
    sr = (successful_runs / num_runs) * 100
    print(f"Success Rate (SR):")
    print(f"  {successful_runs}/{num_runs} erfolgreiche Läufe = {sr:.2f}%")
    print()
    
    # Average Evaluations to Solution (AES)
    if successful_runs > 0:
        aes_evaluations = total_evaluations_to_solution / successful_runs
        aes_generations = total_generations_to_solution / successful_runs
        print(f"Average Evaluations to Solution (AES):")
        print(f"  Durchschnitt: {aes_evaluations:.2f} Evaluationen")
        print()
        print(f"Average Generations to Solution (AES_Gen):")
        print(f"  Durchschnitt: {aes_generations:.2f} Generationen")
    else:
        print(f"Average Evaluations to Solution (AES):")
        print(f"  Nicht berechenbar (keine erfolgreichen Läufe)")
        print()
        print(f"Average Generations to Solution (AES_Gen):")
        print(f"  Nicht berechenbar (keine erfolgreichen Läufe)")
    
    print()
    print(f"Beste Fitness über alle Läufe:")
    print(f"  Durchschnitt: {sum(best_fitness_values)/len(best_fitness_values):.2f}")
    print(f"  Maximum: {max(best_fitness_values)}")
    print(f"  Minimum: {min(best_fitness_values)}")
    print("=" * 70)
    
    return sr, aes_evaluations if successful_runs > 0 else None, aes_generations if successful_runs > 0 else None

# Example usage
population_size = 20
num_generations = 200
parents_per_generation = 5

# Wähle Modus: 'single' für einen einzelnen Lauf, 'experiment' für mehrere Läufe
mode = 'experiment'  # Ändere zu 'single' für detaillierten einzelnen Lauf

if mode == 'single':
    # Einzelner detaillierter Lauf
    print(f"\nStarte genetischen Algorithmus...")
    print(f"Populationsgröße: {population_size}")
    print(f"Maximale Generationen: {num_generations}")
    print(f"Anzahl Eltern pro Generation: {parents_per_generation}")
    print("=" * 60)
    print()
    
    success, gen, evals, best_fit = run_single_ga(
        population_size, num_generations, parents_per_generation, queens, verbose=True
    )
    
    if not success:
        print(f"\nKeine optimale Lösung in {num_generations} Generationen gefunden.")
        print(f"Beste erreichte Fitness: {best_fit}/{int(maxFitness)}")

elif mode == 'experiment':
    # Mehrere Läufe für SR und AES Analyse
    num_runs = 10000  # Anzahl der Experimente
    sr, aes_evals, aes_gens = run_multiple_experiments(
        num_runs, population_size, num_generations, parents_per_generation, queens
    )


