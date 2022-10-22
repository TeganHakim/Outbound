import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter
import tkcalendar
import datetime
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
# Tkinter App
class App(customtkinter.CTk):
    # Dimensions
    WIDTH = 1200
    HEIGHT = 720

    MINWIDTH = 780
    MINHEIGHT = 520

    def __init__(self):
        super().__init__()
        self.title("Outbound v1.0")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(App.MINWIDTH, App.MINHEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  
        # Configure grid layout for whole app
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Left side
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.switch_frame(MessageCenter)
        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.title = customtkinter.CTkLabel(master=self.frame_left,
                                            text="Outbound SMS",
                                            text_font=("Roboto Medium", -22, "bold")) 
        self.title.grid(row=0, column=0, pady=(10, 0), padx=10)

        self.subtitle = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Top Notch Sports",
                                              text_font=("Roboto Medium", -15, "italic"))
        self.subtitle.grid(row=1, column=0, pady=(0, 10), padx=10)

        self.message_center_frame = customtkinter.CTkFrame(master=self.frame_left,
                                                            width=180,
                                                            corner_radius=0,
                                                            fg_color=self.frame_right.bg_color)
        self.message_center_frame.grid(row=2, column=0, sticky="nswe")

        self.message_center_button = customtkinter.CTkButton(master=self.message_center_frame,
                                                            text="Message Center",
                                                            command=self.message_center)
        self.message_center_button.grid(row=2, column=0, pady=10, padx=20)

        self.client_manager_frame = customtkinter.CTkFrame(master=self.frame_left,
                                                            width=180,
                                                            corner_radius=0,
                                                            fg_color=self.frame_left.fg_color)
        self.client_manager_frame.grid(row=3, column=0, sticky="nswe")
        self.client_manager_button = customtkinter.CTkButton(master=self.client_manager_frame,
                                                            text="Client Manager",
                                                            command=self.client_manager)
        self.client_manager_button.grid(row=3, column=0, pady=10, padx=20)

        self.appearance_label = customtkinter.CTkLabel(master=self.frame_left, 
                                                        text="Appearance Mode:",
                                                        text_font=("Roboto Medium", -14))
        self.appearance_label.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.appearance_dropdown = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode)
        self.appearance_dropdown.grid(row=10, column=0, pady=(5, 10), padx=20, sticky="w")
        self.appearance_dropdown.set("Dark")

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self.frame_right is not None:
            self.frame_right.destroy()
        self.frame_right = new_frame
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    
    def on_closing(self, event=0):
        self.destroy()

    def message_center(self):
        self.switch_frame(MessageCenter)
        self.message_center_frame.configure(fg_color=self.frame_right.bg_color)
        self.client_manager_frame.configure(fg_color=self.frame_left.fg_color)

    def client_manager(self):
        self.switch_frame(ClientManager)
        self.message_center_frame.configure(fg_color=self.frame_left.fg_color)
        self.client_manager_frame.configure(fg_color=self.frame_right.bg_color)

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

