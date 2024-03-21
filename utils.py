def paginate(elements, page):
    if page < 1:
        return {"error": "Invalid page number"}
    if len(elements) <= 20:
        return elements
    return elements[min(len(elements) - 20, (page - 1) * 20): min(len(elements), page * 20)]


relationship_levels = {
    1: "Very Close Relationship",
    2: "Close Relationship",
    3: "Strong Relationship",
    4: "Good Relationship",
    5: "Normal Relationship",
    6: "Fair Relationship",
    7: "Weak Relationship",
    8: "Poor Relationship",
    9: "Very Poor Relationship",
    10: "Farthest Relationship"
}
