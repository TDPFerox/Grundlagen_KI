# Es ist wieder Wahlkampf: Zwei Kandidaten O und M bewerben sich um die Kanzlerschaft.
# Die folgende Tabelle zeigt die Präferenzen von sieben Wählern.
#
# Nr.   Alter   Einkommen   Bildung     Kandidat
# 1     ≥ 35    hoch        Abitur      O
# 2     < 35    niedrig     Master      O
# 3     ≥ 35    hoch        Bachelor    M
# 4     ≥ 35    niedrig     Abitur      M
# 5     ≥ 35    hoch        Master      O
# 6     < 35    hoch        Bachelor    O
# 7     < 35    niedrig     Abitur      M
#
# Implementierung des CAL3-Algorithmus mit Schwellen S1 = 4 und S2 = 0.7

from collections import Counter
import pandas as pd


class CAL3DecisionTree:
    """
    CAL3 (Concept Acquisition Learning 3) Algorithmus
    
    Verwendet zwei Schwellenwerte:
    - S1: Minimale Anzahl von Beispielen für einen Split
    - S2: Minimaler Reinheitsgrad (Anteil der häufigsten Klasse)
    """
    
    def __init__(self, s1=4, s2=0.7):
        """
        s1: Minimale Anzahl Beispiele für Split (Standard: 4)
        s2: Minimaler Reinheitsgrad (Standard: 0.7)
        """
        self.s1 = s1  # Schwelle für minimale Beispielanzahl
        self.s2 = s2  # Schwelle für Reinheit
        self.tree = None
        self.feature_names = None
        self.target_name = None
    
    def purity(self, target_col):
        """
        Berechnet den Reinheitsgrad (Anteil der häufigsten Klasse)
        """
        if len(target_col) == 0:
            return 0
        
        counts = Counter(target_col)
        max_count = max(counts.values())
        total = len(target_col)
        
        return max_count / total
    
    def majority_class(self, target_col):
        """
        Gibt die häufigste Klasse zurück
        """
        counts = Counter(target_col)
        return counts.most_common(1)[0][0]
    
    def is_pure_enough(self, data, target):
        """
        Prüft ob der Knoten rein genug ist (≥ S2)
        """
        purity_value = self.purity(data[target])
        return purity_value >= self.s2
    
    def has_enough_samples(self, data):
        """
        Prüft ob genug Beispiele vorhanden sind (≥ S1)
        """
        return len(data) >= self.s1
    
    def select_best_feature_cal3(self, data, features, target):
        """
        CAL3-spezifische Attributauswahl:
        Wählt das Attribut, das die höchste durchschnittliche Reinheit erzeugt
        """
        best_feature = None
        best_purity = -1
        purities = {}
        
        for feature in features:
            # Berechne gewichtete durchschnittliche Reinheit nach Split
            total_samples = len(data)
            weighted_purity = 0
            
            for value in data[feature].unique():
                subset = data[data[feature] == value]
                weight = len(subset) / total_samples
                subset_purity = self.purity(subset[target])
                weighted_purity += weight * subset_purity
            
            purities[feature] = weighted_purity
            
            if weighted_purity > best_purity:
                best_purity = weighted_purity
                best_feature = feature
        
        return best_feature, purities
    
    def build_tree(self, data, features, target, depth=0, parent_path="Root"):
        """
        Rekursiver Aufbau des CAL3-Entscheidungsbaums
        
        Stopbedingungen:
        1. Reinheit ≥ S2
        2. Anzahl Beispiele < S1
        3. Keine Attribute mehr verfügbar
        """
        n_samples = len(data)
        current_purity = self.purity(data[target])
        majority = self.majority_class(data[target])
        
        print(f"\n{'  '*depth}Knoten: {parent_path}")
        print(f"{'  '*depth}  Beispiele: {n_samples}")
        print(f"{'  '*depth}  Reinheit: {current_purity:.3f}")
        print(f"{'  '*depth}  Mehrheitsklasse: {majority}")
        
        # Stopbedingung 1: Reinheit ≥ S2
        if current_purity >= self.s2:
            print(f"{'  '*depth}  → BLATT (Reinheit {current_purity:.3f} ≥ S2={self.s2})")
            return {
                'leaf': True,
                'class': majority,
                'count': n_samples,
                'purity': current_purity,
                'reason': f'Purity {current_purity:.3f} >= S2={self.s2}'
            }
        
        # Stopbedingung 2: Zu wenige Beispiele (< S1)
        if n_samples < self.s1:
            print(f"{'  '*depth}  → BLATT (Beispiele {n_samples} < S1={self.s1})")
            return {
                'leaf': True,
                'class': majority,
                'count': n_samples,
                'purity': current_purity,
                'reason': f'Samples {n_samples} < S1={self.s1}'
            }
        
        # Stopbedingung 3: Keine Features mehr
        if len(features) == 0:
            print(f"{'  '*depth}  → BLATT (Keine Attribute mehr)")
            return {
                'leaf': True,
                'class': majority,
                'count': n_samples,
                'purity': current_purity,
                'reason': 'No features left'
            }
        
        # Bestes Attribut wählen
        best_feat, purities = self.select_best_feature_cal3(data, features, target)
        
        print(f"{'  '*depth}  Attribut-Reinheiten:")
        for feat, pur in purities.items():
            marker = " ← GEWÄHLT" if feat == best_feat else ""
            print(f"{'  '*depth}    {feat}: {pur:.3f}{marker}")
        
        # Knoten erstellen
        tree = {
            'leaf': False,
            'feature': best_feat,
            'purities': purities,
            'children': {},
            'count': n_samples,
            'purity': current_purity
        }
        
        # Für jeden Attributwert einen Teilbaum erstellen
        for value in data[best_feat].unique():
            subset = data[data[best_feat] == value]
            remaining_features = [f for f in features if f != best_feat]
            
            # Rekursiver Aufruf
            tree['children'][value] = self.build_tree(
                subset, remaining_features, target, depth + 1, 
                f"{parent_path} → {best_feat}={value}"
            )
        
        return tree
    
    def fit(self, data, target):
        """
        Trainiert den CAL3-Entscheidungsbaum
        """
        self.target_name = target
        self.feature_names = [col for col in data.columns if col != target]
        
        print("\n" + "="*70)
        print(f"CAL3 TRAINING (S1={self.s1}, S2={self.s2})")
        print("="*70)
        
        self.tree = self.build_tree(data, self.feature_names, target)
        
        print("\n" + "="*70)
        
        return self.tree
    
    def predict_sample(self, sample, tree=None):
        """
        Klassifiziert ein einzelnes Beispiel
        """
        if tree is None:
            tree = self.tree
        
        if tree['leaf']:
            return tree['class']
        
        feature = tree['feature']
        value = sample[feature]
        
        if value in tree['children']:
            return self.predict_sample(sample, tree['children'][value])
        else:
            # Fallback: Mehrheitsklasse
            return 'O'
    
    def print_tree(self, tree=None, indent="", feature_value=""):
        """
        Gibt den Baum lesbar aus
        """
        if tree is None:
            tree = self.tree
        
        if tree['leaf']:
            print(f"{indent}→ BLATT: Klasse={tree['class']}, "
                  f"n={tree['count']}, Reinheit={tree['purity']:.3f}")
            print(f"{indent}  ({tree['reason']})")
        else:
            if feature_value:
                print(f"{indent}{feature_value}:")
            print(f"{indent}[{tree['feature']}] (n={tree['count']}, "
                  f"Reinheit={tree['purity']:.3f})")
            
            for value, subtree in tree['children'].items():
                self.print_tree(subtree, indent + "  ", 
                              f"  {tree['feature']}={value}")


