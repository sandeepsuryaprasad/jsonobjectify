from json import load, loads
from pathlib import Path
from re import sub

from .json_object import JsonObject


class JsonPath:
    def __init__(self):
        """Initialize an empty JSON parser."""
        self._root_json_object = None

    def _normalize_key(self, key: str) -> str:
        """Normalize a JSON key for Python attribute access."""
        return sub(r"[-\s\.]+", "_", key)

    def __getattr__(self, name):
        """Return a value from the underlying JSON data using dot notation."""
        for key, value in self._info.items():
            if self._normalize_key(key) == name:
                return value
        raise AttributeError(f"{type(self).__name__} has no attribute {name!r}") from None

    def __getattr__(self, name):
        """Delegate attribute access to the root JSON object.

        Raises:
            AttributeError: If the requested attribute is 'value' or does not
            exist on the root JSON object.
        """
        if name == "value":
            raise AttributeError("'value' attribute is available only for scalar values")
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
        """Set an attribute on the root JSON object.

        Delegates attribute assignment to the root JSON object, except for
        `_root_json_object`, which is assigned directly.
        """
        if name == "_root_json_object":
            super().__setattr__(name, value)
        else:
            setattr(self._root_json_object, name, value)

    def __str__(self):
        """Return the string representation of the root JSON value.

        Serializes a root `JsonObject` as a JSON string. For scalar values,
        returns their standard Python string representation without JSON
        quoting or formatting.
        """
        if isinstance(self._root_json_object, JsonObject):
            return self._root_json_object.to_json()
        return f"{self._root_json_object}"

    def __repr__(self):
        """Return an unambiguous string representation of the instance.

        Includes the class name and root JSON value. Converts a `JsonObject`
        to a Python dictionary; scalar values use their standard Python
        representation.
        """
        if isinstance(self._root_json_object, JsonObject):
            return f"{type(self).__name__}({self._root_json_object.to_dict()})"
        return f"{type(self).__name__}({self._root_json_object})"

    def _wrap_dict(self, data):
        """Wrap a dictionary in a JsonObject."""
        return JsonObject(data)

    def _process_list(self, data: list):
        """Recursively process items in a list."""
        return [self._process_object(item) for item in data]

    def _process_dict(self, data: dict):
        """Recursively process values in a dictionary."""
        _data = {
            key: self._process_object(value)
            for key, value in data.items()
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

    @property
    def value(self):
        """Return the root value if the JSON response is a scalar.
        
        Raises:
            AttributeError: If the root JSON response is an object or array.
        """
        if isinstance(self._root_json_object, (JsonObject, list)):
            raise AttributeError("'value' attribute is available only for scalar values")
        return self._root_json_object

    @classmethod
    def _from_py_object(cls, py_object):
        """Create a `JsonPath` instance from a Python object.

        Builds the root JSON structure from the supplied Python object and
        returns the initialized instance.
        """
        obj = cls()
        obj._root_json_object = obj._build_root_object(py_object)
        return obj

    @classmethod
    def from_string(cls, json_string):
        """Create a JsonPath instance from a JSON string."""
        if not isinstance(json_string, str):
            raise TypeError("json_string must be a string")
        if not json_string.strip():
            raise ValueError("JSON string cannot be empty")
        return cls._from_py_object(loads(json_string))

    @classmethod
    def from_file(cls, filename: str):
        """Create a JsonPath instance from a JSON file."""
        path = Path(filename)
        if not path.is_file():
            raise FileNotFoundError(f"File not found {filename}")
        with open(path, mode="r", encoding="utf-8") as json_file:
            return cls._from_py_object(load(json_file))
