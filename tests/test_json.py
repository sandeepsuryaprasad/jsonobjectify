from jsonobjectify.json_object import JsonObject
from jsonobjectify.json_path import JsonPath


def test_response_from_json_string(response_from_json_string):
    json = JsonPath.from_json_string(response_from_json_string)
    assert json.name == "Michael Anderson"
    assert json.address.city == "Austin"
    assert len(json.skills) == 3
    assert isinstance(json.skills[0], JsonObject) == True
    assert json.skills[0].name == "Python"
    assert json.skills[-1].level == "Intermediate"

def test_response_from_json_file(response_from_json_file):
    json = JsonPath.from_json_file(response_from_json_file)
    assert json.name == "Michael Anderson"
    assert json.address.city == "Austin"
    assert len(json.skills) == 3
    assert isinstance(json.skills[0], JsonObject) == True
    assert json.skills[0].name == "Python"
    assert json.skills[-1].level == "Intermediate"

def test_empty_list():
    assert len(JsonPath.from_json_string("[]")) == 0

def test_empty_json_object():
    assert len(JsonPath.from_json_string("{}")) == 0

