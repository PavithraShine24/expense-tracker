from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tkcalendar import DateEntry


users = {}

def clear_entries():
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)


def register_user():
    username = e1.get()
    email = e2.get()
    password = e3.get()
    
    if username and email and password:
        try:
           
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                      (username, email, password))
            conn.commit()
            messagebox.showinfo("Success", f"User '{username}' registered successfully!")
            switch_to_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Error", "Username or Email already exists.")
    else:
        messagebox.showwarning("Input Error", "Please fill out all fields.")

# Login function
def login():
    global username
    username = f1.get()
    password = f2.get()

  
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()

    if user:
        messagebox.showinfo("Login", f"Welcome, {username}!")
        welcome_page()
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")

def switch_to_login():
    registration_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)


def forgot_password():
    bad = tk.Toplevel(root)
    bad.title("Forgot Password")
    bad.geometry("300x150")

    mat = tk.Label(bad, text="Enter your email:")
    mat.pack(pady=10)

    global map
    map = tk.Entry(bad)
    map.pack(pady=5)

    def send_code():
        email = map.get()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()

        if user:
            messagebox.showinfo("Reset Code Sent", f"A code has been sent to {email}.")
            bad.destroy()
        else:
            messagebox.showerror("Error", "Email not found.")

    hep = tk.Button(bad, text="Send Code", command=send_code)
    hep.pack(pady=10)


def remember_me():
    if x.get():
        messagebox.showinfo("Remember Me", "Username will be remembered.")
    else:
        messagebox.showinfo("Remember Me", "Username will not be remembered.")