def explain_cal3_algorithm():
    """
    Erklärt den CAL3-Algorithmus
    """
    print("\n" + "="*70)
    print("CAL3 ALGORITHMUS - ERKLÄRUNG")
    print("="*70)
    print("""
CAL3 (Concept Acquisition Learning 3) ist ein Entscheidungsbaum-
Algorithmus, der zwei Schwellenwerte verwendet:

• S1 (Minimale Beispielanzahl):
  - Split nur wenn ≥ S1 Beispiele vorhanden
  - Verhindert Overfitting bei kleinen Teilmengen
  - In dieser Aufgabe: S1 = 4

• S2 (Minimaler Reinheitsgrad):
  - Reinheit = Anteil der häufigsten Klasse
  - Stoppt wenn Reinheit ≥ S2
  - In dieser Aufgabe: S2 = 0.7 (70%)

Attributauswahl:
  - Wählt das Attribut mit der höchsten gewichteten
    durchschnittlichen Reinheit nach dem Split

Stopbedingungen (Blattknoten):
  1. Reinheit ≥ S2
  2. Beispiele < S1
  3. Keine Attribute mehr verfügbar
    """)
    print("="*70)


def main():
    """
    Hauptfunktion: Führt CAL3 auf dem Wahlkampf-Datensatz aus
    """
    # Datensatz definieren
    data = pd.DataFrame({
        'Nr': [1, 2, 3, 4, 5, 6, 7],
        'Alter': ['≥35', '<35', '≥35', '≥35', '≥35', '<35', '<35'],
        'Einkommen': ['hoch', 'niedrig', 'hoch', 'niedrig', 'hoch', 'hoch', 'niedrig'],
        'Bildung': ['Abitur', 'Master', 'Bachelor', 'Abitur', 'Master', 'Bachelor', 'Abitur'],
        'Kandidat': ['O', 'O', 'M', 'M', 'O', 'O', 'M']
    })
    
    print("\n" + "="*70)
    print("WAHLKAMPF-DATENSATZ")
    print("="*70)
    print(data.to_string(index=False))
    print("="*70)
    
    # Algorithmus erklären
    explain_cal3_algorithm()
    
    # CAL3 mit S1=4, S2=0.7 ausführen
    cal3 = CAL3DecisionTree(s1=4, s2=0.7)
    tree = cal3.fit(data[['Alter', 'Einkommen', 'Bildung', 'Kandidat']], 'Kandidat')
    
    print("\n" + "="*70)
    print("RESULTIERENDER CAL3-BAUM")
    print("="*70 + "\n")
    cal3.print_tree()
    
    # Test mit Trainingsbeispielen
    print("\n" + "="*70)
    print("KLASSIFIKATION DER TRAININGSBEISPIELE")
    print("="*70 + "\n")
    
    for idx, row in data.iterrows():
        prediction = cal3.predict_sample(row)
        actual = row['Kandidat']
        match = "✓" if prediction == actual else "✗"
        print(f"Nr. {row['Nr']}: Vorhergesagt={prediction}, Tatsächlich={actual} {match}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()