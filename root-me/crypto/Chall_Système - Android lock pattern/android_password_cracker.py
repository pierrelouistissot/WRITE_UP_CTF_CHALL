# But du programme :
#   - Lire le fichier gesture.key (20 octets, SHA-1)
#   - Générer tous les motifs Android possibles (4 à 9 points)
#   - Pour chaque motif, calculer SHA-1(bytes(motif))
#   - Quand on trouve un motif qui donne le même hash que gesture.key,
#     on l'affiche.

import sys
from hashlib import sha1
from pathlib import Path

# -----------------------
# Règles du motif Android
# -----------------------
# On numérote les 9 points comme ça (0-based) :
#
#   0 1 2
#   3 4 5
#   6 7 8
#
# Certaines lignes passent par un point du milieu.
# Exemple : 0 -> 2 passe par 1.
# Si 1 n'a PAS déjà été utilisé, ce mouvement est interdit.

MIDDLE_POINTS = {
    (0, 2): 1, (2, 0): 1,
    (0, 6): 3, (6, 0): 3,
    (2, 8): 5, (8, 2): 5,
    (6, 8): 7, (8, 6): 7,
    (0, 8): 4, (8, 0): 4,
    (2, 6): 4, (6, 2): 4,
    (1, 7): 4, (7, 1): 4,
    (3, 5): 4, (5, 3): 4,
}

MIN_LENGTH = 4  # un motif Android doit avoir au moins 4 points
MAX_LENGTH = 9  # au maximum on peut utiliser tous les points

def move_is_allowed(last_point, next_point, used_points):
    """
    Vérifie si on a le droit d'aller de last_point vers next_point.

    - Si next_point a déjà été utilisé -> interdit.
    - Si la paire (last_point, next_point) a un "milieu" MIDDLE_POINTS[(last, next)] :
        - alors ce milieu doit déjà être dans used_points.
        - sinon, le mouvement est interdit.
    - Dans tous les autres cas -> mouvement autorisé.
    """
    if next_point in used_points:
        return False

    key = (last_point, next_point)
    if key in MIDDLE_POINTS:
        middle = MIDDLE_POINTS[key]
        if middle not in used_points:
            return False

    return True

def try_extend_pattern(current_pattern, used_points, target_hash):
    """
    current_pattern : liste d'indices (0..8) qui représente le motif en cours
    used_points     : ensemble des points déjà utilisés
    target_hash     : contenu de gesture.key (20 octets)

    Cette fonction essaie de continuer le motif en ajoutant un point,
    puis teste si le SHA-1 du motif correspond au target_hash.
    Elle renvoie :
      - le motif complet (liste d'indices) si on a trouvé,
      - None sinon.
    """

    # 1) Si la longueur est suffisante (>= MIN_LENGTH), on peut tester le hash
    if len(current_pattern) >= MIN_LENGTH:
        # On transforme la liste [1,4,5,2,...] en bytes(b'\x01\x04\x05\x02...')
        pattern_bytes = bytes(current_pattern)
        pattern_hash = sha1(pattern_bytes).digest()

        if pattern_hash == target_hash:
            # On a trouvé le bon motif !
            return current_pattern[:]  # on renvoie une copie de la liste

    # 2) Si on a déjà utilisé 9 points, on s'arrête (on ne peut pas ajouter plus)
    if len(current_pattern) == MAX_LENGTH:
        return None

    # 3) Sinon, on essaie d'ajouter un nouveau point (de 0 à 8)
    last_point = current_pattern[-1]

    for next_point in range(9):
        if move_is_allowed(last_point, next_point, used_points):
            # On ajoute ce point au motif
            used_points.add(next_point)
            current_pattern.append(next_point)

            # On continue récursivement
            result = try_extend_pattern(current_pattern, used_points, target_hash)
            if result is not None:
                return result  # on remonte la solution

            # Si ça n'a pas marché, on "annule" (backtrack)
            current_pattern.pop()
            used_points.remove(next_point)

    # Si on a testé tous les next_point possibles sans succès -> rien trouvé
    return None

def find_pattern(gesture_bytes):
    """
    Lance la recherche à partir de chaque point de départ possible (0 à 8).
    Renvoie :
      - le motif trouvé (liste 0-based) si succès
      - None sinon
    """
    if len(gesture_bytes) != 20:
        print("Erreur : gesture.key doit faire 20 octets (SHA-1).")
        return None

    # On essaie tous les points de départ possibles
    for start in range(9):
        current_pattern = [start]
        used_points = set([start])

        result = try_extend_pattern(current_pattern, used_points, gesture_bytes)
        if result is not None:
            return result

    return None

def main():
    # Vérification des arguments
    if len(sys.argv) != 2:
        print("Usage :")
        print("  ./find_gesture_simple.py /chemin/vers/gesture.key")
        sys.exit(1)

    gesture_path = Path(sys.argv[1])

    if not gesture_path.exists():
        print("Fichier introuvable :", gesture_path)
        sys.exit(1)

    # On lit le fichier gesture.key
    gesture_bytes = gesture_path.read_bytes()
    print("[*] gesture.key lu ({} octets)".format(len(gesture_bytes)))
    print("[*] Hex :", gesture_bytes.hex())

    # On cherche le motif
    pattern_0based = find_pattern(gesture_bytes)

    if pattern_0based is None:
        print("[-] Aucun motif valide trouvé.")
        sys.exit(1)

    # Conversion en version humaine (1-based)
    pattern_1based = [x + 1 for x in pattern_0based]
    pattern_str = ''.join(str(x) for x in pattern_1based)

    print("[+] Motif (0-based) :", pattern_0based)
    print("[+] Motif (1-based) :", pattern_1based)
    print("[+] Suite de chiffres :", pattern_str)

if __name__ == "__main__":
    main()