def main_page():
    global user_balance
    user_balance = 0
    win = tk.Tk()
    win.title("Expense Tracker")
    win.geometry("800x700")

    # Balance Frame - Top
    balance_frame = tk.Frame(win, bg="lavender", relief=tk.SUNKEN, bd=2)
    balance_frame.grid(row=0, column=0, padx=20, pady=10, columnspan=2, sticky="ew")

    balance_label = tk.Label(balance_frame, text="Set Initial Balance", font=("Helvetica", 12), bg="#f0f0f0")
    balance_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    balance_entry = ttk.Entry(balance_frame, width=20)
    balance_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    def set_balance():
        global user_balance
        try:
            user_balance = float(balance_entry.get())
            messagebox.showinfo("Balance Set", f"Balance set to: {user_balance:.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the balance.")

    set_balance_button = ttk.Button(balance_frame, text="Set Balance", command=set_balance)
    set_balance_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")


    expense_frame = tk.Frame(win, bg="pink", relief=tk.SUNKEN, bd=2)
    expense_frame.grid(row=1, column=0, padx=20, pady=10, columnspan=2, sticky="nsew")

    title_label = tk.Label(expense_frame, text="Expense Tracker", font=("Helvetica", 16), fg='white', bg='#3b3b3b')
    title_label.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

   
    input_frame = tk.Frame(expense_frame, bg="pink")
    input_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    
    desc_label = ttk.Label(input_frame, text="Category", background="#E0FFFF")
    desc_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    categories = ["Food", "Transport", "Entertainment", "Utilities"]
    category_combobox = ttk.Combobox(input_frame, values=categories, width=30)
    category_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

   
    amount_label = ttk.Label(input_frame, text="Amount", background="#E0FFFF")
    amount_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    e2 = ttk.Entry(input_frame, width=30)
    e2.grid(row=1, column=1, padx=10, pady=5, sticky="w")

   
    date_label = ttk.Label(input_frame, text="Date (Select)", background="#E0FFFF")
    date_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    

    e3 = DateEntry(input_frame, width=30, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    e3.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    def add_to_tree():
        description = category_combobox.get()
        amount = e2.get()
        date = e3.get()

        if description and amount and date:
            try:
                float(amount)
                tree.insert('', 'end', values=(description, amount, date))
                category_combobox.set('')
                e2.delete(0, tk.END)
                e3.set_date(datetime.today())  

                c.execute("INSERT INTO expenses (description, amount, date, username) VALUES (?, ?, ?, ?)",
                          (description, float(amount), date, username))
                conn.commit()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number for the amount.")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")


    def calculate_balance():
      try:
     
        conn = sqlite3.connect("expenses.db")
        c = conn.cursor()

        c.execute("SELECT balance FROM user_balance WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()

        if not result:
            messagebox.showerror("Balance Error", "Please set an initial balance first.")
            return

        user_balance = float(result[0])

        
        total_expense = 0
        for child in tree.get_children():
            total_expense += float(tree.item(child, 'values')[1])

        
        remaining_balance = max(0, user_balance - total_expense)

        messagebox.showinfo("Total Balance", f"Remaining Balance: {remaining_balance:.2f}")

      except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

      except ValueError:
        messagebox.showerror("Value Error", "Invalid data found in expenses or balance.")

    def delete_record():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            description = item['values'][0]
            amount = item['values'][1]
            date = item['values'][2]

            c.execute("DELETE FROM expenses WHERE description = ? AND amount = ? AND date = ? AND username=?",
                      (description, amount, date, username))
            conn.commit()

            tree.delete(selected_item)
        else:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")

    def display_history():
        for row in tree.get_children():
            tree.delete(row)

        c.execute("SELECT description, amount, date FROM expenses WHERE username = ?", (username,))
        rows = c.fetchall()

        for row in rows:
            tree.insert('', 'end', values=row)

    def plot_pie_chart():
     global username 

     if username is None:
        messagebox.showerror("Error", "No user is logged in.")
        return

     conn = sqlite3.connect("expenses.db")
     c = conn.cursor()
     
  
     c.execute("""
        SELECT strftime('%Y-%m', date) AS month, description, SUM(amount) 
        FROM expenses 
        WHERE username = ? 
        GROUP BY month, description 
        ORDER BY month
     """, (username,))
     data = c.fetchall()
     conn.close()
  
     if not data:
        messagebox.showinfo("Pie Chart Info", "No data available for chart.")
        return

    
     month_data = {}
     for row in data:
        month, description, amount = row
        if month not in month_data:
            month_data[month] = {}
        month_data[month][description] = amount

    # Plotting pie charts 
     for month, expenses in month_data.items():
        categories = list(expenses.keys())
        amounts = list(expenses.values())

        plt.figure(figsize=(8, 8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        plt.title(f'Expenses Breakdown by Category for {month}')
        plt.axis('equal')
        plt.show()

    def filter_expenses():
        for row in tree.get_children():
            tree.delete(row)

        query = "SELECT description, amount, date FROM expenses WHERE username = ?"
        params = [username]

        selected_range = date_range_combobox.get()

        if selected_range == "Last 1 Month":
            from_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
            to_date = datetime.today().strftime('%Y-%m-%d')
            query += " AND date BETWEEN ? AND ?"
            params.extend([from_date, to_date])
        elif selected_range == "Last 2 Months":
            from_date = (datetime.today() - timedelta(days=60)).strftime('%Y-%m-%d')
            to_date = datetime.today().strftime('%Y-%m-%d')
            query += " AND date BETWEEN ? AND ?"
            params.extend([from_date, to_date])
        elif selected_range == "Select Range":
            from_date = from_date_entry.get()
            to_date = to_date_entry.get()

            if from_date:
                try:
                    datetime.strptime(from_date, '%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Input Error", "From Date must be in YYYY-MM-DD format.")
                    return
            else:
                messagebox.showwarning("Input Error", "Please enter From Date.")
                return

            if to_date:
                try:
                    datetime.strptime(to_date, '%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Input Error", "To Date must be in YYYY-MM-DD format.")
                    return
            else:
                messagebox.showwarning("Input Error", "Please enter To Date.")
                return

            query += " AND date BETWEEN ? AND ?"
            params.extend([from_date, to_date])
        elif selected_range == "":
            pass
        else:
            messagebox.showwarning("Selection Error", "Please select a valid date range.")
            return

        filter_category = filter_category_combobox.get()
        if filter_category:
            query += " AND description = ?"
            params.append(filter_category)

        amount_limit = amount_limit_entry.get()
        if amount_limit:
            try:
                query += " AND amount <= ?"
                params.append(float(amount_limit))
            except ValueError:
                messagebox.showerror("Input Error", "Amount limit must be a number.")
                return

        c.execute(query, tuple(params))
        rows = c.fetchall()

        for row in rows:
            tree.insert('', 'end', values=row)

    # Buttons for actions 
    add_button = ttk.Button(expense_frame, text="Add Expense", command=add_to_tree)
    add_button.grid(row=2, column=0, padx=10, pady=10)

    calculate_button = ttk.Button(expense_frame, text="Calculate Balance", command=calculate_balance)
    calculate_button.grid(row=2, column=1, padx=10, pady=10)

    delete_button = ttk.Button(expense_frame, text="Delete Expense", command=delete_record)
    delete_button.grid(row=2, column=2, padx=10, pady=10)

    history_button = ttk.Button(expense_frame, text="View History", command=display_history)
    history_button.grid(row=2, column=3, padx=10, pady=10)

    plot_button = ttk.Button(expense_frame, text="Plot Pie Chart", command=plot_pie_chart)
    plot_button.grid(row=2, column=4, padx=10, pady=10)

    # Filter Frame
    filter_frame = tk.Frame(expense_frame, bg="lavender", relief=tk.SUNKEN, bd=2)
    filter_frame.grid(row=3, column=0, padx=20, pady=10, columnspan=5, sticky="ew")

    filter_title = tk.Label(filter_frame, text="Filter Expenses", font=("Helvetica", 16), bg="#3b3b3b", fg="white")
    filter_title.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

    date_range_label = ttk.Label(filter_frame, text="Date Range:", background="#E0FFFF")
    date_range_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    date_ranges = ["", "Last 1 Month", "Last 2 Months", "Select Range"]
    date_range_combobox = ttk.Combobox(filter_frame, values=date_ranges, state="readonly")
    date_range_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Function to enable/disable date entries 
    def update_date_entry_state(event):
        if date_range_combobox.get() == "Select Range":
            from_date_entry.config(state="normal")
            to_date_entry.config(state="normal")
        else:
            from_date_entry.config(state="disabled")
            to_date_entry.config(state="disabled")

    date_range_combobox.bind("<<ComboboxSelected>>", update_date_entry_state)

    # Date entries for filtering
    from_date_label = ttk.Label(filter_frame, text="From Date:", background="#E0FFFF")
    from_date_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    # Change from_date_entry to DateEntry
    from_date_entry = DateEntry(filter_frame, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', state="disabled")
    from_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    to_date_label = ttk.Label(filter_frame, text="To Date:", background="#E0FFFF")
    to_date_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")

    # Change to_date_entry to DateEntry
    to_date_entry = DateEntry(filter_frame, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', state="disabled")
    to_date_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")

    filter_category_label = ttk.Label(filter_frame, text="Category:", background="#E0FFFF")
    filter_category_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    filter_category_combobox = ttk.Combobox(filter_frame, values=categories, state="readonly")
    filter_category_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    amount_limit_label = ttk.Label(filter_frame, text="Amount Limit:", background="#E0FFFF")
    amount_limit_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    amount_limit_entry = ttk.Entry(filter_frame, width=20)
    amount_limit_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    filter_button = ttk.Button(filter_frame, text="Filter", command=filter_expenses)
    filter_button.grid(row=5, column=0, padx=10, pady=10, columnspan=4)

    #tree view
    tree = ttk.Treeview(expense_frame, columns=("Description", "Amount", "Date"), show='headings')
    tree.heading("Description", text="Description")
    tree.heading("Amount", text="Amount")
    tree.heading("Date", text="Date")

    # to center align
    tree.column("Description", anchor="center")
    tree.column("Amount", anchor="center")
    tree.column("Date", anchor="center")

    tree.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

    # Scrollbar
    scrollbar = ttk.Scrollbar(expense_frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=4, column=5, sticky='ns')
    tree.configure(yscroll=scrollbar.set)

    win.mainloop()




conn = sqlite3.connect('expenses.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (description TEXT, amount REAL, date TEXT)''')

try:
    c.execute("ALTER TABLE expenses ADD COLUMN username TEXT")
except sqlite3.OperationalError:
  
    pass

conn.commit()

root = tk.Tk()
root.title("Login")
root.geometry("400x300")

def edit_profile_page():
    edit_win = tk.Toplevel() 
    edit_win.title("Edit Profile")
    edit_win.geometry("400x300")  
    edit_win.config(bg="lavender")  

   
    edit_title = tk.Label(edit_win, text="Edit Profile", font=("Helvetica", 18, "bold"), 
                          bg="pink", fg="white", relief=tk.SOLID, padx=10, pady=10)
    edit_title.pack(pady=20)

   
    edit_frame = tk.Frame(edit_win, bg="lightblue", padx=20, pady=20)
    edit_frame.pack(pady=20)

    
    username_label = tk.Label(edit_frame, text="New Username", font=("Helvetica", 12), 
                              bg="lightblue", fg="black")
    username_label.grid(row=0, column=0, padx=10, pady=5)
    new_username_entry = tk.Entry(edit_frame, width=30)
    new_username_entry.grid(row=0, column=1, padx=10, pady=5)

    
    password_label = tk.Label(edit_frame, text="New Password", font=("Helvetica", 12), 
                              bg="lightblue", fg="black")
    password_label.grid(row=1, column=0, padx=10, pady=5)
    new_password_entry = tk.Entry(edit_frame, show="*", width=30)
    new_password_entry.grid(row=1, column=1, padx=10, pady=5)

    # update profile
    def update_profile():
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()

        if new_username and new_password:
            
            if new_username in users:
                messagebox.showwarning("Edit Error", f"Username '{new_username}' is already taken!")
            else:
                old_username = e1.get()  
                if old_username in users:
                    del users[old_username]  
                    users[new_username] = new_password  
                    messagebox.showinfo("Profile Updated", f"Profile updated to '{new_username}' successfully!")
                    edit_win.destroy()  
                else:
                    messagebox.showerror("Update Error", "User not found. Please log in again.")
        else:
            messagebox.showwarning("Input Error", "Please fill in both username and password")

    
    update_button = tk.Button(edit_frame, text="Update Profile", font=("Helvetica", 12, "bold"), 
                              bg="darkblue", fg="white", command=update_profile)
    update_button.grid(row=2, column=0, columnspan=2, pady=10)


    footer_label = tk.Label(edit_win, text="Update your credentials securely", 
                            font=("Helvetica", 10), bg="lavender", fg="darkblue")
    footer_label.pack(side=tk.BOTTOM, pady=10)

    welcome_page.config(menu=menubar)

def welcome_page():
    welcome_win = tk.Toplevel() 
    welcome_win.title("Welcome Page")
    welcome_win.geometry("800x600")
    welcome_win.config(bg="lavender")  

    welcome_label = tk.Label(welcome_win, text="WELCOME TO THE EXPENSE TRACKER", font=("Helvetica", 24, "bold"), 
                             bg="pink", fg="black", relief=tk.SOLID, padx=10, pady=20)
    welcome_label.pack(pady=40) 


    menubar = tk.Menu(welcome_win, bg="lightblue")

    
    file_menu = tk.Menu(menubar, tearoff=0, bg="lightblue", font=("Helvetica", 12))
    file_menu.add_command(label="Track Expense", command=lambda: [welcome_win.destroy(), main_page()]) 
    file_menu.add_command(label="Exit", command=welcome_win.quit)
    menubar.add_cascade(label="FILE", menu=file_menu)

    
    edit_menu = tk.Menu(menubar, tearoff=0, bg="lightblue", font=("Helvetica", 12))
    edit_menu.add_command(label="Edit Profile", command=edit_profile_page)  
    menubar.add_cascade(label="EDIT", menu=edit_menu)

 
    help_menu = tk.Menu(menubar, tearoff=0, bg="lightblue", font=("Helvetica", 12))
    help_menu.add_command(label="ABOUT", command=lambda: messagebox.showinfo("About", "Expense Tracker v1.0"))
    help_menu.add_command(label="HELP", command=lambda: messagebox.showinfo("Help", "For support, contact us at etsupportteam@outlook.com"))
    menubar.add_cascade(label="HELP", menu=help_menu)

    
    menubar.add_command(label="LOGOUT", command=lambda: [welcome_win.destroy(), root.deiconify()])  
    welcome_win.config(menu=menubar)

    # Footer 
    footer_label = tk.Label(welcome_win, text="Thank you for using Expense Tracker!", 
                            font=("Helvetica", 16), bg="lavender", fg="darkblue")
    footer_label.pack(side=tk.BOTTOM, pady=30)

# User Registration Frame
registration_frame = tk.Frame(root, bg="lightblue")
registration_frame.pack(fill="both", expand=True)

tk.Label(registration_frame, text="Register", font=("times new roman", 20)).pack(pady=10)
tk.Label(registration_frame, text="Name", font=("times new roman", 12)).pack(pady=5)
e1 = tk.Entry(registration_frame, width=30)
e1.pack(pady=5)

tk.Label(registration_frame, text="Email", font=("times new roman", 12)).pack(pady=5)
e2 = tk.Entry(registration_frame, width=30)
e2.pack(pady=5)

tk.Label(registration_frame, text="Password", font=("times new roman", 12)).pack(pady=5)
e3 = tk.Entry(registration_frame, show="*", width=30)
e3.pack(pady=5)

tk.Button(registration_frame, text="Register", command=register_user, font=("times new roman", 12), bg="blue", fg="white").pack(pady=15)
switch_login_label = tk.Label(registration_frame, text="Already have an account? Login here.", bg="lightblue", fg="blue" ,cursor="hand2")
switch_login_label.pack(pady=5)
switch_login_label.bind("<Button-1>", lambda e: switch_to_login())



login_frame = tk.Frame(root)

# Login labels and entries
tk.Label(login_frame, text="Login", font=("times new roman", 20)).pack(pady=10)
tk.Label(login_frame, text="Username:", font=("times new roman", 12)).pack(pady=5)
f1 = tk.Entry(login_frame, width=30)
f1.pack(pady=5)

tk.Label(login_frame, text="Password:", font=("times new roman", 12)).pack(pady=5)
f2 = tk.Entry(login_frame, show="*", width=30)
f2.pack(pady=5)

x = tk.IntVar()  
y = tk.Checkbutton(login_frame, text="Remember Me", variable=x, command=remember_me)
y.pack(pady=5)

tk.Button(login_frame, text="Login", command=login, font=("times new roman", 12), bg="blue", fg="white").pack(pady=10)
tk.Button(login_frame, text="Forgot Password?", command=forgot_password, font=("times new roman", 12), bg="lightgrey").pack(pady=5)

root.mainloop()


conn.close() 

