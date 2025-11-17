"""
CSP.02: Framework für Constraint Satisfaction
Implementierung verschiedener CSP-Algorithmen für das Einstein-Rätsel
"""

import random
from typing import Dict, List, Set, Tuple, Any, Optional


class CSP:
    """Constraint Satisfaction Problem"""
    
    def __init__(self):
        self.variables: List[str] = []
        self.domains: Dict[str, List[Any]] = {}
        self.constraints: List[Tuple] = []
        self.neighbors: Dict[str, Set[str]] = {}
    
    def add_variable(self, var: str, domain: List[Any]):
        self.variables.append(var)
        self.domains[var] = domain.copy()
        self.neighbors[var] = set()
    
    def add_constraint(self, var1: str, var2: str, constraint_func):
        self.constraints.append((var1, var2, constraint_func))
        self.neighbors[var1].add(var2)
        self.neighbors[var2].add(var1)


# ============================================================
# Teil 1: Basis-Backtracking
# ============================================================

def BT_Search(csp: CSP, assignment: Dict = None) -> Optional[Dict]:
    """
    Basis-Backtracking ohne Heuristiken
    """
    if assignment is None:
        assignment = {}
    
    if is_complete(assignment, csp):
        return assignment
    
    # Einfach: erste unassignierte Variable
    var = select_unassigned_variable_simple(csp, assignment)
    
    # Natürliche Reihenfolge der Werte
    for value in csp.domains[var]:
        if is_consistent(value, var, assignment, csp):
            assignment[var] = value
            result = BT_Search(csp, assignment)
            if result is not None:
                return result
            del assignment[var]
    
    return None


def select_unassigned_variable_simple(csp: CSP, assignment: Dict) -> str:
    """Wähle erste unassignierte Variable"""
    for var in csp.variables:
        if var not in assignment:
            return var
    return None


def is_complete(assignment: Dict, csp: CSP) -> bool:
    """Prüfe ob alle Variablen zugewiesen sind"""
    return len(assignment) == len(csp.variables)


def is_consistent(value: Any, var: str, assignment: Dict, csp: CSP) -> bool:
    """Prüfe ob Zuweisung mit Constraints konsistent ist"""
    for (var1, var2, constraint_func) in csp.constraints:
        if var == var1 and var2 in assignment:
            if not constraint_func(value, assignment[var2]):
                return False
        elif var == var2 and var1 in assignment:
            if not constraint_func(assignment[var1], value):
                return False
    return True


# ============================================================
# Teil 2: BT mit MRV und Gradheuristik
# ============================================================

def BT_Search_with_heuristics(csp: CSP, assignment: Dict = None) -> Optional[Dict]:
    """
    Backtracking mit MRV und Gradheuristik
    """
    if assignment is None:
        assignment = {}
    
    if is_complete(assignment, csp):
        return assignment
    
    # MRV + Gradheuristik
    var = select_unassigned_variable_MRV(csp, assignment)
    
    for value in order_domain_values(csp, var, assignment):
        if is_consistent(value, var, assignment, csp):
            assignment[var] = value
            result = BT_Search_with_heuristics(csp, assignment)
            if result is not None:
                return result
            del assignment[var]
    
    return None


def select_unassigned_variable_MRV(csp: CSP, assignment: Dict) -> str:
    """
    MRV (Minimum Remaining Values) mit Gradheuristik als Tie-Breaker
    """
    unassigned = [v for v in csp.variables if v not in assignment]
    
    if not unassigned:
        return None
    
    # MRV: Variable mit kleinstem Wertebereich
    min_values = min(len(csp.domains[v]) for v in unassigned)
    candidates = [v for v in unassigned if len(csp.domains[v]) == min_values]
    
    # Gradheuristik als Tie-Breaker
    if len(candidates) > 1:
        return max(candidates, key=lambda v: len(csp.neighbors[v]))
    
    return candidates[0]


def order_domain_values(csp: CSP, var: str, assignment: Dict) -> List[Any]:
    """Ordne Werte (hier: einfach natürliche Reihenfolge)"""
    return csp.domains[var]


# ============================================================
# Teil 3: AC-3 Algorithmus
# ============================================================

def AC3(csp: CSP, queue: List[Tuple[str, str]] = None) -> bool:
    """
    Arc Consistency 3 Algorithmus
    Reduziert Domänen durch Kantenkonsistenz
    """
    if queue is None:
        # Initialisiere Queue mit allen Kanten in beide Richtungen
        queue = [(Xi, Xj) for Xi in csp.variables for Xj in csp.neighbors[Xi]]
    
    while queue:
        (Xi, Xj) = queue.pop(0)
        if revise(csp, Xi, Xj):
            if len(csp.domains[Xi]) == 0:
                return False  # Unlösbar
            # Füge Nachbarn von Xi (außer Xj) zur Queue hinzu
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    
    return True


def revise(csp: CSP, Xi: str, Xj: str) -> bool:
    """
    Entferne Werte aus D_Xi, die keine konsistente Zuweisung in D_Xj haben
    """
    revised = False
    
    # Finde Constraint zwischen Xi und Xj
    constraint_func = None
    for (var1, var2, func) in csp.constraints:
        if (var1 == Xi and var2 == Xj) or (var1 == Xj and var2 == Xi):
            constraint_func = func
            break
    
    if constraint_func is None:
        return False
    
    to_remove = []
    for x in csp.domains[Xi]:
        # Prüfe ob es ein y in D_Xj gibt, sodass Constraint erfüllt ist
        has_support = False
        for y in csp.domains[Xj]:
            if constraint_func(x, y):
                has_support = True
                break
        
        if not has_support:
            to_remove.append(x)
            revised = True
    
    for val in to_remove:
        csp.domains[Xi].remove(val)
    
    return revised


