def paginate(elements, page):
    if page < 1 or page > 20:
        return {"error": "Invalid page number"}
    if len(elements) <= 20:
        return elements
    return elements[min(len(elements) - 20, (page - 1) * 20): min(len(elements), page * 20)]
