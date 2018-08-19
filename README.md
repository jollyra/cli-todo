# cli-todo

A Unix CLI todo app framework designed with the Git UI in mind.


```
> ./todo.py -h
usage: todo list [-h] [-a description | -d ordering | -l]

optional arguments:
  -h, --help                           show this help message and exit
  -a description, --add description    add a todo item to your todo list
  -d ordering, --delete ordering       delete a todo item from your todo list
  -l, --list                           show your todo list
  ```
  
## Requirements

* Install [Pyenv](https://github.com/pyenv/pyenv#basic-github-checkout)

## First Time Setup

You should only need to do these steps once:
```
git clone https://github.com/jollyra/cli-todo.git
cd cli-todo
pyenv install 3.6.3
pyenv local 3.6.3
python -m venv venv
source venv/bin/activate
pip install -U pip
```
## Development

Every time you work you should do these steps:
```
source venv/bin/activate
pip install -r requirements.txt
make test migrate
```
