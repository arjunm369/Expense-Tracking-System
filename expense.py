import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from tkinter import font
from datetime import datetime

# Custom Colors and Fonts
BG_COLOR = "#f4f4f4"  # Background color
PRIMARY_COLOR = "#4caf50"  # Primary button color
TEXT_COLOR = "#333"  # Text color
FONT_NAME = "Helvetica"

# Define a reusable font
HEADER_FONT = (FONT_NAME, 16, "bold")
LABEL_FONT = (FONT_NAME, 12)
ENTRY_FONT = (FONT_NAME, 12)




# MySQL Database Connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="expense_tracker_db"
)
cursor = db_connection.cursor()

# Global Variables
current_user_id = None
current_username = None


# Function to Add Categories (Admin Page)
def add_category():
    category = new_category_entry.get()
    if not category:
        messagebox.showwarning("Warning", "Category cannot be empty!")
        return

    try:
        # Insert category associated with the current user
        cursor.execute(
            "INSERT INTO categories (name, user_id) VALUES (%s, %s)", 
            (category, current_user_id)
        )
        db_connection.commit()
        messagebox.showinfo("Success", "Category added successfully!")
        admin_window.destroy()
        refresh_categories()
    except mysql.connector.errors.IntegrityError as e:
        if e.errno == 1062:  # Duplicate entry error
            messagebox.showerror("Error", f"Category '{category}' already exists for your account!")
        else:
            messagebox.showerror("Error", str(e))



# Admin Page



# View Total Expense
def view_total_expense():
    from_date = from_date_entry.get()
    to_date = to_date_entry.get()
    try:
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE user_id = %s AND date BETWEEN %s AND %s",
            (current_user_id, from_date, to_date)
        )
        total = cursor.fetchone()[0]
        total_label.config(text=f"Total Expenses: Rs{total:.2f}" if total else "Total Expenses: Rs0.00")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# View Expenses by Category or All
def view_expenses_by_category():
    category = category_filter_combobox.get()
    from_date = from_date_entry.get()
    to_date = to_date_entry.get()

    try:
        # Clear previous results
        for item in expenses_tree.get_children():
            expenses_tree.delete(item)

        # Build the SQL query dynamically based on filters
        query = "SELECT date, category, description, amount FROM expenses WHERE user_id = %s"
        params = [current_user_id]

        if category and category != "Others":
            query += " AND category = %s"
            params.append(category)
        elif category == "Others":
            query += " AND category LIKE 'Others%'"

        # Apply date range only if both dates are provided
        if from_date and to_date:
            query += " AND date BETWEEN %s AND %s"
            params.extend([from_date, to_date])

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        for row in records:
            expenses_tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", str(e))

#
def view_expenses_by_range():
    from_date = from_date_range_entry.get()
    to_date = to_date_range_entry.get()

    if not from_date or not to_date:
        messagebox.showwarning("Warning", "Both From Date and To Date are required!")
        return

    try:
        # Clear previous results
        for item in range_tree.get_children():
            range_tree.delete(item)

        # Query expenses by date range
        query = """
            SELECT date, category, description, amount 
            FROM expenses 
            WHERE user_id = %s AND date BETWEEN %s AND %s
        """
        cursor.execute(query, (current_user_id, from_date, to_date))
        records = cursor.fetchall()

        for row in records:
            range_tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Fetch Categories for Dropdown
def fetch_categories():
    try:
        cursor.execute(
            "SELECT DISTINCT name FROM categories WHERE user_id IS NULL OR user_id = %s", 
            (current_user_id,)
        )
        categories = [row[0] for row in cursor.fetchall()]
        # Include "Others" only if not already present
        if "Others" not in categories:
            categories.append("Others")
        return categories
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []





def refresh_categories():
    categories = fetch_categories()
    category_combobox["values"] = categories
    category_filter_combobox["values"] = categories



# Logout User
def logout_user(app):
    global current_user_id, current_username
    current_user_id = None
    current_username = None
    app.destroy()
    show_login_window()


