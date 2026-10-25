# jsonobjectify

[![CI](https://github.com/sandeepsuryaprasad/jsonobjectify/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sandeepsuryaprasad/jsonobjectify/actions/workflows/ci.yml)
[![Development Status](https://img.shields.io/pypi/status/jsonobjectify)](https://pypi.org/project/jsonobjectify/)
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
Consider the following JSON string/response:

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
#### Construct python object from JSON string/response
```console
>>> from jsonobjectify import JsonPath
>>> employee = JsonPath.from_string(response)
```
#### Attribute look-up
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
#### Attribute Assignment
```console
>>> employee.name = "Jane Doe"
>>> employee.address.city = "Fort Worth"
```
#### Array of JSON objects
A JSON response can contain an array of objects at the root level. You can use 
`JsonPath.from_string` to parse the response and access each object's properties using 
dot notation.
```python
response = """[
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "website": "www.example.dev"
  },
  {
    "name": "Foo Bar",
    "email": "foo.bar@example.com",
    "website": "www.example.io"
  },
  {
    "name": "Baz Qux",
    "email": "baz.qux@example.com",
    "website": "www.example.edu"
  }
]"""
```
```console
>>> employees = JsonPath.from_string(response)
>>> len(employees)
3
```
#### Indexing each employee
```console
>>> employees[0]
<jsonobjectify.jsonobject.JsonObject object at 0x101bb7d50>
>>> employees[1]
<jsonobjectify.jsonobject.JsonObject object at 0x101bb7b50>
>>> employees[2]
<jsonobjectify.jsonobject.JsonObject object at 0x101aa2120>
>>> employees[0].name
'John Doe'
>>> employees[0].email
'john.doe@example.com'
>>> employees[0].website
'www.example.dev'
>>> 
```
Iterating over JSON arrays using a standard Python for loop and access each 
element's properties using dot notation.
```console
>>> for employee in employees:
...     print(f"{employee.name}, {employee.email}, {employee.website}")
...     
John Doe, john.doe@example.com, www.example.dev
Foo Bar, foo.bar@example.com, www.example.io
Baz Qux, baz.qux@example.com, www.example.edu
>>> 
```

#### `JsonPath` object from a JSON file
Create a JsonPath object directly from a JSON file using the `from_file`
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
'John Doe'
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
  "first-name": "Alice",
  "job title": "Software Engineer",
  "contact.email": "alice@example.com",
  "class": "Business"
}"""
```
```console
>>> employee = JsonPath.from_string(response)
```
You can access these properties using normalized attribute names,

```console
>>> employee.first_name
'Alice'
>>> employee.job_title
'Software Engineer'
>>> employee.contact_email
'alice@example.com'
>>> employee._class
'Business'
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
### Reading response from httpx
```python
>>> from httpx import get

>>> response = get("https://reqres.in/api/users/2")
>>> result = JsonPath.from_string(response.text)
>>> print(result)
```
```console
{
  "data": {
    "id": 2,
    "email": "janet.weaver@reqres.in",
    "first_name": "Janet",
    "last_name": "Weaver",
    "avatar": "https://reqres.in/img/faces/2-image.jpg"
  },
  "support": {
    "url": "https://reqres.in/go/posthog",
    "text": "PostHog ingests and stores your analytics, errors, replays, and business data so you and your agents can query and act on it. Get started.",
    "sponsored_by": "PostHog"
  },
  "_meta": {
    "powered_by": "ReqRes",
    "docs_url": "https://app.reqres.in/documentation",
    "upgrade_url": "https://app.reqres.in/upgrade",
    "example_url": "https://app.reqres.in/examples/notes-app",
    "variant": "key_v1",
    "message": "You are on the shared demo (no personal key), which has a low daily limit. A free account gives you your own key with 250 requests a day, plus request logs and your own collections.",
    "cta": {
      "label": "Get a free key",
      "url": "https://app.reqres.in/?utm_source=reqres_api&utm_medium=json&utm_campaign=demo_meta_key"
    },
    "context": "keyless_success"
  }
}
```
```console
>>> result.data.id
2
>>> result.data.email
'janet.weaver@reqres.in'
>>> result.support.url
'https://reqres.in/go/posthog'
```

### Installed version
To get to know the version of `jsonobjectify`,
```console
>>> import jsonobjectify
>>> print(jsonobjectify.__version__)
```
or
```console
>>> from jsonobjectify import __version__
>>> print(__version__)
```

### Requirements
* Python 3.12 or later

### Contributing
Contributions, bug reports, and feature suggestions are welcome. Please open an issue to 
discuss a proposed change before submitting a pull request.

### License

This package is distributed under the terms of [MIT](https://github.com/sandeepsuryaprasad/jsonobjectify/blob/main/LICENSE) license
