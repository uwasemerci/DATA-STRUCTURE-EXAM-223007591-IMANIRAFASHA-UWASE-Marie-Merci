import tkinter as tk
from tkinter import ttk, messagebox

# Stack Class for managing bookings
class BookingStack:
    def __init__(self, max_size=3):
        self.stack = []
        self.max_size = max_size

    def is_full(self):
        return len(self.stack) == self.max_size

    def push(self, name, phone, booking):
        if self.is_full():
            return "Stack is full. Cannot add more bookings."
        self.stack.append((name, phone, booking))
        return "Booking added successfully"

    def pop(self):
        if not self.stack:
            return "No bookings to remove"
        return self.stack.pop()

    def peek(self):
        if not self.stack:
            return "No bookings to show"
        return self.stack[-1]

    def display(self):
        return self.stack


# GUI Application
class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourism and Travel Booking System")
        
        # Set window to maximized
        self.root.state('zoomed')  # Maximizes the window without full screen
        self.root.configure(bg="#f8f9fa")
        
        self.booking_stack = BookingStack(max_size=3)

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

        # Frame for Stack Operations (Viewing and Removing bookings)
        stack_frame = ttk.LabelFrame(self.root, text="Booking Stack", padding=20)
        stack_frame.pack(padx=20, pady=10, fill="x")

        self.stack_tree = ttk.Treeview(
            stack_frame, columns=("Name", "Phone", "Booking"), show="headings", height=6
        )
        self.stack_tree.heading("Name", text="Name")
        self.stack_tree.heading("Phone", text="Phone")
        self.stack_tree.heading("Booking", text="Booking")
        self.stack_tree.column("Name", anchor="center", width=200)
        self.stack_tree.column("Phone", anchor="center", width=150)
        self.stack_tree.column("Booking", anchor="center", width=300)

        # Scrollbar for the stack table
        stack_scrollbar = ttk.Scrollbar(
            stack_frame, orient="vertical", command=self.stack_tree.yview
        )
        self.stack_tree.configure(yscroll=stack_scrollbar.set)
        stack_scrollbar.pack(side="right", fill="y")
        self.stack_tree.pack(fill="both", expand=True)

        ttk.Button(stack_frame, text="Remove Last Booking", command=self.remove_booking).pack(pady=5)
        ttk.Button(stack_frame, text="View Last Booking", command=self.view_last_booking).pack(pady=5)

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

        result = self.booking_stack.push(name, phone, booking)
        if result == "Stack is full. Cannot add more bookings.":
            messagebox.showwarning("Stack Full", "You cannot add more bookings. The stack is full.")

        self.update_stack_table()

        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.booking_entry.delete(0, tk.END)

    def update_stack_table(self):
        # Clear all existing entries in the table
        for item in self.stack_tree.get_children():
            self.stack_tree.delete(item)

        # Populate the table with the current stack of bookings
        bookings = self.booking_stack.display()
        for booking in bookings:
            self.stack_tree.insert("", "end", values=booking)

    def remove_booking(self):
        removed_booking = self.booking_stack.pop()
        if removed_booking == "No bookings to remove":
            messagebox.showinfo("Empty Stack", "No bookings to remove.")
        else:
            messagebox.showinfo(
                "Booking Removed", f"Booking for {removed_booking[0]} has been removed."
            )

        self.update_stack_table()

    def view_last_booking(self):
        last_booking = self.booking_stack.peek()
        if last_booking == "No bookings to show":
            messagebox.showinfo("No Bookings", "There are no bookings in the stack.")
        else:
            messagebox.showinfo(
                "Last Booking",
                f"Name: {last_booking[0]}\nPhone: {last_booking[1]}\nBooking: {last_booking[2]}",
            )


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()
