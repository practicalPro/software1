import tkinter as tk
from tkinter import messagebox

class ToDoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple To-Do List App")
        
        self.tasks = []
        self.task_entries = []
        self.task_history = []  # Store task history for undo
        self.filtered_tasks = []
        self.filter_var = tk.StringVar(value="All")
        self.create_widgets()

    #simple interfaces consists of the features needed for the add tasks: 3
    def create_widgets(self):
        
        self.task_entry = tk.Entry(self.master, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        #simple click for adding tasks: 1
        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=5, pady=10)

        #different organizing method (filter C/I/All): 8 
        self.filter_options = tk.OptionMenu(self.master, self.filter_var, "All", "Completed", "Incomplete", command=self.filter_tasks)
        self.filter_options.grid(row=0, column=2, padx=5, pady=10)

        #Undo backtracking: 5
        self.undo_button = tk.Button(self.master, text="Undo Add/Delete", command=self.undo_task)
        self.undo_button.grid(row=0, column=3, padx=5, pady=10)

        #clear path through tasks: 6
        self.instruction = tk.Label(self.master, text="Click on the check box to complete task")
        self.instruction.grid(row=1, column=0, padx=5, pady=10)

        
        self.task_list_frame = tk.Frame(self.master)
        self.task_list_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")

        #familiar feature of scroll bar and buttons: 4
        self.scrollbar = tk.Scrollbar(self.task_list_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.task_list_canvas = tk.Canvas(self.task_list_frame, yscrollcommand=self.scrollbar.set)
        self.task_list_canvas.pack(side="left", fill="both", expand=True)

        self.task_list = tk.Frame(self.task_list_canvas)
        self.task_list.pack(expand=True, fill="both")

        self.scrollbar.config(command=self.task_list_canvas.yview)

        self.task_list_canvas.create_window((0,0), window=self.task_list, anchor="nw")

        self.task_list.bind("<Configure>", self.on_frame_configure)

        # different approach to add task using enter key: 7
        self.master.bind('<Return>', lambda event: self.add_task())

    def on_frame_configure(self, event):
        self.task_list_canvas.configure(scrollregion=self.task_list_canvas.bbox("all"))

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.task_history.append(list(self.tasks))  # Save current tasks to history
            self.tasks.append({"text": task_text, "completed": False})
            self.task_entry.delete(0, tk.END)  # Clear the entry after adding task
            self.filter_tasks()

    def filter_tasks(self, *args):
        filter_value = self.filter_var.get()
        if filter_value == "All":
            self.filtered_tasks = self.tasks
        elif filter_value == "Completed":
            self.filtered_tasks = [task for task in self.tasks if task["completed"]]
        elif filter_value == "Incomplete":
            self.filtered_tasks = [task for task in self.tasks if not task["completed"]]
        self.display_tasks()

    def display_tasks(self):
        for widget in self.task_list.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.filtered_tasks):
            task_label = tk.Label(self.task_list, text=task["text"])
            task_label.grid(row=index, column=0, sticky="w")
            
            task_checkbutton = tk.Checkbutton(self.task_list, command=lambda index=index: self.complete_task(index))
            task_checkbutton.grid(row=index, column=1)
            task_checkbutton.select() if task["completed"] else task_checkbutton.deselect()
            
            delete_button = tk.Button(self.task_list, text="Delete", command=lambda index=index: self.confirm_delete(index))
            delete_button.grid(row=index, column=2)

    def complete_task(self, index):
        self.task_history.append(list(self.tasks))  # Save current tasks to history
        self.filtered_tasks[index]["completed"] = not self.filtered_tasks[index]["completed"]
        self.filter_tasks()

    #pop up messagebox to explain cost of using features: 2
    def confirm_delete(self, index):
        result = messagebox.askquestion("Confirm Delete", "Are you sure you want to delete this task?")
        if result == "yes":
            self.task_history.append(list(self.tasks))  # Save current tasks to history
            del self.tasks[self.tasks.index(self.filtered_tasks[index])]
            self.filter_tasks()

    def undo_task(self):
        if self.task_history:
            self.tasks = self.task_history.pop()  # Restore tasks from history
            self.filter_tasks()


def main():
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
