#!/usr/bin/env python3
"""Interactive menu for querying the todos dataset.

Loads the data once at startup, then answers questions from an index
until the user quits. All logic is imported - this file only handles
the menu loop and input.
"""

import sys

from load_data import load_todos
from indexing import (
    build_user_index,
    build_completion_index,
    count_completed_by_user_indexed,
    get_users_with_all_completed_indexed,
    get_todos_by_user_indexed,
)

DEFAULT_PATH = "data/todos.json"

MENU = """
--- todos query shell ---
1  completed todos per user
2  users who completed everything
3  totals and unique users
4  todos for one user
q  quit
"""


def show_completed_per_user(state):
    counts = count_completed_by_user_indexed(state["user_index"])
    for uid in sorted(counts):
        total = len(state["user_index"][uid])
        print(f"  user {uid:>2}: {counts[uid]:>2} / {total:>2} completed")


def show_all_completed(state):
    done = get_users_with_all_completed_indexed(state["user_index"])
    if done:
        print(f"  fully finished: {sorted(done)}")
    else:
        print("  nobody has completed all their todos")


def show_totals(state):
    completion = state["completion_index"]
    print(f"  total todos:  {len(state['todos'])}")
    print(f"  unique users: {len(state['user_index'])}")
    print(f"  completed:    {len(completion['completed'])}")
    print(f"  pending:      {len(completion['pending'])}")


def show_one_user(state):
    raw = input("  userId: ").strip()
    if not raw.isdigit():
        print("  not a number")
        return

    items = get_todos_by_user_indexed(state["user_index"], int(raw))
    if not items:
        print(f"  no todos for user {raw}")
        return

    for todo in items:
        mark = "x" if todo["completed"] else " "
        print(f"  [{mark}] {todo['id']:>3}  {todo['title'][:50]}")


ACTIONS = {
    "1": show_completed_per_user,
    "2": show_all_completed,
    "3": show_totals,
    "4": show_one_user,
}

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH

    todos = load_todos(path)
    state = {
        "todos": todos,
        "user_index": build_user_index(todos),
        "completion_index": build_completion_index(todos),
    }
    print(f"Loaded {len(todos)} todos from {path}")

    while True:
        print(MENU)
        try:
            choice = input("choice: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break

        if choice in ("q", "quit", "exit"):
            print("bye")
            break

        action = ACTIONS.get(choice)
        if action is None:
            print(f"  unknown option: {choice!r}")
            continue

        try:
            action(state)
        except (EOFError, KeyboardInterrupt):
            print("\ncancelled")


if __name__ == "__main__":
    main()