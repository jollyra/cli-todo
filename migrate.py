#!/usr/bin/env python3


import sqlite3


def drop_tables(conn):
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS todo;
    """)


def create_db(conn):
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            ordering INTEGER NOT NULL
        );
    """)


if __name__ == '__main__':
    conn = sqlite3.connect('todo.db')
    drop_tables(conn)
    create_db(conn)
