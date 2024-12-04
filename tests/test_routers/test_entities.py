from uuid import uuid4

import pytest


@pytest.fixture(scope="function")
def added_entity_body(test_api_client, request_entity_json):
    post_response = test_api_client.post("/entities/", json=request_entity_json)
    assert post_response.status_code == 200
    post_response_body = post_response.json()
    return post_response_body


def test_get_all_entities(test_api_client):
    response = test_api_client.get("/entities/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    "description",
    [None, "Some Test description"],
    ids=["without description", "with description"],
)
def test_create_new_entity(test_api_client, request_entity_json, description: str):
    request_entity_json["description"] = description

    response = test_api_client.post("/entities/", json=request_entity_json)
    response_body = response.json()
    entity_id = response_body.get("id")
    del response_body["id"]
    assert response.status_code == 200
    assert response_body == request_entity_json
    assert entity_id is not None


@pytest.mark.parametrize(
    "remove_field",
    [
        "case_id",
        "case_date",
        "name",
    ],
)
def test_create_new_entity_raises_error_when_missing_required_fields(
    test_api_client, request_entity_json, remove_field
):
    del request_entity_json[remove_field]
    response = test_api_client.post("/entities/", json=request_entity_json)

    assert response.status_code == 422
    response_body = response.json()
    error_details = response_body.get("detail")
    assert len(error_details) == 1
    error = error_details[0]
    assert error["type"] == "missing"
    assert error["loc"] == ["body", remove_field]
    assert error["msg"] == "Field required"


@pytest.mark.parametrize(
    "field, invalid_value, error_type",
    [
        ("case_id", "", "string_too_short"),
        ("case_id", "Neque porro quisquam est qui dolore", "string_too_short"),
        ("case_id", "Neque porro quisquam est qui dolorem!", "string_too_long"),
        ("case_id", 1000, "string_type"),
        (
            "case_date",
            "Neque porro quisquam est qui dolorem!",
            "datetime_from_date_parsing",
        ),
        ("description", 12.4, "string_type"),
        ("name", -0, "string_type"),
    ],
)
def test_create_new_entity_raises_error_when_fields_incorrect(
    test_api_client, request_entity_json, field, invalid_value, error_type
):
    request_entity_json[field] = invalid_value
    response = test_api_client.post("/entities/", json=request_entity_json)

    assert response.status_code == 422
    response_body = response.json()
    error_details = response_body.get("detail")
    assert len(error_details) == 1
    error = error_details[0]
    assert error["type"] == error_type
    assert error["loc"] == ["body", field]


def test_get_existing_entity_returns_correct_body(test_api_client, added_entity_body):
    get_response = test_api_client.get(f"/entities/{added_entity_body['id']}")
    assert get_response.status_code == 200
    get_response_body = get_response.json()
    assert added_entity_body == get_response_body


def test_get_non_existing_entity_raises_error_response(
    test_api_client, request_entity_json
):
    non_existing_id = uuid4()
    get_response = test_api_client.get(f"/entities/{non_existing_id}")

    assert get_response.status_code == 404
    response_body = get_response.json()
    assert response_body == {
        f"detail": f"Entity with id {non_existing_id} was not found."
    }


def test_update_existing_entity_returns_correct_body(
    test_api_client, request_entity_json, added_entity_body
):
    request_entity_json["name"] = "UPDATED VALUE"
    request_entity_json["description"] = "SOME TEST DESCRIPTION"

    put_response = test_api_client.put(
        f"/entities/{added_entity_body['id']}", json=request_entity_json
    )

    assert put_response.status_code == 200
    put_response_body = put_response.json()
    assert put_response_body["id"] == added_entity_body["id"]
    del put_response_body["id"]
    assert put_response_body == request_entity_json


def test_update_non_existing_entity_raises_error_response(
    test_api_client, request_entity_json
):
    non_existing_id = uuid4()
    put_response = test_api_client.put(
        f"/entities/{non_existing_id}", json=request_entity_json
    )
    assert put_response.status_code == 404
    response_body = put_response.json()
    assert response_body == {
        f"detail": f"Entity with id {non_existing_id} was not found."
    }


def test_delete_existing_entity_returns_correct_body(
    test_api_client, request_entity_json, added_entity_body
):
    delete_response = test_api_client.delete(f"/entities/{added_entity_body['id']}")
    assert delete_response.status_code == 200
    delete_response_body = delete_response.json()
    assert delete_response_body == added_entity_body


def test_delete_non_existing_entity_raises_error_response(
    test_api_client, request_entity_json
):
    non_existing_id = uuid4()
    delete_response = test_api_client.delete(f"/entities/{non_existing_id}")
    assert delete_response.status_code == 404
    response_body = delete_response.json()
    assert response_body == {
        f"detail": f"Entity with id {non_existing_id} was not found."
    }


def test_cannot_delete_entity_twice(
    test_api_client, request_entity_json, added_entity_body
):
    delete_response = test_api_client.delete(f"/entities/{added_entity_body['id']}")
    assert delete_response.status_code == 200
    delete_response = test_api_client.delete(f"/entities/{added_entity_body['id']}")
    assert delete_response.status_code == 404
