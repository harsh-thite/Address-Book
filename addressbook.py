import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AddressBookApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Address Book")
        self.master.geometry("600x400")
        self.master.configure(bg="#222222")

        self.contacts = [
            {"Name": "John Doe", "Phone": "123-456-7890", "Email": "john@example.com"},
            {"Name": "Jane Smith", "Phone": "987-654-3210", "Email": "jane@example.com"},
            {"Name": "Alice Johnson", "Phone": "456-789-0123", "Email": "alice@example.com"},
            {"Name": "Bob Brown", "Phone": "789-012-3456", "Email": "bob@example.com"}
        ]

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Address Book", font=("San Francisco", 28, "bold"), bg="#222222", fg="red", padx=10, pady=5)
        self.label.pack(fill=tk.X)

        self.search_frame = tk.Frame(self.master, bg="#222222")
        self.search_frame.pack(pady=10)

        tk.Label(self.search_frame, text="Search:", font=("San Francisco", 14, "bold"), bg="#222222", fg="white").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(self.search_frame, width=30, font=("San Francisco", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(self.search_frame, text="Search", command=self.search_contact, bg="black", fg="white", padx=10).pack(side=tk.LEFT, padx=5)

        ttk.Button(self.master, text="Add Contact", command=self.add_contact).pack(pady=5)

        self.treeview = ttk.Treeview(self.master, columns=("Name", "Phone", "Email"), show="headings", style="Custom.Treeview")
        self.treeview.pack(expand=True, fill=tk.BOTH, padx=10)
        for contact in self.contacts:
            self.treeview.insert("", "end", values=(contact["Name"], contact["Phone"], contact["Email"]))

        for btn in [("Edit", self.edit_contact), ("Delete", self.delete_contact)]:
            ttk.Button(self.master, text=btn[0], command=btn[1]).pack(side=tk.LEFT, padx=5, pady=5)

        self.treeview.bind("<Double-1>", self.open_contact_popup)

        self.custom_style = ttk.Style()
        self.custom_style.theme_use("default")
        self.custom_style.configure("Custom.Treeview", background="#333333", foreground="white", fieldbackground="#333333", font=("San Francisco", 10))

        self.custom_style.configure("TButton", background="black", foreground="white", font=("San Francisco", 12, "bold"))
        self.custom_style.map("TButton", background=[("active", "red")])

    def search_contact(self):
        search_term = self.search_entry.get().lower()
        if search_term:
            results = [contact for contact in self.contacts if search_term in contact["Name"].lower()]
            self.display_search_results(results)
        else:
            messagebox.showinfo("Search", "Please enter a search term.")

    def display_search_results(self, results):
        self.treeview.delete(*self.treeview.get_children())
        for contact in results:
            self.treeview.insert("", "end", values=(contact["Name"], contact["Phone"], contact["Email"]))

    def add_contact(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Contact")
        add_window.configure(bg="#222222")

        fields = [("Name", 0), ("Phone", 1), ("Email", 2)]
        for field, row in fields:
            tk.Label(add_window, text=field + ":", font=("San Francisco", 14, "bold"), bg="#222222", fg="white").grid(row=row, column=0, padx=5, pady=5)
            entry = tk.Entry(add_window, width=30, font=("San Francisco", 12))
            entry.grid(row=row, column=1, padx=5, pady=5)
            setattr(self, field.lower() + "_entry", entry)

        ttk.Button(add_window, text="Save", command=self.save_contact).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def save_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if all((name, phone, email)):
            self.contacts.append({"Name": name, "Phone": phone, "Email": email})
            self.treeview.insert("", "end", values=(name, phone, email))
            messagebox.showinfo("Success", "Contact added successfully.")
        else:
            messagebox.showwarning("Error", "All fields must be filled.")

    def edit_contact(self):
        selected_item = self.treeview.focus()
        if selected_item:
            contact_data = self.treeview.item(selected_item, "values")
            name, phone, email = contact_data

            edit_window = tk.Toplevel(self.master)
            edit_window.title("Edit Contact")
            edit_window.configure(bg="#222222")

            fields = [("Name", 0, name), ("Phone", 1, phone), ("Email", 2, email)]
            for field, row, value in fields:
                tk.Label(edit_window, text=field + ":", font=("San Francisco", 14, "bold"), bg="#222222", fg="white").grid(row=row, column=0, padx=5, pady=5)
                entry = tk.Entry(edit_window, width=30, font=("San Francisco", 12))
                entry.grid(row=row, column=1, padx=5, pady=5)
                entry.insert(0, value)
                setattr(self, field.lower() + "_entry", entry)

            ttk.Button(edit_window, text="Save", command=self.update_contact).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def update_contact(self):
        selected_item = self.treeview.focus()
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if all((name, phone, email)):
            self.treeview.item(selected_item, values=(name, phone, email))
            messagebox.showinfo("Success", "Contact updated successfully.")
        else:
            messagebox.showwarning("Error", "All fields must be filled.")

    def delete_contact(self):
        selected_item = self.treeview.focus()
        if selected_item:
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this contact?")
            if confirm:
                self.treeview.delete(selected_item)
                messagebox.showinfo("Deleted", "Contact deleted successfully.")

    def open_contact_popup(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            contact_data = self.treeview.item(selected_item, "values")
            name, phone, email = contact_data

            popup_window = tk.Toplevel(self.master)
            popup_window.title("Contact Details")
            popup_window.geometry("300x150")
            popup_window.configure(bg="#222222")

            fields = [("Name", name), ("Phone", phone), ("Email", email)]
            for field, value in fields:
                tk.Label(popup_window, text=field + ":", font=("San Francisco", 14, "bold"), bg="#222222", fg="white").grid(row=fields.index((field, value)), column=0, padx=5, pady=5)
                tk.Label(popup_window, text=value, font=("San Francisco", 12), bg="#222222", fg="white").grid(row=fields.index((field, value)), column=1, padx=5, pady=5)

def main():
    root = tk.Tk()
    app = AddressBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