class MessageCenter(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=0, sticky="nswe")
        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")
        # ============ frame_info ============

        # configure grid layout (1x1)
        # self.frame_info.rowconfigure(0, minsize=50)
        self.frame_info.rowconfigure(1, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.message_label = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="Message Content:",
                                                    text_font=("Roboto Medium", -18, "bold"))
        self.message_label.grid(column=0, row=0, sticky="new", padx=(15, 10), pady=(10, 0))
        self.message = customtkinter.CTkTextbox(master=self.frame_info,
                                                corner_radius=10,
                                                fg_color=("white", "gray38"),
                                                text_font=("Roboto", -14))
        self.message.grid(column=0, row=1, sticky="nsew", padx=15, pady=(10, 15))
        # ============ frame_right ============

        self.selected_groups_label = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Selected Groups:",
                                                        text_font=("Roboto Medium", -16, "bold"))
        self.selected_groups_label.grid(row=0, column=2, columnspan=1, pady=(20, 0), padx=(0, 20), sticky="")

        self.selected_groups_frame = customtkinter.CTkFrame(master=self.frame_right)
        self.selected_groups_frame.grid(row=1, column=2, pady=10, padx=(0, 20), sticky="nsew")
        self.selected_groups_frame.rowconfigure(0, weight=1)
        self.selected_groups_frame.rowconfigure(1, weight=1)
        self.selected_groups_frame.rowconfigure(2, weight=1)
        self.selected_groups_frame.rowconfigure(3, weight=1)
        self.selected_groups_frame.rowconfigure(4, weight=1)

        self.selected_group_1 = customtkinter.CTkCheckBox(master=self.selected_groups_frame,
                                                     text="Paypal")
        self.selected_group_1.grid(row=0, column=0, pady=(20, 5), padx=20, sticky="nws")
        self.selected_group_2 = customtkinter.CTkCheckBox(master=self.selected_groups_frame,
                                                     text="Venmo")
        self.selected_group_2.grid(row=1, column=0, pady=5, padx=20, sticky="nws")
        self.selected_group_3 = customtkinter.CTkCheckBox(master=self.selected_groups_frame,
                                                     text="Zelle")
        self.selected_group_3.grid(row=2, column=0, pady=5, padx=20, sticky="nws")
        self.selected_group_4 = customtkinter.CTkCheckBox(master=self.selected_groups_frame,
                                                     text="CashApp")
        self.selected_group_4.grid(row=3, column=0, pady=5, padx=20, sticky="nws")
        self.selected_group_5 = customtkinter.CTkCheckBox(master=self.selected_groups_frame,
                                                     text="Credit/Debit")
        self.selected_group_5.grid(row=4, column=0, pady=(5, 20), padx=20, sticky="nws")

        self.date_select_label = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Scheduled Send:",
                                                        text_font=("Roboto Medium", -16, "bold"))
        self.date_select_label.grid(row=3, column=2, columnspan=1, pady=(20, 0), padx=(0, 20), sticky="")
        self.date_select_frame = customtkinter.CTkFrame(master=self.frame_right)
        self.date_select_frame.grid(row=4, column=2, pady=10, padx=(0, 20), sticky="nsew")
        self.date_select_frame.rowconfigure((1, 2, 3, 4), weight=1)
        self.date_select_frame.columnconfigure((0, 1), weight=1)
        self.month = customtkinter.CTkComboBox(master=self.date_select_frame,
                                                command=self.month_changed,
                                                values=("January", "February", "March", "April", "May", "June", 
                                                "July", "August", "September", "October", "November", "December"))                            
        self.month.grid(row=0, column=0, pady=10, padx=5, sticky="nsew")  
        self.month.set(datetime.datetime.now().strftime("%B"))      
        self.day = customtkinter.CTkComboBox(master=self.date_select_frame,
                                            command=self.day_changed,
                                            values=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
                                            "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24",
                                             "25", "26", "27", "28", "29", "30", "31"))
        self.day.grid(row=1, column=0, pady=10, padx=5, sticky="nsew")
        self.day.set(datetime.datetime.now().day)
        current_year = datetime.datetime.now().year
        self.year = customtkinter.CTkComboBox(master=self.date_select_frame,
                                            command=self.year_changed,
                                            values=(str(current_year), str(current_year + 1), str(current_year + 2)))
        self.year.grid(row=2, column=0, pady=10, padx=5, sticky="nsew")
        self.year.set(current_year)
        self.time = customtkinter.CTkEntry(master=self.date_select_frame,
                                            width=100,
                                            placeholder_text="hh:mm")
        self.time.grid(row=3, column=0, pady=10, padx=5, sticky="nsw")
        self.am_pm = customtkinter.CTkComboBox(master=self.date_select_frame,
                                            width=75,
                                            command=self.am_pm_changed,
                                            values=["AM", "PM"])
        self.am_pm.grid(row=3, column=0, pady=10, padx=5, sticky="nse")
        
        self.instant = customtkinter.IntVar(value=1)
        self.instant_switch = customtkinter.CTkSwitch(master=self.date_select_frame, 
                                                    text="Send Instantly", 
                                                    command=self.instant_changed,
                                                    variable=self.instant, 
                                                    onvalue=1, 
                                                    offvalue=0,
                                                    text_font=("Roboto Medium", -16))
        self.instant_switch.grid(row=4, column=0, pady=(5, 10), padx=20, sticky="we")
        self.sendMessage = customtkinter.CTkButton(master=self.frame_right,
                                                text="Send Message",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.button_event)
        self.sendMessage.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

    def button_event(self):
        print(self.master.winfo_width())

    def month_changed(self, event):
        if str(event) != str(datetime.datetime.now().strftime("%B")):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if int(self.day.get()) == int(datetime.datetime.now().day) and int(self.year.get()) == int(datetime.datetime.now().year):
                self.instant_switch.select()
                self.instant.set(1)            

    def day_changed(self, event):
        if int(event) != int(datetime.datetime.now().day):
            self.instant_switch.deselect();
            self.instant.set(0)
        else:
            if str(self.month.get()) == str(datetime.datetime.now().strftime("%B")) and int(self.year.get()) == int(datetime.datetime.now().year):
                self.instant_switch.select()
                self.instant.set(1)
            
    def year_changed(self, event):
        if int(event) != int(datetime.datetime.now().year):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if str(self.month.get()) == str(datetime.datetime.now().strftime("%B")) and int(self.day.get()) == int(datetime.datetime.now().day):
                self.instant_switch.select()
                self.instant.set(1)
    def am_pm_changed(self, event):
        pass
    def instant_changed(self):
        if self.instant.get() == 1:
            self.month.set(datetime.datetime.now().strftime("%B"))
            self.day.set(datetime.datetime.now().day)
            self.year.set(datetime.datetime.now().year)

