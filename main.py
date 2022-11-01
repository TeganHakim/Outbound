import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter
import datetime, re, os
import base64

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
# Tkinter App
class App(customtkinter.CTk):
    # Dimensions
    WIDTH = 1200
    HEIGHT = 720

    MINWIDTH = 860
    MINHEIGHT = 700

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

        # self.appearance_label = customtkinter.CTkLabel(master=self.frame_left, 
        #                                                 text="Appearance Mode:",
        #                                                 text_font=("Roboto Medium", -14))
        # self.appearance_label.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        # self.appearance_dropdown = customtkinter.CTkOptionMenu(master=self.frame_left,
        #                                                         values=["Light", "Dark", "System"],
        #                                                         command=self.change_appearance_mode)
        # self.appearance_dropdown.grid(row=10, column=0, pady=(5, 10), padx=20, sticky="w")
        # self.appearance_dropdown.set("Dark")

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

    # def change_appearance_mode(self, new_appearance_mode):
    #     customtkinter.set_appearance_mode(new_appearance_mode)

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
        self.message_label.grid(row=0, column=0, sticky="new", padx=(15, 10), pady=(10, 0))
        self.message = customtkinter.CTkTextbox(master=self.frame_info,
                                                corner_radius=10,
                                                fg_color=("white", "gray38"),
                                                text_font=("Roboto", -14))
        self.message.grid(row=1, column=0, sticky="nsew", padx=15, pady=(10, 15))

        self.send_filter_frame = customtkinter.CTkFrame(master=self.frame_right, corner_radius=10)
        self.send_filter_frame.grid(row=4, column=0, columnspan=2, rowspan=5, sticky="nsew", padx=15, pady=(0, 15))

        self.send_filter_frame.rowconfigure(1, weight=1)
        self.send_filter_frame.columnconfigure(0, weight=1)
        
        self.send_filter_label = customtkinter.CTkLabel(master=self.send_filter_frame,
                                                    corner_radius=10,
                                                    text="Filter By Date:",
                                                    text_font=("Roboto Medium", -18, "bold"))
        self.send_filter_label.grid(row=0, column=0, sticky="new", padx=(15, 10), pady=(10, 0))

        self.select_dates_frame = customtkinter.CTkFrame(master=self.send_filter_frame)
        self.select_dates_frame.grid(row=1, column=0, columnspan=2, rowspan=5, sticky="nsew", padx=15, pady=(0, 15))

        self.select_dates_frame.rowconfigure(0, weight=1)
        self.select_dates_frame.rowconfigure(1, weight=1)
        self.select_dates_frame.rowconfigure(2, weight=1)
        self.select_dates_frame.rowconfigure(3, weight=1)
        self.select_dates_frame.columnconfigure(0, weight=1)
        self.select_dates_frame.columnconfigure(1, weight=1)
        self.select_dates_frame.columnconfigure(2, weight=1)

        self.possible_dates = tkinter.Listbox(self.select_dates_frame, activestyle="none", bg="gray38", fg="white", font=("Roboto", -16), highlightthickness=0, highlightbackground= "gray38", bd=0)
        # self.possible_dates = customtkinter.CTkTextbox(self.select_dates_frame, 
        #                                                 fg_color=("white", "gray38"),
        #                                                 text_font=("Roboto", -16))
        self.possible_dates.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=(15, 0), pady=(10, 15))
        self.possible_dates_list = []
        self.possible_dates.bind("<FocusIn>", self.possible_dates_focused)
        self.possible_dates.bind("<FocusOut>", self.possible_dates_unfocused)
        self.possible_dates_focus = False

        self.select_button = customtkinter.CTkButton(master=self.select_dates_frame,
                                                text="Select Date",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,
                                                command=self.select_date)  # <- no fg_color)
        self.select_button.grid(row=1, column=1, sticky="")
        self.delete_button = customtkinter.CTkButton(master=self.select_dates_frame,
                                                text="Remove Date",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,
                                                command=self.remove_date)  # <- no fg_color)
        self.delete_button.grid(row=2, column=1, sticky="")
        self.final_dates = tkinter.Listbox(self.select_dates_frame, activestyle="none", bg="gray38", fg="white", font=("Roboto", -16), highlightthickness=0, highlightbackground= "gray38", bd=0)
        # self.final_dates = customtkinter.CTkTextbox(self.select_dates_frame, fg_color=("white", "gray38"))
        self.final_dates.grid(row=0, column=2, rowspan=4, sticky="nsew", padx=(0, 15), pady=(10, 15))
        self.final_dates_list = []
        self.final_dates.bind("<FocusIn>", self.final_dates_focused)
        self.final_dates.bind("<FocusOut>", self.final_dates_unfocused)
        self.final_dates_focus = False
        # ============ frame_right ============

        self.selected_groups_label = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Filter Selection:",
                                                        text_font=("Roboto Medium", -16, "bold"))
        self.selected_groups_label.grid(row=0, column=2, columnspan=1, pady=(20, 0), padx=(0, 20), sticky="")

        self.selected_groups_frame = customtkinter.CTkFrame(master=self.frame_right)
        self.selected_groups_frame.grid(row=1, column=2, pady=10, padx=(0, 20), sticky="nsew")
        self.selected_groups_frame.rowconfigure(0, weight=1)
        self.selected_groups_frame.rowconfigure(1, weight=1)
        self.selected_groups_frame.rowconfigure(2, weight=1)
        self.selected_groups_frame.rowconfigure(3, weight=1)
        self.selected_groups_frame.rowconfigure(4, weight=1)

        self.filter_selection_master = customtkinter.CTkCheckBox(master=self.selected_groups_frame,
                                                     text="Master Files",
                                                     command=self.filter_selection,
                                                     onvalue="on", 
                                                     offvalue="off")
        self.filter_selection_master.grid(row=0, column=0, pady=(20, 5), padx=20, sticky="nws")
        self.filter_selection_client = customtkinter.CTkCheckBox(master=self.selected_groups_frame,
                                                     text="Client Files",
                                                     command=self.filter_selection,
                                                     onvalue="on", 
                                                     offvalue="off")
        self.filter_selection_client.grid(row=1, column=0, pady=5, padx=20, sticky="nws")
        # self.selected_group_3 = customtkinter.CTkCheckBox(master=self.selected_groups_frame,
        #                                              text="Zelle")
        # self.selected_group_3.grid(row=2, column=0, pady=5, padx=20, sticky="nws")
        # self.selected_group_4 = customtkinter.CTkCheckBox(master=self.selected_groups_frame,
        #                                              text="CashApp")
        # self.selected_group_4.grid(row=3, column=0, pady=5, padx=20, sticky="nws")
        # self.selected_group_5 = customtkinter.CTkCheckBox(master=self.selected_groups_frame,
        #                                              text="Credit/Debit")
        # self.selected_group_5.grid(row=4, column=0, pady=(5, 20), padx=20, sticky="nws")

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
       
        self.error_label = customtkinter.CTkLabel(master=self.date_select_frame,
                                                        text="",
                                                        text_color="#D5806B",
                                                        text_font=("Roboto", -12, "italic"))
        self.error_label.grid(row=4, column=0, columnspan=1, sticky="nsew")

        self.vcmd = (self.register(self.validate), '%P')
        self.ivcmd = (self.register(self.on_invalid),)

        self.time = customtkinter.CTkEntry(master=self.date_select_frame,
                                            width=100,
                                            fg_color=self.date_select_frame.bg_color,
                                            validate="focusout",
                                            validatecommand=self.vcmd, 
                                            invalidcommand=self.ivcmd,
                                            placeholder_text="hh:mm")
        self.time.grid(row=3, column=0, pady=10, padx=5, sticky="nsw")

        self.am_pm = customtkinter.CTkComboBox(master=self.date_select_frame,
                                            width=75,
                                            command=self.am_pm_changed,
                                            values=["AM", "PM"])
        self.am_pm.grid(row=3, column=0, pady=10, padx=5, sticky="nse")
        

        self.instant = customtkinter.IntVar(value=0)
        self.instant_switch = customtkinter.CTkSwitch(master=self.date_select_frame, 
                                                    text="Send Instantly", 
                                                    command=self.instant_changed,
                                                    variable=self.instant, 
                                                    onvalue=1, 
                                                    offvalue=0,
                                                    text_font=("Roboto Medium", -16))
        self.instant_switch.grid(row=5, column=0, pady=(5, 10), padx=20, sticky="we")
        self.send_message = customtkinter.CTkButton(master=self.frame_right,
                                                text="Send Message",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.send_message)
        self.send_message.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

    def button_event(self):
        pass

    def filter_selection(self):
        if (self.filter_selection_master.get() == "off" and self.filter_selection_client.get() == "off"):
            self.possible_dates_list = []
            self.final_dates_list = []
        if (self.filter_selection_master.get() == "on" and self.filter_selection_client.get() == "off"):
            self.possible_dates_list = []
            self.populate_masters()
            temp_final_list = []
            for date in self.final_dates_list:
                if date not in os.listdir(os.getcwd() + "/clients"):
                    temp_final_list.append(date)
            self.final_dates_list = temp_final_list
        if (self.filter_selection_master.get() == "off" and self.filter_selection_client.get() == "on"): 
            
            self.possible_dates_list = []
            self.populate_clients()
            temp_final_list = []
            for date in self.final_dates_list:
                if date not in os.listdir(os.getcwd() + "/masters"):
                   temp_final_list.append(date)
            self.final_dates_list = temp_final_list     
        if (self.filter_selection_master.get() == "on" and self.filter_selection_client.get() == "on"):
            self.possible_dates_list = []
            self.populate_masters()
            self.populate_clients()
        self.update_final_list()
        self.update_possible_list()
        

    def populate_clients(self):
        client_files = os.listdir(os.getcwd() + "/clients")
        for file in client_files:
            self.possible_dates_list.append(file)

    def populate_masters(self):
        master_files = os.listdir(os.getcwd() + "/masters")
        for file in master_files:
            self.possible_dates_list.append(file)

    def possible_dates_focused(self, event):
        self.possible_dates_focus = True;
    def possible_dates_unfocused(self, event):
        self.possible_dates_focus = False;
    def final_dates_focused(self, event):
        self.final_dates_focus = True;
    def final_dates_unfocused(self, event):
        self.final_dates_focus = False;


    def select_date(self):
        if self.possible_dates_focus == True and self.final_dates_focus == False:
            if self.possible_dates.get(self.possible_dates.curselection()) not in self.final_dates_list:
                self.final_dates_list.append(self.possible_dates.get(self.possible_dates.curselection()))
            self.possible_dates_list.remove(self.possible_dates.get(self.possible_dates.curselection()))
            self.update_final_list()
            self.update_possible_list()
 
    def remove_date(self):
        if self.final_dates_focus == True and self.possible_dates_focus == False:
            if self.final_dates.get(self.final_dates.curselection()) not in self.possible_dates_list:
                self.possible_dates_list.append(self.final_dates.get(self.final_dates.curselection()))
            self.final_dates_list.remove(self.final_dates.get(self.final_dates.curselection()))
            self.update_final_list()
            self.update_possible_list()
 
    def update_possible_list(self):
        self.possible_dates.delete(0, 'end')
        for date in self.possible_dates_list:
            if date not in self.final_dates_list:
                self.possible_dates.insert('end', date)

    def update_final_list(self):
        self.final_dates.delete(0, 'end')
        for date in self.final_dates_list:
            self.final_dates.insert('end', date)

    def send_message(self):
        self.master.focus()
        
    def month_changed(self, event):
        time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if str(event) != str(datetime.datetime.now().strftime("%B")):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if int(self.day.get()) == int(datetime.datetime.now().day) and int(self.year.get()) == int(datetime.datetime.now().year and str(self.time.get()) == str(time.strftime("%I:%M")) and str(self.am_pm.get()) == str(time.strftime("%p"))):
                self.instant_switch.select()
                self.instant.set(1)            

    def day_changed(self, event):
        time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if int(event) != int(datetime.datetime.now().day):
            self.instant_switch.deselect();
            self.instant.set(0)
        else:
            if str(self.month.get()) == str(datetime.datetime.now().strftime("%B")) and int(self.year.get()) == int(datetime.datetime.now().year and str(self.time.get()) == str(time.strftime("%I:%M")) and str(self.am_pm.get()) == str(time.strftime("%p"))):
                self.instant_switch.select()
                self.instant.set(1)
            
    def year_changed(self, event):
        time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if int(event) != int(datetime.datetime.now().year):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if str(self.month.get()) == str(datetime.datetime.now().strftime("%B")) and int(self.day.get()) == int(datetime.datetime.now().day and str(self.time.get()) == str(time.strftime("%I:%M")) and str(self.am_pm.get()) == str(time.strftime("%p"))):
                self.instant_switch.select()
                self.instant.set(1)

    def time_changed(self, *args):
        time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if str(self.time.get()) != str(time.strftime("%I%M")):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if str(self.month.get()) == str(datetime.datetime.now().strftime("%B")) and int(self.day.get()) == int(datetime.datetime.now().day) and int(self.year.get()) == int(datetime.datetime.now().year) and str(self.am_pm.get()) == str(time.strftime("%p")):
                self.instant_switch.select()
                self.instant.set(1)

    def am_pm_changed(self, event):
        time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if str(event) != str(time.strftime("%p")):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if str(self.month.get()) == str(datetime.datetime.now().strftime("%B")) and int(self.day.get()) == int(datetime.datetime.now().day) and int(self.year.get()) == int(datetime.datetime.now().year) and str(self.time.get()) == str(time.strftime("%I:%M")):
                self.instant_switch.select()
                self.instant.set(1)

    def show_message(self, error=''):
        self.error_label.configure(text=error)
        if (error == ''):
            self.time.configure(fg_color=self.date_select_frame.bg_color)
        else:
            self.time.configure(fg_color="#B66A58")

    def validate(self, event):   
        pattern = r'^(0?[1-9]|1[0-2]):[0-5][0-9]$'
        if (re.fullmatch(pattern, event) is None):
            return False
        self.show_message()
        return True         

    def on_invalid(self):
        self.show_message('Enter a valid time (hh:mm)')

    def instant_changed(self):
        if self.instant.get() == 1:
            self.month.set(datetime.datetime.now().strftime("%B"))
            self.day.set(datetime.datetime.now().day)
            self.year.set(datetime.datetime.now().year)
            self.time.delete(0, "end")
            time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
            self.time.insert(0, time.strftime("%I:%M"))
            self.am_pm.set(time.strftime("%p"))

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

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right,
                                                 corner_radius=10)
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
                                                text_color=("gray38", "white"),
                                                text_font=("Roboto", -14))
        self.client_list.grid(row=1, column=0, sticky="nsew", padx=15, pady=(10, 15))
        self.client_list.configure(state="disabled") #read only

        self.client_list_scrollbar = customtkinter.CTkScrollbar(self.frame_info, 
                                                                scrollbar_color=self.frame_right.bg_color,
                                                                fg_color=("white", "gray38"),
                                                                corner_radius=10,
                                                                command=self.client_list.yview)
        self.client_list_scrollbar.grid(row=1, column=0, sticky="nse", pady=(15, 25), padx=(0, 15))
        self.client_list.configure(yscrollcommand=self.client_list_scrollbar.set)

        self.utility_frame = customtkinter.CTkFrame(master=self.frame_info,
                                                    corner_radius=10,
                                                    fg_color=self.frame_info.fg_color)
        self.utility_frame.grid(row=2, column=0, sticky="nsew")
        self.utility_frame.rowconfigure(0, weight=1)
        self.utility_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.edit_button = customtkinter.CTkButton(master=self.utility_frame,
                                                    text="Edit",
                                                    border_width=2,
                                                    text_font=("Roboto Medium", -14, "bold"),
                                                    fg_color=None,
                                                    command=self.edit_client_list)
        self.edit_button.grid(row=2, column=2, sticky="nsew", padx=15, pady=(0, 15))
        self.save_button = customtkinter.CTkButton(master=self.utility_frame,
                                                    text="Save/Update",
                                                    border_width=2,
                                                    text_font=("Roboto Medium", -14, "bold"),
                                                    fg_color=None,
                                                    command=self.save_client_list)
        self.save_button.grid(row=2, column=3, sticky="nsew", padx=15, pady=(0, 15))
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
        file_types = [('CSV Files', '*.csv'), ('Excel Files', '*.xlsx'), ('All Files', '*.*')]
        client_file = filedialog.askopenfilename(title="Import Client List", filetypes=file_types)
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
    
    def edit_client_list(self):
        if self.client_list.cget("state") == "disabled":
            self.client_list.configure(state="normal")
            self.edit_button.configure(text="Cancel")
        else:
            self.client_list.configure(state="disabled")
            self.edit_button.configure(text="Edit")
    
        if self.client_list.cget("state") == "normal":
            self.save_button.configure(fg_color="#B66A58")
        else:
            self.save_button.configure(fg_color=self.edit_button.fg_color)

    def save_client_list(self):
        self.save_button.configure(fg_color=self.edit_button.fg_color)
        client_list = self.client_list.get("0.0", "end")
        client_surname = self.client_list_label.cget("text").split(": ")[-1]
        if client_surname.strip() != "Client List: ".strip():
            filepath = os.getcwd() + "/clients/" + client_surname
            with open(filepath, 'w') as f:
                f.write(client_list)
            self.edit_button.configure(text="Edit")
            self.client_list.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()