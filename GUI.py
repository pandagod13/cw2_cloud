import tkinter as tk


class WaiterAppGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Waiter Mobile App")

        # Create and configure GUI elements
        self.label_username = tk.Label(self.window, text="Username:")
        self.entry_username = tk.Entry(self.window)
        self.label_password = tk.Label(self.window, text="Password:")
        self.entry_password = tk.Entry(self.window, show="*")
        self.btn_login = tk.Button(self.window, text="Login", command=self.login)
        self.label_menu = tk.Label(self.window, text="Menu:")
        self.menu_listbox = tk.Listbox(self.window)
        self.btn_add_to_order = tk.Button(self.window, text="Add to Order", command=self.add_to_order)
        self.label_order = tk.Label(self.window, text="Order:")
        self.order_listbox = tk.Listbox(self.window)
        self.btn_submit_order = tk.Button(self.window, text="Submit Order", command=self.submit_order)

        # Place GUI elements in the window
        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.btn_login.pack()
        self.label_menu.pack()
        self.menu_listbox.pack()
        self.btn_add_to_order.pack()
        self.label_order.pack()
        self.order_listbox.pack()
        self.btn_submit_order.pack()

        self.window.mainloop()

    def login(self):
        # Perform login logic
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Call the login API with the provided credentials
        response = waitstaff_login(username, password)

        # Process the response
        if response["success"]:
            print("Login successful!")
            self.load_menu()  # Load menu items after successful login
        else:
            print("Login failed:", response["message"])

    def load_menu(self):
        # Call the API to retrieve menu items
        menu_items = get_menu_items()

        # Clear the menu listbox
        self.menu_listbox.delete(0, tk.END)

        # Populate the menu listbox with menu items
        for item in menu_items:
            self.menu_listbox.insert(tk.END, item)

    def add_to_order(self):
        # Get the selected menu item from the listbox
        selected_item = self.menu_listbox.get(tk.ACTIVE)

        # Add the selected item to the order listbox
        self.order_listbox.insert(tk.END, selected_item)

    def submit_order(self):
        # Get the ordered items from the order listbox
        ordered_items = list(self.order_listbox.get(0, tk.END))

        # Call the API to submit the order
        response = submit_order(ordered_items)

        # Process the response
        if response["success"]:
            print("Order submitted successfully!")
            self.clear_order()  # Clear the order listbox after successful submission
        else:
            print("Failed to submit order:", response["message"])

    def clear_order(self):
        self.order_listbox.delete(0, tk.END)


# Create an instance of the GUI
waiter_app_gui = WaiterAppGUI()
