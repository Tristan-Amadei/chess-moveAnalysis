# Chess - Move Analysis ♟️:desktop_computer:

Le but de ce projest est d'entrainer une petite IA à jouer aux échecs. L'idée est d'analyser une base de données de parties de Maitres, et créer une métrique pour chaque coup joué dans chaque partie.

## Téléchargement de la base de données

La base de données utilisée peut se trouver ici: https://www.kaggle.com/datasets/milesh1/35-million-chess-games (projet Kaggle), ou peut être téléchargée en cliquant sur ce [lien](https://minio.lab.sspcloud.fr/tamadei/chessDB/chessDB.txt). 
</br> Il faut ensuite nommer le fichier "chessDB.txt" et le placer dans le dossier Data. 

## Installation des dépendences

Le projet utilise plusieurs modules Python, pour les installer, utilisez la commande suivante: 
```sh
$ pip install -r requirements.txt
```

<!-- ## Ordre des Notebooks

- [Data cleaning et processing](#data-cleaning--processing)
  - [1. Clean_dataset](#1-Clean_datasetipynb)
  - [2. Create_metric_multithread](#2-Create_metric_multithreadipynb)
- [3. Data Visualisation](#Data-visualisation)
- [GUI](#Interface-graphique)
  - [4. GUI](#Test_moderne)
- [Machine Learning](#Machine-learning)
  - [5. Clustering](#5-Clusteringipynb)
  - [6. Prediction](#6-Predictionipynb)
  -->
## Data Cleaning / Processing
### 1. Clean_dataset.ipynb
La première étape ce de projet était de rendre utilisable la base de données. Le fichier de base ressemble à ceci: ![base_brute](/assets/images/chessDB.png)
</br> </br> Le premier notebook à utiliser est "Clean_datset.ipynb". Il sert surtout à nettoyer la base, c'est-à-dire enlever les donnes impropres et les features inutiles. Avec ce notebook, on crée un fichier csv, téléchargeable [ici](https://minio.lab.sspcloud.fr/tamadei/chessDB/clean_df.csv), qui correspond à cette base de données 'cleaned'. </br> Il faut placer ce ficher, nommé "clean_df.csv" directement dans le dossier Data. 

### 2. Create_metric_multithread.ipynb

Ce deuxième notebook reprend la base de données nettoyée, obtenue précédemment. Ici, on crée une base de données ou chaque ligne ne correspond non pas à une partie entière comme précédemment, mais simplement à un coup joué lors d'une partie. 
</br> En utilisant le moteur d'échecs [Stockfish](https://stockfishchess.org/), capable d'analyser une position d'échecs et lui donner une valeur, afin de créer notre propre métrique. Nous créons alors une base de données avec chaque coup joué lors des parties de notre base initiale, tous évalués par Stockfish. 
</br> Nous allons maintenant pouvoir travailler sur cette base de données : ![moves_df](/assets/images/moves_df.png)
</br> La base est disponible [ici](https://minio.lab.sspcloud.fr/tamadei/chessDB/moves_df.csv). Le fichier doit se nommer "moves_df" est doit être placé dans le dossier Data. 

## Data Visualisation

Le notebook "Data visualisation.ipynb" permet de faire des visualisations et des statistiques descriptives de nos données, afin de permettre de bien les comprendre et les prendre en main. 

## Interface Graphique
Le fichier GUI.py correspond au code permet de créer notre interface graphique, et l'autre fichier .py (Fonction_GUI.py) permet de stocker les méthodes utilisées pour afficher et jouer avec notre base de données, directement dans l'interface graphique. 
</br> ![gui](/assets/images/gui.png) </br>
Cela nous permet de bien visualiser nos données. Lors d'une partie, les cases en vert indiquent le dernier coup qui a été joué, et la flèche en rouge indique le coup qui était le meilleur à jouer. En effet, pour chaque coup de notre base de données, nous invoquons le moteur d'échecs Stockfish pour déterminer le meilleur coup de la position actuelle. Puis nous jouons ce coup sur l'échiquier, et on analyse la position après ce coup pour connaitre son évaluation. Enfin, nous enlevons ce coup et jouons le coup présent dans notre base; le but étant de comparer l'évolution de l'évaluation de la position de la partie dans notre base, avec l'évaluation si les coups joués sonjt toujours les meilleurs (c'est pourquoi l'affichage de chaque coup prend un peu de temps dans la GUI). 
</br> Sur l'interface, les graphes sur la gauche montrent l'évolution de l'évaluation et de la probabilité de gagner sur la partie entière, les graphes sur la droite montrent ces même valeurs mais seulement sur les 5 derniers coups, et permet aussi de comparer ces valeurs avec les valeurs optimales qui seraient obtenues en jouant les meilleurs coups. 
</br> Les boutons permettent de se déplacer dans une partie; et on peut choisir le numéro de la partie à afficher avec la barre en-dessous du bouton 'Mes Options' en y tapant un numéro de partie (entre 0 et 118318). 
</br> Le code étant parfois lourd dans les fichiers .py, nous avons repris les idées du code et les avons mises dans le notebook BrideData_GUI.ipynb, qui se veut plus simple à lire. 

## CNNs
Le but final était d'entrainer un CNN, prenant en entrée des matrices représentant les différentes positions de la base d'entrainement, avec les pièces one-hot encoded, afin qu'il soit capable d'évaluer une position quelconque. </br>
Ce problème est une régression sur les valeurs associées aux positions dans le training set. Comme nous utilisons des parties de Maitres, la majorité des positions dans la base sont des positions plus ou moins égales. Ainsi, nous utilisons une MSE modifiée, qui applique, sur les potentielles erreurs, une pénalisation de moins en moins forte plus l'évaluation réelle devient grande en valeur absolue. </br>
L'idée est, une fois le modèle entrainé, de pouvoir l'utiliser comme moteur d'échecs: sur une position donnée, on calcule tous les coups légaux que le joueur peut jouer, puis on utilise ce modèle pour évaluer la position atteinte après chaque coup potentiel, pour finalement jouer le coup le plus prometteur. 
