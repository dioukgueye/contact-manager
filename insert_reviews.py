#Question 1: insertion de données dans Mongo
from pymongo import MongoClient

# Connexion à MongoDB
MONGO_URI = "mongodb+srv://gueye:Abdou2025@abdou.6xgcm.mongodb.net/"  # Remplacez par MON URI MongoDB Atlas 
client = MongoClient(MONGO_URI)

# Sélection de la base et de la collection
db = client["store_reviews"]  # Nom de la base de données
collection = db["reviews"]    # Nom de la collection

# Données des avis clients
Avis_clients = [
    {"client_id": "C001", "product_id": "P001", "rating": 5, "comment": "Excellent!", "date": "2024-01-01"},
    {"client_id": "C002", "product_id": "P002", "rating": 3, "comment": "Average product.", "date": "2024-01-02"},
    {"client_id": "C001", "product_id": "P003", "rating": 4, "comment": "Very good", "date": "2024-01-03"},
]

# Insérer les données dans MongoDB
try:
    result = collection.insert_many(Avis_clients)
    print(f"Documents insérés avec succès : {result.inserted_ids}")
except Exception as e:
    print("Erreur lors de l'insertion :", e)

# Question 2: extractions de données

from pymongo import MongoClient

# Connexion à MongoDB
MONGO_URI = "mongodb+srv://gueye:Abdou2025@abdou.6xgcm.mongodb.net/"  # Remplacez par votre URI MongoDB Atlas ou utilisez "mongodb://localhost:27017" pour un serveur local
client = MongoClient(MONGO_URI)

# Sélection de la base et de la collection
db = client["store_reviews"]  # Nom de la base de données
collection = db["reviews"]    # Nom de la collection

# Récupérer les données depuis MongoDB
try:
    # Extraire les documents de la collection
    documents = collection.find()
    
    # Convertir les documents en une liste de tuples
    list_of_tuples = [
        (doc["client_id"], doc["product_id"], doc["rating"], doc["comment"], doc["date"]) 
        for doc in documents
    ]
    
    # Afficher la liste des tuples
    print("Données récupérées sous forme de liste de tuples :")
    for record in list_of_tuples:
        print(record)

except Exception as e:
    print("Erreur lors de la récupération des données :", e)

# Question 3: Manipulation et analyse de données

from collections import defaultdict, Counter

# données récupérées depuis MongoDB sous forme de liste de dictionnaires
Avis_clients = [
    {"client_id": "C001", "product_id": "P001", "rating": 5, "comment": "Excellent!", "date": "2024-01-01"},
    {"client_id": "C002", "product_id": "P002", "rating": 3, "comment": "Average product.", "date": "2024-01-02"},
    {"client_id": "C001", "product_id": "P003", "rating": 4, "comment": "Very good", "date": "2024-01-03"},
    {"client_id": "C003", "product_id": "P001", "rating": 4, "comment": "Good value.", "date": "2024-01-04"},
    {"client_id": "C004", "product_id": "P003", "rating": 2, "comment": "Not satisfied.", "date": "2024-01-05"},
    {"client_id": "C001", "product_id": "P002", "rating": 5, "comment": "Great product!", "date": "2024-01-06"},
]

# 1. Trouver le produit avec la meilleure note moyenne
def best_product_by_rating(reviews):
    product_ratings = defaultdict(list)

    # Grouper les notes par produit
    for review in reviews:
        product_ratings[review["product_id"]].append(review["rating"])

    # Calculer la note moyenne pour chaque produit
    average_ratings = {product: sum(ratings) / len(ratings) for product, ratings in product_ratings.items()}

    # Trouver le produit avec la meilleure note moyenne
    best_product = max(average_ratings, key=average_ratings.get)
    print(f"Produit avec la meilleure note moyenne : {best_product} (Note moyenne : {average_ratings[best_product]:.2f})")

# 2. Trouver le client ayant laissé le plus d'avis
def most_active_client(reviews):
    client_count = Counter(review["client_id"] for review in reviews)

    # Trouver le client avec le plus grand nombre d'avis
    top_client = max(client_count, key=client_count.get)
    print(f"Client ayant laissé le plus d'avis : {top_client} ({client_count[top_client]} avis)")

# 3. Compter le nombre total d'avis par produit
def reviews_count_by_product(reviews):
    product_count = Counter(review["product_id"] for review in reviews)

    print("Nombre total d'avis par produit :")
    for product, count in product_count.items():
        print(f"  Produit {product} : {count} avis")

# Appeler les fonctions pour effectuer les analyses
best_product_by_rating(Avis_clients)
most_active_client(Avis_clients)
reviews_count_by_product(Avis_clients)

# question 4 visualiser les résultats dans un format lisible

from collections import defaultdict, Counter

# données récupérées depuis MongoDB sous forme de liste de dictionnaires
Avis_clients = [
    {"client_id": "C001", "product_id": "P001", "rating": 5, "comment": "Excellent!", "date": "2024-01-01"},
    {"client_id": "C002", "product_id": "P002", "rating": 3, "comment": "Average product.", "date": "2024-01-02"},
    {"client_id": "C001", "product_id": "P003", "rating": 4, "comment": "Very good", "date": "2024-01-03"},
    {"client_id": "C003", "product_id": "P001", "rating": 4, "comment": "Good value.", "date": "2024-01-04"},
    {"client_id": "C004", "product_id": "P003", "rating": 2, "comment": "Not satisfied.", "date": "2024-01-05"},
    {"client_id": "C001", "product_id": "P002", "rating": 5, "comment": "Great product!", "date": "2024-01-06"},
]

# 1. Trouver le produit avec la meilleure note moyenne
def best_product_by_rating(reviews):
    product_ratings = defaultdict(list)

    # Grouper les notes par produit
    for review in reviews:
        product_ratings[review["product_id"]].append(review["rating"])

    # Calculer la note moyenne pour chaque produit
    average_ratings = {product: sum(ratings) / len(ratings) for product, ratings in product_ratings.items()}

    # Trouver le produit avec la meilleure note moyenne
    best_product = max(average_ratings, key=average_ratings.get)
    best_rating = average_ratings[best_product]

    # Affichage formaté
    print(f"Le produit {best_product} a la meilleure note moyenne : {best_rating:.2f}.")

# 2. Trouver le client ayant laissé le plus d'avis
def most_active_client(reviews):
    client_count = Counter(review["client_id"] for review in reviews)

    # Trouver le client avec le plus grand nombre d'avis
    top_client = max(client_count, key=client_count.get)
    review_count = client_count[top_client]

    # Affichage formaté
    print(f"Le client {top_client} a laissé le plus d'avis : {review_count} avis.")

# 3. Compter le nombre total d'avis par produit
def reviews_count_by_product(reviews):
    product_count = Counter(review["product_id"] for review in reviews)

    # Affichage formaté
    print("Nombre total d'avis par produit :")
    for product, count in product_count.items():
        print(f"  - Produit {product} : {count} avis")

# Appeler les fonctions pour effectuer les analyses
print("=== Résultats des analyses ===")
best_product_by_rating(Avis_clients)
most_active_client(Avis_clients)
reviews_count_by_product(Avis_clients)
