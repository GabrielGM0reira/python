import datetime
import sqlite3
from tkcalendar import DateEntry
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk

# Connecting to the Database
connector = sqlite3.connect("expense_Tracker.db")
cursor = connector.cursor()
connector.execute(
  'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)'
)

connector.commit()

# Modern Color Scheme
PRIMARY_COLOR = '#1e3a8a'        # Dark Blue
SECONDARY_COLOR = '#3b82f6'      # Bright Blue
ACCENT_COLOR = '#10b981'         # Green
LIGHT_BG = '#f8fafc'             # Light gray
DARK_TEXT = '#1e293b'            # Dark text
BORDER_COLOR = '#e2e8f0'         # Light border
WARNING_COLOR = '#ef4444'        # Red

# Fonts
title_font = ('Segoe UI', 18, 'bold')
header_font = ('Segoe UI', 12, 'bold')
label_font = ('Segoe UI', 11)
entry_font = ('Segoe UI', 11)
btn_font = ('Segoe UI', 11, 'bold')
small_font = ('Segoe UI', 9)

# Initializing the GUI window
root = Tk()
root.title('💰 Smart Expense Tracker')
root.geometry('1300x700')
root.resizable(0, 0)
root.configure(bg=LIGHT_BG)

# Custom title bar
title_frame = Frame(root, bg=PRIMARY_COLOR, height=60)
title_frame.pack(side=TOP, fill=X)
Label(title_frame, text='💰 Smart Expense Tracker', font=title_font, bg=PRIMARY_COLOR, 
      fg='white', pady=15).pack(side=LEFT, padx=20)

# StringVar and DoubleVar variables
desc = StringVar()
amnt = DoubleVar()
payee = StringVar()
MoP = StringVar(value='Cash')

# ===== FUNCTION DEFINITIONS =====
def list_all_expenses():
  global connector, table
  table.delete(*table.get_children())
  all_data = connector.execute('SELECT * FROM ExpenseTracker')
  data = all_data.fetchall()
  for values in data:
     table.insert('', END, values=values)

def view_expense_details():
  global table
  global date, payee, desc, amnt, MoP
  if not table.selection():
     mb.showerror('No expense selected', 'Please select an expense from the table to view its details')
     return
  current_selected_expense = table.item(table.focus())
  values = current_selected_expense['values']
  expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))
  date.set_date(expenditure_date) ; payee.set(values[2]) ; desc.set(values[3]) ; amnt.set(values[4]) ; MoP.set(values[5])

def clear_fields():
  global desc, payee, amnt, MoP, date, table
  today_date = datetime.datetime.now().date()
  desc.set('') ; payee.set('') ; amnt.set(0.0) ; MoP.set('Cash'); date.set_date(today_date)
  table.selection_remove(*table.selection())

def remove_expense():
  if not table.selection():
     mb.showerror('No record selected!', 'Please select a record to delete!')
     return
  current_selected_expense = table.item(table.focus())
  values_selected = current_selected_expense['values']
  surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')
  if surety:
     connector.execute('DELETE FROM ExpenseTracker WHERE ID=?', (values_selected[0],))
     connector.commit()
     list_all_expenses()
     mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')

def remove_all_expenses():
  surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')
  if surety:
     table.delete(*table.get_children())
     connector.execute('DELETE FROM ExpenseTracker')
     connector.commit()
     clear_fields()
     list_all_expenses()
     mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
  else:
     mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')

def add_another_expense():
  global date, payee, desc, amnt, MoP
  global connector
  if not date.get() or not payee.get() or not desc.get() or not amnt.get() or not MoP.get():
     mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
  else:
     connector.execute(
     'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
     (date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get())
     )
     connector.commit()
     clear_fields()
     list_all_expenses()
     mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')

def edit_expense():
  global table
  def edit_existing_expense():
     global date, amnt, desc, payee, MoP
     global connector, table
     current_selected_expense = table.item(table.focus())
     contents = current_selected_expense['values']
     connector.execute('UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
                       (date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get(), contents[0]))
     connector.commit()
     clear_fields()
     list_all_expenses()
     mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
     edit_btn.destroy()
     return
  if not table.selection():
     mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
     return
  view_expense_details()
  edit_btn = Button(left_panel, text='💾 Save Changes', font=btn_font,
                    bg='#059669', fg='white', relief=FLAT, bd=0, cursor='hand2',
                    activebackground='#059669', command=edit_existing_expense)
  edit_btn.pack(fill=X, pady=5)

