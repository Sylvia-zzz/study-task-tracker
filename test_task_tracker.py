import tempfile
import unittest
from pathlib import Path

from task_tracker import (
    add_task,
    complete_task,
    format_tasks,
    load_tasks,
    remove_task,
    save_tasks,
)


class TaskTrackerTests(unittest.TestCase):
    def test_add_and_complete_task(self) -> None:
        tasks = []
        first = add_task(tasks, "Review Scrum notes")
        second = add_task(tasks, "Practise Git commands")

        self.assertEqual(first["id"], 1)
        self.assertEqual(second["id"], 2)
        self.assertFalse(first["completed"])

        completed = complete_task(tasks, 1)
        self.assertTrue(completed["completed"])
        self.assertIn("[x] Review Scrum notes", format_tasks(tasks))

    def test_save_and_load_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            tasks = [{"id": 1, "title": "Read lecture slides", "completed": False}]

            save_tasks(path, tasks)

            self.assertEqual(load_tasks(path), tasks)

    def test_empty_title_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            add_task([], "   ")

    def test_unknown_task_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            complete_task([], 99)

    def test_remove_task(self) -> None:
        tasks = [
            {"id": 1, "title": "Review Kanban notes", "completed": False},
            {"id": 2, "title": "Practise Git branches", "completed": False},
        ]

        removed = remove_task(tasks, 1)

        self.assertEqual(removed["title"], "Review Kanban notes")
        self.assertEqual([task["id"] for task in tasks], [2])


if __name__ == "__main__":
    unittest.main()
