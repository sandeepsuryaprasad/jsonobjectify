from json import dumps
from re import sub


class JsonObject:
    """Represent a JSON object as a Python object."""

    def __init__(self, info):
        self._info = info
        self._normalized_keys = {}
        for original_key, _ in self._info.items():
            self._normalized_keys[self._normalize_key(original_key)] = original_key

    def _normalize_key(self, original_key: str) -> str:
        """Normalize a JSON key for Python attribute access."""
        normalized_key = sub(r"[-\s.]+", "_", original_key)
        return normalized_key

    def __getattr__(self, name):
        """Return a value from the underlying JSON data using dot notation."""
        original_key = self._normalized_keys.get(name)
        if original_key is None:
            raise AttributeError(f"{type(self).__name__} has no attribute {name!r}") from None
        return self._info[original_key]

    def __setattr__(self, name, value):
        """Set an attribute (_info) or update the underlying JSON data."""
        if name in {"_info", "_normalized_keys"}:
            super().__setattr__(name, value)
        else:
            original_key = self._normalized_keys.get(name)
            if original_key is None:
                original_key = name
                self._normalized_keys[name] = original_key
            self._info[original_key] = value

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