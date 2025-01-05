import tkinter as tk
from tkinter import ttk, messagebox

# Linked List Node
class Node:
    def __init__(self, name, phone, booking):
        self.name = name
        self.phone = phone
        self.booking = booking
        self.next = None

# Linked List Class
class LinkedList:
    def __init__(self, max_size=3):
        self.head = None
        self.tail = None
        self.size = 0
        self.max_size = max_size

    def is_full(self):
        return self.size == self.max_size

    def add_booking(self, name, phone, booking):
        if self.is_full():
            return "List is full. Cannot add more bookings."
        
        new_node = Node(name, phone, booking)
        
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1
        return "Booking added successfully"

    def remove_booking(self):
        if self.head is None:
            return "No bookings to remove"
        
        # Remove the first booking (head of the list)
        removed_booking = self.head
        self.head = self.head.next
        self.size -= 1
        
        if self.head is None:  # List is now empty
            self.tail = None

        return removed_booking

    def display(self):
        bookings = []
        current = self.head
        while current:
            bookings.append((current.name, current.phone, current.booking))
            current = current.next
        return bookings


# GUI Application
class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourism and Travel Booking System")
        self.root.geometry("700x700")
        self.root.configure(bg="#f8f9fa")

        self.booking_list = LinkedList(max_size=3)

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

        # Frame for Booking
        booking_frame = ttk.LabelFrame(self.root, text="Add Booking", padding=20)
        booking_frame.pack(padx=20, pady=10, fill="x")

        ttk.Label(booking_frame, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = ttk.Entry(booking_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(booking_frame, text="Phone:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.phone_entry = ttk.Entry(booking_frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(booking_frame, text="Booking:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.booking_entry = ttk.Entry(booking_frame, width=30)
        self.booking_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(booking_frame, text="Add Booking", command=self.add_booking).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Table Frame for Queue Processing
        queue_frame = ttk.LabelFrame(self.root, text="Booking List", padding=20)
        queue_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.queue_tree = ttk.Treeview(
            queue_frame, columns=("Name", "Phone", "Booking"), show="headings", height=10
        )
        self.queue_tree.heading("Name", text="Name")
        self.queue_tree.heading("Phone", text="Phone")
        self.queue_tree.heading("Booking", text="Booking")
        self.queue_tree.column("Name", anchor="center", width=200)
        self.queue_tree.column("Phone", anchor="center", width=150)
        self.queue_tree.column("Booking", anchor="center", width=300)

        # Scrollbar for the queue table
        queue_scrollbar = ttk.Scrollbar(
            queue_frame, orient="vertical", command=self.queue_tree.yview
        )
        self.queue_tree.configure(yscroll=queue_scrollbar.set)
        queue_scrollbar.pack(side="right", fill="y")
        self.queue_tree.pack(fill="both", expand=True)

        # Footer
        footer_label = ttk.Label(
            self.root,
            text="© 2025 Tourism Booking System",
            font=("Arial", 10),
            foreground="#6c757d",
        )
        footer_label.pack(side="bottom", pady=10)

    def add_booking(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        booking = self.booking_entry.get()

        if not name or not phone or not booking:
            messagebox.showwarning("Warning", "Please fill out all fields.")
            return

        if not phone.isdigit() or len(phone) != 10 or not (phone.startswith("078") or phone.startswith("079")):
            messagebox.showwarning(
                "Warning", "Phone number must start with '078' or '079' and contain 10 digits."
            )
            return

        result = self.booking_list.add_booking(name, phone, booking)
        if result == "List is full. Cannot add more bookings.":
            messagebox.showwarning("List Full", "You cannot add more bookings. The list is full.")

        self.update_queue_table()

        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.booking_entry.delete(0, tk.END)

    def update_queue_table(self):
        # Clear all existing entries in the table
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)

        # Populate the table with the current list of bookings
        bookings = self.booking_list.display()
        for booking in bookings:
            self.queue_tree.insert("", "end", values=booking)

    def remove_booking(self):
        removed_booking = self.booking_list.remove_booking()
        if removed_booking == "No bookings to remove":
            messagebox.showinfo("Empty List", "No bookings to remove.")
        else:
            messagebox.showinfo(
                "Booking Removed", f"Booking for {removed_booking.name} has been removed."
            )
        
        self.update_queue_table()


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()