class ClientManager(customtkinter.CTkFrame):
    def __init__(self, master):
        customtkinter.CTkFrame.__init__(self, master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=0, sticky="nswe")

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(5, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=9, pady=20, padx=20, sticky="nsew")
        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(1, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.client_list_label = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="Client List:",
                                                    text_font=("Roboto Medium", -18, "bold"))
        self.client_list_label.grid(column=0, row=0, sticky="new", padx=(15, 10), pady=(10, 0))
        self.client_list = customtkinter.CTkTextbox(master=self.frame_info,
                                                corner_radius=10,
                                                height=200,
                                                fg_color=("white", "gray38"),
                                                text_font=("Roboto", -14))
        self.client_list.grid(row=1, column=0, sticky="nsew", padx=15, pady=(10, 15))
        with open("clients.csv", "r") as f:
            self.client_list.insert('0.0', f.read())
        self.client_list.configure(state="disabled") #read only

        self.client_list_scrollbar = customtkinter.CTkScrollbar(self.frame_info, 
                                                                scrollbar_color=self.frame_right.bg_color,
                                                                fg_color=("white", "gray38"),
                                                                corner_radius=10,
                                                                command=self.client_list.yview)
        self.client_list_scrollbar.grid(row=1, column=0, sticky="nse", pady=(15, 25), padx=(0, 15))
        self.client_list.configure(yscrollcommand=self.client_list_scrollbar.set)

        # ============ frame_right ============
        self.upload_file_label = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Update Client List:",
                                                        text_font=("Roboto Medium", -16, "bold"))
        self.upload_file_label.grid(row=0, column=2, columnspan=1, pady=(20, 0), padx=(0, 20), sticky="")
        self.upload_file_button = customtkinter.CTkButton(master=self.frame_right,
                                                text="Upload File",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.upload_file)
        self.upload_file_button.grid(row=1, column=2, pady=0, padx=(0, 20), sticky="new")


        self.filter_groups_label = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Filter by Group:",
                                                        text_font=("Roboto Medium", -16, "bold"))
        self.filter_groups_label.grid(row=6, column=2, columnspan=1, pady=(20, 0), padx=(0, 20), sticky="")

        self.filter_groups_frame = customtkinter.CTkFrame(master=self.frame_right)
        self.filter_groups_frame.grid(row=7, column=2, pady=10, padx=(0, 20), sticky="nsew")
        self.filter_groups_frame.rowconfigure(0, weight=1)
        self.filter_groups_frame.rowconfigure(1, weight=1)
        self.filter_groups_frame.rowconfigure(2, weight=1)
        self.filter_groups_frame.rowconfigure(3, weight=1)
        self.filter_groups_frame.rowconfigure(4, weight=1)

        self.filter_group_1 = customtkinter.CTkCheckBox(master=self.filter_groups_frame,
                                                     text="Paypal")
        self.filter_group_1.grid(row=0, column=0, pady=(20, 5), padx=20, sticky="nws")
        self.filter_group_2 = customtkinter.CTkCheckBox(master=self.filter_groups_frame,
                                                     text="Venmo")
        self.filter_group_2.grid(row=1, column=0, pady=5, padx=20, sticky="nws")
        self.filter_group_3 = customtkinter.CTkCheckBox(master=self.filter_groups_frame,
                                                     text="Zelle")
        self.filter_group_3.grid(row=2, column=0, pady=5, padx=20, sticky="nws")
        self.filter_group_4 = customtkinter.CTkCheckBox(master=self.filter_groups_frame,
                                                     text="CashApp")
        self.filter_group_4.grid(row=3, column=0, pady=5, padx=20, sticky="nws")
        self.filter_group_5 = customtkinter.CTkCheckBox(master=self.filter_groups_frame,
                                                     text="Credit/Debit")
        self.filter_group_5.grid(row=4, column=0, pady=(5, 20), padx=20, sticky="nws")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="CTkButton",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.button_event)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=(0, 20), sticky="we")

    def button_event(self):
        print("Button pressed")

    def upload_file(self):
        file_types = [('Excel Files', '*.xlsx'), ('CSV Files', '*.csv'), ('All Files', '*.*')]
        filename = filedialog.askopenfilename(title="Import Client List", filetypes=file_types)

if __name__ == "__main__":
    app = App()
    app.mainloop()