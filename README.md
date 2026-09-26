# Study Task Tracker

A small Python command-line application for recording study tasks and marking them as completed.
Tasks are stored locally in a JSON file, so the project has no external dependencies.

## Features

- Add a study task
- List pending and completed tasks
- Mark a task as completed
- Remove a task that is no longer needed
- Save task data between runs
- Automated tests using Python's built-in `unittest` module

## Requirements

- Python 3.9 or newer

## Usage

Add a task:

```bash
python task_tracker.py add "Review Scrum notes"
```

List tasks:

```bash
python task_tracker.py list
```

Complete a task:

```bash
python task_tracker.py complete 1
```

Remove a task:

```bash
python task_tracker.py remove 1
```

Use a different data file:

```bash
python task_tracker.py --data-file my_tasks.json list
```

## Tests

Run the automated tests from the project directory:

```bash
python -m unittest -v
```

## Project Structure

```text
study-task-tracker/
|-- task_tracker.py
|-- test_task_tracker.py
|-- README.md
`-- .gitignore
```
