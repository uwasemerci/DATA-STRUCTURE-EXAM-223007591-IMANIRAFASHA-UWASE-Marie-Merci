import tkinter as tk
from tkinter import ttk, messagebox


# Circular Queue Class
class CircularQueue:
    def __init__(self, size):
        self.size = size
        self.queue = [None] * size
        self.front = -1
        self.rear = -1

    def is_full(self):
        return (self.rear + 1) % self.size == self.front

    def is_empty(self):
        return self.front == -1

    def enqueue(self, item):
        if self.is_full():
            return "Queue is full"
        elif self.is_empty():
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = item

    def dequeue(self):
        if self.is_empty():
            return "Queue is empty"
        elif self.front == self.rear:
            item = self.queue[self.front]
            self.front = self.rear = -1
            return item
        else:
            item = self.queue[self.front]
            self.front = (self.front + 1) % self.size
            return item

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[self.front]

    def display(self):
        if self.is_empty():
            return []
        elif self.rear >= self.front:
            return self.queue[self.front : self.rear + 1]
        else:
            return self.queue[self.front :] + self.queue[: self.rear + 1]

    def replace(self, index, new_item):
        # Replace an item at a specific index
        actual_index = (self.front + index) % self.size
        self.queue[actual_index] = new_item


# GUI Application
class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourism and Travel Booking System")
        self.root.geometry("700x700")
        self.root.configure(bg="#f8f9fa")

        self.booking_queue = CircularQueue(5)  # Circular Queue with a size of 5

        # Styling
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12), background="#f8f9fa")
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        self.style.configure("TEntry", font=("Arial", 12))
        self.style.configure("Treeview", font=("Arial", 11), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Selected Item Index
        self.selected_index = None

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
        booking_frame = ttk.LabelFrame(self.root, text="Add/Replace Booking", padding=20)
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

        ttk.Button(booking_frame, text="Add/Replace Booking", command=self.add_or_replace_booking).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Table Frame for Queue Processing
        queue_frame = ttk.LabelFrame(self.root, text="Booking Queue", padding=20)
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

        self.queue_tree.bind("<<TreeviewSelect>>", self.on_item_select)

        # Footer
        footer_label = ttk.Label(
            self.root,
            text="© 2025 Tourism Booking System",
            font=("Arial", 10),
            foreground="#6c757d",
        )
        footer_label.pack(side="bottom", pady=10)

    def add_or_replace_booking(self):
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

        if self.selected_index is not None:
            # Replace booking
            replace_confirmation = messagebox.askyesno(
                "Confirm Replace",
                f"Do you want to replace the selected booking with:\n\nName: {name}\nPhone: {phone}\nBooking: {booking}?",
            )
            if replace_confirmation:
                self.booking_queue.replace(self.selected_index, (name, phone, booking))
                self.selected_index = None
        else:
            # Add booking
            result = self.booking_queue.enqueue((name, phone, booking))
            if result == "Queue is full":
                messagebox.showwarning("Queue Full", "The booking queue is full. Please process some bookings.")

        self.update_queue_table()

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.booking_entry.delete(0, tk.END)

    def on_item_select(self, event):
        selected_item = self.queue_tree.selection()
        if selected_item:
            self.selected_index = self.queue_tree.index(selected_item[0])

    def update_queue_table(self):
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)

        for booking in self.booking_queue.display():
            self.queue_tree.insert("", "end", values=booking)


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    
    root.mainloop()
