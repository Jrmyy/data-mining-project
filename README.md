# Prédictions des prix des logements en Californie

## Auteurs:

Solène Duchamp et Jérémy Guiselin

## La récupération des données:

La récupération des données se fait à l'aide d'un scrapper disponible dans le fichier `scrapper.py`. Ce fichier s'articule de la manière suivante:

- Tout d'abord, une première fonction va boucler sur toutes les pages du site _www.apartments.com/ca_ afin de récupérer tous les liens vers les biens disponibles de la plateforme. Ces liens sont ensuite stockés au format texte. C'est la fonction `create_url_db`
- Ensuite, nous avons récupéré les données pour chaque lien. Nous avons donc lu le fichier précédent, et pour chaque lien, récupéré des informations sur le nombre de chambres, le nombre de salle de bain, le prix, la suface, l'adresse, les équipements, la présence d'un parking, ... Chaque lien correspond à un lieu géographique pouvant contenir plusieurs logements. Ensuite, cette liste de dictionnaire est sauvegardée. C'est la fonction `create_dict_housing`
- Enfin, nous avons lu ce fichier encore brut et extraire les caractéristiques de telle sorte que nos listes apparaissent comme différentes colonnes de type booléennes. Ce fichier est ensuite converti en `DataFrame` et stocké au format CSV. C'est la fonction `create_dataframe_with_features`
 
## La récupération des données GPS:

Nous avons voulu travailler sur les données GPS et essayer de réaliser un clustering des logements pour décéler les quartiers huppés des quartiers plus modestes. Ayant donc les adresses grâce au scrapping, notre but était de convertir ces adresses en coordonnées GPS. En recensant les adresses distinctes du Dataframe, nous avons récupéré les coordonnées GPS en appelant l'API _Geolocalisation de Google Maps_. Une fois ceci fait, les données ont été ajoutées au dataframe initial et sauvegardées. Tout ceci se trouver dans le fichier `fetch_geo.py`

## Le clustering des appartements (voir notebook "Geo Clustering"):

Afin de classer les biens en cluster nous avons procédé en plusieurs étapes. Tout d'abord, nous avons, de manière intuitive, commencé à classer les biens selon leur longitude et leur latitude. La visualisation des données nous a montré des points abérrants qui, une fois supprimés, nous a permis de réaliser un K-Means. En utilisant la méthode "elbow", on a pu déterminer le nombre optimal de cluster. Après avoir eu cette vue schématique en deux dimensions, nous avons décidé de modifier nos données et d'ajouter en plus le loyer, afin d'estimer les quartiers huppés des quartiers plus abordables. Le même processus a été réalisé, cependant le résultat ne fut pas concluant et il fut difficile d'obtenir des zones claires représentant les différences de quartiers.

Nous avons donc décidé d'abandonner cette étude pour deux raisons principales:

- Comme nous le verrons par la suite, l'ajout de la localisation n'apporte pas plus de précision, elle n'est donc pas un critère déterminant
- Une méthode à laquelle nous avions pensé, et qui suggérait de créer des grilles et de réaliser des algorithmes locaux pour déterminer des caractéristiques de quartier nous a paru fastidieuse et non prioritaire.

## La prédiction des loyers:

Pour réaliser la prédiction des loyers, nous nous sommes appuyés sur 4 algorithmes que nous avons comparé:

- Naives Bayes
- Random Forest
- Support Vector Machine
- Gradient Boosting
