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


def test_list_empty_prints_no_tasks(capsys):
    todo.list_tasks()

    out = capsys.readouterr().out
    assert out.strip() == "No tasks yet."


def test_list_shows_numbered_tasks_with_marks(capsys):
    todo.add_task("First")
    todo.add_task("Second")
    todo.done_task(1)
    capsys.readouterr()  # discard output from the calls above

    todo.list_tasks()
    out = capsys.readouterr().out

    assert "1. [x] First" in out
    assert "2. [ ] Second" in out


def test_done_marks_task_done():
    todo.add_task("Buy milk")

    todo.done_task(1)

    assert todo.load_tasks()[0]["done"] is True


def test_done_out_of_range_does_nothing():
    todo.add_task("Only task")

    todo.done_task(5)
    todo.done_task(0)

    assert todo.load_tasks() == [{"task": "Only task", "done": False}]


def test_delete_removes_right_task_and_renumbers():
    todo.add_task("First")
    todo.add_task("Second")
    todo.add_task("Third")

    todo.delete_task(2)

    descriptions = [t["task"] for t in todo.load_tasks()]
    assert descriptions == ["First", "Third"]


def test_delete_out_of_range_does_nothing():
    todo.add_task("Keep me")

    todo.delete_task(9)
    todo.delete_task(0)

    assert todo.load_tasks() == [{"task": "Keep me", "done": False}]


def test_clear_removes_all_tasks():
    todo.add_task("First")
    todo.add_task("Second")

    todo.clear_tasks()

    assert todo.load_tasks() == []


def test_clear_on_empty_is_noop():
    todo.clear_tasks()

    assert todo.load_tasks() == []
