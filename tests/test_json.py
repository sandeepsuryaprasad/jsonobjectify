import pytest
import json
from pathlib import Path
from jsonobjectify.jsonpath import JsonPath

JSON_FILE_PATH = Path.joinpath(Path(__file__).parent, "json_file.json")

def test_json_object():
    response = """{
    "k1": "v1",
    "k2": "v2"
    }
    """
    result = JsonPath.from_string(response)
    assert result.k1 == "v1"
    assert result.k2 == "v2"

def test_nested_json_object():
    response = """{
        "k1": {"n1": "v1"},
        "k2": {"n2": {"n3": "v2"}}
    }
    """
    result = JsonPath.from_string(response)
    assert result.k1.n1 == "v1"
    assert result.k2.n2.n3 == "v2"

def test_json_array():
    response = "[1, 2, 3]"
    result = JsonPath.from_string(response)
    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 3

def test_list_json_objects():
    response = """[
        {"k1": "v1"},
        {"k2": "v2"}
    ]
    """
    result = JsonPath.from_string(response)
    assert result[0].k1 == "v1"
    assert result[1].k2 == "v2"

def test_empty_json_array():
    assert len(JsonPath.from_string("[]")) == 0

def test_empty_json_object():
    assert len(JsonPath.from_string("{}")) == 0

def test_response_from_file():
    result = JsonPath.from_file(JSON_FILE_PATH)
    assert result[0].k1 == "v1"
    assert result[0].k2 == "v2"
    assert result[1].k3 == "v3"
    assert result[1].k4 == "v4"

def test_json_null():
    response = '{"k1": null}'
    result = JsonPath.from_string(response)
    assert result.k1 is None

def test_json_bool():
    response = '{"is_active": true, "is_admin": false}'
    result = JsonPath.from_string(response)
    assert result.is_active is True
    assert result.is_admin is False

@pytest.mark.parametrize(
    ("response", "expected"),
    [
        ("26", 26),
        ("true", True),
        ("false", False),
        ("null", None),
        ('"hello world"', "hello world"),
    ],
)
def test_scalar_values(response, expected):
    result = JsonPath.from_string(response)
    assert result.value == expected

def test_key_normalization():
    response = """{
        "user-name": "John Doe",
        "first name": "John",
        "city": "Austin",
        "email.id": "john.doe@example.com"
    }"""
    result = JsonPath.from_string(response)
    assert result.user_name == "John Doe"
    assert result.first_name == "John"
    assert result.city == "Austin"
    assert result.email_id == "john.doe@example.com"

def test_missing_attribute():
    result = JsonPath.from_string('{"name": "John"}')
    with pytest.raises(AttributeError):
        _ = result.age

def test_invalid_json():
    with pytest.raises(json.JSONDecodeError):
        JsonPath.from_string('{"name": }')

def test_to_dict():
    result = JsonPath.from_string(
        '{"name": "John", "address": {"city": "Austin"}}'
    )
    assert result.to_dict() == {
        "name": "John",
        "address": {"city": "Austin"},
    }

def test_to_json():
    data = JsonPath.from_string('{"name": "John", "age": 26}')
    assert json.loads(data.to_json()) == {
        "name": "John",
        "age": 26,
    }