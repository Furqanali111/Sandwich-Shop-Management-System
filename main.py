import tkinter as tk
import sqlite3
import os



# global vaiables
root = tk.Tk()
root.title("Sandwichshop")
root.geometry("500x500")
db_file = 'sandwich_shop.db'

root.minsize(500, 500)
root.maxsize(500, 500)

startwin = tk.Frame(root)
adminframe = tk.Frame(root)
customerframe = tk.Frame(root)
viewframe = tk.Frame(root)
addtomenu = tk.Frame(root)
deleteframe = tk.Frame(root)
viewframecus = tk.Frame(root)
customermenuframe = tk.Frame(root)
viewframeorder = tk.Frame(root)
createorderframe = tk.Frame(root)
updateframecus = tk.Frame(root)
delereorderframe=tk.Frame(root)

def startwind():
    adminbut = tk.Button(startwin, text="Admin Menu", fg="black", height=2, width=20,
                         command=lambda: adminwinstart(adminframe))
    adminbut.pack(pady=20)

    customerbut = tk.Button(startwin, text="Customer Menu", fg="black", height=2, width=20,
                            command=lambda: gotocustomer(customerframe))
    customerbut.pack()


def adminwinstart(fram):
    if startwin.winfo_ismapped():  # if frame 1 is visible
        startwin.pack_forget()  # hide frame 1
        adminframed()
        fram.pack(pady=80, )  # show frame 2


def gobactostart(frame):
    if frame.winfo_ismapped():
        frame.pack_forget()
        startwin.pack(pady=150)
        for widget in frame.winfo_children():
            widget.destroy()


def gobacktoadmin(frame):
    if frame.winfo_ismapped():  # if frame 1 is visible
        frame.pack_forget()  # hide frame 1
        adminframe.pack(pady=80)  # show frame 2
    for widget in frame.winfo_children():
        widget.destroy()


def adminframed():
    Viewmenu = tk.Button(adminframe, text="View Menu", fg="black", height=2, width=20,
                         command=lambda: gotoview(adminframe))
    Viewmenu.pack(pady=20)

    addmenu = tk.Button(adminframe, text="Add to Menu", fg="black", height=2, width=20, command=lambda: gotoaddmenu())
    addmenu.pack(pady=20)

    delmenu = tk.Button(adminframe, text="Delete From Menu", fg="black", height=2, width=20,
                        command=lambda: gotodelmenu())
    delmenu.pack(pady=20)

    goback = tk.Button(adminframe, text="GoBack", fg="black", height=2, width=20,
                       command=lambda: gobactostart(adminframe))
    goback.pack(pady=20)


def gotodelmenu():
    if adminframe.winfo_ismapped():
        adminframe.pack_forget()
        for widget in deleteframe.winfo_children():
            widget.destroy()
        deleteitem()
        deleteframe.pack(fill="both", expand=True, pady=10)
    else:
        deleteitem()
        deleteframe.pack(fill="both", expand=True, pady=10)


def deleteitem():
    menu_items = conn.execute('SELECT id, name, price FROM menu2')

    canvas = tk.Canvas(deleteframe)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(deleteframe, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True)

    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    label = tk.Label(inner_frame, text='Menu', font=("Arial", 10))
    label.pack()
    for item in menu_items:
        label = tk.Label(inner_frame, text=f'{item[0]}. {item[1]} - ${item[2]}')
        label.pack(pady=2, anchor="nw")

    label = tk.Label(inner_frame, text='Enter id of item you want to delete: ', font=("Arial", 12))
    label.pack(pady=5, anchor="nw")

    delentry = tk.Entry(inner_frame)
    delentry.pack()

    but = tk.Button(inner_frame, text="DELETE", height=2, width=15, command=lambda: deleteite(delentry))
    but.pack(pady=5)

    but1 = tk.Button(inner_frame, text="Go Back", height=2, width=15, command=lambda: gobacktoadmin(deleteframe))
    but1.pack(pady=5)


