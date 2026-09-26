"""A small command-line study task tracker."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_DATA_FILE = Path("tasks.json")


def load_tasks(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("Task data must be a JSON list")
    return data


def save_tasks(path: Path, tasks: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)
        file.write("\n")


def add_task(tasks: list[dict[str, Any]], title: str) -> dict[str, Any]:
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty")
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": title, "completed": False}
    tasks.append(task)
    return task


def complete_task(tasks: list[dict[str, Any]], task_id: int) -> dict[str, Any]:
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task
    raise ValueError(f"Task {task_id} was not found")


def remove_task(tasks: list[dict[str, Any]], task_id: int) -> dict[str, Any]:
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            return tasks.pop(index)
    raise ValueError(f"Task {task_id} was not found")


def format_tasks(tasks: list[dict[str, Any]]) -> str:
    if not tasks:
        return "No tasks yet."
    lines = []
    for task in tasks:
        marker = "x" if task["completed"] else " "
        lines.append(f"{task['id']:>3}. [{marker}] {task['title']}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track study tasks from the command line.")
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help="JSON file used to store tasks (default: tasks.json)",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add_command = commands.add_parser("add", help="Add a task")
    add_command.add_argument("title", help="Task description")

    commands.add_parser("list", help="List tasks")

    complete_command = commands.add_parser("complete", help="Mark a task as completed")
    complete_command.add_argument("task_id", type=int, help="Numeric task ID")

    remove_command = commands.add_parser("remove", help="Remove a task")
    remove_command.add_argument("task_id", type=int, help="Numeric task ID")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    tasks = load_tasks(args.data_file)

    try:
        if args.command == "add":
            task = add_task(tasks, args.title)
            save_tasks(args.data_file, tasks)
            print(f"Added task {task['id']}: {task['title']}")
        elif args.command == "complete":
            task = complete_task(tasks, args.task_id)
            save_tasks(args.data_file, tasks)
            print(f"Completed task {task['id']}: {task['title']}")
        elif args.command == "remove":
            task = remove_task(tasks, args.task_id)
            save_tasks(args.data_file, tasks)
            print(f"Removed task {task['id']}: {task['title']}")
        else:
            print(format_tasks(tasks))
    except ValueError as error:
        print(f"Error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
