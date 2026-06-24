import argparse
import json
import os

TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def add_task(description):
    tasks = load_tasks()
    tasks.append({"task": description, "done": False})
    save_tasks(tasks)
    print(f"Added task: {description}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet.")
        return
    for i, task in enumerate(tasks, start=1):
        mark = "x" if task.get("done") else " "
        print(f"{i}. [{mark}] {task['task']}")


def done_task(number):
    tasks = load_tasks()
    if number < 1 or number > len(tasks):
        print(f"No task numbered {number}.")
        return
    task = tasks[number - 1]
    if task.get("done"):
        print(f"Task already done: {task['task']}")
        return
    task["done"] = True
    save_tasks(tasks)
    print(f"Marked task as done: {task['task']}")


def delete_task(number):
    tasks = load_tasks()
    if number < 1 or number > len(tasks):
        print(f"No task numbered {number}.")
        return
    task = tasks.pop(number - 1)
    save_tasks(tasks)
    print(f"Deleted task: {task['task']}")


def main():
    parser = argparse.ArgumentParser(description="A simple todo CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", help="The task description")

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark a task as completed")
    done_parser.add_argument("number", type=int, help="The task number (as shown by list)")

    delete_parser = subparsers.add_parser("delete", help="Delete a task by its number")
    delete_parser.add_argument("number", type=int, help="The task number (as shown by list)")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.task)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        done_task(args.number)
    elif args.command == "delete":
        delete_task(args.number)


if __name__ == "__main__":
    main()