def deleteite(delentry):
    id = delentry.get()

    conn.execute('DELETE FROM menu2 WHERE id = ?', (id,))
    delentry.delete(0, tk.END)
    gobacktoadmin(deleteframe)


def gotoaddmenu():
    if adminframe.winfo_ismapped():
        adminframe.pack_forget()
        addtomenuwin()
        addtomenu.pack()


def addtomenuwin():
    label = tk.Label(addtomenu, text="Add new items to menu")
    label.pack(pady=10, anchor="nw")
    label = tk.Label(addtomenu, text="Enter item name")
    label.pack(pady=5, anchor="nw")
    nameitem = tk.Entry(addtomenu)
    nameitem.pack()
    label = tk.Label(addtomenu, text="Enter item description")
    label.pack(pady=5, anchor="nw")
    desentry = tk.Entry(addtomenu)
    desentry.pack()
    label = tk.Label(addtomenu, text="Enter item price")
    label.pack(pady=5, anchor="nw")
    priceent = tk.Entry(addtomenu)
    priceent.pack()

    but = tk.Button(addtomenu, text="Add item", height=2, width=17,
                    command=lambda: additemtomenu(nameitem, desentry, priceent))
    but.pack(pady=10)
    but1 = tk.Button(addtomenu, text="Go back", height=2, width=17, command=lambda: gobacktoadmin(addtomenu))
    but1.pack()


def additemtomenu(nameitem, desentry, priceent):
    conn.execute(
        "INSERT INTO menu2 (name, description, price) VALUES (?, ?, ?)",
        (nameitem.get(), desentry.get(), priceent.get())
    )

    nameitem.delete(0, tk.END)
    desentry.delete(0, tk.END)
    priceent.delete(0, tk.END)


def gotoview(frame):
    if frame.winfo_ismapped():
        frame.pack_forget()
        viewmenu()
        viewframe.pack(padx=5, pady=15, anchor="nw", fill="both", expand=True)


def viewmenu():
    menu_items = conn.execute('SELECT id, name, price FROM menu2')

    canvas = tk.Canvas(viewframe)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(viewframe, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True)

    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    label = tk.Label(inner_frame, text='MENU')
    label.pack(pady=2, anchor="center")
    for item in menu_items:
        label = tk.Label(inner_frame, text=f'{item[0]}. {item[1]} - ${item[2]}')
        label.pack(pady=2, anchor="nw")

    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=2, width=20,
                       command=lambda: gobacktoadmin(viewframe))
    goback.pack(pady=10, anchor="nw")


def gotocustomer(fram):
    if startwin.winfo_ismapped():  # if frame 1 is visible
        startwin.pack_forget()  # hide frame 1
        custimerdata()
        fram.pack(anchor="center")


def custimerdata():
    labe = tk.Label(customerframe, text="Customer Menu: ")
    labe.pack(padx=5, pady=5, anchor="center")

    labe = tk.Label(customerframe, text="Enter name: ")
    labe.pack(padx=5, pady=5, anchor="nw")
    nameentry = tk.Entry(customerframe)
    nameentry.pack(pady=5, padx=5)

    labe = tk.Label(customerframe, text="Enter location: ")
    labe.pack(padx=5, pady=5, anchor="nw")
    locationent = tk.Entry(customerframe)
    locationent.pack(pady=5, padx=5)

    but = tk.Button(customerframe, text="Submit", height=2, width=15,
                    command=lambda: gotocustomermenu(customerframe, nameentry, locationent))
    but.pack(pady=5, padx=5)


def gotocustomermenu(frm, nameentry=None, locationent=None):
    if frm.winfo_ismapped():
        frm.pack_forget()
        customermenu(nameentry, locationent)
        customermenuframe.pack(anchor="center", pady=50)


