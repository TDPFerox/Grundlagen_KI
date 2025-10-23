# Landkarten-Färbeproblem - Genetischer Algorithmus
import random

# Darstellung: [1, 3, 0, 2] bedeutet:
# - Land 0 hat Farbe 1
# - Land 1 hat Farbe 3
# - Land 2 hat Farbe 0
# - Land 3 hat Farbe 2

# Beispielhafte Nachbarschaftsstruktur (Adjazenzliste)
neighbors = {
    0: [],
    1: [2,3],
    2: [1,3,4],
    3: [1,2,4],
    4: [2,3,5],
    5: [4]
}

# Anzahl der Länder und verfügbare Farben
NUM_COUNTRIES = len(neighbors)
NUM_COLORS = 5  # 4-Farben-Problem

# Fitness-Funktion: Zählt die Anzahl der Konflikte (benachbarte Länder mit gleicher Farbe)
def fitness(individual):
    """
    Berechnet die Fitness eines Individuums mit zwei Kriterien:
    1. Primär: Anzahl der korrekten Färbungen (keine Konflikte mit Nachbarn)
    2. Sekundär: Möglichst wenige verschiedene Farben verwenden
    
    Returns: Tuple (conflicts_fitness, color_fitness) für mehrstufigen Vergleich
    """
    conflicts = 0
    total_edges = 0
    
    for country, neighbor_list in neighbors.items():
        for neighbor in neighbor_list:
            total_edges += 1
            if individual[country] == individual[neighbor]:
                conflicts += 1
    
    # Jede Kante wird zweimal gezählt (von beiden Seiten)
    total_edges //= 2
    conflicts //= 2
    
    # Primäre Fitness: Je weniger Konflikte, desto besser
    conflicts_fitness = total_edges - conflicts
    
    # Sekundäre Fitness: Je weniger verschiedene Farben verwendet, desto besser
    num_colors_used = len(set(individual))
    color_fitness = NUM_COLORS - num_colors_used
    
    # Kombinierte Fitness: Konflikte haben absolute Priorität
    # Multiplizieren mit großem Faktor, damit Konflikte wichtiger sind
    combined_fitness = conflicts_fitness * 1000 + color_fitness
    
    return combined_fitness

def get_fitness_details(individual):
    """
    Hilfsfunktion: Gibt detaillierte Fitness-Informationen zurück.
    Returns: (conflicts, num_colors_used, combined_fitness)
    """
    conflicts = 0
    total_edges = 0
    
    for country, neighbor_list in neighbors.items():
        for neighbor in neighbor_list:
            total_edges += 1
            if individual[country] == individual[neighbor]:
                conflicts += 1
    
    total_edges //= 2
    conflicts //= 2
    
    num_colors_used = len(set(individual))
    conflicts_fitness = total_edges - conflicts
    color_fitness = NUM_COLORS - num_colors_used
    combined_fitness = conflicts_fitness * 1000 + color_fitness
    
    return conflicts, num_colors_used, combined_fitness

# Initialisierung: Erstellt eine zufällige Population
def create_individual():
    """
    Erstellt ein zufälliges Individuum (eine zufällige Färbung).
    Stellt sicher, dass alle NUM_COLORS verschiedenen Farben verwendet werden.
    """
    individual = []
    
    # Wenn wir genug Länder haben, stelle sicher dass alle Farben mindestens einmal vorkommen
    if NUM_COUNTRIES >= NUM_COLORS:
        # Erst jede Farbe einmal zuweisen
        individual = list(range(NUM_COLORS))
        # Dann die restlichen Länder zufällig färben
        for _ in range(NUM_COUNTRIES - NUM_COLORS):
            individual.append(random.randint(0, NUM_COLORS - 1))
        # Zufällig mischen
        random.shuffle(individual)
    else:
        # Wenn es weniger Länder als Farben gibt, einfach zufällig färben
        individual = [random.randint(0, NUM_COLORS - 1) for _ in range(NUM_COUNTRIES)]
    
    return individual

def create_population(size):
    """Erstellt eine Population von zufälligen Individuen"""
    return [create_individual() for _ in range(size)]