# Login User
def login_user():
    global current_user_id, current_username
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showwarning("Warning", "Username and Password are required!")
        return

    try:
        cursor.execute("SELECT id, username FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            current_user_id, current_username = user
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            show_main_app()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Register User
import re
from datetime import datetime

# Register User with Validation
def register_user():
    username = reg_username_entry.get().strip()
    password = reg_password_entry.get().strip()
    email = reg_email_entry.get().strip()
    dob = reg_dob_entry.get().strip()
    job = reg_job_entry.get().strip()

    # Validate username
    if not username:
        messagebox.showwarning("Warning", "Username is required!")
        return

    # Validate password
    if len(password) < 8:
        messagebox.showwarning("Warning", "Password must be at least 8 characters long!")
        return
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password) :
        messagebox.showwarning("Warning", "Password must contain letters, numbers!")
        return

    # Validate email
    if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
        messagebox.showwarning("Warning", "Invalid email address!")
        return

    # Validate Date of Birth
    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        if dob_date >= datetime.now():
            messagebox.showwarning("Warning", "Date of Birth cannot be today or a future date!")
            return
    except ValueError:
        messagebox.showwarning("Warning", "Invalid Date of Birth! Use format YYYY-MM-DD.")
        return

    # Validate job
    if not job:
        messagebox.showwarning("Warning", "Job field is required!")
        return

    # Save user to the database
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email, dob, job) VALUES (%s, %s, %s, %s, %s)",
            (username, password, email, dob, job)
        )
        db_connection.commit()
        messagebox.showinfo("Success", "Registration successful!")
        registration_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", str(e))



# Add Expense
def add_expense():
    date = date_entry.get()
    category = category_combobox.get()
    custom_category = category_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()

    if not date or not amount:
        messagebox.showwarning("Warning", "Date and Amount are required!")
        return

    if category == "Others":
        if not custom_category:
            messagebox.showwarning("Warning", "Please specify a custom category for 'Others'.")
            return
        category = f"Others({custom_category})"

        # Ensure the custom category exists for the current user
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM categories WHERE name = %s AND user_id = %s", 
                (category, current_user_id)
            )
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO categories (name, user_id) VALUES (%s, %s)", 
                    (category, current_user_id)
                )
                db_connection.commit()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

    try:
        # Insert the expense
        cursor.execute(
            "INSERT INTO expenses (user_id, date, category, description, amount) VALUES (%s, %s, %s, %s, %s)",
            (current_user_id, date, category, description, float(amount))
        )
        db_connection.commit()
        messagebox.showinfo("Success", "Expense added successfully!")
        clear_entries()
        refresh_categories()
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Clear Entries
def clear_entries():
    date_entry.delete(0, tk.END)
    category_combobox.set("")
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


# Registration Window
def show_registration_window():
    global reg_username_entry, reg_password_entry, reg_email_entry, reg_dob_entry, reg_job_entry, registration_window

    registration_window = tk.Toplevel()
    registration_window.title("Register")
    registration_window.geometry("300x300")

    tk.Label(registration_window, text="Username").pack()
    reg_username_entry = tk.Entry(registration_window)
    reg_username_entry.pack()

    tk.Label(registration_window, text="Password").pack()
    reg_password_entry = tk.Entry(registration_window, show="*")
    reg_password_entry.pack()

    tk.Label(registration_window, text="Email").pack()
    reg_email_entry = tk.Entry(registration_window)
    reg_email_entry.pack()

    tk.Label(registration_window, text="Date of Birth (YYYY-MM-DD)").pack()
    reg_dob_entry = tk.Entry(registration_window)
    reg_dob_entry.pack()

    tk.Label(registration_window, text="Job").pack()
    reg_job_entry = tk.Entry(registration_window)
    reg_job_entry.pack()

    tk.Button(registration_window, text="Register", command=register_user).pack(pady=10)