def customermenu(name=None, location=None):
    but = tk.Button(customermenuframe, text="View Menu", width=20, height=2,
                    command=lambda: gotoviewcustomer(customermenuframe))
    but.pack(padx=30, pady=10)
    but = tk.Button(customermenuframe, text="View Order", width=20, height=2,
                    command=lambda: gotovieworder(customermenuframe))
    but.pack(padx=30, pady=10)
    but = tk.Button(customermenuframe, text="Create Order", width=20, height=2,
                    command=lambda: createordermenuview(customermenuframe, name, location))
    but.pack(padx=30, pady=10)
    but = tk.Button(customermenuframe, text="Update Order", width=20, height=2,
                    command=lambda: gotoupdatecustomer(customermenuframe))
    but.pack(padx=30, pady=10)
    but = tk.Button(customermenuframe, text="Delete Order", width=20, height=2,
                    command=lambda: gotodeleteorder(customermenuframe))
    but.pack(padx=30, pady=10)
    goback = tk.Button(customermenuframe, text="GoBack", fg="black", height=2, width=20,
                       command=lambda: gobactostartcus(customermenuframe))
    goback.pack(pady=20)


def gotodeleteorder(frame):
    if frame.winfo_ismapped():
        frame.pack_forget()
        deleteorder()
        delereorderframe.pack(fill="both", expand=True)


def deleteorder():
    menu_items = conn.execute('SELECT * FROM orders')

    canvas = tk.Canvas(delereorderframe)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(delereorderframe, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True)

    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    label = tk.Label(inner_frame, text='Menu', font=("Arial", 10))
    label.pack()
    for item in menu_items:
        label = tk.Label(inner_frame, text=f'{item[0]}. {item[1]} - ${item[2]}- ${item[3]}- ${item[4]}- ${item[5]}')
        label.pack(pady=2, anchor="nw")

    label = tk.Label(inner_frame, text='Enter id of item you want to delete: ', font=("Arial", 12))
    label.pack(pady=5, anchor="nw")

    delentry = tk.Entry(inner_frame)
    delentry.pack()

    but = tk.Button(inner_frame, text="DELETE", height=2, width=15, command=lambda: deleteiteorder(delentry))
    but.pack(pady=5)

    but1 = tk.Button(inner_frame, text="Go Back", height=2, width=15, command=lambda: gotocustomer55(delereorderframe))
    but1.pack(pady=5)


def deleteiteorder(delentry):
    id = delentry.get()

    conn.execute('DELETE FROM orders WHERE id = ?', (id,))
    delentry.delete(0, tk.END)
    for widget in delereorderframe.winfo_children():
        widget.destroy()

    gotodeleteorder(delereorderframe)


def gotoupdatecustomer(frame):
    if frame.winfo_ismapped():
        frame.pack_forget()
        updatemenu()
        updateframecus.pack(fill="both", expand=True,anchor='center')


def updatemenu():
    canvas = tk.Canvas(updateframecus)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(updateframecus, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True)

    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    label = tk.Label(inner_frame, text='CART')
    label.pack(pady=2, anchor="center")

    orderitems = conn.execute('SELECT id, menu_id,quantity, total_price,customer_name,customer_phone FROM orders')

    for item in orderitems:
        menu_items = conn.execute('SELECT  name FROM menu2 WHERE id = ?', (item[1],))
        menu_items = menu_items.fetchone()
        label = tk.Label(inner_frame, text=f'{item[0]}. {menu_items[0]} - {item[2]} - ${item[3]}- {item[4]}- {item[5]}')

        label.pack(pady=2, anchor="nw")

    label = tk.Label(inner_frame, text="Enter id of order you want to update: ")
    label.pack()
    ident = tk.Entry(inner_frame)
    ident.pack()

    label=tk.Label(inner_frame,text="Enter new quantity")
    label.pack()

    newqun=tk.Entry(inner_frame)
    newqun.pack()

    submit = tk.Button(inner_frame, text="Submit", fg="black", height=2, width=20,
                       command=lambda: submit12(ident,newqun))
    submit.pack(pady=10,padx=15, anchor="nw")

    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=2, width=20,
                       command=lambda: gotocustomer55(updateframecus))
    goback.pack(pady=10,padx=15, anchor="nw")


