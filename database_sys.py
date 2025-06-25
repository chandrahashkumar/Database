from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import mysql.connector
import login

root =Tk()
root.title('DataBase')
root.iconbitmap('data_icon.ico')
root.geometry("400x600")

#Database connection
conn = mysql.connector.connect(
    host ='localhost',
    user = 'root',
    password = login.password,
    database ='universitydb'
)

cur = conn.cursor()
'''
cur.execute("""CREATE TABLE sudb(
        PRN VARCHAR(12) PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100),
        email_id VARCHAR(100) NOT NULL,
        mobile_number BIGINT NOT NULL,
        address TEXT NOT NULL

)""")

'''
# Create Edit function to update a record
def update():
    conn = mysql.connector.connect(
    host ='localhost',
    user = 'root',
    password = login.password,
    database ='universitydb')
    # CURSOR
    cur = conn.cursor()

    record_id = delete_box.get()
    cur.execute(f"""UPDATE sudb SET 
        first_name = '{first_name.get()}',
        last_name = '{last_name.get()}',
        email_id = '{email_id.get()}',
        mobile_number = {mobile_number.get()},
        address = '{address.get()}'

        WHERE PRN = '{record_id}' """,
    
    )

    conn.commit()
    #Close Connection
    conn.close()

    editor.destroy()

def edit():
    global editor
    editor =Tk()
    editor.title('Update a Record')
    editor.iconbitmap('data_icon.ico')
    editor.geometry("400x300")

    conn = mysql.connector.connect(
    host ='localhost',
    user = 'root',
    password = login.password,
    database ='universitydb')
    # CURSOR
    cur = conn.cursor()

    record_id = delete_box.get()
    # Query the database
    cur.execute("SELECT * FROM sudb WHERE PRN =" + record_id)
    records = cur.fetchall()

    # Create global variables for text box
    global PRN
    global first_name
    global last_name
    global email_id
    global mobile_number
    global address

    # text box
    PRN = Entry(editor, width= 30)
    PRN.grid(row=0, column=1, padx=20, pady=(10,0))
    first_name = Entry(editor, width=30)
    first_name.grid(row=1, column=1, padx=20)
    last_name = Entry(editor, width=30)
    last_name.grid(row=2, column=1, padx=20)
    email_id = Entry(editor, width=30)
    email_id.grid(row=3, column=1, padx = 20)
    mobile_number = Entry(editor, width=30)
    mobile_number.grid(row=4, column=1, padx = 20)
    address = Entry(editor, width=30)
    address.grid(row=5, column=1, padx = 20)

    # label
    prn_label = Label(editor, text="PRN")
    prn_label.grid(row = 0, column = 0, pady=(10,0))
    f_name_label = Label(editor, text="First Name")
    f_name_label.grid(row = 1, column = 0)
    l_name_label = Label(editor, text="Last Name")
    l_name_label.grid(row = 2, column = 0)
    email_label = Label(editor, text="Email ID")
    email_label.grid(row = 3, column = 0)
    phone_no_label = Label(editor, text="Mobile Number")
    phone_no_label.grid(row = 4, column = 0)
    address_label = Label(editor, text="Full Address")
    address_label.grid(row = 5, column = 0)

    # Loop thru results
    for record in records:
        PRN.insert(0, record[0])
        first_name.insert(0, record[1])
        last_name.insert(0, record[2])
        email_id.insert(0, record[3])
        mobile_number.insert(0, record[4])
        address.insert(0, record[5])

    # Create a Save Button to edited record
    save_button = Button(editor, text='Save Record', command=update, fg='white', bg='green')
    save_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx = 145)

# Create function to delete a record
def delete():
    conn = mysql.connector.connect(
    host ='localhost',
    user = 'root',
    password = login.password,
    database ='universitydb')
    # CURSOR
    cur = conn.cursor()

    # Delete a record
    cur.execute("DELETE FROM sudb WHERE PRN =" + delete_box.get())

    delete_box.delete(0, END)

    conn.commit()
    #Close Connection
    conn.close()

# Create Submit Function

def submit():
    conn = mysql.connector.connect(
    host ='localhost',
    user = 'root',
    password = login.password,
    database ='universitydb')
    # CURSOR
    cur = conn.cursor()
    # Insert Into Table
    cur.execute(f"INSERT INTO sudb(PRN, first_name, last_name, email_id, mobile_number, address) VALUES ('{PRN.get()}','{first_name.get()}', '{last_name.get()}', '{email_id.get()}', '{int(mobile_number.get())}', '{address.get()}')")
    #Commit Change
    conn.commit()
    #Close Connection
    conn.close()

    # Clear the text box
    PRN.delete(0,END)
    first_name.delete(0, END)
    last_name.delete(0, END)
    email_id.delete(0, END)
    mobile_number.delete(0, END)
    address.delete(0, END)

