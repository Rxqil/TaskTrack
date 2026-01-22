import json
import os


class Task:
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

    def mark_complete(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed
        }


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def add_task(self, title):
        self.tasks.append(Task(title))
        self.save_tasks()

    def view_tasks(self):
        if not self.tasks:
            print("\nNo tasks available.\n")
            return

        print("\nTasks:")
        for index, task in enumerate(self.tasks, start=1):
            status = "✔" if task.completed else "✖"
            print(f"{index}. {task.title} [{status}]")
        print()

    def complete_task(self, task_number):
        try:
            self.tasks[task_number - 1].mark_complete()
            self.save_tasks()
            print("Task marked as complete.\n")
        except IndexError:
            print("Invalid task number.\n")

    def delete_task(self, task_number):
        try:
            del self.tasks[task_number - 1]
            self.save_tasks()
            print("Task deleted.\n")
        except IndexError:
            print("Invalid task number.\n")

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.tasks = [Task(item["title"], item["completed"]) for item in data]
        except (json.JSONDecodeError, KeyError):
            print("Error loading task file. Starting with an empty list.\n")
            self.tasks = []


def main():
    manager = TaskManager()

    while True:
        print("TaskTrack - Task Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter task title: ")
            manager.add_task(title)

        elif choice == "2":
            manager.view_tasks()

        elif choice == "3":
            manager.view_tasks()
            number = int(input("Enter task number to complete: "))
            manager.complete_task(number)

        elif choice == "4":
            manager.view_tasks()
            number = int(input("Enter task number to delete: "))
            manager.delete_task(number)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.\n")


if __name__ == "__main__":
    main()