def submit12(ide,newqun):
    conn.execute("UPDATE orders SET quantity = ? WHERE id = ?", (int(newqun.get()), int(ide.get())))

    price = conn.execute('SELECT  price FROM menu2 WHERE id=?', (ide.get(),))
    qun = int(newqun.get())
    bb = price.fetchone()[0]
    price1 = bb * qun
    price1 = round(price1, 2)

    conn.execute("UPDATE orders SET total_price = ? WHERE id = ?",(price1,int(ide.get())))

    ide.delete(0,tk.END)
    newqun.delete(0,tk.END)


    for widget in updateframecus.winfo_children():
        widget.destroy()

    gotoupdatecustomer(updateframecus)

def gobactostartcus(frame):
    if frame.winfo_ismapped():
        frame.pack_forget()
        startwin.pack(pady=150)
    for widget in customerframe.winfo_children():
        widget.destroy()


def gotoviewcustomer(frame):
    if frame.winfo_ismapped():
        frame.pack_forget()
        viewmenucus()
        viewframecus.pack(padx=5, pady=15, anchor="nw", fill="both", expand=True)


def viewmenucus():
    menu_items = conn.execute('SELECT id, name, price FROM menu2')

    canvas = tk.Canvas(viewframecus)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(viewframecus, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True)

    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    label = tk.Label(inner_frame, text='MENU')
    label.pack(pady=2, anchor="center")
    for item in menu_items:
        label = tk.Label(inner_frame, text=f'{item[0]}. {item[1]} - ${item[2]}')
        label.pack(pady=2, anchor="nw")

    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=2, width=20,
                       command=lambda: gotocustomer55(viewframecus))
    goback.pack(pady=10, anchor="nw")


def gotocustomer55(frame):
    if frame.winfo_ismapped():
        frame.pack_forget()
        customermenuframe.pack()
    for widget in frame.winfo_children():
        widget.destroy()


def gotovieworder(frame):
    if frame.winfo_ismapped():
        frame.pack_forget()
        viewordermenu()
        viewframeorder.pack(padx=5, pady=15, anchor="nw", fill="both", expand=True)


def viewordermenu():
    canvas = tk.Canvas(viewframeorder)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(viewframeorder, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True)

    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    label = tk.Label(inner_frame, text='CART')
    label.pack(pady=2, anchor="center")

    orderitems = conn.execute('SELECT id, menu_id,quantity, total_price,customer_name,customer_phone FROM orders')

    for item in orderitems:
        menu_items = conn.execute('SELECT  name FROM menu2 WHERE id = ?', (item[1],))
        menu_items = menu_items.fetchone()
        label = tk.Label(inner_frame, text=f'{item[0]}. {menu_items[0]} - {item[2]} - ${item[3]}- {item[4]}- {item[5]}')

        label.pack(pady=2, anchor="nw")

    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=2, width=20,
                       command=lambda: gotocustomer55(viewframeorder))
    goback.pack(pady=10, anchor="nw")


def createordermenuview(frame, name=None, location=None):
    if frame.winfo_ismapped():
        frame.pack_forget()
        createordermenu(name, location)
        createorderframe.pack(padx=5, pady=15, anchor="nw", fill="both", expand=True)