def selected_expense_to_words():
  global table
  if not table.selection():
     mb.showerror('No expense selected!', 'Please select an expense from the table for us to read')
     return
  current_selected_expense = table.item(table.focus())
  values = current_selected_expense['values']
  message = f'Your expense can be read like: \n"You paid {values[4]} to {values[2]} for {values[3]} on {values[1]} via {values[5]}"'
  mb.showinfo('Here\'s how to read your expense', message)

def expense_to_words_before_adding():
  global date, desc, amnt, payee, MoP
  if not payee.get() or not desc.get() or amnt.get() == 0.0 or not MoP.get():
     mb.showerror('Incomplete data', 'The data is incomplete, meaning fill all the fields first!')
     return
  message = f'Your expense can be read like: \n"You paid {amnt.get()} to {payee.get()} for {desc.get()} on {date.get_date()} via {MoP.get()}"'
  add_question = mb.askyesno('Read your record like: ', f'{message}\n\nShould I add it to the database?')
  if add_question:
     add_another_expense()
  else:
     mb.showinfo('Ok', 'Please take your time to add this record')

def create_styled_button(parent, text, command, bg_color, fg_color='white', icon=''):
    btn = Button(parent, text=icon + ' ' + text, command=command, font=btn_font, 
                 bg=bg_color, fg=fg_color, relief=FLAT, bd=0, cursor='hand2',
                 activebackground=bg_color, activeforeground=fg_color, padx=15, pady=10)
    return btn

# ===== END FUNCTION DEFINITIONS =====

# Main container frame
main_container = Frame(root, bg=LIGHT_BG)
main_container.pack(fill=BOTH, expand=True, padx=0, pady=0)

# Left Panel - Data Entry
left_panel = Frame(main_container, bg='white', relief=FLAT)
left_panel.pack(side=LEFT, fill=BOTH, padx=15, pady=15, expand=False)

# Title for left panel
entry_title = Label(left_panel, text='📝 New Expense', font=header_font, bg='white', fg=PRIMARY_COLOR)
entry_title.pack(pady=(0, 20))

# Date frame
date_frame = Frame(left_panel, bg='white')
date_frame.pack(fill=X, pady=8)
Label(date_frame, text='📅 Date', font=label_font, bg='white', fg=DARK_TEXT).pack(anchor=W)
date = DateEntry(date_frame, date=datetime.datetime.now().date(), font=entry_font, 
                 foreground=DARK_TEXT, background=SECONDARY_COLOR, headersforeground='white',
                 normalforeground=DARK_TEXT, weekendforeground=DARK_TEXT)
date.pack(fill=X, pady=(5, 0))

# Description frame
desc_frame = Frame(left_panel, bg='white')
desc_frame.pack(fill=X, pady=8)
Label(desc_frame, text='📋 Description', font=label_font, bg='white', fg=DARK_TEXT).pack(anchor=W)
desc_entry = Entry(desc_frame, font=entry_font, textvariable=desc, relief=FLAT, bd=0, 
                   bg='#f1f5f9', fg=DARK_TEXT, insertbackground=SECONDARY_COLOR)
desc_entry.pack(fill=X, pady=(5, 0), ipady=8, padx=8)
desc_entry.configure(highlightbackground=BORDER_COLOR, highlightthickness=1)

# Payee frame
payee_frame = Frame(left_panel, bg='white')
payee_frame.pack(fill=X, pady=8)
Label(payee_frame, text='👤 Payee', font=label_font, bg='white', fg=DARK_TEXT).pack(anchor=W)
payee_entry = Entry(payee_frame, font=entry_font, textvariable=payee, relief=FLAT, bd=0,
                    bg='#f1f5f9', fg=DARK_TEXT, insertbackground=SECONDARY_COLOR)
payee_entry.pack(fill=X, pady=(5, 0), ipady=8, padx=8)
payee_entry.configure(highlightbackground=BORDER_COLOR, highlightthickness=1)

# Amount frame
amount_frame = Frame(left_panel, bg='white')
amount_frame.pack(fill=X, pady=8)
Label(amount_frame, text='💵 Amount', font=label_font, bg='white', fg=DARK_TEXT).pack(anchor=W)
amount_entry = Entry(amount_frame, font=entry_font, textvariable=amnt, relief=FLAT, bd=0,
                     bg='#f1f5f9', fg=DARK_TEXT, insertbackground=SECONDARY_COLOR, width=15)
amount_entry.pack(fill=X, pady=(5, 0), ipady=8, padx=8)
amount_entry.configure(highlightbackground=BORDER_COLOR, highlightthickness=1)

