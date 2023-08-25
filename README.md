# README : Power Analysis Tool pour Cyclistes

## Explication scientifique des équations

La formule principale derrière cet outil est basée sur une combinaison de fonctions logarithmiques : 
f(x) = a/ln(x) + b * ln(x) + c

La combinaison d'une division par un logarithme et d'une multiplication par un logarithme crée un modèle qui peut décrire la manière dont la puissance d'un cycliste évolue pendant des efforts de différentes durées.

N.B : Cette equation est basée sur des observations de différents profils cyclistes sur différentes epreuves.

## Utilisation des scripts

### `auto.py`

Ce script est un analyseur en direct qui utilise la connectivité Bluetooth pour recevoir et traiter les données de puissance en temps réel.

#### Comment l'utiliser :

1. Assurez-vous que votre appareil Bluetooth est correctement configuré et jumelé avec la source de données.
2. Exécutez le script : 
python auto.py
3. Suivez les instructions à l'écran pour démarrer l'analyse en direct.

### `computation.py`

Ce script analyse les données de puissance à partir de fichiers `.gpx` ou `.tcx`.

#### Comment l'utiliser :

1. Préparez votre fichier `.gpx` ou `.tcx` contenant les données de puissance.
2. Exécutez le script en fournissant le fichier comme argument :
python computation.py chemin_vers_votre_fichier.gpx
3. Le script traitera les données et fournira une analyse détaillée basée sur la formule ci-dessus.

---

N'oubliez pas que ces interprétations sont basées sur les constantes fournies et les modèles mathématiques utilisés. Pour des analyses plus spécifiques ou adaptées, consultez un expert en physiologie de l'exercice ou un entraîneur cycliste professionnel.

By Gabriel Quint
