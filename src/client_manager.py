# Import libraries for tkinter GUI and system utilities
import tkinter
import tkinter.messagebox
from tkinter import filedialog
import customtkinter
import base64, os
import toml, tomli
from util import getSubDir

# ==================== #
# Client Manager Frame #
# ==================== #
class ClientManager(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.PATH = os.getcwd().replace("\src", "")

        # Loads all data from toml file
        with open(self.PATH + "\config.toml", "rb") as toml:
            self.config = tomli.load(toml)

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
        if self.config["client_manager"]["filename"] != "":
            self.client_list_label.configure(text = "Client List: " + self.config["client_manager"]["filename"])
        
        # Configure client list textbox
        self.client_list = customtkinter.CTkTextbox(master = self.client_list_frame, corner_radius = 10, height = 200, fg_color = ("white", "gray38"), text_color = ("gray38", "white"), text_font = ("Roboto", -14))
        self.client_list.grid(row = 1, column = 0, sticky = "nsew", padx = 15, pady = (10, 15))
        # Initialize as read-only 
        self.client_list.configure(state = "disabled")
        self.file_open = False

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

        # Configure statistics frame
        self.statistics_label_frame =  customtkinter.CTkFrame(master = self.frame_right, corner_radius = 10, fg_color = self.frame_right.fg_color)
        self.statistics_label_frame.grid(row = 6, column = 2, pady = (10, 0), padx = (0, 20), sticky = "nsew")
        
        # Configure statistics frame's grid layout
        self.statistics_label_frame.rowconfigure(0, weight = 1)
        self.statistics_label_frame.columnconfigure(0, weight = 1)
        self.statistics_label_frame.columnconfigure((1, 2), weight = 1)
        self.statistics_label_frame.columnconfigure(3, weight = 1)

        # Display statistics label
        self.statistics_label = customtkinter.CTkLabel(master = self.statistics_label_frame, text = "Statistics", text_font = ("Roboto Medium", -16, "bold"))
        self.statistics_label.grid(row = 0, column = 1, columnspan = 1)

        #Display refresh Button
        self.statistics_refresh = customtkinter.CTkButton(master = self.statistics_label_frame, text = "↻", text_font = ("Roboto Medium", -14, "bold"), border_width= 2, fg_color=None, width = 20, command = self.update_statistics)
        self.statistics_refresh.grid(row = 0, column = 2, padx = (0, 30))

        # Configure filter groups frame
        self.statistics_frame = customtkinter.CTkFrame(master = self.frame_right)
        self.statistics_frame.grid(row = 7, column = 2, pady = 10, padx = (0, 20), sticky = "nsew")
        
        # Configure filter groups frame's grid layout
        self.statistics_frame.rowconfigure(0, weight = 1)
        self.statistics_frame.columnconfigure(0, weight = 1)
        # Configure statistics read-only text box
        self.statistics = customtkinter.CTkTextbox(master = self.statistics_frame, height = 100, fg_color = self.frame_right.bg_color, text_font = ("Roboto Medium", -13))
        self.statistics.grid(row = 0, column = 0, columnspan = 1, rowspan = 2, pady = (5, 0), padx = (0, 0), sticky = "nsew")
        # Configure statistics scrollbar
        self.statistics_scrollbar = customtkinter.CTkScrollbar(master = self.statistics_frame, scrollbar_color = ("white", "grey38"), fg_color = self.frame_right.bg_color, corner_radius = 10, command = self.statistics.yview)
        self.statistics_scrollbar.grid(row = 0, column = 0, sticky = "nse", pady = (5, 3), padx = (0, 0))
        self.statistics.configure(yscrollcommand = self.statistics_scrollbar.set)
        # Update the statistics text
        self.update_statistics()
        # Read-only
        self.statistics.configure(state = "disabled")

        # Clear all button
        self.clear = customtkinter.CTkButton(master = self.frame_right, text = "Clear File", border_width = 2, fg_color = None, command = self.clear_file)
        self.clear.grid(row = 8, column = 2, columnspan = 1, pady = 15, padx = (0, 20), sticky = "ew")
         
        if self.config["client_manager"]["filename"] != "":
            self.file_viewer(self.config["client_manager"]["filename"])
            self.view_file.select_set(self.view_file_list.index(self.config["client_manager"]["filename"]))

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
            filepath = self.PATH + "\clients\\" + client_surname
            with open(filepath, 'w') as local:
                local.write(file_content)
            self.client_list_label.configure(text="Client List: " + client_surname)
            self.client_list.configure(state="normal")
            self.client_list.delete('0.0', 'end')
            self.client_list.insert('0.0', file_content)  
            self.file_open = True  
            self.edit_button.configure(text="Edit")
            self.client_list.configure(state="disabled")     

    # Clear file
    def clear_file(self):
        self.client_list.configure(state = "normal")
        self.client_list.delete('0.0', 'end')
        self.client_list.configure(state = "disabled")
        self.file_open = False
        self.edit_button.configure(text = "Edit")
        self.client_list_label.configure(text = "Client List:")
        self.view_file.selection_clear(0, 'end')
        self.update_statistics()
        
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
            filepath = self.PATH + getSubDir(client_surname) + client_surname
            with open(filepath, 'w') as f:
                f.write(client_list)
            self.edit_button.configure(text = "Edit")
            self.client_list.configure(state = "disabled")
            self.update_statistics()

    # Add all files to view file list
    def populate_view_file(self):
        master_files = os.listdir(self.PATH + "\masters")
        for file in master_files:
            self.view_file_list.append(file)
        client_files = os.listdir(self.PATH + "\clients")
        for file in client_files:
            self.view_file_list.append(file)
    
    # update view file listbox with values
    def update_view_file(self):
        for file in self.view_file_list:
            self.view_file.insert("end", file)
    
    # Triggered by <ButtonRelease-1> event on view file listbox
    def view_file_clicked(self, event):
        client_surname = self.view_file.get(self.view_file.curselection())
        self.file_viewer(client_surname)
    
    # View file
    def file_viewer(self, client_surname):
        original_filepath = self.PATH + getSubDir(client_surname) + client_surname
        file_content = open(original_filepath, "r").read()        
        self.client_list_label.configure(text = "Client List: " + client_surname)
        self.client_list.configure(state = "normal")
        self.client_list.delete('0.0', 'end')
        self.client_list.insert('0.0', file_content)   
        self.file_open = True 
        self.edit_button.configure(text = "Edit")
        self.client_list.configure(state = "disabled")  
        self.update_statistics() 

    # Update statistics
    def update_statistics(self):
        self.statistics.configure(state = "normal")
        self.statistics.delete("0.0", "end")
        total_clients = 0
        client_surname = self.client_list_label.cget("text").split(": ")[-1]
        if client_surname.strip() != "Client List: ".strip():
            filepath = self.PATH + getSubDir(client_surname) + client_surname
            total_clients = len(open(filepath, "r").read().strip().splitlines())
        message_rate = 50
        approx_time = round((total_clients) / message_rate, 2) 
        message_price = 0.0078
        num_credits = total_clients
        approx_price = round((total_clients) * message_price, 4)
        message = "Total Recieving Clients:\n- {} clients\n\nApproximate Send Time:\n- {} seconds\n\nApproximate Price:\n- {} credits (${})".format(total_clients, approx_time, num_credits, approx_price)
        self.statistics.insert("0.0", message)
        self.statistics.configure(state = "disabled")

    # Save data to toml
    def save_data(self):
        if self.file_open:
            self.config["client_manager"]["filename"] = self.client_list_label.cget("text").split(": ")[-1]
        else:
            self.config["client_manager"]["filename"] = ""
        data = toml.dumps(self.config)
        with open(self.PATH + "\config.toml", "w") as f:
            f.write(data)

    # Close app
    def on_closing(self, event = 0):
        self.save_data()
        self.master.destroy()