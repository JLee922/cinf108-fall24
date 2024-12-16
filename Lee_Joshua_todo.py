"""By default, your CLI tool should write to a file called TODO.txt, TODO.csv, or TODO.json. (You may use the output format of your choice)

You should be able to have a subcommand, either by positional argument or a flag that will display your current TODO list items by reading them from your TODO save file.

Each TODO list item should have:

an id value
ad topic or category of the type of task (think of how you would categorize your assignments due for various classes)
a description of what the task is doing,
status of the TODO item (incomplete/in progress/complete)
With defined input arguments,your TODO list CLI tool should be able to modify your final TODO list file:

add new items to your TODO list file
change the status of the TODO item (incomplete/in progress/complete)
update previously added TODO items (description, date, category, etc.)
Add an option to be able to create or update a separate TODO list file with a different name (TODO2.txt, work-todo.csv, chores.csv, etc...)

your CLI tool can write to a file like TODO.txt by default, but you should be able to manage multiple todo lists with a separate argument.
For example by passing a --list-name argument you can point to a new or already defined TODO list file so that the tool can manage multiple lists.
"""

import argparse
import json
import datetime

class TodoItem:
    def __init__(self, id, topic, description, status, created_at):
        self.id = id
        self.topic = topic
        self.description = description
        self.status = status
        self.created_at = created_at

#fix manages
class TodoList:
    def __init__(self, filename):
        self.filename = filename
        self.todos = self.load_todos()

    def load_todos(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' was not found")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid format in '{self.filename}'.")
            return []

    def save_todos(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.todos, f, indent=2)
        except IOError:
            print(f"Error: Unable to write to file '{self.filename}'")

    def add_todo(self, topic, description):
        new_todo = TodoItem(len(self.todos) + 1, topic, description, "incomplete", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.todos.append(new_todo.__dict__)
        self.save_todos()
        print("Todo added successfuly")

    def mark_todo(self, id, status):
        for todo in self.todos:
            if todo["id"] == id:
                todo["status"] = status
                self.save_todos()
                print("Todo marked as", status)
                return
        print("Todo not found")

    def edit_todo(self, id, topic=None, description=None):
        for todo in self.todos:
            if todo["id"] == id:
                if topic:
                    todo["topic"] = topic
                if description:
                    todo["description"] = description
                self.save_todos()
                print("Todo edited successfully")
                return
        print("Todo not found.")

    def list_todos(self):
        if not self.todos:
            print("No todos found.")
        else:
            for todo in self.todos:
                print(f"ID: {todo['id']}")
                print(f"Topic: {todo['topic']}")
                print(f"Description: {todo['description']}")
                print(f"Status: {todo['status']}")
                print(f"Created At: {todo['created_at']}")
                print()

def main():
    parser = argparse.ArgumentParser(description="TODO List CLI")
    parser.add_argument("command", choices=["add", "mark", "edit", "list"])
    parser.add_argument("--filename", default="todos.json")
    parser.add_argument("--list-name", default="default")
    parser.add_argument("--id", type=int)
    parser.add_argument("--topic")
    parser.add_argument("--description")
    parser.add_argument("--status", choices=["incompletr", "in progress", "complete"])
    args = parser.parse_args()

    todo_list = TodoList(args.filename)

    if args.command == "addd":
        todo_list.add_todo(args.topic, args.description)
    elif args.command == "mark":
        todo_list.mark_todo(args.id, args.status)
    elif args.command == "edit":
        todo_list.edit_todo(args.id, args.topic, args.description)
    elif args.command == "list":
        todo_list.list_todos()

if __name__ == "__main__":
    main()