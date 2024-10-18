import tkinter as tk
from tkinter import filedialog, messagebox
import vobject
import quopri  # Add this import for decoding

class VCFEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VCF Contact Viewer/Editor")
        self.root.geometry("600x400")
        self.contacts = []

        # Setup GUI elements
        self.setup_widgets()

    def setup_widgets(self):
        # Button to open VCF file
        self.open_button = tk.Button(self.root, text="Open VCF File", command=self.open_vcf_file)
        self.open_button.pack(pady=10)

        # Listbox to show contacts
        self.contact_list = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.contact_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Entry widgets for editing selected contact
        self.name_entry = tk.Entry(self.root)
        self.phone_entry = tk.Entry(self.root)
        self.email_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)
        self.phone_entry.pack(pady=5)
        self.email_entry.pack(pady=5)

        # Save button
        self.save_button = tk.Button(self.root, text="Save Changes", command=self.save_changes)
        self.save_button.pack(pady=10)

        # Bind listbox selection
        self.contact_list.bind("<<ListboxSelect>>", self.show_contact_details)

    def open_vcf_file(self):
        # Open file dialog to select VCF file
        file_path = filedialog.askopenfilename(filetypes=[("VCF files", "*.vcf")])
        if not file_path:
            return

        # Read and decode VCF file
        with open(file_path, "r") as file:
            raw_data = file.read()

        # Decode quoted-printable encoded content if necessary
        decoded_data = quopri.decodestring(raw_data).decode('utf-8')

        # Parse VCF data
        try:
            self.contacts = list(vobject.readComponents(decoded_data))
        except vobject.base.ParseError as e:
            messagebox.showerror("Parse Error", f"Failed to parse the VCF file: {e}")
            return

        # Populate the contact list
        self.contact_list.delete(0, tk.END)
        for contact in self.contacts:
            name = contact.fn.value if hasattr(contact, 'fn') else "Unknown"
            self.contact_list.insert(tk.END, name)

    def show_contact_details(self, event):
        # Display selected contact details
        index = self.contact_list.curselection()
        if not index:
            return
        contact = self.contacts[index[0]]
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.name_entry.insert(0, contact.fn.value if hasattr(contact, 'fn') else "")
        phone = next((tel.value for tel in contact.tel_list), "") if hasattr(contact, 'tel_list') else ""
        email = contact.email.value if hasattr(contact, 'email') else ""
        self.phone_entry.insert(0, phone)
        self.email_entry.insert(0, email)

    def save_changes(self):
        # Save changes to the selected contact
        index = self.contact_list.curselection()
        if not index:
            messagebox.showwarning("Warning", "Select a contact to edit")
            return
        contact = self.contacts[index[0]]
        contact.fn.value = self.name_entry.get()
        contact.tel_list[0].value = self.phone_entry.get() if hasattr(contact, 'tel_list') else None
        if hasattr(contact, 'email'):
            contact.email.value = self.email_entry.get()
        messagebox.showinfo("Info", "Contact updated")

if __name__ == "__main__":
    root = tk.Tk()
    app = VCFEditorApp(root)
    root.mainloop()
