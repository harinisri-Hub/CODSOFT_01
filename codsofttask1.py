import pickle
import tkinter as tk
from tkinter import messagebox

# Task Class Definition
class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.description}"

# ToDoList Class Definition
class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        task = Task(description)
        self.tasks.append(task)

    def list_tasks(self):
        return "\n".join(f"{i + 1}. {task}" for i, task in enumerate(self.tasks))

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
        else:
            raise IndexError("Invalid task number.")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
        else:
            raise IndexError("Invalid task number.")

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.tasks, f)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.tasks = pickle.load(f)
        except FileNotFoundError:
            self.tasks = []

# CLI Functions
def print_menu():
    print("\nTo-Do List Application")
    print("1. Add a new task")
    print("2. List all tasks")
    print("3. Mark a task as completed")
    print("4. Delete a task")
    print("5. Exit")

def cli_main(todo_list):
    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            description = input("Enter the task description: ")
            todo_list.add_task(description)
        elif choice == "2":
            print(todo_list.list_tasks())
        elif choice == "3":
            index = int(input("Enter the task number to mark as completed: ")) - 1
            try:
                todo_list.complete_task(index)
            except IndexError as e:
                print(e)
        elif choice == "4":
            index = int(input("Enter the task number to delete: ")) - 1
            try:
                todo_list.delete_task(index)
            except IndexError as e:
                print(e)
        elif choice == "5":
            todo_list.save_to_file('tasks.pkl')
            break
        else:
            print("Invalid choice, please try again.")

# GUI Application
class ToDoApp:
    def __init__(self, root, todo_list):
        self.root = root
        self.root.title("To-Do List")
        self.todo_list = todo_list

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.task_entry = tk.Entry(self.frame, width=50)
        self.task_entry.pack(side=tk.LEFT)

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        self.tasks_listbox = tk.Listbox(root, width=50, height=20)
        self.tasks_listbox.pack()

        self.complete_button = tk.Button(root, text="Mark as Completed", command=self.complete_task)
        self.complete_button.pack()

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        self.update_tasks_listbox()

    def add_task(self):
        description = self.task_entry.get()
        if description:
            self.todo_list.add_task(description)
            self.task_entry.delete(0, tk.END)
            self.update_tasks_listbox()

    def complete_task(self):
        try:
            index = self.tasks_listbox.curselection()[0]
            self.todo_list.complete_task(index)
            self.update_tasks_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "No task selected.")

    def delete_task(self):
        try:
            index = self.tasks_listbox.curselection()[0]
            self.todo_list.delete_task(index)
            self.update_tasks_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "No task selected.")

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.todo_list.tasks:
            self.tasks_listbox.insert(tk.END, str(task))

# Main Function
def main():
    todo_list = ToDoList()
    todo_list.load_from_file('tasks.pkl')

    mode = input("Choose mode (cli/gui): ").strip().lower()
    
    if mode == "cli":
        cli_main(todo_list)
    elif mode == "gui":
        root = tk.Tk()
        app = ToDoApp(root, todo_list)
        root.mainloop()
        todo_list.save_to_file('tasks.pkl')
    else:
        print("Invalid mode selected. Please choose either 'cli' or 'gui'.")

if __name__ == "__main__":
    main()
