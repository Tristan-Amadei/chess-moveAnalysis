# chess-moveAnalysis

Le but de ce projest est d'entrainer une petite IA à jouer aux échecs. L'idée est d'analyser une base de données de parties de Maitres, et créer une métrique pour chaque coup joué dans chaque partie.

## Téléchargement de la base de données

La base de données utilisée peut se trouver ici: https://www.kaggle.com/datasets/milesh1/35-million-chess-games (projet Kaggle), ou peut être téléchargée en cliquant sur ce [lien](https://minio.lab.sspcloud.fr/tamadei/chessDB/chessDB.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=49336FAAB9232PUJR6RC%2F20221210%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20221210T165121Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI0OTMzNkZBQUI5MjMyUFVKUjZSQyIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNjcwNjkwNDE4LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6InRyaXN0YW4uYW1hZGVpQGVuc2FlLmZyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTY3MDc3NjgyMCwiZmFtaWx5X25hbWUiOiJBbWFkZWkiLCJnaXZlbl9uYW1lIjoiVHJpc3RhbiIsImdyb3VwcyI6W10sImlhdCI6MTY3MDY5MDQxOSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6IjMyMzc4ZWQ0LTAwNzAtNGNhZi04MTUwLWQwYTZmZTZjZjY4ZiIsIm5hbWUiOiJUcmlzdGFuIEFtYWRlaSIsIm5vbmNlIjoiZDkzNjc2ZmYtZTI0Zi00YzY3LTk0Y2EtYTRkZTEyOTY0ZDAxIiwicG9saWN5Ijoic3Rzb25seSIsInByZWZlcnJlZF91c2VybmFtZSI6InRhbWFkZWkiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGdyb3VwcyBlbWFpbCIsInNlc3Npb25fc3RhdGUiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzaWQiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzdWIiOiJhNzI5NmYwOC1lZjBlLTRjNGQtODllNy1lYjRmYTY4YmM5MTEiLCJ0eXAiOiJCZWFyZXIifQ.y7-CSjBQx6LtmOn9-_DBa_T3kFvfACc7GscXb-W7gvDA_RkRue19POVfEoxKmrvFGCvdG-Z2G0evY8yvRn-Jpg&X-Amz-Signature=882fb03443a70e85d7a651c63f7b66220d8df1d0218c8fe8393fa7e046348c0c&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI0OTMzNkZBQUI5MjMyUFVKUjZSQyIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNjcwNjkwNDE4LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6InRyaXN0YW4uYW1hZGVpQGVuc2FlLmZyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTY3MDc3NjgyMCwiZmFtaWx5X25hbWUiOiJBbWFkZWkiLCJnaXZlbl9uYW1lIjoiVHJpc3RhbiIsImdyb3VwcyI6W10sImlhdCI6MTY3MDY5MDQxOSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6IjMyMzc4ZWQ0LTAwNzAtNGNhZi04MTUwLWQwYTZmZTZjZjY4ZiIsIm5hbWUiOiJUcmlzdGFuIEFtYWRlaSIsIm5vbmNlIjoiZDkzNjc2ZmYtZTI0Zi00YzY3LTk0Y2EtYTRkZTEyOTY0ZDAxIiwicG9saWN5Ijoic3Rzb25seSIsInByZWZlcnJlZF91c2VybmFtZSI6InRhbWFkZWkiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGdyb3VwcyBlbWFpbCIsInNlc3Npb25fc3RhdGUiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzaWQiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzdWIiOiJhNzI5NmYwOC1lZjBlLTRjNGQtODllNy1lYjRmYTY4YmM5MTEiLCJ0eXAiOiJCZWFyZXIifQ.y7-CSjBQx6LtmOn9-_DBa_T3kFvfACc7GscXb-W7gvDA_RkRue19POVfEoxKmrvFGCvdG-Z2G0evY8yvRn-Jpg). 
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
  - [4. Test_moderne](#Test_moderne)
- [Machine Learning](#Machine-learning)
  - [5. Clustering](#5-Clusteringipynb)
  - [6. Prediction](#6-Predictionipynb)
  
## Data Cleaning / Processing
### 1. Clean_dataset.ipynb
La première étape ce de projet était de rendre utilisable la base de données. Le fichier de base ressemble à ceci: ![base_brute](/assets/images/chessDB.png)
</br> </br> Le premier notebook à utiliser est "Clean_datset.ipynb". Il sert surtout à nettoyer la base, c'est-à-dire enlever les donnes impropres et les features inutiles. Avec ce notebook, on crée un fichier csv, téléchargeable [ici](https://minio.lab.sspcloud.fr/tamadei/chessDB/clean_df.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=49336FAAB9232PUJR6RC%2F20221210%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20221210T173616Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI0OTMzNkZBQUI5MjMyUFVKUjZSQyIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNjcwNjkwNDE4LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6InRyaXN0YW4uYW1hZGVpQGVuc2FlLmZyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTY3MDc3NjgyMCwiZmFtaWx5X25hbWUiOiJBbWFkZWkiLCJnaXZlbl9uYW1lIjoiVHJpc3RhbiIsImdyb3VwcyI6W10sImlhdCI6MTY3MDY5MDQxOSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6IjMyMzc4ZWQ0LTAwNzAtNGNhZi04MTUwLWQwYTZmZTZjZjY4ZiIsIm5hbWUiOiJUcmlzdGFuIEFtYWRlaSIsIm5vbmNlIjoiZDkzNjc2ZmYtZTI0Zi00YzY3LTk0Y2EtYTRkZTEyOTY0ZDAxIiwicG9saWN5Ijoic3Rzb25seSIsInByZWZlcnJlZF91c2VybmFtZSI6InRhbWFkZWkiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGdyb3VwcyBlbWFpbCIsInNlc3Npb25fc3RhdGUiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzaWQiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzdWIiOiJhNzI5NmYwOC1lZjBlLTRjNGQtODllNy1lYjRmYTY4YmM5MTEiLCJ0eXAiOiJCZWFyZXIifQ.y7-CSjBQx6LtmOn9-_DBa_T3kFvfACc7GscXb-W7gvDA_RkRue19POVfEoxKmrvFGCvdG-Z2G0evY8yvRn-Jpg&X-Amz-Signature=fd9310068bd1ecb5290750ef58e296b1ff4a5fb6279dddf088dbdcf22c14939e&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI0OTMzNkZBQUI5MjMyUFVKUjZSQyIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNjcwNjkwNDE4LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6InRyaXN0YW4uYW1hZGVpQGVuc2FlLmZyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTY3MDc3NjgyMCwiZmFtaWx5X25hbWUiOiJBbWFkZWkiLCJnaXZlbl9uYW1lIjoiVHJpc3RhbiIsImdyb3VwcyI6W10sImlhdCI6MTY3MDY5MDQxOSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6IjMyMzc4ZWQ0LTAwNzAtNGNhZi04MTUwLWQwYTZmZTZjZjY4ZiIsIm5hbWUiOiJUcmlzdGFuIEFtYWRlaSIsIm5vbmNlIjoiZDkzNjc2ZmYtZTI0Zi00YzY3LTk0Y2EtYTRkZTEyOTY0ZDAxIiwicG9saWN5Ijoic3Rzb25seSIsInByZWZlcnJlZF91c2VybmFtZSI6InRhbWFkZWkiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGdyb3VwcyBlbWFpbCIsInNlc3Npb25fc3RhdGUiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzaWQiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzdWIiOiJhNzI5NmYwOC1lZjBlLTRjNGQtODllNy1lYjRmYTY4YmM5MTEiLCJ0eXAiOiJCZWFyZXIifQ.y7-CSjBQx6LtmOn9-_DBa_T3kFvfACc7GscXb-W7gvDA_RkRue19POVfEoxKmrvFGCvdG-Z2G0evY8yvRn-Jpg), qui correspond à cette base de données 'cleaned'. </br> Il faut placer ce ficher, nommé "clean_df.csv" directement dans le dossier Data. 

### 2. Create_metric_multithread.ipynb

Ce deuxième notebook reprend la base de données nettoyée, obtenue précédemment. Ici, on crée une base de données ou chaque ligne ne correspond non pas à une partie entière comme précédemment, mais simplement à un coup joué lors d'une partie. 
</br> En utilisant le moteur d'échecs [Stockfish](https://stockfishchess.org/), capable d'analyser une position d'échecs et lui donner une valeur, afin de créer notre propre métrique. Nous créons alors une base de données avec chaque coup joué lors des parties de notre base initiale, tous évalués par Stockfish. 
</br> Nous allons maintenant pouvoir travailler sur cette base de données : ![moves_df](/assets/images/moves_df.png)
</br> La base est disponible [ici](https://minio.lab.sspcloud.fr/tamadei/chessDB/moves_df.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=49336FAAB9232PUJR6RC%2F20221210%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20221210T175039Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI0OTMzNkZBQUI5MjMyUFVKUjZSQyIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNjcwNjkwNDE4LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6InRyaXN0YW4uYW1hZGVpQGVuc2FlLmZyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTY3MDc3NjgyMCwiZmFtaWx5X25hbWUiOiJBbWFkZWkiLCJnaXZlbl9uYW1lIjoiVHJpc3RhbiIsImdyb3VwcyI6W10sImlhdCI6MTY3MDY5MDQxOSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6IjMyMzc4ZWQ0LTAwNzAtNGNhZi04MTUwLWQwYTZmZTZjZjY4ZiIsIm5hbWUiOiJUcmlzdGFuIEFtYWRlaSIsIm5vbmNlIjoiZDkzNjc2ZmYtZTI0Zi00YzY3LTk0Y2EtYTRkZTEyOTY0ZDAxIiwicG9saWN5Ijoic3Rzb25seSIsInByZWZlcnJlZF91c2VybmFtZSI6InRhbWFkZWkiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGdyb3VwcyBlbWFpbCIsInNlc3Npb25fc3RhdGUiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzaWQiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzdWIiOiJhNzI5NmYwOC1lZjBlLTRjNGQtODllNy1lYjRmYTY4YmM5MTEiLCJ0eXAiOiJCZWFyZXIifQ.y7-CSjBQx6LtmOn9-_DBa_T3kFvfACc7GscXb-W7gvDA_RkRue19POVfEoxKmrvFGCvdG-Z2G0evY8yvRn-Jpg&X-Amz-Signature=dda4a283854be65eb81106f57c2d5321c45c56c884adb238af03ece05a43da0b&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI0OTMzNkZBQUI5MjMyUFVKUjZSQyIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNjcwNjkwNDE4LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6InRyaXN0YW4uYW1hZGVpQGVuc2FlLmZyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTY3MDc3NjgyMCwiZmFtaWx5X25hbWUiOiJBbWFkZWkiLCJnaXZlbl9uYW1lIjoiVHJpc3RhbiIsImdyb3VwcyI6W10sImlhdCI6MTY3MDY5MDQxOSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6IjMyMzc4ZWQ0LTAwNzAtNGNhZi04MTUwLWQwYTZmZTZjZjY4ZiIsIm5hbWUiOiJUcmlzdGFuIEFtYWRlaSIsIm5vbmNlIjoiZDkzNjc2ZmYtZTI0Zi00YzY3LTk0Y2EtYTRkZTEyOTY0ZDAxIiwicG9saWN5Ijoic3Rzb25seSIsInByZWZlcnJlZF91c2VybmFtZSI6InRhbWFkZWkiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGdyb3VwcyBlbWFpbCIsInNlc3Npb25fc3RhdGUiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzaWQiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzdWIiOiJhNzI5NmYwOC1lZjBlLTRjNGQtODllNy1lYjRmYTY4YmM5MTEiLCJ0eXAiOiJCZWFyZXIifQ.y7-CSjBQx6LtmOn9-_DBa_T3kFvfACc7GscXb-W7gvDA_RkRue19POVfEoxKmrvFGCvdG-Z2G0evY8yvRn-Jpg). Le fichier doit se nommer "moves_df" est doit être placé dans le dossier Data. 

## Data Visualisation

## Interface Graphique

## Machine Learning
Le but ici est d'utiliser notre base afin d'entrainer des algorithmes de ML à déterminer la qualité d'un coup sur une position donnée. 
</br> L'idée serait alors d'avoir une IA qui peut jouer aux échecs: pour jouer, elle détermine tous les coups jouables sur une position, les analyse tous avec ce qu'elle a appris de son entrainement et sélectionne celui qu'elle juge le meilleur. 

### 5. Clustering.ipynb
Nous voulons créer des algorithmes de classification de coups d'échecs. Nous devons donc créer nos classes; pour cela nous entrainons un K-Means pour créer nos clusters de coups d'échecs, qui deviendrons les classes que nous chercherons à predire à l'étape suivante. Le notebook utilisé ici est "Clustering.ipynb". 
</br> On sauvegarde ces classes dans une nouvelle [base](https://minio.lab.sspcloud.fr/tamadei/chessDB/full_moves_df.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=49336FAAB9232PUJR6RC%2F20221210%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20221210T181120Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI0OTMzNkZBQUI5MjMyUFVKUjZSQyIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNjcwNjkwNDE4LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6InRyaXN0YW4uYW1hZGVpQGVuc2FlLmZyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTY3MDc3NjgyMCwiZmFtaWx5X25hbWUiOiJBbWFkZWkiLCJnaXZlbl9uYW1lIjoiVHJpc3RhbiIsImdyb3VwcyI6W10sImlhdCI6MTY3MDY5MDQxOSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6IjMyMzc4ZWQ0LTAwNzAtNGNhZi04MTUwLWQwYTZmZTZjZjY4ZiIsIm5hbWUiOiJUcmlzdGFuIEFtYWRlaSIsIm5vbmNlIjoiZDkzNjc2ZmYtZTI0Zi00YzY3LTk0Y2EtYTRkZTEyOTY0ZDAxIiwicG9saWN5Ijoic3Rzb25seSIsInByZWZlcnJlZF91c2VybmFtZSI6InRhbWFkZWkiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGdyb3VwcyBlbWFpbCIsInNlc3Npb25fc3RhdGUiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzaWQiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzdWIiOiJhNzI5NmYwOC1lZjBlLTRjNGQtODllNy1lYjRmYTY4YmM5MTEiLCJ0eXAiOiJCZWFyZXIifQ.y7-CSjBQx6LtmOn9-_DBa_T3kFvfACc7GscXb-W7gvDA_RkRue19POVfEoxKmrvFGCvdG-Z2G0evY8yvRn-Jpg&X-Amz-Signature=bd713d06593c7c0d9d989c6ad1eb7794a49668327ac089f3e494396887c10f7c&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI0OTMzNkZBQUI5MjMyUFVKUjZSQyIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNjcwNjkwNDE4LCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6InRyaXN0YW4uYW1hZGVpQGVuc2FlLmZyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTY3MDc3NjgyMCwiZmFtaWx5X25hbWUiOiJBbWFkZWkiLCJnaXZlbl9uYW1lIjoiVHJpc3RhbiIsImdyb3VwcyI6W10sImlhdCI6MTY3MDY5MDQxOSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6IjMyMzc4ZWQ0LTAwNzAtNGNhZi04MTUwLWQwYTZmZTZjZjY4ZiIsIm5hbWUiOiJUcmlzdGFuIEFtYWRlaSIsIm5vbmNlIjoiZDkzNjc2ZmYtZTI0Zi00YzY3LTk0Y2EtYTRkZTEyOTY0ZDAxIiwicG9saWN5Ijoic3Rzb25seSIsInByZWZlcnJlZF91c2VybmFtZSI6InRhbWFkZWkiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGdyb3VwcyBlbWFpbCIsInNlc3Npb25fc3RhdGUiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzaWQiOiIzZjgwM2YzNi04NGM2LTQyZDEtYmI5Zi1jNjlkZDI3MWI2NDQiLCJzdWIiOiJhNzI5NmYwOC1lZjBlLTRjNGQtODllNy1lYjRmYTY4YmM5MTEiLCJ0eXAiOiJCZWFyZXIifQ.y7-CSjBQx6LtmOn9-_DBa_T3kFvfACc7GscXb-W7gvDA_RkRue19POVfEoxKmrvFGCvdG-Z2G0evY8yvRn-Jpg), qui est la concatenation de la base précédente, moves_df, et des classes créées par K-Means. 
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

