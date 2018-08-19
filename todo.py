#!/usr/bin/env python3


import argparse
import sqlite3
from collections import namedtuple


Todo = namedtuple('Todo', ['id', 'description', 'ordering'])


class TodoApp:
    def __init__(self, todo_repo):
        self.repo = todo_repo

    def run(self, args):
        if args.add:
            self.add(args.add)
        elif args.delete:
            self.delete(args.delete)
        self.list()

    def add(self, description, ordering=None):
        if not ordering:
            ordering = self.repo.count_todos() + 1
        self.repo.save(description, ordering)

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
            print('{}. {}'.format(todo.ordering, todo.description))

    def recalculate_ordering(self, todos):
        reordered_todos = []
        for count, todo in enumerate(self.sorted(todos), start=1):
            reordered_todos.append(Todo(todo.id, todo.description, count))
        return reordered_todos

    def sorted(self, todos):
        return sorted(todos, key=lambda x: x.ordering)


class TodoRepository:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')

    def find_all(self):
        c = self.conn.cursor()
        c.execute(""" SELECT id, description, ordering FROM todo """)
        self.conn.commit()
        return [Todo(id=row[0], description=row[1], ordering=row[2]) for row in c]

    def save(self, description, ordering):
        c = self.conn.cursor()
        c.execute(""" INSERT INTO todo (description, ordering) VALUES (?, ?) """, (description, ordering))
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
    group.add_argument('-a', '--add', metavar='description', help='add a todo item to you list')
    group.add_argument('-d', '--delete', metavar='ordering', type=int, help='delete a todo item from you list')
    group.add_argument('-l', '--list', action='store_true', help='show todo list')
    args = parser.parse_args()

    todo_repo = TodoRepository()
    app = TodoApp(todo_repo)
    app.run(args)
