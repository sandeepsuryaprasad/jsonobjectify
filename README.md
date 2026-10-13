# jsonobjectify

[![CI](https://github.com/sandeepsuryaprasad/jsonobjectify/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sandeepsuryaprasad/jsonobjectify/actions/workflows/ci-test.yml)  [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A lightweight Python library for converting JSON data into Python objects, 
simplifying access to nested structures through dot notation. Instead of writing chained 
dictionary lookups, you can navigate nested JSON structures using a clean, readable, 
object-oriented interface.

## Installation

```commandline
pip install jsonobjectify
```

## Usage
Consider the following JSON data representing an employee and their department:

```json lines
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

```python
>>> employee = JsonPath.from_string(response)
>>> employee.name
'Michael Anderson'
>>> employee.address.city
'Austin'
>>> employee.skills[0].name
'Python'
>>> employee.skills[1].level
'Advanced'
>>>
```
```python
>>> for skill in employee.skills:
...     print(f"{skill.name}, {skill.level}")
...     
Python, Advanced
C, Advanced
C++, Intermediate
>>> 
```
## Converting Objects Back to JSON

`jsonobjectify` is intended to support conversion back to standard Python dictionaries and 
JSON strings, making it convenient to work with transformed data.

```python
# Convert the object to a Python dictionary
data = employee.to_dict()

# Serialize the object to a JSON string
json_data = employee.to_json()
```

## Requirements

* Python 3.12 or later

## Contributing

Contributions, bug reports, and feature suggestions are welcome. Please open an issue to 
discuss a proposed change before submitting a pull request.

## License

This package is distributed under the terms of [MIT](https://github.com/sandeepsuryaprasad/jsonobjectify/blob/main/LICENSE) license