# Create query function
def query():
    conn = mysql.connector.connect(
    host ='localhost',
    user = 'root',
    password = login.password,
    database ='universitydb')
    # CURSOR
    cur = conn.cursor()

    # Query the database
    cur.execute("SELECT * FROM sudb")

    # Table show on screen

    tree =ttk.Treeview(root)
    tree['show'] = 'headings'

    # Style
    s = ttk.Style(root)
    s.theme_use('clam')

    s.configure(".", font=('Helvetica', 11))
    s.configure("Treeview.Heading", foreground='blue', font= ('Helvetica', 11, "bold"))

    # columns
    tree["columns"] = ('PRN', 'first_name', 'last_name', 'email_id', 'mobile_number', 'address')

    # Assign the width, minwidth and anchor to the respective columns
    tree.column("PRN", width=100, minwidth=150, anchor=CENTER)
    tree.column("first_name", width=100, minwidth=150, anchor=CENTER)
    tree.column("last_name", width=100, minwidth=150, anchor=CENTER)
    tree.column("email_id", width=200, minwidth=300, anchor=CENTER)
    tree.column("mobile_number", width=100, minwidth=150, anchor=CENTER)
    tree.column("address", width=250, minwidth=400, anchor=CENTER)

    # Assign the heading names to the respective columns
    tree.heading("PRN", text="PRN", anchor=CENTER)
    tree.heading("first_name", text="first_name", anchor=CENTER)
    tree.heading("last_name", text="last_name", anchor=CENTER)
    tree.heading("email_id", text="email_id", anchor=CENTER)
    tree.heading("mobile_number", text="mobile_number", anchor=CENTER)
    tree.heading("address", text="address", anchor=CENTER)

    i =0
    for ro in cur:
        tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5]))
        i = i + 1
    
    horizontal = ttk.Scrollbar(root, orient="horizontal")
    horizontal.configure(command=tree.xview)
    tree.configure(xscrollcommand=horizontal.set)
    horizontal.grid(row=13, column=0, columnspan=2, sticky="ew")
    tree.grid(row=12, column=0, columnspan=2, pady=10)

    #Commit Change
    conn.commit()
    #Close Connection
    conn.close()

# text box
PRN = Entry(root, width= 30)
PRN.grid(row=0, column=1, padx=20, pady=(10,0))
first_name = Entry(root, width=30)
first_name.grid(row=1, column=1, padx=20)
last_name = Entry(root, width=30)
last_name.grid(row=2, column=1, padx=20)
email_id = Entry(root, width=30)
email_id.grid(row=3, column=1, padx = 20)
mobile_number = Entry(root, width=30)
mobile_number.grid(row=4, column=1, padx = 20)
address = Entry(root, width=30)
address.grid(row=5, column=1, padx = 20)
delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

# label
prn_label = Label(root, text="PRN")
prn_label.grid(row = 0, column = 0, pady=(10,0))
f_name_label = Label(root, text="First Name")
f_name_label.grid(row = 1, column = 0)
l_name_label = Label(root, text="Last Name")
l_name_label.grid(row = 2, column = 0)
email_label = Label(root, text="Email ID")
email_label.grid(row = 3, column = 0)
phone_no_label = Label(root, text="Mobile Number")
phone_no_label.grid(row = 4, column = 0)
address_label = Label(root, text="Full Address")
address_label.grid(row = 5, column = 0)
delete_box_label = Label(root, text='Select PRN')
delete_box_label.grid(row=9, column=0, pady=5)

#Create Submit Button

submit_btn = Button(root, text='Add Record To Database', command =submit, fg='white', bg ='green')
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx =103)

# Create a Query Button
query_button = Button(root, text='Show Record', command=query)
query_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx = 135)

# Create a Delete Button
delete_button = Button(root, text='Delete Record', command=delete,fg = 'black',bg = 'red')
delete_button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx = 135)

# Create an Update Button
edit_button = Button(root, text='Edit Record', command=edit, fg ='black', bg ='yellow')
edit_button.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx = 141)


conn.commit()

conn.close()

root.mainloop()