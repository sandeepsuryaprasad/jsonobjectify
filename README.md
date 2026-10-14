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
### Create `JsonPath` object from JSON string.
Here, response is a string containing valid JSON. The `from_string` class method parses 
the JSON data and creates a `JsonPath` object that allows you to access properties using 
dot notation.
```python
>>> employee = JsonPath.from_string(response)
```
You can now access and traverse nested JSON objects using **dot notation**. 
For JSON arrays, use the standard Python indexing syntax.
```python
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
You can also iterate over JSON arrays using a standard Python for loop and access each 
element's properties using dot notation.
```python
>>> for skill in employee.skills:
...     print(f"{skill.name}, {skill.level}")
...     
Python, Advanced
C, Advanced
C++, Intermediate
>>> 
```
### Create a `JsonPath` object from a JSON file
You can also create a JsonPath object directly from a JSON file using the `from_file`
class method. This allows you to work with JSON data stored in a file without having to 
read and parse its contents manually.

For example, consider an `employee.json` file containing the employee data shown in the 
previous example.

```python
>>> employee = JsonPath.from_file("employee.json")
```
Once the object is created, you can access nested properties and iterate over JSON arrays
in the same way
```python
>>> employee.name
'Michael Anderson'
>>> employee.address.city
'Austin'
>>> for skill in employee.skills:
...     print(f"{skill.name}, {skill.level}")
...
Python, Advanced
C, Advanced
C++, Intermediate
```
### Working with Scalar Values
If the **root JSON** value is a scalar, such as a string, number, boolean or null, you can 
access the underlying value using the `value` property.

```python
>>> data = JsonPath.from_string("26")
>>> data.value
26
>>> data = JsonPath.from_string("true")
>>> data.value
True
>>> data = JsonPath.from_string("null")
>>> data.value
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
