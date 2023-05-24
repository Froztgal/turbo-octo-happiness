class NotValidAttributeForFiltering(Exception):
    def __init__(self, obj: object, attribute: str) -> None:
        super().__init__(
            f"No such attribute for filtering ({obj.__name__}.{attribute})."
        )


class NotValidAttributeForOrdering(Exception):
    def __init__(self, obj: object, attribute: str) -> None:
        super().__init__(
            f"No such attribute for ordering ({obj.__name__}.{attribute})."
        )
