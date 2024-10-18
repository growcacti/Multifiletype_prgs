import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET

class XMLParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Parser")
        
        # Load XML button
        self.load_button = tk.Button(root, text="Load XML", command=self.load_xml)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Frame to display XML content
        self.content_frame = tk.Frame(root)
        self.content_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
    def load_xml(self):
        # Open file dialog to select XML file
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            # Parse XML file
            tree = ET.parse(file_path)
            root_element = tree.getroot()
            
            # Clear the content frame before displaying new content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Display XML content
            self.display_xml(root_element, self.content_frame, row=0)
    
    def display_xml(self, element, parent, row):
        """Recursively display XML elements and their attributes in the Tkinter grid."""
        tk.Label(parent, text=f"Tag: {element.tag}", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w")
        
        if element.attrib:
            tk.Label(parent, text=f"Attributes: {element.attrib}", font=("Arial", 10)).grid(row=row, column=1, sticky="w")
        
        row += 1
        
        if element.text and element.text.strip():
            tk.Label(parent, text=f"Text: {element.text.strip()}", font=("Arial", 10)).grid(row=row, column=1, sticky="w")
            row += 1
        
        for child in element:
            row = self.display_xml(child, parent, row)
        
        return row

# Create the main window
root = tk.Tk()

# Make the window resizable
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Run the application
app = XMLParserApp(root)
root.mainloop()
