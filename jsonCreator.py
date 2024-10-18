import tkinter as tk
from tkinter import filedialog, messagebox
import json

class JSONCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Creator")

        # Create UI
        self.create_ui()

        # Store key-value pairs
        self.data = {}

    def create_ui(self):
        """Create the UI components for inputting key-value pairs."""
        # Entry for the key
        tk.Label(self.root, text="Key:").grid(row=0, column=0, padx=10, pady=5)
        self.key_entry = tk.Entry(self.root, width=30)
        self.key_entry.grid(row=0, column=1, padx=10, pady=5)

        # Entry for the value
        tk.Label(self.root, text="Value:").grid(row=1, column=0, padx=10, pady=5)
        self.value_entry = tk.Entry(self.root, width=30)
        self.value_entry.grid(row=1, column=1, padx=10, pady=5)

        # Button to add key-value pairs
        self.add_button = tk.Button(self.root, text="Add Key-Value Pair", command=self.add_key_value)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Text area to display added key-value pairs
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Button to create the JSON file
        self.save_button = tk.Button(self.root, text="Save JSON", command=self.save_json)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def add_key_value(self):
        """Add the key-value pair to the dictionary and display it."""
        key = self.key_entry.get().strip()
        value = self.value_entry.get().strip()

        if key and value:
            self.data[key] = value
            self.text_area.insert(tk.END, f"{key}: {value}\n")
            self.key_entry.delete(0, tk.END)
            self.value_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Both key and value must be provided!")

    def save_json(self):
        """Save the current key-value pairs as a JSON file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as json_file:
                json.dump(self.data, json_file, indent=4)
            messagebox.showinfo("Success", f"JSON file saved at {file_path}")

# Create the main Tkinter window
root = tk.Tk()

# Run the application
app = JSONCreatorApp(root)
root.mainloop()
