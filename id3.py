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
# Implementierung des ID3-Algorithmus (Iterative Dichotomiser 3)

import math
from collections import Counter
import pandas as pd


class ID3DecisionTree:
    """
    ID3 (Iterative Dichotomiser 3) Algorithmus
    Verwendet Information Gain (basierend auf Entropie) zur Attributauswahl
    """
    
    def __init__(self):
        self.tree = None
        self.feature_names = None
        self.target_name = None
    
    def entropy(self, target_col):
        """
        Berechnet die Entropie eines Zielvektors
        H(S) = -Σ p_i * log2(p_i)
        """
        elements, counts = np.unique(target_col, return_counts=True)
        entropy = 0
        total = len(target_col)
        
        for count in counts:
            probability = count / total
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def information_gain(self, data, feature, target):
        """
        Berechnet den Information Gain für ein Attribut
        IG(S, A) = H(S) - Σ (|S_v| / |S|) * H(S_v)
        
        wobei:
        - H(S) = Entropie des gesamten Datensatzes
        - S_v = Teilmenge mit Attributwert v
        - H(S_v) = Entropie der Teilmenge
        """
        # Gesamtentropie
        total_entropy = self.entropy(data[target])
        
        # Gewichtete Entropie nach Split
        values = data[feature].unique()
        weighted_entropy = 0
        total_samples = len(data)
        
        for value in values:
            subset = data[data[feature] == value]
            weight = len(subset) / total_samples
            weighted_entropy += weight * self.entropy(subset[target])
        
        # Information Gain
        return total_entropy - weighted_entropy
    
    def best_feature(self, data, features, target):
        """
        Wählt das Attribut mit dem höchsten Information Gain
        """
        gains = {}
        for feature in features:
            gains[feature] = self.information_gain(data, feature, target)
        
        best_feature = max(gains, key=gains.get)
        return best_feature, gains
    
    def build_tree(self, data, features, target, depth=0, max_depth=10):
        """
        Rekursiver Aufbau des Entscheidungsbaums
        
        Stopbedingungen:
        1. Alle Beispiele haben dieselbe Klasse
        2. Keine Attribute mehr verfügbar
        3. Maximale Tiefe erreicht
        """
        # Stopbedingung: Alle Beispiele derselben Klasse
        target_values = data[target].unique()
        if len(target_values) == 1:
            return {'leaf': True, 'class': target_values[0], 'count': len(data)}
        
        # Stopbedingung: Keine Features mehr oder maximale Tiefe
        if len(features) == 0 or depth >= max_depth:
            # Mehrheitsentscheidung
            majority_class = data[target].mode()[0]
            return {'leaf': True, 'class': majority_class, 'count': len(data)}
        
        # Bestes Attribut wählen
        best_feat, gains = self.best_feature(data, features, target)
        
        # Knoten erstellen
        tree = {
            'leaf': False,
            'feature': best_feat,
            'information_gains': gains,
            'children': {},
            'count': len(data)
        }
        
        # Für jeden Attributwert einen Teilbaum erstellen
        for value in data[best_feat].unique():
            subset = data[data[best_feat] == value]
            remaining_features = [f for f in features if f != best_feat]
            
            # Rekursiver Aufruf
            tree['children'][value] = self.build_tree(
                subset, remaining_features, target, depth + 1, max_depth
            )
        
        return tree
    
    def fit(self, data, target):
        """
        Trainiert den Entscheidungsbaum
        """
        self.target_name = target
        self.feature_names = [col for col in data.columns if col != target]
        self.tree = self.build_tree(data, self.feature_names, target)
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
            # Fallback: Häufigste Klasse im Knoten
            return 'O'  # Default
    
    def print_tree(self, tree=None, indent="", feature_value=""):
        """
        Gibt den Baum lesbar aus
        """
        if tree is None:
            tree = self.tree
        
        if tree['leaf']:
            print(f"{indent}→ Klasse: {tree['class']} (n={tree['count']})")
        else:
            if feature_value:
                print(f"{indent}{feature_value}:")
            print(f"{indent}[{tree['feature']}] (n={tree['count']})")
            
            for value, subtree in tree['children'].items():
                self.print_tree(subtree, indent + "  ", f"  {tree['feature']}={value}")


