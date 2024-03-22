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
    """
    Analyze the correlation between a character's species and their status.
    :return: List of species and their survival rates
    """
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


def native_species():
    """
    Estimate the native species of each location.
    :return: List of locations and their native species
    """
    characters = cache.get_all_characters()
    locations = cache.get_all_locations()
    species = list(set([character["species"] for character in characters]))

    # Create a matrix where each row is a location and each column is a species
    # The value is the number of characters of that species in that location
    matrix = np.zeros((len(locations), len(species)))
    for character in characters:
        c_origin = character["origin"]["url"].split("/")[-1]
        if c_origin != "":
            location_idx = [location["id"] for location in locations].index(int(c_origin))
            species_idx = species.index(character["species"])
            matrix[location_idx, species_idx] += 1

    # Find the most common species in each location
    native_species_list = []
    for i, location in enumerate(locations):
        native_species_idx = np.argmax(matrix[i])
        native_species_list.append((location["name"], species[native_species_idx]))

    return native_species_list


def dangerous_locations(danger_threshold: float = 0.75):
    """
    Analyze the correlation between a character's location and their status.
    Are there locations with higher mortality rates?
    :param danger_threshold:  Threshold for dangerous locations
    :return:  List of dangerous locations and their danger rates
    """
    characters = cache.get_all_characters()
    locations = cache.get_all_locations()
    statuses = list(set([character["status"] for character in characters]))

    # Create a matrix where each row is a location and each column is a status
    # The value is the number of characters with that status in that location
    matrix = np.zeros((len(locations), len(statuses)))
    for character in characters:
        c_location = character["location"]["url"].split("/")[-1]
        if c_location != "":
            location_idx = [location["id"] for location in locations].index(int(c_location))
            status_idx = statuses.index(character["status"])
            matrix[location_idx, status_idx] += 1

    # Find the most dangerous locations
    dangerous_locations_list = []
    dead_idx, unknown_idx = statuses.index("Dead"), statuses.index("unknown")
    for i, location in enumerate(locations):
        row_sum = np.sum(matrix[i])
        danger_rate = (matrix[i, dead_idx] + matrix[i, unknown_idx]) / row_sum if row_sum > 0 else 0
        if danger_rate >= danger_threshold:
            dangerous_locations_list.append((location["name"], danger_rate))

    return dangerous_locations_list


def dimension_species_diversity(n_clusters: int = 5):
    """
    List dimensions and the number of species that appear in each one.
    Are there dimensions with higher species diversity?
    :param n_clusters:  Number of diversity levels
    :return:  List of dimensions and their species diversity
    """
    characters = cache.get_all_characters()
    species = list(set([character["species"] for character in characters]))
    locations = cache.get_all_locations()
    dimensions = list(set([location["dimension"] for location in locations]))
    dimensions = [dimension for dimension in dimensions if dimension != "unknown"]

    # Create a matrix where each row is a dimension and each column is a species
    # The value is 1 if the species appears in that dimension, 0 otherwise
    matrix = np.zeros((len(dimensions), len(species)))
    for character in characters:
        c_location = character["location"]["url"].split("/")[-1]
        if c_location != "":
            location_idx = [location["id"] for location in locations].index(int(c_location))
            c_dimension = locations[location_idx]["dimension"]
            if c_dimension != "" and c_dimension != "unknown":
                dimension_idx = dimensions.index(c_dimension)
                species_idx = species.index(character["species"])
                matrix[dimension_idx, species_idx] = 1

    # Apply KMeans clustering to group dimensions
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(matrix)
    clusters = kmeans.predict(matrix)

    # Create a list of dimension Name and their corresponding clusters
    dimension_clusters = [(dimension, cluster_id) for dimension, cluster_id in zip(dimensions, clusters)]

    # Sort dimensions based on their clusters
    sorted_dimensions = sorted(dimension_clusters, key=lambda x: x[1])

    # Group dimensions by cluster
    dimension_species_diversity_groups = {}
    for dimension, cluster_id in sorted_dimensions:
        if cluster_id not in dimension_species_diversity_groups:
            dimension_species_diversity_groups[cluster_id] = []
        dimension_species_diversity_groups[cluster_id].append(dimension)

    # Sort clusters based on the average amount of species in each cluster
    clusters_avg_species_count = {}
    for cluster_id, dimensions in dimension_species_diversity_groups.items():
        avg_species_count = np.mean([np.sum(matrix[dimensions.index(dimension)]) for dimension in dimensions])
        clusters_avg_species_count[cluster_id] = avg_species_count

    return sorted(dimension_species_diversity_groups.items(),
                  key=lambda x: clusters_avg_species_count[x[0]])
