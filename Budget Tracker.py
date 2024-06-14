import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Connect to the SQLite database
conn = sqlite3.connect('budget_tracker.db')
cursor = conn.cursor()

# Create tables if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    amount REAL,
    date TEXT,
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
''')

conn.commit()

# CRUD operations for categories
def add_category():
    name = simpledialog.askstring("Add Category", "Enter category name:")
    description = simpledialog.askstring("Add Category", "Enter category description:")
    
    if name and description:
        cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        messagebox.showinfo("Success", f"Category '{name}' added successfully.")
    else:
        messagebox.showerror("Error", "Please provide all details for the category.")

def update_category():
    category_id = simpledialog.askinteger("Update Category", "Enter category ID to update:")
    
    if category_id:
        cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
        category = cursor.fetchone()
        
        if category:
            name = simpledialog.askstring("Update Category", "Enter new category name:", initialvalue=category[1])
            description = simpledialog.askstring("Update Category", "Enter new category description:", initialvalue=category[2])
            
            if name and description:
                cursor.execute('''
                    UPDATE categories
                    SET name = ?, description = ?
                    WHERE id = ?
                ''', (name, description, category_id))
                conn.commit()
                messagebox.showinfo("Success", f"Category details updated successfully.")
            else:
                messagebox.showerror("Error", "Please provide all details for the category.")
        else:
            messagebox.showerror("Error", "Category ID not found.")

def delete_category():
    category_id = simpledialog.askinteger("Delete Category", "Enter category ID to delete:")
    
    if category_id:
        cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
        category = cursor.fetchone()
        
        if category:
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete category '{category[1]}'?")
            if confirm:
                cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Category '{category[1]}' deleted successfully.")
        else:
            messagebox.showerror("Error", "Category ID not found.")

def view_categories():
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    
    if categories:
        category_list = "\n\n".join([f"ID: {category[0]}, Name: {category[1]}, Description: {category[2]}" for category in categories])
        messagebox.showinfo("Categories List", category_list)
    else:
        messagebox.showinfo("Categories List", "No categories found.")

# CRUD operations for expenses
def add_expense():
    category_id = simpledialog.askinteger("Add Expense", "Enter category ID:")
    amount = simpledialog.askfloat("Add Expense", "Enter amount:")
    date = simpledialog.askstring("Add Expense", "Enter date (YYYY-MM-DD):")
    description = simpledialog.askstring("Add Expense", "Enter description:")
    
    if category_id and amount and date and description:
        cursor.execute('INSERT INTO expenses (category_id, amount, date, description) VALUES (?, ?, ?, ?)',
                       (category_id, amount, date, description))
        conn.commit()
        messagebox.showinfo("Success", f"Expense of {amount} added successfully.")
    else:
        messagebox.showerror("Error", "Please provide all details for the expense.")

def update_expense():
    expense_id = simpledialog.askinteger("Update Expense", "Enter expense ID to update:")
    
    if expense_id:
        cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
        expense = cursor.fetchone()
        
        if expense:
            category_id = simpledialog.askinteger("Update Expense", "Enter new category ID:", initialvalue=expense[1])
            amount = simpledialog.askfloat("Update Expense", "Enter new amount:", initialvalue=expense[2])
            date = simpledialog.askstring("Update Expense", "Enter new date (YYYY-MM-DD):", initialvalue=expense[3])
            description = simpledialog.askstring("Update Expense", "Enter new description:", initialvalue=expense[4])
            
            if category_id and amount and date and description:
                cursor.execute('''
                    UPDATE expenses
                    SET category_id = ?, amount = ?, date = ?, description = ?
                    WHERE id = ?
                ''', (category_id, amount, date, description, expense_id))
                conn.commit()
                messagebox.showinfo("Success", f"Expense details updated successfully.")
            else:
                messagebox.showerror("Error", "Please provide all details for the expense.")
        else:
            messagebox.showerror("Error", "Expense ID not found.")

def delete_expense():
    expense_id = simpledialog.askinteger("Delete Expense", "Enter expense ID to delete:")
    
    if expense_id:
        cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
        expense = cursor.fetchone()
        
        if expense:
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete expense ID: {expense_id}?")
            if confirm:
                cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Expense ID: {expense_id} deleted successfully.")
        else:
            messagebox.showerror("Error", "Expense ID not found.")

def view_expenses():
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    
    if expenses:
        expense_list = "\n\n".join([f"ID: {expense[0]}, Category ID: {expense[1]}, Amount: {expense[2]}, Date: {expense[3]}, Description: {expense[4]}" for expense in expenses])
        messagebox.showinfo("Expenses List", expense_list)
    else:
        messagebox.showinfo("Expenses List", "No expenses found.")

# GUI setup
root = tk.Tk()
root.title("Budget Tracker")

# Applying ttk style
style = ttk.Style()
style.configure('TButton', font=('Arial', 12), padding=10)
style.configure('TLabel', font=('Arial', 14))
style.configure('TFrame', background='#f0f0f0')  # Light gray background for frames
style.configure('TLabelFrame.Label', font=('Arial', 16), foreground='#333333')  # Dark gray label for frames

# Main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill='both', expand=True)

# Category operations frame
category_frame = ttk.LabelFrame(main_frame, text="Category Operations", padding="10")
category_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

add_category_button = ttk.Button(category_frame, text="Add Category", command=add_category)
add_category_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

update_category_button = ttk.Button(category_frame, text="Update Category", command=update_category)
update_category_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

delete_category_button = ttk.Button(category_frame, text="Delete Category", command=delete_category)
delete_category_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

view_categories_button = ttk.Button(category_frame, text="View Categories", command=view_categories)
view_categories_button.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

# Expense operations frame
expense_frame = ttk.LabelFrame(main_frame, text="Expense Operations", padding="10")
expense_frame.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

add_expense_button = ttk.Button(expense_frame, text="Add Expense", command=add_expense)
add_expense_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

update_expense_button = ttk.Button(expense_frame, text="Update Expense", command=update_expense)
update_expense_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

delete_expense_button = ttk.Button(expense_frame, text="Delete Expense", command=delete_expense)
delete_expense_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

view_expenses_button = ttk.Button(expense_frame, text="View Expenses", command=view_expenses)
view_expenses_button.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

root.mainloop()

# Close the database connection
conn.close()
