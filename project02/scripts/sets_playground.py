#!/usr/bin/env python3
"""Set operations over the todos dataset.

Sets answer questions about membership and uniqueness: who appears,
who overlaps, who is missing. Order and counts are not preserved -
that is the trade you make for O(1) membership tests.
"""

import sys

from load_data import load_todos

DEFAULT_PATH = "data/todos.json"


def all_users(todos):
    """Every distinct userId in the data."""
    return {todo["userId"] for todo in todos}


def users_with_pending(todos):
    """Users who have at least one unfinished todo."""
    return {todo["userId"] for todo in todos if not todo["completed"]}


def users_with_completed(todos):
    """Users who have at least one finished todo."""
    return {todo["userId"] for todo in todos if todo["completed"]}


def users_all_completed(todos):
    """Users whose todos are ALL completed.

    Set difference: everyone, minus anyone with pending work.
    No counting needed - if you never appear in the pending set,
    every one of your todos is done.
    """
    return all_users(todos) - users_with_pending(todos)


def users_nothing_completed(todos):
    """Users who have not finished a single todo."""
    return all_users(todos) - users_with_completed(todos)


def users_mixed(todos):
    """Users with both finished and unfinished work."""
    return users_with_completed(todos) & users_with_pending(todos)

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    todos = load_todos(path)

    everyone = all_users(todos)
    pending = users_with_pending(todos)
    completed = users_with_completed(todos)
    done = users_all_completed(todos)
    idle = users_nothing_completed(todos)
    mixed = users_mixed(todos)

    print(f"Total todos:  {len(todos)}")
    print(f"Unique users: {len(everyone)}  {sorted(everyone)}")

    print("\n--- set operations ---")
    print(f"union        (completed | pending): {sorted(completed | pending)}")
    print(f"intersection (completed & pending): {sorted(mixed)}")
    print(f"difference   (all - pending):       {sorted(done)}")
    print(f"difference   (all - completed):     {sorted(idle)}")
    print(f"symmetric    (completed ^ pending): {sorted(completed ^ pending)}")

    print("\n--- who still has work to do? ---")
    print(f"Work remaining:    {sorted(pending) if pending else 'nobody'}")
    print(f"Fully finished:    {sorted(done) if done else 'none'}")
    print(f"Started nothing:   {sorted(idle) if idle else 'none'}")

    print("\n--- subset checks ---")
    print(f"pending subset of everyone: {pending <= everyone}")
    print(f"done and pending disjoint:  {done.isdisjoint(pending)}")

    assert done | pending == everyone
    assert done & pending == set()
    print("\nPartition check passed: done + pending covers everyone exactly once.")


if __name__ == "__main__":
    main()