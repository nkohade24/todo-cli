import pytest

import todo


@pytest.fixture(autouse=True)
def temp_tasks_file(tmp_path, monkeypatch):
    """Point todo at a throwaway tasks file so the real tasks.json is never touched."""
    tasks_file = tmp_path / "tasks.json"
    monkeypatch.setattr(todo, "TASKS_FILE", str(tasks_file))
    return tasks_file


def test_add_stores_task():
    todo.add_task("Buy milk")

    tasks = todo.load_tasks()
    assert tasks == [{"task": "Buy milk", "done": False}]


def test_add_multiple_tasks_keeps_order():
    todo.add_task("First")
    todo.add_task("Second")
    todo.add_task("Third")

    descriptions = [t["task"] for t in todo.load_tasks()]
    assert descriptions == ["First", "Second", "Third"]


def test_add_starts_from_empty():
    assert todo.load_tasks() == []
