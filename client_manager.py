# Import libraries for tkinter GUI and system utilities
import tkinter
import tkinter.messagebox
from tkinter import filedialog
import customtkinter
import base64, os
from util import getSubDir

# ==================== #
# Client Manager Frame #
# ==================== #
class ClientManager(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)

        # Configure grid layout for frame
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        # Create frame for Client Manager
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row = 0, column = 0, sticky  ="nsew")

        # Configure Client Manager frame's grid layout
        self.frame_right.rowconfigure((0, 1, 2, 3), weight = 1)
        self.frame_right.rowconfigure(5, weight = 10)
        self.frame_right.columnconfigure((0, 1), weight = 1)
        self.frame_right.columnconfigure(2, weight = 0)
        
        # Configure client list frame
        self.client_list_frame = customtkinter.CTkFrame(master = self.frame_right, corner_radius = 10)
        self.client_list_frame.grid(row = 0, column = 0, columnspan = 2, rowspan = 9, pady = 20, padx = 20, sticky = "nsew")

        # Configure client list frame's grid layout
        self.client_list_frame.rowconfigure(1, weight = 1)
        self.client_list_frame.columnconfigure(0, weight = 1)

        # Display client list frame title
        self.client_list_label = customtkinter.CTkLabel(master = self.client_list_frame, text = "Client List:", text_font = ("Roboto Medium", -18, "bold"))
        self.client_list_label.grid(column = 0, row = 0, sticky = "new", padx = (15, 10), pady = (10, 0))
        
        # Configure client list textbox
        self.client_list = customtkinter.CTkTextbox(master = self.client_list_frame, corner_radius = 10, height = 200, fg_color = ("white", "gray38"), text_color = ("gray38", "white"), text_font = ("Roboto", -14))
        self.client_list.grid(row = 1, column = 0, sticky = "nsew", padx = 15, pady = (10, 15))

        # Initialize as read-only 
        self.client_list.configure(state = "disabled")

        # Configure client list scrollbar
        self.client_list_scrollbar = customtkinter.CTkScrollbar(master = self.client_list_frame, scrollbar_color = self.frame_right.bg_color, fg_color = ("white", "gray38"), corner_radius = 10, command = self.client_list.yview)
        self.client_list_scrollbar.grid(row = 1, column = 0, sticky = "nse", pady = (15, 25), padx = (0, 15))
        self.client_list.configure(yscrollcommand = self.client_list_scrollbar.set)

        # Configure client list utility button frame
        self.utility_frame = customtkinter.CTkFrame(master = self.client_list_frame, corner_radius = 10, fg_color = self.client_list_frame.fg_color)
        self.utility_frame.grid(row = 2, column = 0, sticky = "nsew")
        
        # Configure client list utility button frame's grid layout
        self.utility_frame.rowconfigure(0, weight = 1)
        self.utility_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight = 1)

        # Utility edit button
        self.edit_button = customtkinter.CTkButton(master = self.utility_frame, text = "Edit", border_width = 2, text_font = ("Roboto Medium", -14), fg_color = None, command = self.edit_client_list)
        self.edit_button.grid(row = 2, column = 2, sticky = "nsew", padx = 15, pady = (0, 15))
        self.save_button = customtkinter.CTkButton(master = self.utility_frame, text = "Save/Update", border_width = 2, text_font = ("Roboto Medium", -14), fg_color = None, command = self.save_client_list)

        # Utility save button
        self.save_button.grid(row = 2, column = 3, sticky = "nsew", padx = 15, pady = (0, 15))
        
        # Display upload file title
        self.upload_file_label = customtkinter.CTkLabel(master = self.frame_right, text = "Update Client List:", text_font = ("Roboto Medium", -16, "bold"))
        self.upload_file_label.grid(row = 0, column = 2, columnspan = 1, pady = (20, 0), padx = (0, 20))

        # Configure upload file button
        self.upload_file_button = customtkinter.CTkButton(master = self.frame_right, text = "Upload File", border_width = 2, fg_color = None, command = self.upload_file)
        self.upload_file_button.grid(row = 1, column = 2, pady = (5, 0), padx = (0, 20), sticky = "new")

        # Display filename text for upload button
        self.view_file_filenaming_label = customtkinter.CTkLabel(master = self.frame_right, text = "(leadName mm/dd/yyyy)", text_font = ("Roboto Medium", -12, "italic"))
        self.view_file_filenaming_label.grid(row =3 , column = 2, pady = (0, 5), padx = (0, 20), sticky = "new")
        

        # Display view file title
        self.view_file_label = customtkinter.CTkLabel(master = self.frame_right, text = "View List:", text_font = ("Roboto Medium", -16, "bold"))
        self.view_file_label.grid(row = 4, column = 2, columnspan = 1, pady = (5, 0), padx = (0, 20))
        
        # Configure view file listbox
        self.view_file = tkinter.Listbox(self.frame_right, activestyle = "none", bg = "gray38", fg = "white", font = ("Roboto", -16), highlightthickness = 0, highlightbackground = "gray38", bd = 0)
        self.view_file.grid(row = 5, column = 2, pady = (5, 0), padx = (0, 20), sticky = "nsew")
        # Initialize view file list as empty array
        self.view_file_list = []
        # Display values in view file listbox
        self.populate_view_file()
        self.update_view_file()
        # Bind mouse event to view file listbox
        self.view_file.bind("<ButtonRelease-1>", self.view_file_clicked)

        # Display filter groups title
        self.filter_groups_label = customtkinter.CTkLabel(master = self.frame_right, text = "Statistics:", text_font = ("Roboto Medium", -16, "bold"))
        self.filter_groups_label.grid(row = 6, column = 2, columnspan = 1, pady = (10, 0), padx = (0, 20))

        # Configure filter groups frame
        self.filter_groups_frame = customtkinter.CTkFrame(master = self.frame_right)
        self.filter_groups_frame.grid(row = 7, column = 2, pady = 10, padx = (0, 20), sticky = "nsew")
        
        # Configure filter groups frame's grid layout
        self.filter_groups_frame.rowconfigure(0, weight = 1)
        self.filter_groups_frame.rowconfigure(1, weight = 1)
        self.filter_groups_frame.rowconfigure(2, weight = 1)
        self.filter_groups_frame.rowconfigure(3, weight = 1)
        self.filter_groups_frame.rowconfigure(4, weight = 1)

        # Configure filter groups frame's checbox options
        self.filter_group_1 = customtkinter.CTkCheckBox(master = self.filter_groups_frame, text = "Paypal")
        self.filter_group_1.grid(row = 0, column = 0, pady = (20, 5), padx = 20, sticky = "nws")
        self.filter_group_2 = customtkinter.CTkCheckBox(master = self.filter_groups_frame, text = "Venmo")
        self.filter_group_2.grid(row = 1, column=0, pady=5, padx=20, sticky = "nws")
        self.filter_group_3 = customtkinter.CTkCheckBox(master=self.filter_groups_frame, text="Zelle")
        self.filter_group_3.grid(row = 2, column=0, pady=5, padx=20, sticky="nws")
        self.filter_group_4 = customtkinter.CTkCheckBox(master=self.filter_groups_frame, text="CashApp")
        self.filter_group_4.grid(row = 3, column=0, pady=5, padx=20, sticky="nws")
        self.filter_group_5 = customtkinter.CTkCheckBox(master=self.filter_groups_frame, text="Credit/Debit")
        self.filter_group_5.grid(row = 4, column=0, pady=(5, 10), padx=20, sticky="nws")
        self.button_5 = customtkinter.CTkButton(master=self.frame_right, text="CTkButton", border_width=2, fg_color=None)
        self.button_5.grid(row = 8, column = 2, columnspan=1, pady=15, padx=(0, 20), sticky="we")
         
    # Upload Excel or CSV file to Client Manager, save locally
    def upload_file(self):
        file_types = [('CSV Files', '*.csv'), ('Excel Files', '*.xlsx'), ('All Files', '*.*')]
        client_file = filedialog.askopenfilename(title="Import Client List", filetypes=file_types)
        # Base-64 encoding ignores spacing and special characters
        encoded_file = base64.urlsafe_b64encode(client_file.encode('UTF-8'))
        clean_file = base64.urlsafe_b64decode(encoded_file.decode('UTF-8'))
        with open(clean_file, "r") as client:
            file_content = client.read()        
            client_surname = client_file.split("/")[-1]
            filepath = os.getcwd() + "/clients/" + client_surname
            with open(filepath, 'w') as local:
                local.write(file_content)
            self.client_list_label.configure(text="Client List: " + client_surname)
            self.client_list.configure(state="normal")
            self.client_list.delete('0.0', 'end')
            self.client_list.insert('0.0', file_content)    
            self.edit_button.configure(text="Edit")
            self.client_list.configure(state="disabled")     

    # Edit clientel list
    def edit_client_list(self):
        if self.client_list.cget("state") == "disabled":
            self.client_list.configure(state = "normal")
            self.edit_button.configure(text = "Cancel")
        else:
            self.client_list.configure(state = "disabled")
            self.edit_button.configure(text = "Edit")
    
        if self.client_list.cget("state") == "normal":
            self.save_button.configure(fg_color = "#B66A58")
        else:
            self.save_button.configure(fg_color = self.edit_button.fg_color)
    
    # Save clientel list
    def save_client_list(self):
        self.save_button.configure(fg_color=self.edit_button.fg_color)
        client_list = self.client_list.get("0.0", "end")
        client_surname = self.client_list_label.cget("text").split(": ")[-1]
        if client_surname.strip() != "Client List: ".strip():
            filepath = os.getcwd() + getSubDir(client_surname) + client_surname
            with open(filepath, 'w') as f:
                f.write(client_list)
            self.edit_button.configure(text = "Edit")
            self.client_list.configure(state = "disabled")

    # Add all files to view file list
    def populate_view_file(self):
        master_files = os.listdir(os.getcwd() + "/masters")
        for file in master_files:
            self.view_file_list.append(file)
        client_files = os.listdir(os.getcwd() + "/clients")
        for file in client_files:
            self.view_file_list.append(file)
    
    # update view file listbox with values
    def update_view_file(self):
        for file in self.view_file_list:
            self.view_file.insert("end", file)
    
    # Triggered by <ButtonRelease-1> event on view file listbox
    def view_file_clicked(self, event):
        client_surname = self.view_file.get(self.view_file.curselection())
        original_filepath = os.getcwd() + getSubDir(client_surname) + client_surname
        file_content = open(original_filepath, "r").read()        
        self.client_list_label.configure(text = "Client List: " + client_surname)
        self.client_list.configure(state = "normal")
        self.client_list.delete('0.0', 'end')
        self.client_list.insert('0.0', file_content)    
        self.edit_button.configure(text = "Edit")
        self.client_list.configure(state = "disabled")   