def paginate_list(elements, page):
    """
    Paginate a list of elements
    :param elements:
    :param page:
    :return:  List of elements paginated
    """
    if not page or page < 1:
        return {"error": "Invalid page number"}
    if len(elements) <= 20:
        return elements
    return {
        "page": f"{min(page, len(elements) // 20 + 1)} / {len(elements) // 20 + 1}",
        "data": elements[min(len(elements) - 20, (page - 1) * 20): min(len(elements), page * 20)]
    }


def paginate_list_of_tuples(elements, page):
    """
    Paginate a list of tuples
    :param elements:
    :param page:
    :return:  List of tuples paginated
    """
    if not page or page < 1:
        return {"error": "Invalid page number"}

    total_items = sum([len(value) for key, value in elements])
    starting_index = min(total_items - 20, (page - 1) * 20)

    paginated_data = {}
    current_index, items_added = 0, 0
    for key, value in elements:
        for item in value:
            if current_index >= starting_index and items_added < 20:
                if key not in paginated_data:
                    paginated_data[key] = []
                paginated_data[key].append(item)
                items_added += 1
            current_index += 1

    return {"page": f"{min(page, total_items // 20 + 1)} / {total_items // 20 + 1}",
            "data": paginated_data}
