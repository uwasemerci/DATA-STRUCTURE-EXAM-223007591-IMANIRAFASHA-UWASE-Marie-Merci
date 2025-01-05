import tkinter as tk
from tkinter import ttk, messagebox

# TreeNode class to represent each node in the tree
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

# Tree class to represent the tree structure
class Tree:
    def __init__(self, root_data):
        self.root = TreeNode(root_data)

    def add_node(self, parent_node, node_data):
        new_node = TreeNode(node_data)
        parent_node.add_child(new_node)
        return new_node

    def display(self, parent_node, tree_view, parent_item=""):
        """Recursively display tree in the Treeview widget."""
        for child in parent_node.children:
            item = tree_view.insert(parent_item, "end", text=child.data, iid=child.data)
            self.display(child, tree_view, item)

# GUI Application for Tourism & Travel Booking System
class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourism and Travel Booking System")
        self.root.state('zoomed')  # Maximize the window
        self.root.configure(bg="#f8f9fa")

        # Styling
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12), background="#f8f9fa")
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        self.style.configure("TTreeview", font=("Arial", 11), rowheight=25)
        self.style.configure("TTreeview.Heading", font=("Arial", 12, "bold"))

        # Create Tree for managing hierarchical data
        self.tree = Tree("Tourism & Travel System")
        self.destinations_node = self.tree.add_node(self.tree.root, "Destinations")
        self.bookings_node = self.tree.add_node(self.tree.root, "Bookings")

        # Add subcategories to Destinations
        beach_node = self.tree.add_node(self.destinations_node, "Beach")
        self.tree.add_node(beach_node, "Kivu Beach Rubavu")
        self.tree.add_node(beach_node, "Kivu Beach Rusizi")
        
        mountains_node = self.tree.add_node(self.destinations_node, "Mountains")
        self.tree.add_node(mountains_node, "Mount Muhabura")
        self.tree.add_node(mountains_node, "Mount Sabyinyo")
        self.tree.add_node(mountains_node, "Mount Karisimbi")
        self.tree.add_node(mountains_node, "Mount Bisoke")
        self.tree.add_node(mountains_node, "Mount Gahinga")

        # Replace Pending Bookings with Pending for UWASE, IMANIRAFASHA
        pending_node = self.tree.add_node(self.bookings_node, "Pending for UWASE, IMANIRAFASHA")
        
        # Add completed booking for Marie Merci
        completed_node = self.tree.add_node(self.bookings_node, "Completed Bookings")
        self.tree.add_node(completed_node, "Marie Merci")

        # Create Widgets for the GUI
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

        # Treeview for displaying the Tree
        tree_frame = ttk.LabelFrame(self.root, text="Treeview Hierarchical Data", padding=20)
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.tree_view = ttk.Treeview(tree_frame, columns=("Data"), show="tree")
        self.tree_view.pack(fill="both", expand=True)

        # Populate the treeview with the hierarchical data
        self.tree.display(self.tree.root, self.tree_view)

        # Bind item selection to display details
        self.tree_view.bind("<<TreeviewSelect>>", self.on_item_select)

        # Label to display selected node's information
        self.details_label = ttk.Label(self.root, text="Select an item from the tree to view details.", font=("Arial", 14))
        self.details_label.pack(pady=20)

        # Button to show mountain details
        self.reveal_mountains_button = ttk.Button(
            self.root, text="Show Mountain Details", command=self.reveal_mountain_details
        )
        self.reveal_mountains_button.pack(pady=10)

        # Mountain details initially hidden
        self.mountain_details_label = ttk.Label(
            self.root, text="Mountains: Mount Muhabura, Mount Sabyinyo, Mount Karisimbi, Mount Bisoke, Mount Gahinga.", font=("Arial", 12), wraplength=400
        )
        self.mountain_details_label.pack(pady=10)
        self.mountain_details_label.pack_forget()  # Hide initially

        # Footer
        footer_label = ttk.Label(
            self.root,
            text="© 2025 Tourism Booking System",
            font=("Arial", 10),
            foreground="#6c757d",
        )
        footer_label.pack(side="bottom", pady=10)

    def reveal_mountain_details(self):
        """Reveal the hidden mountain details when the button is clicked."""
        self.mountain_details_label.pack()  # Show the label containing mountain details
        self.reveal_mountains_button.pack_forget()  # Hide the button after clicking

    def on_item_select(self, event):
        """Handles the event when a user selects an item in the treeview."""
        selected_item = self.tree_view.selection()
        if selected_item:
            selected_data = self.tree_view.item(selected_item[0], "text")
            self.display_item_details(selected_data)

    def display_item_details(self, selected_data):
        """Display details of the selected item."""
        # Directly checking each destination or category
        if selected_data == "Kivu Beach Rubavu":
            self.details_label.config(text="Beach: Kivu Beach Rubavu - Relax by Lake Kivu in Rubavu.")
        elif selected_data == "Kivu Beach Rusizi":
            self.details_label.config(text="Beach: Kivu Beach Rusizi - Scenic views of Lake Kivu in Rusizi.")
        elif selected_data == "Mount Muhabura":
            self.details_label.config(text="Mountain: Mount Muhabura - A stunning volcano to explore.")
        elif selected_data == "Mount Sabyinyo":
            self.details_label.config(text="Mountain: Mount Sabyinyo - A volcanic ridge with breathtaking views.")
        elif selected_data == "Mount Karisimbi":
            self.details_label.config(text="Mountain: Mount Karisimbi - A majestic peak to conquer.")
        elif selected_data == "Mount Bisoke":
            self.details_label.config(text="Mountain: Mount Bisoke - An active volcano in Rwanda's Volcanoes National Park.")
        elif selected_data == "Mount Gahinga":
            self.details_label.config(text="Mountain: Mount Gahinga - Known for its hiking trails and gorilla tracking.")
        elif selected_data == "Beach":
            self.details_label.config(text="Beach destinations: Kivu Beach Rubavu, Kivu Beach Rusizi.")
        elif selected_data == "Mountains":
            self.details_label.config(text="Mountain destinations: Mount Muhabura, Mount Sabyinyo, Mount Karisimbi, Mount Bisoke, Mount Gahinga.")
        elif selected_data == "Pending for UWASE, IMANIRAFASHA":
            self.details_label.config(text="Pending for UWASE, IMANIRAFASHA: Awaiting confirmation.")
        elif selected_data == "Marie Merci":
            self.details_label.config(text="Completed Booking: Marie Merci - Booking completed successfully.")
        else:
            self.details_label.config(text=f"Category: {selected_data}")

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()