# Main Application
def show_main_app():
    global from_date_entry, to_date_entry, category_filter_combobox, total_label, expenses_tree
    global date_entry, category_combobox, description_entry, amount_entry, category_entry
    global from_date_range_entry, to_date_range_entry, range_tree

    app = tk.Tk()
    app.title("Expense Tracker")
    app.geometry("700x900")  # Increased height to accommodate new section

    tk.Label(app, text=f"Welcome, {current_username}!", font=("Helvetica", 14)).pack(pady=5)
    tk.Button(app, text="Logout", command=lambda: logout_user(app)).pack(pady=5)

    # Add Expense Section
    tk.Label(app, text="Add Expense", font=("Helvetica", 14)).pack(pady=10)
    tk.Label(app, text="Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(app)
    date_entry.pack()

    tk.Label(app, text="Category").pack()
    categories = fetch_categories()
    category_combobox = ttk.Combobox(app, values=categories)
    category_combobox.pack()

    # Add dynamic entry for custom category
    category_entry = tk.Entry(app)
    category_entry.pack()
    category_entry.config(state="disabled")

    def on_category_select(event):
        if category_combobox.get() == "Others":
            category_entry.config(state="normal")
        else:
            category_entry.config(state="disabled")

    category_combobox.bind("<<ComboboxSelected>>", on_category_select)

    tk.Label(app, text="Description").pack()
    description_entry = tk.Entry(app)
    description_entry.pack()

    tk.Label(app, text="Amount").pack()
    amount_entry = tk.Entry(app)
    amount_entry.pack()

    tk.Button(app, text="Add Expense", command=add_expense).pack(pady=10)

    # View Expenses Section
    tk.Label(app, text="View Expenses", font=("Helvetica", 14)).pack(pady=10)
    tk.Label(app, text="From Date (YYYY-MM-DD)").pack()
    from_date_entry = tk.Entry(app)
    from_date_entry.pack()

    tk.Label(app, text="To Date (YYYY-MM-DD)").pack()
    to_date_entry = tk.Entry(app)
    to_date_entry.pack()

    tk.Button(app, text="View Total Expense", command=view_total_expense).pack(pady=5)
    total_label = tk.Label(app, text="Total Expenses: Rs0.00", font=("Helvetica", 12))
    total_label.pack()

    tk.Label(app, text="Category").pack()
    category_filter_combobox = ttk.Combobox(app, values=categories)
    category_filter_combobox.pack()

    tk.Button(app, text="View Expenses", command=view_expenses_by_category).pack(pady=5)

    # Expenses Table
    expenses_tree = ttk.Treeview(app, columns=("Date", "Category", "Description", "Amount"), show="headings")
    expenses_tree.heading("Date", text="Date")
    expenses_tree.heading("Category", text="Category")
    expenses_tree.heading("Description", text="Description")
    expenses_tree.heading("Amount", text="Amount")
    expenses_tree.pack(fill=tk.BOTH, expand=True)

    # New Section: View by Date Range
    tk.Label(app, text="View Expenses by Date Range", font=("Helvetica", 14)).pack(pady=10)

    tk.Label(app, text="From Date (YYYY-MM-DD)").pack()
    from_date_range_entry = tk.Entry(app)
    from_date_range_entry.pack()

    tk.Label(app, text="To Date (YYYY-MM-DD)").pack()
    to_date_range_entry = tk.Entry(app)
    to_date_range_entry.pack()

    tk.Button(app, text="View Expenses by Range", command=view_expenses_by_range).pack(pady=5)

    # Date Range Table
    range_tree = ttk.Treeview(app, columns=("Date", "Category", "Description", "Amount"), show="headings")
    range_tree.heading("Date", text="Date")
    range_tree.heading("Category", text="Category")
    range_tree.heading("Description", text="Description")
    range_tree.heading("Amount", text="Amount")
    range_tree.pack(fill=tk.BOTH, expand=True)

    # Admin Section
    

    app.mainloop()



# Login Window
def show_login_window():
    global login_username_entry, login_password_entry, login_window

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username").pack()
    login_username_entry = tk.Entry(login_window)
    login_username_entry.pack()

    tk.Label(login_window, text="Password").pack()
    login_password_entry = tk.Entry(login_window, show="*")
    login_password_entry.pack()

    tk.Button(login_window, text="Login", command=login_user).pack(pady=10)
    tk.Button(login_window, text="Register", command=show_registration_window).pack(pady=10)

    login_window.mainloop()


# Start the application
if __name__ == "__main__":
    show_login_window()