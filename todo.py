#!/usr/bin/env python3


import argparse
import sqlite3
from collections import namedtuple


Todo = namedtuple('Todo', ['id', 'description', 'ordering', 'priority'])


class TodoApp:
    def __init__(self, todo_repo):
        self.repo = todo_repo

    def run(self, args):
        if args.add:
            self.add(args.add[0], args.add[1])
        elif args.delete:
            self.delete(args.delete)
        elif args.summary:
            self.summary()
        self.list()

    def add(self, description, priority, ordering=None):
        if not ordering:
            ordering = self.repo.count_todos() + 1
        self.repo.save(description, ordering, priority)

    def delete(self, ordering):
        self.repo.delete(ordering)
        todos = self.repo.find_all()
        todos = self.recalculate_ordering(todos)
        for todo in todos:
            self.repo.update_ordering(todo.id, todo.ordering)

    def list(self):
        print('\nTodo List')
        todos = self.repo.find_all()
        for todo in self.sorted(todos):
            print('{}. {} | priority={}'.format(todo.ordering, todo.description, todo.priority))

    def summary(self):
        todos = self.repo.find_all()
        priorities = {}
        for todo in todos:
            p = todo.priority
            if p not in priorities:
                priorities[p] = 1
            else:
                priorities[p] += 1

        print('\nSummary')
        for k, v in priorities.items():
            print('# of priority {}: {}'.format(k, v))

        missing_priorities = self.find_missing_priorities(priorities)
        print('missing priorities', missing_priorities)

    def recalculate_ordering(self, todos):
        reordered_todos = []
        for count, todo in enumerate(self.sorted(todos), start=1):
            reordered_todos.append(Todo(todo.id, todo.description, count, todo.priority))
        return reordered_todos

    def sorted(self, todos):
        return sorted(todos, key=lambda x: x.ordering)

    def find_missing_priorities(self, priorities):
        keys = priorities.keys()
        if not len(keys):
            return []
        min_priority = min(keys)
        max_priority = max(keys)
        missing = []
        for i in range(min_priority, max_priority + 1):
            if i not in keys:
                missing.append(i)
        return missing


class TodoRepository:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')

    def find_all(self):
        c = self.conn.cursor()
        c.execute(""" SELECT id, description, ordering, priority FROM todo """)
        self.conn.commit()
        return [Todo(id=row[0], description=row[1], ordering=row[2], priority=row[3]) for row in c]

    def save(self, description, ordering, priority):
        c = self.conn.cursor()
        c.execute(""" INSERT INTO todo (description, ordering, priority) VALUES (?, ?, ?) """
                  , (description, ordering, priority))
        self.conn.commit()

    def delete(self, ordering):
        c = self.conn.cursor()
        c.execute(""" DELETE FROM todo WHERE ordering = ? """, (ordering,))
        self.conn.commit()

    def count_todos(self):
        c = self.conn.cursor()
        c.execute(""" SELECT COUNT(*) FROM todo """)
        self.conn.commit()
        return c.fetchone()[0]

    def update_ordering(self, id, ordering):
        c = self.conn.cursor()
        c.execute(""" UPDATE todo SET ordering=? where id=?""", (ordering, id))
        self.conn.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('todo list')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', nargs=2, metavar='description', help='add a todo item to you list')
    group.add_argument('-d', '--delete', metavar='ordering', type=int, help='delete a todo item from you list')
    group.add_argument('-l', '--list', action='store_true', help='show todo list')
    group.add_argument('--summary', action='store_true', help='show the count of each priority level')
    args = parser.parse_args()

    todo_repo = TodoRepository()
    app = TodoApp(todo_repo)
    app.run(args)
