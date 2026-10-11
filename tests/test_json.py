from jsonobjectify.json_path import JsonPath


def test_json_object():
    response = """{
    "k1": "v1",
    "k2": "v2"
    }
    """
    json = JsonPath.from_json_string(response)
    assert json.k1 == "v1"
    assert json.k2 == "v2"


def test_nested_json_object():
    response = """{
        "k1": {"n1": "v1"},
        "k2": {"n2": {"n3": "v2"}}
    }
    """
    json = JsonPath.from_json_string(response)
    assert json.k1.n1 == "v1"
    assert json.k2.n2.n3 == "v2"


def test_json_array():
    response = "[1, 2, 3]"
    json = JsonPath.from_json_string(response)
    assert json[0] == 1
    assert json[1] == 2
    assert json[2] == 3


def test_list_json_objects():
    response = """[
        {"k1": "v1"},
        {"k2": "v2"}
    ]
    """
    json = JsonPath.from_json_string(response)
    assert json[0].k1 == "v1"
    assert json[1].k2 == "v2"


def test_empty_json_array():
    assert len(JsonPath.from_json_string("[]")) == 0


def test_empty_json_object():
    assert len(JsonPath.from_json_string("{}")) == 0


def test_empty_list():
    assert len(JsonPath.from_json_string("[]")) == 0

def test_empty_json_object():
    assert len(JsonPath.from_json_string("{}")) == 0

def test_response_from_file():
    json = JsonPath.from_json_file("./tests/json_file.json")
    assert json[0].k1 == "v1"
    assert json[0].k2 == "v2"
    assert json[1].k3 == "v3"
    assert json[1].k4 == "v4"

