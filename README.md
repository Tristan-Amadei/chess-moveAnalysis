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

## Ordre des Notebooks

- [Data cleaning et processing](#data-cleaning--processing)
  - [1. Clean_dataset](#1-Clean_datasetipynb)
  - [2. Create_metric_multithread](#2-Create_metric_multithreadipynb)
- [3. Data Visualisation](#Data-visualisation)
- [GUI](#Interface-graphique)
  - [4. GUI](#Test_moderne)
- [Machine Learning](#Machine-learning)
  - [5. Clustering](#5-Clusteringipynb)
  - [6. Prediction](#6-Predictionipynb)
  
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
</br> Le code étant parfois lourd dans les fichiers .py, nous avons repris les idées du code et les avons mises dans le notebook BrideData_GUI.ipynb, qui se veut plus simple à lire. 

## Machine Learning
Le but ici est d'utiliser notre base afin d'entrainer des algorithmes de ML à déterminer la qualité d'un coup sur une position donnée. 
</br> L'idée serait alors d'avoir une IA qui peut jouer aux échecs: pour jouer, elle détermine tous les coups jouables sur une position, les analyse tous avec ce qu'elle a appris de son entrainement et sélectionne celui qu'elle juge le meilleur. 

### 5. Clustering.ipynb
Nous voulons créer des algorithmes de classification de coups d'échecs. Nous devons donc créer nos classes; pour cela nous entrainons un K-Means pour créer nos clusters de coups d'échecs, qui deviendrons les classes que nous chercherons à predire à l'étape suivante. Le notebook utilisé ici est "Clustering.ipynb". 
</br> On sauvegarde ces classes dans une nouvelle base, qui est la concatenation de la base précédente, moves_df, et des classes créées par K-Means. Elle est constuite dans le notebook, mais vous pouvez également la télécharger [ici](https://minio.lab.sspcloud.fr/tamadei/chessDB/full_moves_df.csv). 
</br> De nouveau, cette base, nommée "full_moves_df.csv", soit être placée dans le dossier Data. 
</br>Chaque classe correspond à un type de coup, déterminé par l'algorithme K-Means. Cependant, aux échecs, la majorité des coups sont "standards", ainsi le set déterminé par K-Means est très déséquilibré : ![clusters_breakdown](/assets/images/clusters_breakdown.png)

### 6. Prediction.ipynb

Il est enfin temps de passer à la prédiction ! On se place ici dans le notebook "Prediction.ipynb", et on reprend les résultats du K-Means précédent. 
</br> On va tester plusieurs façons de travailler avec nos données : 
    </br> - Random Forest
    </br> - Under-Sampling
    </br> - Balanced Random Forest
    </br> - Neural Network
    
</br></br> Cependant, notre set de données est trop déséquilibré, et de plus, il faudrait travailler avec une représentation complète de l'échiquier pour faire apprendre quelque chose à nos algorithmes. 
</br> Voici certains de nos résultats après entrainement d'un réseau de neurones sur nos data: 
![nn](/assets/images/nn.png)
</br>
</br> D'après nos recherches, dont ce [papier](http://cs231n.stanford.edu/reports/2015/pdfs/ConvChess.pdf) de Stanford, il faudrait travailler avec des réseaux de neurones convolutionnels, prenant en entrée soit une image d'un échiquier soit une matrice 8x8 représentant la position actuelle de la partie d'échecs. 

