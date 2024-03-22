def test_apply_kmeans():
    from utils.data_analysis import apply_kmeans
    import numpy as np
    matrix = np.array([[1, 2], [3, 4], [5, 6]])
    n_clusters = 2
    result = apply_kmeans(matrix, n_clusters)
    assert len(result) == 3


def test_sort_and_group_clusters():
    from utils.data_analysis import sort_and_group_clusters
    clusters = [(0, 1), (1, 0), (2, 1)]
    result = sort_and_group_clusters(clusters)
    assert len(result) == 2
    assert 0 in result
    assert 1 in result
    assert result[0] == [1]
    assert result[1] == [0, 2]


def test_counts_dict():
    from utils.data_analysis import counts_dict
    data = [{'a': 1}, {'a': 2}, {'a': 1}]
    key = 'a'
    result = counts_dict(data, key)
    assert len(result) == 2
    assert result[1] == 2
    assert result[2] == 1


def test_get_uniques():
    from utils.data_analysis import get_uniques
    data = [{'a': 1}, {'a': 2}, {'a': 1}]
    key = 'a'
    result = get_uniques(data, key)
    assert len(result) == 2
    assert 1 in result
    assert 2 in result
