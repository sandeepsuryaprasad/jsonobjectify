# jsonobjectify

[![CI](https://github.com/sandeepsuryaprasad/jsonobjectify/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sandeepsuryaprasad/jsonobjectify/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/jsonobjectify?lable=PyPI)](https://pypi.org/project/jsonobjectify/)
[![Python versions](https://img.shields.io/pypi/pyversions/jsonobjectify?label=Python)](https://pypi.org/project/jsonobjectify/)

A lightweight Python library for converting JSON data into Python objects, 
simplifying access to nested structures through dot notation. Instead of writing chained 
dictionary lookups, you can navigate nested JSON structures using a clean, readable, 
object-oriented interface.

## Installation

```console
pip install jsonobjectify
```

## Usage
Consider the following JSON data representing an employee and their department:

```python
response = """{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
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
```console
>>> employee = JsonPath.from_string(response)
```
You can now access and traverse nested JSON objects using **dot notation**. 
For JSON arrays, use the standard Python indexing syntax.
```console
>>> employee.name
'John Doe'
>>> employee.address.city
'Austin'
>>> employee.address.geo_location.lng
'-97.7431'
>>> employee.skills[0].name
'Python'
>>> employee.skills[1].level
'Advanced'
>>>
```
You can also iterate over JSON arrays using a standard Python for loop and access each 
element's properties using dot notation.
```console
>>> for skill in employee.skills:
...     print(f"{skill.name}, {skill.level}")
...     
Python, Advanced
C, Advanced
C++, Intermediate
>>> 
```
### Root response is an array of JSON objects
A JSON response can contain an array of objects at the root level. You can use 
`JsonPath.from_string` to parse the response and access each object's properties using 
dot notation.
```python
response = """[
  {
    "name": "Olivia Bennett",
    "email": "olivia.bennett@example.com",
    "website": "www.example.dev"
  },
  {
    "name": "Ethan Parker",
    "email": "ethan.parker@example.com",
    "website": "www.example.io"
  },
  {
    "name": "Sophia Turner",
    "email": "sophia.turner@example.com",
    "website": "www.example.edu"
  }
]"""
```
```console
>>> employees = JsonPath.from_string(response)
>>> employees[0]
<jsonobjectify.jsonobject.JsonObject object at 0x101bb7d50>
>>> employees[1]
<jsonobjectify.jsonobject.JsonObject object at 0x101bb7b50>
>>> employees[2]
<jsonobjectify.jsonobject.JsonObject object at 0x101aa2120>
>>> employees[0].name
'Olivia Bennett'
>>> employees[0].email
'olivia.bennett@example.com'
>>> employees[0].website
'www.example.dev'
>>> 
```
You can also iterate over JSON arrays using a standard Python for loop and access each 
element's properties using dot notation.
```console
>>> for employee in employees:
...     print(f"{employee.name}, {employee.email}, {employee.website}")
...     
Olivia Bennett, olivia.bennett@example.com, www.example.dev
Ethan Parker, ethan.parker@example.com, www.example.io
Sophia Turner, sophia.turner@example.com, www.example.edu
>>> 
```

### Create a `JsonPath` object from a JSON file
You can also create a JsonPath object directly from a JSON file using the `from_file`
class method. This allows you to work with JSON data stored in a file without having to 
read and parse its contents manually.

For example, consider an `employee.json` file containing the employee data shown in the 
previous example.

```console
>>> employee = JsonPath.from_file("employee.json")
```
Once the object is created, you can access nested properties and iterate over JSON arrays
in the same way

```console
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

```console
>>> data = JsonPath.from_string("26")
>>> data.value
26
>>> data = JsonPath.from_string("true")
>>> data.value
True
>>> data = JsonPath.from_string("null")
>>> data.value
>>>
>>> json = JsonPath.from_string('"hello world"')
>>> json.value
'hello world'
```
### Accessing JSON Properties with Normalized Keys
JSON property names may contain hyphens, spaces, or periods, which cannot be used directly 
in Python attribute names. jsonobjectify normalizes these characters to underscores, 
allowing you to access such properties using dot notation.

```python
response = """{
  "first-name": "Olivia",
  "job title": "Software Engineer",
  "contact.email": "olivia@example.com"
}"""
```
```console
>>> employee = JsonPath.from_string(response)
```
You can access these properties using normalized attribute names,

```console
>>> employee.first_name
'Olivia'
>>> employee.job_title
'Software Engineer'
>>> employee.contact_email
'olivia@example.com'
```
**The original JSON property names are preserved when converting the object back to 
a dictionary or JSON string.**

### Converting Objects Back to JSON

`jsonobjectify` is intended to support conversion back to standard Python dictionaries and 
JSON strings, making it convenient to work with transformed data.

```python
# Convert the object to a Python dictionary
data = employee.to_dict()

# Serialize the object to a JSON string
json_data = employee.to_json()
```

### Requirements
* Python 3.12 or later

### Contributing
Contributions, bug reports, and feature suggestions are welcome. Please open an issue to 
discuss a proposed change before submitting a pull request.

### License

This package is distributed under the terms of [MIT](https://github.com/sandeepsuryaprasad/jsonobjectify/blob/main/LICENSE) license