def createordermenu(nam=None, location=None):
    menu_items = conn.execute('SELECT id, name, price FROM menu2')

    canvas = tk.Canvas(createorderframe)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(createorderframe, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    inner_frame = tk.Frame(canvas)
    inner_frame.pack(fill="both", expand=True)

    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    label = tk.Label(inner_frame, text='MENU')
    label.pack(pady=2, anchor="center")
    for item in menu_items:
        label = tk.Label(inner_frame, text=f'{item[0]}. {item[1]} - ${item[2]}')
        label.pack(pady=2, anchor="nw")

    label = tk.Label(inner_frame, text='Enter id of item you want to buy: ', font=("Arial", 12))
    label.pack(pady=5, anchor="nw")
    ident = tk.Entry(inner_frame)
    ident.pack()

    label = tk.Label(inner_frame, text='Enter quantity of item: ', font=("Arial", 12))
    label.pack(pady=5, anchor="nw")
    quantityent = tk.Entry(inner_frame)
    quantityent.pack()

    but = tk.Button(inner_frame, text="Add To Cart", height=2, width=15,
                    command=lambda: makeorder(ident, quantityent, nam, location))
    but.pack(pady=5)

    goback = tk.Button(inner_frame, text="GoBack", fg="black", height=2, width=20,
                       command=lambda: gotocustomer55(createorderframe))
    goback.pack(pady=10, anchor="nw")


def makeorder(ident, quantityent, nam, loc):
    price = conn.execute('SELECT  price FROM menu2 WHERE id=?', (ident.get(),))
    qun = int(quantityent.get())
    bb = price.fetchone()[0]
    price1 = bb * qun
    price1 = round(price1, 2)

    conn.execute(
        "INSERT INTO orders (menu_id, quantity, total_price, customer_name, customer_phone) "
        "VALUES (?, ?, ?, ?, ?)",
        (ident.get(), quantityent.get(), price1, nam.get(), loc.get())
    )

    ident.delete(0, tk.END)
    quantityent.delete(0, tk.END)


def createdatabase():
    # Create a table for the menu
    conn.execute('''CREATE TABLE IF NOT EXISTS menu2
                     (id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      description TEXT,
                      price REAL NOT NULL)''')

    # Insert data into the menu table
    conn.execute(
        "INSERT INTO menu2 (name, description, price) VALUES ('Turkey Club Sandwich', 'Turkey, lettuce, tomato, mayonnaise, toasted multigrain bread', 7.99)")
    conn.execute(
        "INSERT INTO menu2 (name, description, price) VALUES ('Classic Cheese Sandwich', 'Swiss cheese, lettuce, tomato, mayonnaise, white bread', 5.99)")
    conn.execute(
        "INSERT INTO menu2 (name, description, price) VALUES ('Veggie Delight Sandwich', 'Avocado, cucumber, lettuce, tomato, red onion, bell pepper, hummus, whole wheat bread', 6.99)")
    conn.execute(
        "INSERT INTO menu2 (name, description, price) VALUES ('Italian Sub Sandwich', 'Salami, pepperoni, cheese, lettuce, tomato, red onion, peppers, Italian dressing, sub roll', 8.99)")
    conn.execute(
        "INSERT INTO menu2 (name, description, price) VALUES ('Tuna Salad Sandwich', 'Tuna salad (tuna, mayonnaise, celery, onion, salt, and pepper), lettuce, tomato, white bread', 6.99)")
    conn.execute("INSERT INTO menu2 (name, description, price) VALUES ('Chips', 'Potato chips', 1.99)")
    conn.execute("INSERT INTO menu2 (name, description, price) VALUES ('Pickles', 'Dill pickles', 0.99)")
    conn.execute("INSERT INTO menu2 (name, description, price) VALUES ('Apple Juice', '100% apple juice', 2.99)")
    conn.execute("INSERT INTO menu2 (name, description, price) VALUES ('Bottled Water', 'Bottled water', 1.49)")
    conn.execute("INSERT INTO menu2 (name, description, price) VALUES ('Orange Juice', '100% orange juice', 2.99)")
    conn.execute("INSERT INTO menu2 (name, description, price) VALUES ('Lemonade', 'Lemonade', 2.49)")

    # creating order table
    conn.execute('''CREATE TABLE IF NOT EXISTS orders
                     (id INTEGER PRIMARY KEY,
                      menu_id INTEGER NOT NULL,
                      quantity INTEGER NOT NULL,
                      total_price REAL NOT NULL,
                      customer_name TEXT NOT NULL,
                      customer_phone TEXT NOT NULL
                      )''')


if __name__ == "__main__":
    startwind()

    if not os.path.isfile(db_file):
        conn = sqlite3.connect(db_file)
        createdatabase()
    else:
        conn = sqlite3.connect(db_file)

    startwin.pack(pady=150)
    root.mainloop()
    conn.commit()
    conn.close()
