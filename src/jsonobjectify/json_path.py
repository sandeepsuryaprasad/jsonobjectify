from json import load, loads
from pathlib import Path
from .json_object import JsonObject


class JsonPath:
    def __init__(self):
        """Initialize an empty JSON parser."""
        self._root_json_object = None

    def __getattr__(self, name):
        """Delegate attribute access to the json object."""
        return getattr(self._root_json_object, name)

    def __getitem__(self, index):
        """Return an item from the root JSON array."""
        return self._root_json_object[index]

    def __len__(self):
        """Return the length of root JSON array/object"""
        if isinstance(self._root_json_object, JsonObject):
            return len(self._root_json_object.to_dict())
        return len(self._root_json_object)

    def __setattr__(self, name, value):
        if name == "_root_json_object":
            super().__setattr__(name, value)
        else:
            setattr(self._root_json_object, name, value)

    def __str__(self):
        if isinstance(self._root_json_object, JsonObject):
            return self._root_json_object.to_json()
        return f"{self._root_json_object}"

    def __repr__(self):
        if isinstance(self._root_json_object, JsonObject):
            return f"{type(self).__name__}({self._root_json_object.to_dict()})"
        return f"{type(self).__name__}({self._root_json_object})"

    def _wrap_dict(self, data):
        """Wrap a dictionary in a JsonObject."""
        return JsonObject(data)

    def _is_valid_json_key(self, key):
        """Check whether a JSON key can be used as a Python attribute."""
        if key.isidentifier():
            return True
        else:
            print(f"Skipping invalid JSON key {key!r}")
            return False

    def _process_list(self, data: list):
        """Recursively process items in a list."""
        return [self._process_object(item) for item in data]

    def _process_dict(self, data: dict):
        """Recursively process values in a dictionary."""
        _data = {
            key: self._process_object(value)
            for key, value in data.items()
            if self._is_valid_json_key(key)
        }
        return self._wrap_dict(_data)

    def _process_object(self, value):
        """Process a JSON object based on its Python type."""
        if isinstance(value, dict):
            return self._process_dict(value)
        elif isinstance(value, list):
            return self._process_list(value)
        return value

    def _build_root_object(self, py_object):
        """Build the root object from the deserialized JSON."""
        return self._process_object(py_object)

    @classmethod
    def _from_py_object(cls, py_object):
        obj = cls()
        obj._root_json_object = obj._build_root_object(py_object)
        return obj

    @classmethod
    def from_json_string(cls, json_string):
        """Create a JsonPath instance from a JSON string."""
        if not isinstance(json_string, str):
            raise TypeError("json_string must be a string")
        if not json_string.strip():
            raise ValueError("JSON string cannot be empty")
        return cls._from_py_object(loads(json_string))

    @classmethod
    def from_json_file(cls, filename: str):
        """Create a JsonPath instance from a JSON file."""
        path = Path(filename)
        if not path.is_file():
            raise FileNotFoundError(f"File not found {filename}")
        with open(path, mode="r", encoding="utf-8") as json_file:
            return cls._from_py_object(load(json_file))
