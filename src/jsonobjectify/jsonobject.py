from json import dumps
from re import sub


class JsonObject:
    """Represent a JSON object as a Python object."""

    def __init__(self, info):
        """
        Initialize a JsonObject from a dictionary.

        Stores the supplied dictionary as the underlying JSON data and
        builds a mapping between normalized attribute names and their
        original JSON property names.

        Each property name is normalized using `_normalize_key()`,
        allowing JSON properties containing hyphens, whitespace
        characters, or periods to be accessed using Python dot notation.
        The original property names are preserved in the underlying
        dictionary.

        Args:
            info: A dictionary containing the JSON object's properties
                and their corresponding values.

        Notes:
            The normalized-key mapping is used by `__getattr__` and
            `__setattr__` to resolve attribute names to their original
            JSON property names.

            Nested dictionaries and lists are expected to be processed
            by the surrounding JSON conversion logic before or during
            construction, as appropriate for the implementation.
        """
        self._info = info
        self._normalized_keys = {}
        for original_key, _ in self._info.items():
            self._normalized_keys[self._normalize_key(original_key)] = original_key

    def _normalize_key(self, original_key: str) -> str:
        """
        Normalize a JSON key for Python attribute access.

        Replaces consecutive hyphens, whitespace characters, and periods
        with a single underscore. This allows JSON keys containing these
        characters to be accessed using Python dot notation.

        The original JSON key remains unchanged in the underlying data.
        Normalization is used only to determine the corresponding Python
        attribute name.

        Args:
            original_key: The original JSON property name to normalize.

        Returns:
            The normalized key, with consecutive hyphens, whitespace
            characters, and periods replaced by a single underscore.

        Examples:
            >>> _normalize_key("first-name")
            'first_name'
            >>> _normalize_key("first name")
            'first_name'
            >>> _normalize_key("email.id")
            'email_id'
            >>> _normalize_key("first---last")
            'first_last'
        """
        normalized_key = sub(r"[-\s.]+", "_", original_key)
        return normalized_key

    def __getattr__(self, name):
        """
        Retrieve a JSON property using Python attribute access.

        This method is called when the requested attribute is not found
        through the normal attribute lookup process. It uses the
        normalized-key mapping to resolve the requested attribute name
        to its original JSON property name, then retrieves the
        corresponding value from the underlying dictionary.

        JSON property names may contain hyphens, whitespace characters,
        or periods that are replaced with underscores during
        normalization. The original property names are preserved in
        the underlying data.

        Args:
            name: The attribute name being accessed.

        Returns:
            The value associated with the corresponding JSON property.
            The value may be a scalar, a nested JsonObject, or a list,
            depending on the JSON structure.

        Raises:
            AttributeError: If no JSON property corresponds to the
                requested attribute name.

        Notes:
            Attributes already defined on the class are resolved through
            normal Python attribute lookup before this method is called.

        Examples:
            For a JSON property named "first-name":

            >>> user.first_name
            'John'

            Accessing an unknown property raises AttributeError:

            >>> user.unknown
            AttributeError: JsonObject has no attribute 'unknown'
        """
        original_key = self._normalized_keys.get(name)
        if original_key is None:
            raise AttributeError(f"{type(self).__name__} has no attribute {name!r}") from None
        return self._info[original_key]

    def __setattr__(self, name, value):
        """
        Set an internal attribute or update a JSON property.

        Internal attributes such as `_info` and `_normalized_keys` are
        assigned directly using the default Python attribute-assignment
        mechanism.

        For other attribute names, this method looks up the corresponding
        original JSON property name in the normalized-key mapping. If a
        mapping exists, the associated JSON property is updated. Otherwise,
        a new JSON property is added to the underlying dictionary "self._info",
        and its normalized attribute name is registered in the mapping.

        This allows JSON properties to be modified or added using Python
        dot notation while preserving their original property names in
        the underlying data.

        Args:
            name: The attribute name to assign or the JSON property to
                update.
            value: The value to assign to the attribute or JSON property.

        Notes:
            New property names are normalized using `_normalize_key()`
            before being registered in the mapping. Existing JSON property
            names are preserved when their corresponding attributes are
            updated.

        Examples:
            Update an existing property:

            >>> user.name = "Jane"

            Add a new property:

            >>> user.age = 30
            >>> user.age
            30
        """
        if name in {"_info", "_normalized_keys"}:
            super().__setattr__(name, value)
        else:
            original_key = self._normalized_keys.get(name)
            if original_key is None:
                original_key = name
                self._normalized_keys[self._normalize_key(name)] = original_key
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