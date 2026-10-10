from json import load, loads
from pytest import fixture


@fixture
def response_from_json_string():
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
    return response


@fixture
def response_from_json_file():
    return "./tests/demo.json"