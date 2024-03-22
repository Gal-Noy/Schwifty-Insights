import data.cache as cache
import utils.data_analysis as data_analysis
import numpy as np


def characters_relationships(n_clusters: int = 10):
    """
    Estimate relationships between characters according to their appearances in the whole series.
    :param n_clusters: Number of clusters to group characters
    :return: Dictionary where keys are cluster IDs and values are lists of character IDs
    """
    characters = cache.get_all_characters()
    episodes = cache.get_all_episodes()

    # Create a matrix where each row is a character and each column is an episode
    # The value is 1 if the character appears in the episode, 0 otherwise
    matrix = np.array([[1 if str(character["id"]) in [character.split("/")[-1] for character in episode["characters"]]
                        else 0 for episode in episodes] for character in characters])

    clusters = data_analysis.apply_kmeans(matrix, n_clusters)

    # Create a list of character Name and their corresponding clusters
    character_clusters = [(character["name"], cluster_id) for character, cluster_id in zip(characters, clusters)]

    return data_analysis.sort_and_group_clusters(character_clusters)


def dimension_species_diversity(n_clusters: int = 5):
    """
    List dimensions and the number of species that appear in each one.
    Are there dimensions with higher species diversity?
    :param n_clusters: Number of diversity levels
    :return: List of dimensions and their species diversity
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

    clusters = data_analysis.apply_kmeans(matrix, n_clusters)

    # Create a list of dimension Name and their corresponding clusters
    dimension_clusters = [(dimension, cluster_id) for dimension, cluster_id in zip(dimensions, clusters)]

    # Group dimensions based on the species diversity in each cluster
    dimension_species_diversity_groups = data_analysis.sort_and_group_clusters(dimension_clusters)

    # Sort clusters based on the average amount of species in each cluster
    clusters_avg_species_count = {}
    for cluster_id, dimensions in dimension_species_diversity_groups.items():
        avg_species_count = np.mean([np.sum(matrix[dimensions.index(dimension)]) for dimension in dimensions])
        clusters_avg_species_count[cluster_id] = avg_species_count

    return sorted(dimension_species_diversity_groups.items(),
                  key=lambda x: clusters_avg_species_count[x[0]])


def dangerous_locations(danger_threshold: float = 0.75):
    """
    Analyze the correlation between a character's location and their status.
    Are there locations with higher mortality rates?
    :param danger_threshold:  Threshold for dangerous locations
    :return:  List of dangerous locations and their danger rates
    """
    characters = cache.get_all_characters()
    locations = cache.get_all_locations()
    statuses = data_analysis.get_uniques(characters, "status")

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


def species_survival():
    """
    Analyze the correlation between a character's species and their status.
    :return: List of species and their survival rates
    """
    characters = cache.get_all_characters()
    species_counts = data_analysis.counts_dict(characters, "species")
    status_counts = data_analysis.counts_dict(characters, "status")

    # Create a matrix where each row is a species and each column is a status
    # The value is the number of characters with that status in that species
    matrix = np.zeros((len(species_counts), len(status_counts)))
    for i, (species, species_count) in enumerate(species_counts.items()):
        for j, (status, status_count) in enumerate(status_counts.items()):
            matrix[i, j] = len([character for character in characters
                                if character["species"] == species and character["status"] == status])

    # Calculate the survival rate for each species
    species_survival_rates = {}
    for i, species in enumerate(species_counts.keys()):
        survival_rate = matrix[i, 0] / np.sum(matrix[i])
        species_survival_rates[species] = survival_rate

    return {f"{species} ({species_counts[species]})": survival_rate
            for species, survival_rate in species_survival_rates.items()}


def gender_by_location_type():
    """
    Analyze the correlation between a character's gender and their location type.
    :return: List of locations types and their most common gender
    """
    characters = cache.get_all_characters()
    locations = cache.get_all_locations()
    genders = data_analysis.get_uniques(characters, "gender")
    location_types = data_analysis.get_uniques(locations, "type")
    location_types = [location_type for location_type in location_types if location_type != ""]

    # Create a matrix where each row is a location type and each column is a gender
    # The value is the number of characters of that gender in this location type
    matrix = np.zeros((len(location_types), len(genders)))
    for character in characters:
        c_location = character["location"]["url"].split("/")[-1]
        if c_location != "":
            location_idx = [location["id"] for location in locations].index(int(c_location))
            gender_idx = genders.index(character["gender"])
            location_type = locations[location_idx]["type"]
            if location_type != "":
                location_type_idx = location_types.index(location_type)
                matrix[location_type_idx, gender_idx] += 1

    # Find the most common gender in each location type
    gender_by_location_type_list = []
    for i, location_type in enumerate(location_types):
        most_common_gender_idx = np.argmax(matrix[i])
        gender_by_location_type_list.append((location_type, genders[most_common_gender_idx]))

    return gender_by_location_type_list


def native_species():
    """
    Estimate the native species of each location.
    :return: List of locations and their native species
    """
    characters = cache.get_all_characters()
    locations = cache.get_all_locations()
    species = data_analysis.get_uniques(characters, "species")

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


def frequent_travelers():
    """
    Report characters which change locations frequently.
    :return:  List of characters who change locations frequently
    """
    return [character["name"] for character in cache.get_all_characters()
            if character["location"]["name"] != character["origin"]["name"]]
