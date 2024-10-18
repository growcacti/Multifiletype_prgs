import tkinter as tk
from tkinter import filedialog, messagebox
import json
import csv
import xml.etree.ElementTree as ET
import os


class JSONEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Editor & Converter")

        # Create the main UI for loading, editing, saving JSON, and converting
        self.create_ui()

    def create_ui(self):
        """Create the UI components for the JSON editor."""
        # Text area for displaying and editing JSON content
        self.text_area = tk.Text(self.root, bd=11,height=20, width=60)
        self.text_area.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Load JSON button
        self.load_button = tk.Button(self.root, bd=4,text="Load JSON", command=self.load_json)
        self.load_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Save JSON button
        self.save_button = tk.Button(self.root, bd=4,text="Save JSON", command=self.save_json)
        self.save_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Convert to CSV button
        self.convert_csv_button = tk.Button(self.root, bd=4,text="Convert to CSV", command=self.convert_to_csv)
        self.convert_csv_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        # Convert to XML button
        self.convert_xml_button = tk.Button(self.root,bd=4, text="Convert to XML", command=self.convert_to_xml)
        self.convert_xml_button.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        # Convert to Python Dict button
        self.convert_dict_button = tk.Button(self.root, bd=4,text="Convert to Python Dict", command=self.convert_to_dict)
        self.convert_dict_button.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        self.cleartext_button = tk.Button(self.root, bd=4,text="Clear Text", command=self.clear)
        self.cleartext_button.grid(row=3, column=2, columnspan=2, padx=10, pady=5, sticky="ew")

    def load_json(self):
        """Load a JSON file and display its content in the text area."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as json_file:
                data = json_file.read()
                self.text_area.delete(1.0, tk.END)  # Clear previous content
                self.text_area.insert(tk.END, data)  # Insert new JSON content
            self.status_message(f"Loaded: {file_path}")
        else:
            self.status_message("File loading cancelled")

    def save_json(self):
        """Save the current text area content as a JSON file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            json_data = self.text_area.get(1.0, tk.END)
            try:
                parsed_data = json.loads(json_data)  # Ensure it's valid JSON before saving
                with open(file_path, "w") as json_file:
                    json.dump(parsed_data, json_file, indent=4)
                self.status_message(f"Saved: {file_path}")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format. Please check the content.")
        else:
            self.status_message("File saving cancelled")

    def convert_to_csv(self):
        """Convert the JSON content to a CSV file."""
        json_data = self.text_area.get(1.0, tk.END)
        try:
            parsed_data = json.loads(json_data)
            if isinstance(parsed_data, list):  # Ensure the JSON is a list of dictionaries
                file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
                if file_path:
                    with open(file_path, "w", newline="") as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=parsed_data[0].keys())
                        writer.writeheader()
                        writer.writerows(parsed_data)
                    self.status_message(f"CSV file created: {file_path}")
            else:
                messagebox.showerror("Error", "JSON is not in the format of a list of dictionaries.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format. Cannot convert to CSV.")

    def convert_to_xml(self):
        """Convert the JSON content to an XML file."""
        json_data = self.text_area.get(1.0, tk.END)
        try:
            parsed_data = json.loads(json_data)
            root_element = self.json_to_xml(parsed_data, ET.Element("root"))

            file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
            if file_path:
                tree = ET.ElementTree(root_element)
                tree.write(file_path, encoding="utf-8", xml_declaration=True)
                self.status_message(f"XML file created: {file_path}")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format. Cannot convert to XML.")

    def convert_to_dict(self):
        """Convert the JSON content to a Python dictionary and display it."""
        json_data = self.text_area.get(1.0, tk.END)
        try:
            parsed_data = json.loads(json_data)
            dict_representation = str(parsed_data)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, dict_representation)
            self.status_message("Converted to Python dictionary format.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format. Cannot convert to Python dictionary.")

    def json_to_xml(self, json_obj, parent):
        """Recursively convert JSON data to XML elements."""
        if isinstance(json_obj, dict):
            for key, value in json_obj.items():
                sub_element = ET.SubElement(parent, key)
                self.json_to_xml(value, sub_element)
        elif isinstance(json_obj, list):
            for item in json_obj:
                sub_element = ET.SubElement(parent, "item")
                self.json_to_xml(item, sub_element)
        else:
            parent.text = str(json_obj)
        return parent

    def status_message(self, message):
        """Display status messages in the window title bar."""
        self.root.title(f"JSON Editor & Converter - {message}")

    def clear(self):
        self.text_area.delete("1.0", tk.END)
# Create the main Tkinter window
root = tk.Tk()

# Run the application
app = JSONEditorApp(root)
root.mainloop()
