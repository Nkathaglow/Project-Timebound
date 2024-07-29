import tkinter as tk
from tkinter import ttk, messagebox
from main import tasks, add_task, delete_task, mark_task_complete, edit_task, sort_by_due_date, sort_by_name

root = tk.Tk()
root.title("Timebound App")
root.geometry("700x500+400+100")
root.resizable(False, False)

# Function to refresh the Treeview
def refresh_treeview():
    for i in treeview.get_children():
        treeview.delete(i)
    for i, task in enumerate(tasks):
        status = "✓" if task.get('completed', False) else " "
        treeview.insert('', 'end', iid=i, values=(status, task['name'], task['due_date']))

# Function to add a task
def add_task_gui():
    task_name = task_entry.get()
    due_date = due_date_entry.get()
    if add_task(task_name, due_date):
        messagebox.showinfo("Success", "Task added successfully!")
        refresh_treeview()
    else:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")

# Function to delete a task
def delete_task_gui():
    selected_item = treeview.selection()
    if selected_item:
        selected_index = int(selected_item[0])
        if delete_task(selected_index):
            messagebox.showinfo("Success", "Task deleted successfully!")
            refresh_treeview()
        else:
            messagebox.showerror("Error", "Task not found.")
    else:
        messagebox.showerror("Error", "No task selected.")

# Function to mark a task as complete
def mark_complete_gui():
    selected_item = treeview.selection()
    if selected_item:
        selected_index = int(selected_item[0])
        if mark_task_complete(selected_index):
            messagebox.showinfo("Success", f"Task '{tasks[selected_index]['name']}' marked as complete!")
            refresh_treeview()
        else:
            messagebox.showerror("Error", "Task not found.")
    else:
        messagebox.showerror("Error", "No task selected.")

# Function to edit a task
def edit_task_gui():
    selected_item = treeview.selection()
    if selected_item:
        selected_index = int(selected_item[0])
        new_name = task_entry.get()
        new_due_date = due_date_entry.get()
        task = edit_task(selected_index, new_name, new_due_date)
        if task:
            messagebox.showinfo("Success", f"Task updated to '{task['name']}' (Due: {task['due_date']})")
            refresh_treeview()
        else:
            messagebox.showerror("Error", "Task not found.")
    else:
        messagebox.showerror("Error", "No task selected.")

# Function to sort tasks by due date
def sort_by_due_date_gui():
    sort_by_due_date()
    refresh_treeview()

# Function to sort tasks by name
def sort_by_name_gui():
    sort_by_name()
    refresh_treeview()

# Creating the task input frame
task_frame = tk.Frame(root)
task_frame.pack(pady=10)

tk.Label(task_frame, text="Task:").grid(row=0, column=0, padx=5)
task_entry = tk.Entry(task_frame)
task_entry.grid(row=0, column=1, padx=5)

tk.Label(task_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5)
due_date_entry = tk.Entry(task_frame)
due_date_entry.grid(row=1, column=1, padx=5)

tk.Button(task_frame, text="Add Task", command=add_task_gui).grid(row=2, column=0, padx=5, pady=5, sticky='ew')
tk.Button(task_frame, text="Delete Task", command=delete_task_gui).grid(row=2, column=1, padx=5, pady=5, sticky='ew')
tk.Button(task_frame, text="Mark Complete", command=mark_complete_gui).grid(row=2, column=2, padx=5, pady=5, sticky='ew')
tk.Button(task_frame, text="Edit Task", command=edit_task_gui).grid(row=2, column=3, padx=5, pady=5, sticky='ew')

tk.Button(task_frame, text="Sort by Due Date", command=sort_by_due_date_gui).grid(row=3, column=0, padx=5, pady=5, sticky='ew')
tk.Button(task_frame, text="Sort by Name", command=sort_by_name_gui).grid(row=3, column=1, padx=5, pady=5, sticky='ew')

task_frame.grid_columnconfigure(0, weight=1)
task_frame.grid_columnconfigure(1, weight=1)
task_frame.grid_columnconfigure(2, weight=1)
task_frame.grid_columnconfigure(3, weight=1)

# Creating the Treeview frame
treeview_frame = tk.Frame(root, bd=3, width=700, height=280, bg="#32405b")
treeview_frame.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

# Creating the Treeview widget
treeview = ttk.Treeview(treeview_frame, columns=("Status", "Task", "Due Date"), show='headings', selectmode='browse')
treeview.heading("Status", text="Status")
treeview.heading("Task", text="Task")
treeview.heading("Due Date", text="Due Date")
treeview.column("Status", width=50, anchor='center')
treeview.column("Task", width=400, anchor='w')
treeview.column("Due Date", width=200, anchor='center')

treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Adding a scrollbar to the Treeview
scrollbar = tk.Scrollbar(treeview_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
treeview.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=treeview.yview)

# Initial population of the Treeview
refresh_treeview()

root.mainloop()
