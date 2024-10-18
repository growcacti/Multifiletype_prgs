import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET

class XMLCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Creator")

        # Create the main UI for adding elements and attributes
        self.create_ui()

        # Hold all elements for hierarchy
        self.sub_elements = []

    def create_ui(self):
        """Create the UI components."""
        # Root Element Input
        tk.Label(self.root, text="Root Element:").grid(row=0, column=0, padx=10, pady=5)
        self.root_element_entry = tk.Entry(self.root, width=30)
        self.root_element_entry.grid(row=0, column=1, padx=10, pady=5)

        # Add Button to Add New Sub-element
        self.add_sub_button = tk.Button(self.root, text="Add Sub-element", command=self.add_sub_element)
        self.add_sub_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Frame to hold sub-elements
        self.sub_elements_frame = tk.Frame(self.root)
        self.sub_elements_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Button to Create the XML
        self.create_button = tk.Button(self.root, text="Create XML", command=self.create_xml)
        self.create_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Status label for feedback
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)

    def add_sub_element(self):
        """Add a new row of inputs for a sub-element."""
        row_index = len(self.sub_elements)
        frame = tk.Frame(self.sub_elements_frame)
        frame.grid(row=row_index, column=0, columnspan=2, padx=10, pady=5)

        # Element Tag Input
        tk.Label(frame, text="Tag:").grid(row=0, column=0, padx=5)
        tag_entry = tk.Entry(frame, width=15)
        tag_entry.grid(row=0, column=1, padx=5)

        # Element Text Input
        tk.Label(frame, text="Text:").grid(row=0, column=2, padx=5)
        text_entry = tk.Entry(frame, width=15)
        text_entry.grid(row=0, column=3, padx=5)

        # Element Attributes Input (in the format key=value)
        tk.Label(frame, text="Attributes:").grid(row=0, column=4, padx=5)
        attr_entry = tk.Entry(frame, width=20)
        attr_entry.grid(row=0, column=5, padx=5)

        # Add the new sub-element inputs to the list
        self.sub_elements.append((tag_entry, text_entry, attr_entry))

    def create_xml(self):
        """Create an XML file based on the user's input."""
        root_element_name = self.root_element_entry.get()
        if not root_element_name:
            messagebox.showerror("Error", "Please provide a root element.")
            return

        # Create the root element
        root_element = ET.Element(root_element_name)

        # Loop through all sub-elements and add them to the root
        for tag_entry, text_entry, attr_entry in self.sub_elements:
            tag = tag_entry.get()
            text = text_entry.get()
            attr_input = attr_entry.get()

            if not tag:
                messagebox.showerror("Error", "Please provide a tag for each sub-element.")
                return

            # Create the sub-element
            sub_element = ET.SubElement(root_element, tag)
            sub_element.text = text if text else ""

            # Parse attributes (key=value pairs)
            if attr_input:
                attributes = self.parse_attributes(attr_input)
                sub_element.attrib.update(attributes)

        # Save the XML file
        self.save_xml(root_element)

    def parse_attributes(self, attr_input):
        """Parse attributes from a string in the format 'key1=value1,key2=value2'."""
        attributes = {}
        pairs = attr_input.split(",")
        for pair in pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                attributes[key.strip()] = value.strip()
        return attributes

    def save_xml(self, root_element):
        """Prompt user to save the XML file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            tree = ET.ElementTree(root_element)
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            self.status_label.config(text=f"XML file created successfully at {file_path}", fg="green")
        else:
            self.status_label.config(text="XML creation cancelled.", fg="red")

# Create the main Tkinter window
root = tk.Tk()

# Run the application
app = XMLCreatorApp(root)
root.mainloop()