# Selektion: Turnierselektion
def tournament_selection(population, fitnesses, tournament_size=3):
    """
    Wählt ein Individuum durch Turnierselektion aus.
    Die besten aus einer zufälligen Stichprobe werden ausgewählt.
    """
    tournament_indices = random.sample(range(len(population)), tournament_size)
    tournament_fitnesses = [fitnesses[i] for i in tournament_indices]
    winner_index = tournament_indices[tournament_fitnesses.index(max(tournament_fitnesses))]
    return population[winner_index]

# Crossover: Einpunkt-Crossover
def crossover(parent1, parent2):
    """
    Führt ein Einpunkt-Crossover zwischen zwei Eltern durch.
    Gibt zwei Nachkommen zurück.
    """
    if random.random() < 0.7:  # Crossover-Wahrscheinlichkeit
        crossover_point = random.randint(1, NUM_COUNTRIES - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    else:
        return parent1[:], parent2[:]

# Mutation: Zufällige Änderung einer Farbe
def mutate(individual, mutation_rate=0.1):
    """
    Mutiert ein Individuum mit einer gegebenen Wahrscheinlichkeit.
    Zwei Arten von Mutation:
    1. Normale Mutation: Ändert zufällig die Farbe eines Landes
    2. Farbreduktions-Mutation: Versucht, ungenutzte Farben zu eliminieren
    """
    mutated = individual[:]
    
    # 50% Chance für Farbreduktions-Mutation (versucht Farben zu reduzieren)
    if random.random() < 0.5:
        colors_used = set(mutated)
        # Wenn mehr als 2 Farben verwendet werden, versuche eine zu eliminieren
        if len(colors_used) > 2:
            # Wähle eine zufällig verwendete Farbe
            color_to_replace = random.choice(list(colors_used))
            # Ersetze sie durch eine andere verwendete Farbe
            replacement_color = random.choice(list(colors_used - {color_to_replace}))
            mutated = [replacement_color if c == color_to_replace else c for c in mutated]
    
    # Normale Mutation
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            # Bevorzuge bereits verwendete Farben
            colors_used = list(set(mutated))
            if random.random() < 0.7 and len(colors_used) > 0:
                # 70% Chance: Wähle eine bereits verwendete Farbe
                mutated[i] = random.choice(colors_used)
            else:
                # 30% Chance: Wähle eine beliebige Farbe
                mutated[i] = random.randint(0, NUM_COLORS - 1)
    
    return mutated

# Hauptalgorithmus
def genetic_algorithm(pop_size=100, generations=100, mutation_rate=0.1):
    """
    Führt den genetischen Algorithmus aus.
    
    Parameter:
    - pop_size: Größe der Population
    - generations: Anzahl der Generationen
    - mutation_rate: Mutationsrate
    
    Returns:
    - Bestes gefundenes Individuum und seine Fitness
    """
    # Initialisierung
    population = create_population(pop_size)
    best_individual = None
    best_fitness = -1
    
    # Statistiken über alle Generationen sammeln
    all_aes = []  # Average Evaluation Scores aller Generationen
    all_sr = []   # Selection Rates aller Generationen
    
    # Maximale mögliche Fitness berechnen
    max_possible_fitness = sum(len(neighbors[i]) for i in neighbors) // 2
    
    for generation in range(generations):
        # Fitness für alle Individuen berechnen
        fitnesses = [fitness(ind) for ind in population]
        
        # Statistiken berechnen
        avg_fitness = sum(fitnesses) / len(fitnesses)  # AES: Average Evaluation Score
        max_fitness_in_gen = max(fitnesses)
        min_fitness_in_gen = min(fitnesses)
        
        # Selektionsrate berechnen (SR: Selection Rate)
        # Anteil der Individuen, die besser als der Durchschnitt sind
        above_average = sum(1 for f in fitnesses if f >= avg_fitness)
        selection_rate = (above_average / len(fitnesses)) * 100
        
        # Statistiken sammeln
        all_aes.append(avg_fitness)
        all_sr.append(selection_rate)
        
        # Bestes Individuum der aktuellen Generation finden
        max_fitness_idx = fitnesses.index(max(fitnesses))
        if fitnesses[max_fitness_idx] > best_fitness:
            best_fitness = fitnesses[max_fitness_idx]
            best_individual = population[max_fitness_idx][:]
            
        # Ausgabe des Fortschritts
        if generation % 10 == 0:
            conflicts, num_colors, _ = get_fitness_details(best_individual)
            print(f"Generation {generation:3d}: Konflikte = {conflicts}, Farben = {num_colors}, "
                  f"AES = {avg_fitness:7.2f}, SR = {selection_rate:5.1f}%, "
                  f"Best = {max_fitness_in_gen:7.2f}")
        
        # Optional: Früher Abbruch nur bei optimaler Lösung (keine Konflikte UND minimale Farben)
        # Entfernt, damit der Algorithmus immer alle Generationen durchläuft und Farben optimiert
        
        # Neue Population erstellen
        new_population = []
        
        # Elitismus: Bestes Individuum übernehmen
        new_population.append(best_individual[:])
        
        # Restliche Population durch Selektion, Crossover und Mutation erzeugen
        while len(new_population) < pop_size:
            # Selektion
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            
            # Crossover
            child1, child2 = crossover(parent1, parent2)
            
            # Mutation
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            
            new_population.append(child1)
            if len(new_population) < pop_size:
                new_population.append(child2)
        
        population = new_population
    
    # Durchschnitte über alle Generationen berechnen
    avg_aes_overall = sum(all_aes) / len(all_aes) if all_aes else 0
    avg_sr_overall = sum(all_sr) / len(all_sr) if all_sr else 0
    
    print("\n" + "=" * 60)
    print("STATISTIKEN ÜBER ALLE GENERATIONEN")
    print("=" * 60)
    print(f"Durchschnittlicher AES: {avg_aes_overall:.2f}")
    print(f"Durchschnittlicher SR:  {avg_sr_overall:.1f}%")
    print("=" * 60)
    
    return best_individual, best_fitness, avg_aes_overall, avg_sr_overall

# Hilfsfunktion zur Visualisierung der Lösung
def print_solution(individual):
    """Gibt die Lösung in lesbarer Form aus"""
    # Anzahl verwendeter Farben
    num_colors_used = len(set(individual))
    colors_used = sorted(set(individual))
    
    print("\nGefundene Färbung:")
    print(f"Verwendete Farben: {num_colors_used} von {NUM_COLORS} verfügbaren Farben")
    print(f"Farben-Set: {colors_used}")
    print()
    for country in range(NUM_COUNTRIES):
        color = individual[country]
        print(f"Land {country}: Farbe {color}")
    
    print("\nÜberprüfung der Nachbarschaften:")
    conflicts = 0
    for country, neighbor_list in neighbors.items():
        for neighbor in neighbor_list:
            if country < neighbor:  # Jede Kante nur einmal prüfen
                if individual[country] == individual[neighbor]:
                    print(f"KONFLIKT: Land {country} und Land {neighbor} haben beide Farbe {individual[country]}")
                    conflicts += 1
                else:
                    print(f"OK: Land {country} (Farbe {individual[country]}) und Land {neighbor} (Farbe {individual[neighbor]})")
    
    if conflicts == 0:
        print(f"\nPerfekte Lösung! Keine Konflikte gefunden.")
        print(f"Optimale Anzahl Farben: {num_colors_used}")
    else:
        print(f"\n{conflicts} Konflikt(e) gefunden.")
    
    return conflicts == 0

# Hauptprogramm
if __name__ == "__main__":
    print("=" * 60)
    print("Genetischer Algorithmus für das Landkarten-Färbeproblem")
    print("=" * 60)
    print(f"Anzahl Länder: {NUM_COUNTRIES}")
    print(f"Anzahl Farben: {NUM_COLORS}")
    print(f"Nachbarschaften: {sum(len(neighbors[i]) for i in neighbors) // 2} Kanten")
    print("=" * 60)
    
    # Genetischen Algorithmus ausführen
    solution, fitness_value, avg_aes, avg_sr = genetic_algorithm(
        pop_size=10,
        generations=100,
        mutation_rate=0.9
    )
    
    print("\nERGEBNIS")
    print("=" * 60)
    
    # Detaillierte Fitness-Informationen
    conflicts, num_colors_used, combined_fitness = get_fitness_details(solution)
    print(f"Beste Fitness (kombiniert): {combined_fitness}")
    print(f"Konflikte: {conflicts}")
    print(f"Verwendete Farben: {num_colors_used} von {NUM_COLORS}")
    
    # Lösung anzeigen
    is_valid = print_solution(solution)