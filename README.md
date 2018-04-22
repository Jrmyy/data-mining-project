# Prédictions des prix des logements en Californie

## Auteurs:

Solène Duchamp et Jérémy Guiselin

## La récupération des données:

La récupération des données se fait à l'aide d'un scrapper disponible dans le fichier `scrapper.py`. Ce fichier s'articule de la manière suivante:

- Tout d'abord, une première fonction va fetcher toutes les pages du site _www.apartments.com/ca_ afin de récupérer tous les liens vers les biens disponibles de la plateforme. Ces liens sont ensuite stockés au format texte. C'est la fonction `create_url_db`
- Ensuite, on va récupérer les données pour chaque lien. On va donc lire le fichier précédent, et pour chaque remplir des informations sur le nombre de chambres, le nombre de salle de bain, le prix, la suface, l'adresse, les équipements, la présence d'un parking, ... Chaque lien correspond à un lieu géographique pouvant contenir plusieurs logements. Ensuite, cette liste de dictionnaire est sauvegardée. C'est la fonction `create_dict_housing`
- Enfin, on va lire ce fichier pas encore nettoyé et extraire les caractéristiques de telle sorte que nos listes apparaissent comme différentes colonnes de type booléennes. Ce fichier est ensuite converti en `DataFrame` et stocké au format CSV. C'est la fonction `create_dataframe_with_features`
 
## La récupération des données GPS:

On a voulu travailler sur les données GPS et essayer de réaliser un clustering des logements pour décéler les quartiers huppés des quartiers plus modestes. Ayant donc les adresses grâce au scrapping, on a voulu convertir cela en coordonnées GPS. On a donc recensé les adresses distinctes du Dataframe, récupérer les coordonnées GPS en appelant l'API _Geolocalisation de Google Maps_. Une fois ceci fait, on a injecté les données dans le DataFrame et on a sauvegardé le résultat.

## Le clustering des appartements (voir notebook "Geo Clustering"):

On a voulu catégoriser les biens en clusters. On a donc, de manière intuitive commencer à classer les biens selon leur longitude et leur latitude. On a cherché à visualiser les données, et après avoir enlevé les points aberrants, on a réaliser un K-Means. En utilisant la méthode "elbow" on a pu déterminer le nombre optimal de cluster. Après avoir eu cette vue schématique, en deux dimensions, nous avons décidé de modifier nos données et d'ajouter en plus le loyer, afin d'estimer les quartiers huppés des quartiers plus abordables. On a réalisé le même processus. Cependant le résultat ne fut pas concluant et il fut difficile d'obtenir des zones claires représentant les différences de quartiers.