# Mode of Payment frame
mop_frame = Frame(left_panel, bg='white')
mop_frame.pack(fill=X, pady=8)
Label(mop_frame, text='💳 Payment Method', font=label_font, bg='white', fg=DARK_TEXT).pack(anchor=W)
dd1 = OptionMenu(mop_frame, MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay', 'Razorpay'])
dd1.pack(fill=X, pady=(5, 0), padx=8)
dd1.configure(font=entry_font, bg='#f1f5f9', fg=DARK_TEXT, relief=FLAT, bd=0, 
              highlightbackground=BORDER_COLOR, highlightthickness=1)

# Separator
ttk.Separator(left_panel, orient=HORIZONTAL).pack(fill=X, pady=15)

# Action buttons for left panel
add_btn = create_styled_button(left_panel, 'Add Expense', add_another_expense, ACCENT_COLOR, 'white', '➕')
add_btn.pack(fill=X, pady=5)

convert_btn = create_styled_button(left_panel, 'Preview Before Adding', expense_to_words_before_adding, SECONDARY_COLOR, 'white', '👁️')
convert_btn.pack(fill=X, pady=5)

clear_btn = create_styled_button(left_panel, 'Clear Fields', clear_fields, '#64748b', 'white', '🗑️')
clear_btn.pack(fill=X, pady=5)

# Right Panel - Data Display
right_panel = Frame(main_container, bg=LIGHT_BG)
right_panel.pack(side=RIGHT, fill=BOTH, expand=True, padx=0, pady=15)

# Buttons frame at top of right panel
buttons_frame = Frame(right_panel, bg='white', relief=FLAT)
buttons_frame.pack(fill=X, padx=15, pady=(0, 15))

# Row 1 of buttons
row1_frame = Frame(buttons_frame, bg='white')
row1_frame.pack(fill=X, pady=5)
create_styled_button(row1_frame, 'View Details', view_expense_details, SECONDARY_COLOR).pack(side=LEFT, padx=5)
create_styled_button(row1_frame, 'Edit Expense', edit_expense, PRIMARY_COLOR).pack(side=LEFT, padx=5)
create_styled_button(row1_frame, 'Read as Text', selected_expense_to_words, '#7c3aed').pack(side=LEFT, padx=5)

# Row 2 of buttons
row2_frame = Frame(buttons_frame, bg='white')
row2_frame.pack(fill=X, pady=5)
create_styled_button(row2_frame, 'Delete Selected', remove_expense, '#f97316').pack(side=LEFT, padx=5)
create_styled_button(row2_frame, 'Delete All', remove_all_expenses, WARNING_COLOR).pack(side=LEFT, padx=5)

# Table frame
tree_frame = Frame(right_panel, bg='white', relief=FLAT)
tree_frame.pack(fill=BOTH, expand=True, padx=15)

# Configure Treeview Style
style = ttk.Style()
style.theme_use('clam')
style.configure('Treeview', 
                font=(entry_font[0], 10),
                rowheight=25,
                background='#f8fafc',
                fieldbackground='#f8fafc',
                foreground=DARK_TEXT)
style.configure('Treeview.Heading', 
                font=(label_font[0], 11, 'bold'),
                background=PRIMARY_COLOR,
                foreground='white')
style.map('Treeview', 
          background=[('selected', SECONDARY_COLOR)],
          foreground=[('selected', 'white')])

# Treeview Frame
table = ttk.Treeview(tree_frame, selectmode=BROWSE, columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment'), height=15)
X_Scroller = Scrollbar(tree_frame, orient=HORIZONTAL, command=table.xview)
Y_Scroller = Scrollbar(tree_frame, orient=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)
table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

# Configure column headings
table.heading('#0', text='')
table.heading('ID', text='ID')
table.heading('Date', text='📅 Date')
table.heading('Payee', text='👤 Payee')
table.heading('Description', text='📋 Description')
table.heading('Amount', text='💵 Amount')
table.heading('Mode of Payment', text='💳 Payment')

# Configure column widths
table.column('#0', width=0, stretch=NO)
table.column('ID', width=40, anchor=CENTER)
table.column('Date', width=100, anchor=CENTER)
table.column('Payee', width=120, anchor=W)
table.column('Description', width=300, anchor=W)
table.column('Amount', width=100, anchor=E)
table.column('Mode of Payment', width=120, anchor=CENTER)

table.pack(fill=BOTH, expand=True)
list_all_expenses()
# Finalizing the GUI window
root.update()
root.mainloop()