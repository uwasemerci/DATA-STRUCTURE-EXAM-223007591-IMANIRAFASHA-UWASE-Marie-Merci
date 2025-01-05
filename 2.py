import tkinter as tk
from tkinter import ttk, messagebox


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return "Stack is empty"

    def is_empty(self):
        return len(self.stack) == 0


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, current, key):
        if key < current.key:
            if current.left is None:
                current.left = Node(key)
            else:
                self._insert_recursive(current.left, key)
        else:
            if current.right is None:
                current.right = Node(key)
            else:
                self._insert_recursive(current.right, key)


class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourism and Travel Booking System")
        self.root.state("zoomed")  # Maximized state
        self.root.configure(bg="#f8f9fa")

        self.history_stack = Stack()
        self.booking_tree = BinaryTree()

        # Styling
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12), background="#f8f9fa")
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        self.style.configure("TEntry", font=("Arial", 12))
        self.style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ttk.Label(
            self.root,
            text="Tourism and Travel Booking System",
            font=("Arial", 18, "bold"),
            anchor="center",
            foreground="#007bff",
        )
        title_label.pack(pady=20)

        # Main frame to hold two sections
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame for Search and Booking Form
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", expand=True)

        # Search Section
        search_frame = ttk.LabelFrame(left_frame, text="Search Destination", padding=20)
        search_frame.pack(pady=10, fill="x")

        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(search_frame, text="Search", command=self.add_to_history).grid(
            row=0, column=1, padx=10, pady=5
        )

        ttk.Button(
            search_frame, text="View Last Search", command=self.view_last_search
        ).grid(row=1, column=0, columnspan=2, pady=5)

        # Frame for Booking
        booking_frame = ttk.LabelFrame(left_frame, text="Add Booking", padding=20)
        booking_frame.pack(pady=10, fill="x")

        ttk.Label(booking_frame, text="Name:").grid(
            row=0, column=0, padx=10, pady=5, sticky="e"
        )
        self.name_entry = ttk.Entry(booking_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(booking_frame, text="Phone:").grid(
            row=1, column=0, padx=10, pady=5, sticky="e"
        )
        self.phone_entry = ttk.Entry(booking_frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(booking_frame, text="Booking:").grid(
            row=2, column=0, padx=10, pady=5, sticky="e"
        )
        self.booking_entry = ttk.Entry(booking_frame, width=30)
        self.booking_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(booking_frame, text="Add Booking", command=self.add_booking).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Booking History Section
        right_frame = ttk.LabelFrame(main_frame, text="Booking History", padding=20)
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.tree = ttk.Treeview(
            right_frame, columns=("Name", "Phone", "Booking"), show="headings", height=20
        )
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Booking", text="Booking")
        self.tree.column("Name", anchor="center", width=200)
        self.tree.column("Phone", anchor="center", width=150)
        self.tree.column("Booking", anchor="center", width=300)

        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Footer
        footer_label = ttk.Label(
            self.root,
            text="© 2025 Tourism Booking System",
            font=("Arial", 10),
            foreground="#6c757d",
        )
        footer_label.pack(side="bottom", pady=10)

    def add_to_history(self):
        destination = self.search_entry.get()
        if destination:
            self.history_stack.push(destination)
            messagebox.showinfo("Success", f"Added '{destination}' to search history.")
            self.search_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a destination to search.")

    def view_last_search(self):
        last_search = self.history_stack.pop()
        if last_search == "Stack is empty":
            messagebox.showinfo("Info", "No previous searches.")
        else:
            messagebox.showinfo("Last Search", f"Last Search: {last_search}")

    def add_booking(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        booking = self.booking_entry.get()

        if not name or not phone or not booking:
            messagebox.showwarning("Warning", "Please fill out all fields.")
            return

        if not phone.isdigit() or len(phone) != 10 or not (
            phone.startswith("078") or phone.startswith("079")
        ):
            messagebox.showwarning(
                "Warning", "Phone number must start with '078' or '079' and contain 10 digits."
            )
            return

        self.booking_tree.insert((name, phone, booking))
        self.tree.insert("", "end", values=(name, phone, booking))
        messagebox.showinfo("Success", f"Booking for '{booking}' added successfully.")

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.booking_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()
