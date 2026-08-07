#!/usr/bin/env python3
"""Build in-memory indices over the todos dataset.

An index is a precomputed grouping: instead of scanning the whole list
every time you want one user's todos, you scan once and store the result
keyed by userId. Lookups afterwards are dictionary hits.
"""

import sys

from load_data import load_todos

DEFAULT_PATH = "data/todos.json"


def build_user_index(todos):
    """Return {userId: [todo, ...]}."""
    index = {}
    for todo in todos:
        uid = todo["userId"]
        if uid not in index:
            index[uid] = []
        index[uid].append(todo)
    return index


def build_completion_index(todos):
    """Return {"completed": [...], "pending": [...]}."""
    index = {"completed": [], "pending": []}
    for todo in todos:
        bucket = "completed" if todo["completed"] else "pending"
        index[bucket].append(todo)
    return index


def build_todo_index(todos):
    """Return {id: todo} for direct lookup of a single record."""
    return {todo["id"]: todo for todo in todos}


def get_todos_by_user_indexed(user_index, user_id):
    """Look up one user's todos. Dict hit instead of a full scan."""
    return user_index.get(user_id, [])


def count_completed_by_user_indexed(user_index):
    """Return {userId: number of completed todos}."""
    return {
        uid: sum(1 for t in items if t["completed"])
        for uid, items in user_index.items()
    }


def get_users_with_all_completed_indexed(user_index):
    """Return the set of userIds whose todos are all completed."""
    return {
        uid
        for uid, items in user_index.items()
        if items and all(t["completed"] for t in items)
    }

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    todos = load_todos(path)

    user_index = build_user_index(todos)
    completion_index = build_completion_index(todos)
    todo_index = build_todo_index(todos)

    print(f"Users indexed: {len(user_index)}")
    print(f"Todos per user: {[len(v) for _, v in sorted(user_index.items())]}")

    print(f"\nCompleted: {len(completion_index['completed'])}")
    print(f"Pending:   {len(completion_index['pending'])}")

    print("\nCompleted per user (via index):")
    for uid, n in sorted(count_completed_by_user_indexed(user_index).items()):
        print(f"  user {uid:>2}: {n:>2}")

    done = get_users_with_all_completed_indexed(user_index)
    print(f"\nAll completed: {sorted(done) if done else 'none'}")

    print(f"\nTodo id 42: {todo_index[42]['title']!r}")
    print(f"Todos for user 999: {get_todos_by_user_indexed(user_index, 999)}")


if __name__ == "__main__":
    main()