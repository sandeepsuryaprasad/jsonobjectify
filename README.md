# jsonobjectify

A lightweight Python library for converting JSON data into Python objects, 
simplifying access to nested structures through intuitive dot notation.

## Overview
Working with complex JSON data often involves repetitive dictionary lookups, especially 
when accessing deeply nested structures. `jsonobjectify` simplifies this process by 
converting JSON data into Python objects, allowing you to access JSON properties using 
familiar attribute notation.

Instead of writing chained dictionary lookups, you can navigate nested JSON structures 
using a clean, readable, object-oriented interface.

## Features

* **Dot-notation access:** Access JSON properties using Python attributes.
* **Nested object support:** Navigate deeply nested JSON structures naturally.
* **List support:** Work with collections of JSON objects.
* **Dictionary conversion:** Convert mapped objects back into standard Python dictionaries.
* **JSON serialization:** Serialize objects back into JSON.
* **Simple API:** Keep your code readable when working with complex JSON responses.

## Installation

```bash
pip install jsonobjectify
```

## Usage

Consider the following JSON data representing an employee and their department:

```python
response = """{
    "id": 1,
    "name": "Michael Anderson",
    "email": "michael.anderson@example.com",
    "website": "www.example.dev",
    "address": {
      "city": "Austin",
      "state": "TX",
      "country": "United States",
      "geo_location": {"lat": "30.2672", "lng": "-97.7431"}
    },
    "skills": [
      {"name": "Python", "level": "Advanced"},
      {"name": "C", "level": "Advanced"},
      {"name": "C++", "level": "Intermediate"}
    ]
}"""
```

With `jsonobjectify`, you can access the data through object attributes rather than 
repeated dictionary lookups.

```python
from jsonobjectify import JsonPath

employee = JsonPath.from_json_string(response)

print(employee.name)
print(employee.address.city)
print(employee.skills[0].name)
print(employee.skills[1].level)
```

**Output**

```text
Alice
Engineering
Bengaluru
```

The example above illustrates the intended API. Adjust the import and construction methods to match the implementation in your repository.

## Converting Objects Back to JSON

`jsonobjectify` is intended to support conversion back to standard Python dictionaries and JSON strings, making it convenient to work with transformed data.

```python
# Convert the object to a Python dictionary
data = employee.to_dict()

# Serialize the object to a JSON string
json_data = employee.to_json()
```

## Requirements

* Python 3.9 or later

## Contributing

Contributions, bug reports, and feature suggestions are welcome. Please open an issue to discuss a proposed change before submitting a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
