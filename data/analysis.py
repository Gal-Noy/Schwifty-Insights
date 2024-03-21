import data.cache as cache
from sklearn.cluster import KMeans
import numpy as np


# Unsupervised - we don't have labels for relationships between characters
# We can use clustering algorithms to group characters based on their appearances in same episodes
def estimate_relationships(n_clusters: int = 10):
    characters = cache.get_all_characters()
    episodes = cache.get_all_episodes()

    # Create a matrix where each row is a character and each column is an episode
    # The value is 1 if the character appears in the episode, 0 otherwise
    matrix = np.array([[1 if str(character["id"]) in [character.split("/")[-1] for character in episode["characters"]]
                        else 0 for episode in episodes] for character in characters])

    # Apply KMeans clustering to group characters
    kmeans = KMeans(n_clusters=n_clusters)  # 10 levels of relationships
    kmeans.fit(matrix)
    clusters = kmeans.predict(matrix)

    # Create a list of character Name and their corresponding clusters
    character_clusters = [(character["name"], cluster_id) for character, cluster_id in zip(characters, clusters)]

    # Sort characters based on their clusters
    sorted_characters = sorted(character_clusters, key=lambda x: x[1])

    # Group characters by cluster
    character_relationships_groups = {}
    for character_id, cluster_id in sorted_characters:
        if cluster_id not in character_relationships_groups:
            character_relationships_groups[cluster_id] = []
        character_relationships_groups[cluster_id].append(character_id)

    return character_relationships_groups

