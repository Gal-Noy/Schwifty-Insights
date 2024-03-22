from sklearn.cluster import KMeans


def apply_kmeans(matrix, n_clusters):
    """
    Apply KMeans clustering to the data
    :param matrix: data matrix
    :param n_clusters: number of clusters
    :return: cluster labels
    """
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(matrix)
    return kmeans.predict(matrix)


def sort_and_group_clusters(clusters):
    """
    Sort and group the clusters
    :param clusters: cluster labels
    :return: sorted and grouped clusters
    """
    sorted_elements = sorted(clusters, key=lambda x: x[1])

    grouped_clusters = {}
    for i, cluster in sorted_elements:
        if cluster not in grouped_clusters:
            grouped_clusters[cluster] = []
        grouped_clusters[cluster].append(i)

    return grouped_clusters


def counts_dict(data, key):
    """
    Count the number of occurrences of each key in the data
    :param data: list of dictionaries
    :param key: key to count
    :return: dictionary with counts
    """
    counts = {}
    for item in data:
        value = item[key]
        if value not in counts:
            counts[value] = 0
        counts[value] += 1
    return counts


def get_uniques(data, key):
    """
    Get unique values of a key in a list of dictionaries
    :param data: list of dictionaries
    :param key: key to extract
    :return: unique values
    """
    return list(set([item[key] for item in data]))
