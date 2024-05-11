class array():
    def __new__(cls, item):
        if isinstance(item, list):
            return item
        elif isinstance(item, str):
            return [item]
        else:
            return list(item)
