import pytest

from src.db import actions
from src.db.errors import DBNotFoundError
import uuid


@pytest.mark.parametrize(
    "description",
    [
        None,
        "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.",
    ],
    ids=["without description", "with description"],
)
def test_create_new_entity_can_be_created_successfully(
    test_db, request_entity, description: None | str
):
    request_entity.description = description

    db_entity = actions.create_db_entity(request_entity, test_db)
    db_compare = actions.get_db_entity(db_entity.id, test_db)
    assert db_entity is not None
    assert db_entity.id is not None
    assert db_entity.name == request_entity.name
    assert db_entity.case_id == request_entity.case_id
    assert db_entity.description == description
    assert db_entity == db_compare
    assert db_entity.is_deleted is False
    assert db_entity.created_at.date() == db_entity.updated_at.date()
    assert db_entity.created_at.hour == db_entity.updated_at.hour
    assert db_entity.created_at.minute == db_entity.updated_at.minute
    assert db_entity.created_at.second == db_entity.updated_at.second


def test_get_existing_entity(test_db, request_entity):
    db_entity = actions.create_db_entity(request_entity, test_db)
    item = actions.get_db_entity(db_entity.id, test_db)
    assert item is not None
    assert item.id == db_entity.id
    assert item.name == request_entity.name
    assert item.case_date == request_entity.case_date
    assert item.case_id == request_entity.case_id


def test_get_non_existing_entity(test_db, request_entity):
    actions.create_db_entity(request_entity, test_db)
    non_existing_id = uuid.uuid4()
    with pytest.raises(DBNotFoundError) as e:
        actions.get_db_entity(non_existing_id, test_db)

    assert str(e.value) == f"Entity with id {non_existing_id} was not found."
    assert isinstance(e.value, DBNotFoundError)


def test_update_existing_entity(test_db, request_entity):
    db_entity = actions.create_db_entity(request_entity, test_db)
    request_entity.description = "Updated description"
    updated_db_entity = actions.update_db_entity(db_entity.id, request_entity, test_db)
    assert updated_db_entity.description == request_entity.description
    assert updated_db_entity.created_at < updated_db_entity.updated_at


def test_update_non_existing_entity(test_db, request_entity):
    non_existing_id = uuid.uuid4()
    with pytest.raises(DBNotFoundError) as e:
        actions.update_db_entity(non_existing_id, request_entity, test_db)

    assert str(e.value) == f"Entity with id {non_existing_id} was not found."
    assert isinstance(e.value, DBNotFoundError)


def test_delete_existing_entity(test_db, request_entity):
    db_entity = actions.create_db_entity(request_entity, test_db)
    deleted_db_entity = actions.delete_db_entity(db_entity.id, test_db)
    with pytest.raises(DBNotFoundError) as e:
        actions.get_db_entity(deleted_db_entity.id, test_db)

    assert str(e.value) == f"Entity with id {deleted_db_entity.id} was not found."
    assert isinstance(e.value, DBNotFoundError)


def test_delete_non_existing_entity(test_db, request_entity):
    non_existing_id = uuid.uuid4()
    with pytest.raises(DBNotFoundError) as e:
        actions.delete_db_entity(non_existing_id, test_db)

    assert str(e.value) == f"Entity with id {non_existing_id} was not found."
    assert isinstance(e.value, DBNotFoundError)


def test_get_all_existing_entities(test_db, request_entity):
    db_entity = actions.create_db_entity(request_entity, test_db)
    request_entity.description = "Updated description"
    other_db_entity = actions.create_db_entity(request_entity, test_db)
    all_entities = actions.get_all_db_entities(test_db)
    assert len(all_entities) == 2
    assert db_entity in all_entities
    assert other_db_entity in all_entities


def test_get_all_entities_excludes_deleted_entities(test_db, request_entity):
    db_entity = actions.create_db_entity(request_entity, test_db)
    db_entity = actions.delete_db_entity(db_entity.id, test_db)
    all_entities = actions.get_all_db_entities(test_db)
    assert len(all_entities) == 0
    assert db_entity not in all_entities