def print_calculation_steps(data, target):
    """
    Gibt die Berechnungsschritte detailliert aus
    """
    print("\n" + "="*70)
    print("ID3 ALGORITHMUS - BERECHNUNGSSCHRITTE")
    print("="*70)
    
    # 1. Gesamtentropie berechnen
    print("\n### SCHRITT 1: Berechnung der Gesamtentropie ###\n")
    target_counts = data[target].value_counts()
    total = len(data)
    
    print(f"Klassenverteilung: {dict(target_counts)}")
    print(f"Gesamt: {total} Beispiele\n")
    
    entropy_calc = []
    for cls, count in target_counts.items():
        p = count / total
        entropy_calc.append(f"-({count}/{total}) * log2({count}/{total})")
        print(f"p({cls}) = {count}/{total} = {p:.4f}")
    
    entropy_formula = " + ".join(entropy_calc)
    total_entropy = -sum((count/total) * math.log2(count/total) for count in target_counts)
    print(f"\nH(S) = {entropy_formula}")
    print(f"H(S) = {total_entropy:.4f}\n")
    
    # 2. Information Gain für jedes Attribut
    print("="*70)
    print("### SCHRITT 2: Information Gain für jedes Attribut ###\n")
    
    features = [col for col in data.columns if col != target]
    
    for feature in features:
        print(f"\n--- Attribut: {feature} ---\n")
        
        weighted_entropy = 0
        
        for value in data[feature].unique():
            subset = data[data[feature] == value]
            subset_counts = subset[target].value_counts()
            subset_size = len(subset)
            weight = subset_size / total
            
            print(f"{feature} = {value}: {subset_size} Beispiele")
            print(f"  Verteilung: {dict(subset_counts)}")
            
            if len(subset_counts) == 1:
                subset_entropy = 0
                print(f"  H({value}) = 0 (rein)")
            else:
                subset_entropy = -sum((c/subset_size) * math.log2(c/subset_size) 
                                     for c in subset_counts)
                entropy_parts = []
                for cls, count in subset_counts.items():
                    p = count / subset_size
                    entropy_parts.append(f"-({count}/{subset_size})*log2({count}/{subset_size})")
                print(f"  H({value}) = {' + '.join(entropy_parts)}")
                print(f"  H({value}) = {subset_entropy:.4f}")
            
            weighted_entropy += weight * subset_entropy
            print(f"  Gewicht: {subset_size}/{total} = {weight:.4f}")
            print(f"  Beitrag: {weight:.4f} * {subset_entropy:.4f} = {weight * subset_entropy:.4f}\n")
        
        ig = total_entropy - weighted_entropy
        print(f"IG({feature}) = H(S) - Σ(|S_v|/|S|)*H(S_v)")
        print(f"IG({feature}) = {total_entropy:.4f} - {weighted_entropy:.4f}")
        print(f"IG({feature}) = {ig:.4f}")
        print("-"*70)
    
    print("\n" + "="*70)


# Numpy für Array-Operationen
import numpy as np


def main():
    """
    Hauptfunktion: Führt ID3 auf dem Wahlkampf-Datensatz aus
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
    
    # Berechnungsschritte anzeigen
    print_calculation_steps(data[['Alter', 'Einkommen', 'Bildung', 'Kandidat']], 'Kandidat')
    
    # ID3 ausführen
    print("\n" + "="*70)
    print("ID3 ENTSCHEIDUNGSBAUM")
    print("="*70)
    
    id3 = ID3DecisionTree()
    tree = id3.fit(data[['Alter', 'Einkommen', 'Bildung', 'Kandidat']], 'Kandidat')
    
    print("\n### RESULTIERENDER BAUM ###\n")
    id3.print_tree()
    
    # Test mit Trainingsbeispielen
    print("\n" + "="*70)
    print("KLASSIFIKATION DER TRAININGSBEISPIELE")
    print("="*70 + "\n")
    
    for idx, row in data.iterrows():
        prediction = id3.predict_sample(row)
        actual = row['Kandidat']
        match = "✓" if prediction == actual else "✗"
        print(f"Nr. {row['Nr']}: Vorhergesagt={prediction}, Tatsächlich={actual} {match}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()