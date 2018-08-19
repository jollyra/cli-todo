import unittest

from todo import TodoApp, Todo


class TestSorted(unittest.TestCase):
    def test_three_out_of_order(self):
        todo_app = TodoApp(None)
        todo1 = Todo(0, 'one', 1)
        todo2 = Todo(1, 'two', 3)
        todo3 = Todo(2, 'three', 2)
        todos = [todo1, todo2, todo3]
        self.assertEqual(todo_app.sorted(todos)[0], todo1)
        self.assertEqual(todo_app.sorted(todos)[1], todo3)
        self.assertEqual(todo_app.sorted(todos)[2], todo2)


class TestRecalculateOrdering(unittest.TestCase):
    def test_first_todo_removed(self):
        todo_app = TodoApp(None)
        todos = [Todo(1, 'two', 2), Todo(2, 'three', 3)]
        reordered_todos = todo_app.recalculate_ordering(todos)
        self.assertEqual(reordered_todos[0].ordering, 1)
        self.assertEqual(reordered_todos[1].ordering, 2)

    def test_no_todo_removed(self):
        todo_app = TodoApp(None)
        todos = [Todo(1, 'two', 1), Todo(2, 'three', 2)]
        reordered_todos = todo_app.recalculate_ordering(todos)
        self.assertEqual(reordered_todos[0].ordering, 1)
        self.assertEqual(reordered_todos[1].ordering, 2)

    def test_reorder_one_todo(self):
        todo_app = TodoApp(None)
        todos = [Todo(1, 'two', 2)]
        reordered_todos = todo_app.recalculate_ordering(todos)
        self.assertEqual(reordered_todos[0].ordering, 1)


if __name__ == '__main__':
    unittest.main()
