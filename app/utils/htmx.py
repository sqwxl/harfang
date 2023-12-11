def reselect(response, selector=None):
    if selector is None:
        selector = ""
    response["HX-Reselect"] = selector
    return response