def MAC(csp: CSP, assignment: Dict = None) -> Optional[Dict]:
    """
    Maintaining Arc Consistency
    Backtracking mit AC-3 nach jeder Zuweisung
    """
    if assignment is None:
        assignment = {}
    
    if is_complete(assignment, csp):
        return assignment
    
    var = select_unassigned_variable_MRV(csp, assignment)
    
    for value in order_domain_values(csp, var, assignment):
        if is_consistent(value, var, assignment, csp):
            assignment[var] = value
            
            # Speichere Domänen für Backtracking
            saved_domains = {v: csp.domains[v].copy() for v in csp.variables}
            
            # Kantenkonsistenz erzeugen
            queue = [(Xi, var) for Xi in csp.neighbors[var] if Xi not in assignment]
            if AC3(csp, queue):
                result = MAC(csp, assignment)
                if result is not None:
                    return result
            
            # Backtrack: Stelle Domänen wieder her
            del assignment[var]
            csp.domains = saved_domains
    
    return None


# ============================================================
# Teil 4: Min-Conflicts Heuristik
# ============================================================

def min_conflicts(csp: CSP, max_steps: int = 10000) -> Optional[Dict]:
    """
    Min-Conflicts lokale Suche
    Startet mit zufälliger vollständiger Belegung
    """
    # Zufällige vollständige Initialisierung
    current = {var: random.choice(csp.domains[var]) for var in csp.variables}
    
    for i in range(max_steps):
        # Prüfe ob Lösung gefunden
        if num_conflicts(current, csp) == 0:
            return current
        
        # Wähle konfliktbehaftete Variable
        conflicted = conflicted_vars(current, csp)
        if not conflicted:
            return current
        
        var = random.choice(conflicted)
        
        # Wähle Wert mit minimalen Konflikten
        value = min(csp.domains[var], 
                   key=lambda v: count_conflicts(var, v, current, csp))
        
        current[var] = value
    
    return None  # Keine Lösung gefunden


def num_conflicts(assignment: Dict, csp: CSP) -> int:
    """Zähle Anzahl verletzter Constraints"""
    conflicts = 0
    for (var1, var2, constraint_func) in csp.constraints:
        if var1 in assignment and var2 in assignment:
            if not constraint_func(assignment[var1], assignment[var2]):
                conflicts += 1
    return conflicts


def conflicted_vars(assignment: Dict, csp: CSP) -> List[str]:
    """Finde alle Variablen mit Constraint-Verletzungen"""
    conflicted = []
    for var in csp.variables:
        if count_conflicts(var, assignment[var], assignment, csp) > 0:
            conflicted.append(var)
    return conflicted


def count_conflicts(var: str, value: Any, assignment: Dict, csp: CSP) -> int:
    """Zähle Konflikte für Variable mit gegebenem Wert"""
    conflicts = 0
    for neighbor in csp.neighbors[var]:
        if neighbor in assignment:
            # Finde Constraint
            for (var1, var2, constraint_func) in csp.constraints:
                if (var1 == var and var2 == neighbor) or (var1 == neighbor and var2 == var):
                    if not constraint_func(value, assignment[neighbor]):
                        conflicts += 1
                    break
    return conflicts


# ============================================================
# Beispiel: Einfaches CSP
# ============================================================

def create_simple_csp() -> CSP:
    """
    Erstellt ein einfaches Beispiel-CSP für Tests
    Map Coloring Problem: Färbe Karte mit 3 Farben
    """
    csp = CSP()
    
    # Variablen: Regionen
    regions = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    colors = ['red', 'green', 'blue']
    
    for region in regions:
        csp.add_variable(region, colors)
    
    # Constraints: Nachbarregionen müssen unterschiedliche Farben haben
    def different_colors(c1, c2):
        return c1 != c2
    
    neighbors = [
        ('WA', 'NT'), ('WA', 'SA'),
        ('NT', 'SA'), ('NT', 'Q'),
        ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'),
        ('Q', 'NSW'),
        ('NSW', 'V')
    ]
    
    for (r1, r2) in neighbors:
        csp.add_constraint(r1, r2, different_colors)
    
    return csp


# ============================================================
# Main / Tests
# ============================================================

if __name__ == "__main__":
    print("="*70)
    print("CSP Algorithmen Vergleich")
    print("="*70)
    
    # Erstelle Beispiel-CSP
    csp = create_simple_csp()
    
    print("\n--- Test 1: Basis-Backtracking ---")
    import time
    start = time.time()
    solution = BT_Search(csp)
    end = time.time()
    print(f"Lösung: {solution}")
    print(f"Zeit: {end - start:.4f}s")
    
    print("\n--- Test 2: BT mit MRV + Gradheuristik ---")
    csp2 = create_simple_csp()  # Neues CSP (frische Domänen)
    start = time.time()
    solution = BT_Search_with_heuristics(csp2)
    end = time.time()
    print(f"Lösung: {solution}")
    print(f"Zeit: {end - start:.4f}s")
    
    print("\n--- Test 3: AC-3 + MAC ---")
    csp3 = create_simple_csp()
    start = time.time()
    AC3(csp3)
    print(f"Domänen nach AC-3: {csp3.domains}")
    solution = MAC(csp3)
    end = time.time()
    print(f"Lösung: {solution}")
    print(f"Zeit: {end - start:.4f}s")
    
    print("\n--- Test 4: Min-Conflicts ---")
    csp4 = create_simple_csp()
    start = time.time()
    solution = min_conflicts(csp4, max_steps=1000)
    end = time.time()
    print(f"Lösung: {solution}")
    print(f"Zeit: {end - start:.4f}s")
    
    print("\n" + "="*70)
