from json import dumps


class JsonObject:
    """Represent a JSON object as a Python object."""
    def __init__(self, info):
        self._info = info

    def __getattr__(self, name):
        """Return a value from the underlying JSON data using dot notation."""
        try:
            return self._info[name]
        except KeyError:
            raise AttributeError(f"{type(self).__name__} has no attribute {name!r}") from None

    def __setattr__(self, name, value):
        """Set an attribute (_info) or update the underlying JSON data."""
        if name == "_info":
            super().__setattr__(name, value)
        else:
            self._info[name] = value

    def to_dict(self):
        """Convert a JsonObject to dictionary."""
        out_dict = {}
        for key, value in self._info.items():
            if isinstance(value, JsonObject):
                out_dict[key] = value.to_dict()
            elif isinstance(value, list):
                out_dict[key] = [
                    item.to_dict() if isinstance(item, JsonObject) else item
                    for item in value
                ]
            else:
                out_dict[key] = value
        return out_dict

    def to_json(self):
        """Convert JsonObject to a JSON string."""
        return dumps(self.to_dict())