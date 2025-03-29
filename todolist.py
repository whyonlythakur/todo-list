import tkinter as tk

# Create Main Window
root = tk.Tk()
root.title("To-Do List App")
root.geometry("700x500")  # Default window size

# --- Functionality ---

def add_task(event=None):
    """Add task to the To-Do list."""
    task_text = task_entry.get().strip()
    if task_text:
        var = tk.IntVar()
        checkbox = tk.Checkbutton(todo_frame, text=task_text, variable=var)
        checkbox.var = var  # Store IntVar in the checkbox
        checkbox.pack(anchor="w", padx=5, pady=2)
        task_entry.delete(0, tk.END)
        update_task_numbers()
        update_scroll()

def mark_completed():
    """Move selected tasks to the Completed section."""
    for widget in todo_frame.winfo_children():
        if isinstance(widget, tk.Checkbutton) and widget.var.get():
            widget.pack_forget()
            var = tk.IntVar()
            completed_checkbox = tk.Checkbutton(completed_frame, text=widget.cget("text"), variable=var)
            completed_checkbox.var = var
            completed_checkbox.pack(anchor="w", padx=5, pady=2)
    update_task_numbers()
    update_scroll()

def move_to_todo():
    """Move selected tasks back to To-Do."""
    for widget in completed_frame.winfo_children():
        if isinstance(widget, tk.Checkbutton) and widget.var.get():
            widget.pack_forget()
            var = tk.IntVar()
            todo_checkbox = tk.Checkbutton(todo_frame, text=widget.cget("text"), variable=var)
            todo_checkbox.var = var
            todo_checkbox.pack(anchor="w", padx=5, pady=2)
    update_task_numbers()
    update_scroll()

def delete_selected():
    """Delete selected tasks from both sections."""
    for frame in [todo_frame, completed_frame]:
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Checkbutton) and widget.var.get():
                widget.pack_forget()
    update_task_numbers()
    update_scroll()

def clear_completed():
    """Clear all tasks from the Completed section."""
    for widget in completed_frame.winfo_children():
        widget.pack_forget()
    update_scroll()

def delete_all():
    """Delete all tasks from both sections."""
    for frame in [todo_frame, completed_frame]:
        for widget in frame.winfo_children():
            widget.pack_forget()
    update_task_numbers()
    update_scroll()

def select_all(frame):
    """Select all checkboxes in a given section."""
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Checkbutton):
            if not hasattr(widget, "var"):
                widget.var = tk.IntVar()  # Ensure every checkbox has an IntVar
            widget.var.set(1)  # Select all

def update_task_numbers():
    """Reorder task numbers in To-Do and Completed sections."""
    for i, widget in enumerate(todo_frame.winfo_children(), start=1):
        if isinstance(widget, tk.Checkbutton):
            widget.config(text=f"{i}. {widget.cget('text').split('. ', 1)[-1]}")

    for i, widget in enumerate(completed_frame.winfo_children(), start=1):
        if isinstance(widget, tk.Checkbutton):
            widget.config(text=f"{i}. {widget.cget('text').split('. ', 1)[-1]}")

def update_scroll():
    """Update the scroll region for both sections."""
    todo_canvas.update_idletasks()
    todo_canvas.configure(scrollregion=todo_canvas.bbox("all"))
    completed_canvas.update_idletasks()
    completed_canvas.configure(scrollregion=completed_canvas.bbox("all"))

# --- UI Layout ---

# Task Entry
task_entry = tk.Entry(root, width=50)
task_entry.pack(pady=5)
task_entry.bind("<Return>", add_task)  # Bind "Enter" key to add task

# Task Sections (To-Do & Completed)
task_container = tk.Frame(root)
task_container.pack(fill="both", expand=True, padx=10, pady=10)

# To-Do Section with Scrollbar
todo_container = tk.Frame(task_container)
todo_container.pack(side="left", fill="both", expand=True, padx=10, pady=10)

todo_label = tk.Label(todo_container, text="To-Do Tasks", font=("Arial", 12, "bold"))
todo_label.pack()

select_all_todo = tk.Button(todo_container, text="Select All", command=lambda: select_all(todo_frame))
select_all_todo.pack(pady=5)

todo_canvas = tk.Canvas(todo_container)
todo_scrollbar = tk.Scrollbar(todo_container, orient="vertical", command=todo_canvas.yview)
todo_frame = tk.Frame(todo_canvas)

todo_canvas.create_window((0, 0), window=todo_frame, anchor="nw")
todo_canvas.configure(yscrollcommand=todo_scrollbar.set)

todo_canvas.pack(side="left", fill="both", expand=True)
todo_scrollbar.pack(side="right", fill="y")

# Completed Section with Scrollbar
completed_container = tk.Frame(task_container)
completed_container.pack(side="right", fill="both", expand=True, padx=10, pady=10)

completed_label = tk.Label(completed_container, text="Completed Tasks", font=("Arial", 12, "bold"))
completed_label.pack()

select_all_completed = tk.Button(completed_container, text="Select All", command=lambda: select_all(completed_frame))
select_all_completed.pack(pady=5)

completed_canvas = tk.Canvas(completed_container)
completed_scrollbar = tk.Scrollbar(completed_container, orient="vertical", command=completed_canvas.yview)
completed_frame = tk.Frame(completed_canvas)

completed_canvas.create_window((0, 0), window=completed_frame, anchor="nw")
completed_canvas.configure(yscrollcommand=completed_scrollbar.set)

completed_canvas.pack(side="left", fill="both", expand=True)
completed_scrollbar.pack(side="right", fill="y")

# Footer Menu (Responsive)
footer_frame = tk.Frame(root)
footer_frame.pack(side="bottom", fill="x", padx=10, pady=10)
footer_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

mark_completed_button = tk.Button(footer_frame, text="Mark Completed", command=mark_completed)
mark_completed_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

move_to_todo_button = tk.Button(footer_frame, text="Move to To-Do", command=move_to_todo)
move_to_todo_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

delete_button = tk.Button(footer_frame, text="Delete Selected", command=delete_selected)
delete_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

clear_completed_button = tk.Button(footer_frame, text="Clear Completed", command=clear_completed)
clear_completed_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

delete_all_button = tk.Button(footer_frame, text="Delete All", command=delete_all)
delete_all_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

# Run the Application
root.mainloop()
