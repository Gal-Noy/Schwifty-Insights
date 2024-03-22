import os

from fastapi import HTTPException

page_size = int(os.getenv("PAGE_SIZE"))


def paginate_list(elements, page):
    """
    Paginate a list of elements
    :param elements:
    :param page:
    :return: List of elements paginated
    """
    if not page or page < 1:
        return HTTPException(status_code=404, detail="Invalid page number")
    if len(elements) <= page_size:
        return elements
    return {
        "page": f"{min(page, len(elements) // page_size + 1)} / {len(elements) // page_size + 1}",
        "data": elements[min(len(elements) - page_size, (page - 1) * page_size): min(len(elements), page * page_size)]
    }


def paginate_list_of_tuples(elements, page):
    """
    Paginate a list of tuples
    :param elements:
    :param page:
    :return: List of tuples paginated
    """
    if not page or page < 1:
        return HTTPException(status_code=404, detail="Invalid page number")

    total_items = sum([len(value) for key, value in elements])
    starting_index = min(total_items - page_size, (page - 1) * page_size)

    paginated_data = {}
    current_index, items_added = 0, 0
    for key, value in elements:
        for item in value:
            if current_index >= starting_index and items_added < page_size:
                if key not in paginated_data:
                    paginated_data[key] = []
                paginated_data[key].append(item)
                items_added += 1
            current_index += 1

    return {"page": f"{min(page, total_items // page_size + 1)} / {total_items // page_size + 1}",
            "data": paginated_data}
