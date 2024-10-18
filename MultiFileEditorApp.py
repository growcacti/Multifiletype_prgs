import tkinter as tk
from tkinter import filedialog, messagebox
import json
import csv


class FileHandler:
    def __init__(self):
        self.data = []
        self.file_type = None
        self.delimiter = ','  # Default delimiter for CSV

    def load_file(self, file_type):
        """Load a file based on the file type."""
        file_path = filedialog.askopenfilename(filetypes=[(f"{file_type.upper()} files", f"*.{file_type}")])
        if not file_path:
            return

        if file_type == 'csv':
            self.file_type = 'csv'
            self.load_csv(file_path)
        elif file_type == 'json':
            self.file_type = 'json'
            self.load_json(file_path)

    def save_file(self):
        """Save the data to a file based on the current file type."""
        if not self.file_type:
            messagebox.showerror("Error", "No file type selected for saving.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=f".{self.file_type}", filetypes=[(f"{self.file_type.upper()} files", f"*.{self.file_type}")])
        if not file_path:
            return

        if self.file_type == 'csv':
            self.save_csv(file_path)
        elif self.file_type == 'json':
            self.save_json(file_path)

    def load_csv(self, file_path):
        """Load CSV file and store its data."""
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            self.data = list(reader)

    def save_csv(self, file_path):
        """Save CSV data to file."""
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter)
            for row in self.data:
                writer.writerow(row)
        messagebox.showinfo("Success", "CSV file saved successfully!")

    def load_json(self, file_path):
        """Load JSON file and store its data."""
        with open(file_path, "r") as json_file:
            self.data = json.load(json_file)

    def save_json(self, file_path):
        """Save JSON data to file."""
        with open(file_path, "w") as json_file:
            json.dump(self.data, json_file, indent=4)
        messagebox.showinfo("Success", "JSON file saved successfully!")

    def update_data(self, row, col, value):
        """Update the data array when the user edits the grid."""
        self.data[row][col] = value

    def change_delimiter(self, new_delimiter):
        """Change the delimiter for CSV files."""
        if new_delimiter.lower() == "tab":
            self.delimiter = '\t'
        else:
            self.delimiter = new_delimiter


class MultiFileEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-File Editor")
        self.file_handler = FileHandler()

        # Create UI components
        self.create_ui()

    def create_ui(self):
        """Create the UI components."""
        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=0, padx=10, pady=5)

        # Load CSV button
        self.load_csv_button = tk.Button(button_frame, text="Load CSV", command=lambda: self.load_file('csv'))
        self.load_csv_button.grid(row=0, column=0, padx=5, pady=5)

        # Load JSON button
        self.load_json_button = tk.Button(button_frame, text="Load JSON", command=lambda: self.load_file('json'))
        self.load_json_button.grid(row=0, column=1, padx=5, pady=5)

        # Save button
        self.save_button = tk.Button(button_frame, text="Save", command=self.save_file)
        self.save_button.grid(row=0, column=2, padx=5, pady=5)

        # Change Delimiter button
        self.delimiter_button = tk.Button(button_frame, text="Change Delimiter", command=self.change_delimiter)
        self.delimiter_button.grid(row=0, column=3, padx=5, pady=5)

        # Frame to display file content in a grid
        self.file_frame = tk.Frame(self.root)
        self.file_frame.grid(row=1, column=0, padx=10, pady=10)

    def load_file(self, file_type):
        """Load a file and display its content."""
        self.file_handler.load_file(file_type)
        self.display_data()

    def save_file(self):
        """Save the file."""
        self.file_handler.save_file()

    def change_delimiter(self):
        """Change the CSV delimiter."""
        delimiter = tk.simpledialog.askstring("Input", "Enter delimiter (e.g., comma, tab, semicolon):")
        if delimiter:
            self.file_handler.change_delimiter(delimiter)

    def display_data(self):
        """Display the loaded data in the grid."""
        # Clear the current grid
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        # Display data in a grid of Entry widgets
        for r, row in enumerate(self.file_handler.data):
            for c, value in enumerate(row):
                entry = tk.Entry(self.file_frame, width=15)
                entry.grid(row=r, column=c, padx=5, pady=5)
                entry.insert(0, value)
                entry.bind('<KeyRelease>', lambda event, row=r, col=c: self.file_handler.update_data(row, col, event.widget.get()))


# Create the main Tkinter window
root = tk.Tk()

# Run the application
app = MultiFileEditorApp(root)
root.mainloop()
