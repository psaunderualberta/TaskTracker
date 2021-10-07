#! /usr/bin/env python


import sqlite3
import argparse
import sys


class TaskTracker():
    def __init__(self, add_tasks=[], delete_tasks=[], move_tasks=[], clear_tasks=False, shift_tasks=False, db="/p/psg/swip/w/psaunder/scripts/tasks/tasks.db"):
        self.conn = sqlite3.connect(db)

        self.add_tasks = add_tasks
        self.delete_tasks = delete_tasks
        self.move_tasks = move_tasks
        self.clear_tasks = clear_tasks
        self.shift_tasks = shift_tasks

        self.connect()

        self.tasks = self.read_tasks()

    def connect(self):
        self.c = self.conn.cursor()
        with open("/p/psg/swip/w/psaunder/scripts/tasks/schema.sql", "r") as schema:
            self.c.executescript(schema.read())

    def close(self):
        self.conn.commit()
        self.conn.close()

    def read_tasks(self):
        self.c.execute("SELECT title FROM tasks ORDER BY i ASC;")
        return [str(task[0]) for task in self.c.fetchall()]

    def write_tasks(self):
        tasks = [[str(title), str(i+1)] for i, title in enumerate(self.tasks)]
        self.c.execute("DELETE FROM tasks")
        self.c.executemany("INSERT INTO tasks VALUES (?, ?)", tasks)

    def run(self):
        if self.shift_tasks:
            self.shift()
        elif len(sys.argv) != 1:
            if self.delete_tasks:
                self.delete(self.delete_tasks)
            if self.add_tasks:
                self.add(self.add_tasks)
            if self.move_tasks:
                self.move(self.move_tasks)
            if self.clear_tasks:
                self.clear()

        self.write_tasks()
        self.show()
        self.close()

    def show(self):
        self.c.execute("SELECT i, title FROM tasks ORDER BY i ASC;")
        tasks = self.c.fetchall()
        if tasks:
            for index, title in tasks:
                print("%s. %s" % (index, title))
        else:
            print("No tasks currently active")

    def add(self, tasks):
        self.tasks.extend(tasks)
        print("Successfully added tasks %s" % (tasks))

    def delete(self, indexes):
        new_tasks = []
        deleted_tasks = []
        indexes = set(int(i) for i in indexes)  # Unique indices
        for i, task in enumerate(self.tasks):
            if i+1 not in indexes:
                new_tasks.append(task)
            else:
                deleted_tasks.append(task)

        self.tasks = new_tasks
        print("Successfully deleted tasks %s" % (deleted_tasks))

    def shift(self):
        self.tasks = self.tasks[1:] + self.tasks[:1]
        if self.tasks:
            print("Successfully shifted task '%s'" % (self.tasks[-1]))

    def move(self, moves):
        moves = [str(move) for move in moves]
        if len(moves) != 2 or any(not move.isdigit() for move in moves):
            raise ValueError(
                "Must provide two numbers for arguments to --move")
        moves = [int(move) for move in moves]
        if any(not (0 < move <= len(self.tasks)) for move in moves):
            raise ValueError(
                "Arguments for --move must be within bounds of current task list size (0 - size)")

        src, dest = moves
        src -= 1
        dest -= 1

        task = self.tasks[src]
        del self.tasks[src]
        self.tasks.insert(dest, task)

        print("Successfully moved %s from position %s to %s" %
              (task, src+1, dest+1))

    def clear(self):
        self.tasks = []


def check_args(args):
    if args.delete_tasks and args.move:
        raise ValueError(
            "You cannot delete tasks and move tasks at the same time. This leads to undefined behaviour.")


def run():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('--add_tasks', nargs='*',
                        help='Append one or more tasks to the list, in the order they are given')
    parser.add_argument('--delete_tasks', nargs='*',
                        help='Delete the tasks by referencing their index')
    parser.add_argument('--move', nargs="*",
                        help="Moves a task from one position to another (i.e. --move 1 2 moves task '1' to task '2')")
    parser.add_argument('--clear', action='store_true',
                        help="Deletes all tasks in database")
    parser.add_argument('--shift', action='store_true',
                        help="Moves the task at the front of the list to the back.")

    args = parser.parse_args()
    check_args(args)
    task_tracker = TaskTracker(
        args.add_tasks, args.delete_tasks, args.move, args.clear, args.shift)
    task_tracker.run()


if __name__ == "__main__":
    run()
