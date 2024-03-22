import data.cache as cache
from sklearn.cluster import KMeans
import numpy as np


# Unsupervised - we don't have labels for relationships between characters
# We can use clustering algorithms to group characters based on their appearances in same episodes
def estimate_relationships(n_clusters: int = 10):
    """
    Estimate relationships between characters according to their appearances in the whole series.
    :param n_clusters:  Number of clusters to group characters
    :return:  Dictionary where keys are cluster IDs and values are lists of character IDs
    """
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


def species_survival():
    species_counts, status_counts = {}, {}
    characters = cache.get_all_characters()

    for character in characters:
        species = character["species"]
        status = character["status"]

        if species not in species_counts:
            species_counts[species] = 0
        species_counts[species] += 1

        if status not in status_counts:
            status_counts[status] = 0
        status_counts[status] += 1

    matrix = np.zeros((len(species_counts), len(status_counts)))
    for i, (species, species_count) in enumerate(species_counts.items()):
        for j, (status, status_count) in enumerate(status_counts.items()):
            matrix[i, j] = len([character for character in characters
                                if character["species"] == species and character["status"] == status])

    species_survival_rates = {}
    for i, species in enumerate(species_counts.keys()):
        survival_rate = matrix[i, 0] / np.sum(matrix[i])
        species_survival_rates[species] = survival_rate

    return {f"{species} ({species_counts[species]})": survival_rate
            for species, survival_rate in species_survival_rates.items()}
