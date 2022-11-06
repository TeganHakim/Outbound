# Import libraries for tkinter GUI and system utilities
import tkinter
import tkinter.messagebox
import customtkinter
import datetime, re, os, math
import vonage_task as vonage_task
import toml
import tomli
from util import getSubDir

# ==================== #
# Message Center Frame #
# ==================== #
class MessageCenter(customtkinter.CTkFrame):
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

        # Setup Message Center frame
        self.frame_right = customtkinter.CTkFrame(master = self)
        self.frame_right.grid(row = 0, column = 0, sticky = "nsew")

        # Configure grid layout for Message Center frame
        self.frame_right.rowconfigure((0, 1, 2, 3), weight = 1)
        self.frame_right.rowconfigure((6, 7), weight = 1)
        self.frame_right.columnconfigure((0, 1), weight = 1)
        self.frame_right.columnconfigure(2, weight = 0)

        # Configure message frame
        self.message_frame = customtkinter.CTkFrame(master = self.frame_right)
        self.message_frame.grid(row = 0, column = 0, columnspan = 2, rowspan = 4, pady = 20, padx = 20, sticky = "nsew")

        # Configure message frame's grid layout
        self.message_frame.rowconfigure(1, weight = 1)
        self.message_frame.columnconfigure(0, weight = 1)

        # Message frame title
        self.message_label = customtkinter.CTkLabel(master = self.message_frame,text = "Message Content:", text_font = ("Roboto Medium", -18, "bold"))
        self.message_label.grid(row = 0, column = 0, sticky = "new", padx = (15, 10), pady = (10, 0))
        
        # Message frame text box
        self.message = customtkinter.CTkTextbox(master = self.message_frame, corner_radius = 10, fg_color = ("white", "gray38"), text_font = ("Roboto", -14))
        self.message.grid(row = 1, column = 0, sticky="nesw", padx = 15, pady = (10, 15))
        self.message.insert("0.0", self.config["message_center"]["message"].lstrip("\n"))

        # Configure send filter frame
        self.send_filter_frame = customtkinter.CTkFrame(master=self.frame_right, corner_radius=10)
        self.send_filter_frame.grid(row=4, column=0, columnspan=2, rowspan=5, sticky="nsew", padx=15, pady=(0, 15))
        
        # Configure send filter frame's grid layout
        self.send_filter_frame.rowconfigure(1, weight = 1)
        self.send_filter_frame.columnconfigure(0, weight = 1)
        
        # Send filter frame title
        self.send_filter_label = customtkinter.CTkLabel(master = self.send_filter_frame, corner_radius = 10, text = "Filter By Date:", text_font = ("Roboto Medium", -18, "bold"))
        self.send_filter_label.grid(row = 0, column = 0, sticky = "new", padx = (15, 10), pady = (10, 0))
        
        # Configure select dates frame
        self.select_dates_frame = customtkinter.CTkFrame(master = self.send_filter_frame)
        self.select_dates_frame.grid(row = 1, column = 0, columnspan = 2, rowspan = 5, sticky = "nsew", padx = 15, pady = (0, 15))

        # Configure select dates frame's grid layout
        self.select_dates_frame.rowconfigure(0, weight = 1)
        self.select_dates_frame.rowconfigure(1, weight = 1)
        self.select_dates_frame.rowconfigure(2, weight = 1)
        self.select_dates_frame.rowconfigure(3, weight = 1)
        self.select_dates_frame.columnconfigure(0, weight = 1)
        self.select_dates_frame.columnconfigure(1, weight = 1)
        self.select_dates_frame.columnconfigure(2, weight = 1)

        # Setup possible dates listbox
        self.possible_dates = tkinter.Listbox(self.select_dates_frame, activestyle = "none", bg = "gray38", fg = "white", font = ("Roboto", -16), highlightthickness = 0, highlightbackground = "gray38", bd = 0)
        self.possible_dates.grid(row = 0, column = 0, rowspan = 4, sticky = "nsew", padx = (15, 0), pady = (10, 15))
        # Initialize list of possible dates as empty array
        self.possible_dates_list = self.config["message_center"]["possible_dates"]
        # Bind focus mouse events to listbox
        self.possible_dates.bind("<FocusIn>", self.possible_dates_focused)
        self.possible_dates.bind("<FocusOut>", self.possible_dates_unfocused)
        # Initialize listbox's focus state
        self.possible_dates_focus = False

        # Setup select & delete buttons
        self.select_button = customtkinter.CTkButton(master  =self.select_dates_frame, text = "Select Date", border_width = 2, fg_color = None, command = self.select_date) 
        self.select_button.grid(row = 1, column = 1)
        self.delete_button = customtkinter.CTkButton(master = self.select_dates_frame, text = "Remove Date", border_width = 2, fg_color = None, command = self.remove_date)
        self.delete_button.grid(row = 2, column = 1)

        # Setup final dates listbox
        self.final_dates = tkinter.Listbox(self.select_dates_frame, activestyle = "none", bg = "gray38", fg = "white", font = ("Roboto", -16), highlightthickness = 0, highlightbackground = "gray38", bd = 0)
        self.final_dates.grid(row = 0, column = 2, rowspan = 4, sticky = "nsew", padx = (0, 15), pady = (10, 15))
        # Initialize list of final dates as empty array
        self.final_dates_list = self.config["message_center"]["final_dates"]
        # Bind focus mouse events to listbox
        self.final_dates.bind("<FocusIn>", self.final_dates_focused)
        self.final_dates.bind("<FocusOut>", self.final_dates_unfocused)
        # Initialize listbox's focus state
        self.final_dates_focus = False
        
        # Display new values from toml
        self.update_possible_list()
        self.update_final_list()

        # Display selected groups title
        self.selected_groups_label = customtkinter.CTkLabel(master = self.frame_right, text = "Filter Selection:", text_font = ("Roboto Medium", -16, "bold"))
        self.selected_groups_label.grid(row = 0, column = 2, columnspan = 1, pady = (20, 0), padx = (0, 20))

        # Configure selected groups frame
        self.selected_groups_frame = customtkinter.CTkFrame(master = self.frame_right)
        self.selected_groups_frame.grid(row = 1, column = 2, pady = 10, padx = (0, 20), sticky = "nsew")
        
        # Setup Master filter
        self.filter_selection_master = customtkinter.CTkCheckBox(master = self.selected_groups_frame, text = "Master Files", command = self.filter_selection, onvalue = "on", offvalue = "off")
        self.filter_selection_master.grid(row = 0, column = 0, pady = (20, 5), padx = 20, sticky = "nsw")
        if self.config["message_center"]["master_select"] == "on":
            self.filter_selection_master.select()

        # Setup Client filter
        self.filter_selection_client = customtkinter.CTkCheckBox(master = self.selected_groups_frame, text = "Client Files", command = self.filter_selection, onvalue = "on", offvalue = "off")
        self.filter_selection_client.grid(row = 1, column = 0, pady = (5, 20), padx = 20, sticky = "nsw")
        if self.config["message_center"]["client_select"] == "on":
            self.filter_selection_client.select()       

        # Display date selection title
        self.date_select_label = customtkinter.CTkLabel(master = self.frame_right, text="Scheduled Send:", text_font=("Roboto Medium", -16, "bold"))
        self.date_select_label.grid(row = 2, column = 2, columnspan = 1, pady = (10, 0), padx = (0, 20))

        # Configure date selection frame
        self.date_select_frame = customtkinter.CTkFrame(master = self.frame_right)
        self.date_select_frame.grid(row = 3, column = 2, pady = 10, padx = (0, 20), sticky = "nsew")

        # Configure date selection frame's grid layout
        self.date_select_frame.rowconfigure((1, 2, 3, 4), weight = 1)
        self.date_select_frame.columnconfigure((0, 1), weight = 1)

        # Date selection month button 
        current_month = datetime.datetime.now().strftime("%B")
        self.month = customtkinter.CTkComboBox(master = self.date_select_frame, command = self.month_changed, values = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))                            
        self.month.grid(row = 0, column = 0, pady = 10, padx = 5, sticky="nsew")  
        if self.config["message_center"]["month"] != "":
            self.month.set(self.config["message_center"]["month"])
        else:
            self.month.set(current_month)   

        # Date selection day button 
        current_day = datetime.datetime.now().day
        self.day = customtkinter.CTkComboBox(master = self.date_select_frame, command = self.day_changed, values = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"))
        self.day.grid(row = 1, column = 0, pady = 10, padx = 5, sticky = "nsew")
        if self.config["message_center"]["day"] != 0:
            self.day.set(self.config["message_center"]["day"])
        else:
            self.day.set(current_day)  
        
        # Date Selection year button
        current_year = datetime.datetime.now().year
        self.year = customtkinter.CTkComboBox(master = self.date_select_frame, command = self.year_changed, values = (str(current_year), str(current_year + 1), str(current_year + 2)))
        self.year.grid(row = 2, column = 0, pady = 10, padx = 5, sticky="nsew")
        if self.config["message_center"]["year"] != "":
            self.year.set(self.config["message_center"]["year"])
        else:
            self.year.set(current_year) 
       
       # Configure error label when entry not valid
        self.error_label = customtkinter.CTkLabel(master = self.date_select_frame, text = "", text_color = "#D5806B", text_font = ("Roboto", -12, "italic"))
        self.error_label.grid(row = 4, column = 0, columnspan = 1, sticky = "nsew")

        # (In)validation entry registration
        self.vcmd = (self.register(self.validate), '%P')
        self.ivcmd = (self.register(self.on_invalid),)

        # Date selection time entry
        self.time = customtkinter.CTkEntry(master = self.date_select_frame, width = 100, fg_color = self.date_select_frame.bg_color, validate = "focusout", validatecommand = self.vcmd, invalidcommand = self.ivcmd, placeholder_text = "hh:mm")
        self.time.grid(row = 3, column = 0, pady = 10, padx = 5, sticky = "nsw")
        if self.config["message_center"]["time"] != "":
            self.time.insert(0, self.config["message_center"]["time"])

        # Date selection Am/PM selection
        self.am_pm = customtkinter.CTkComboBox(master = self.date_select_frame, width = 75, command = self.am_pm_changed, values = ["AM", "PM"])
        self.am_pm.grid(row = 3, column = 0, pady = 10, padx = 5, sticky = "nse")
        self.am_pm.set(self.config["message_center"]["am_pm"])

        # Date selection send instantly button
        self.instant = customtkinter.IntVar(value = 1)
        self.instant_switch = customtkinter.CTkSwitch(master = self.date_select_frame, text = "Send Instantly", command = self.instant_changed, variable = self.instant, onvalue = 1, offvalue = 0, text_font = ("Roboto Medium", -16))
        self.instant_switch.grid(row = 5, column = 0, pady = (5, 10), padx =20, sticky = "ew")
        if self.config["message_center"]["instant"] == 0:
            self.instant_switch.deselect()

        # Configure statistics frame
        self.statistics_label_frame =  customtkinter.CTkFrame(master = self.frame_right, corner_radius = 10, fg_color = self.frame_right.fg_color)
        self.statistics_label_frame.grid(row = 5, column = 2, pady = (5, 0), padx = (0, 20), sticky = "nsew")
        
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
        
        # Configure statistics frame
        self.statistics_frame = customtkinter.CTkFrame(master = self.frame_right, corner_radius = 10, fg_color = self.frame_right.fg_color)
        self.statistics_frame.grid(row = 6, column = 2, pady = (5, 0), padx = (0, 20), sticky = "nsew")
        # Configure statistics frame's grid layout
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

        # Configure send message button
        self.send_message = customtkinter.CTkButton(master = self.frame_right, text = "Send Message", border_width= 2, fg_color=None, command = self.send_message)
        self.send_message.grid(row = 8, column = 2, columnspan = 1, pady = 20, padx = (0, 20), sticky = "ew")

    # ========================== #
    #  Message Center Functions  #
    # ========================== #

    # Filter through possible and final date selection lists
    def filter_selection(self):

        # Display NONE
        if (self.filter_selection_master.get() == "off" and self.filter_selection_client.get() == "off"):
            self.possible_dates_list = []
            self.final_dates_list = []
            
        # Display MASTER
        if (self.filter_selection_master.get() == "on" and self.filter_selection_client.get() == "off"):
            self.possible_dates_list = []
            self.populate_masters()
            temp_final_list = []
            for date in self.final_dates_list:
                if date not in os.listdir(self.PATH + "\clients"):
                    temp_final_list.append(date)
            self.final_dates_list = temp_final_list
        
        # Display CLIENTS
        if (self.filter_selection_master.get() == "off" and self.filter_selection_client.get() == "on"):             
            self.possible_dates_list = []
            self.populate_clients()
            temp_final_list = []
            for date in self.final_dates_list:
                if date not in os.listdir(self.PATH + "\masters"):
                   temp_final_list.append(date)
            self.final_dates_list = temp_final_list 
            
        # Display MASTER & CLIENT    
        if (self.filter_selection_master.get() == "on" and self.filter_selection_client.get() == "on"):
            self.possible_dates_list = []
            self.populate_masters()
            self.populate_clients()

        # Update MASTER & CLIENT listboxes with curr val
        self.update_final_list()
        self.update_possible_list()
        # Update the statistics text
        self.update_statistics()
        
    # Populate the possible dates list for clients
    def populate_clients(self):
        client_files = os.listdir(self.PATH + "\clients")
        for file in client_files:
            self.possible_dates_list.append(file)
            
    # Populate the possible dates list for masters
    def populate_masters(self):
        master_files = os.listdir(self.PATH + "\masters")
        for file in master_files:
            self.possible_dates_list.append(file)

    # Possible dates <Focusin> event
    def possible_dates_focused(self, event):
        self.possible_dates_focus = True
    # Possible dates <Focusout> event
    def possible_dates_unfocused(self, event):
        self.possible_dates_focus = False

    # Final dates <Focusin> event
    def final_dates_focused(self, event):
        self.final_dates_focus = True
    # Final dates <Focusout> event
    def final_dates_unfocused(self, event):
        self.final_dates_focus = False

    # Select button triggered, update possible/final dates list
    def select_date(self):
        if self.possible_dates_focus == True and self.final_dates_focus == False:
            if self.possible_dates.get(self.possible_dates.curselection()) not in self.final_dates_list:
                self.final_dates_list.append(self.possible_dates.get(self.possible_dates.curselection()))
            self.possible_dates_list.remove(self.possible_dates.get(self.possible_dates.curselection()))
            self.update_final_list()
            self.update_possible_list()
            self.update_statistics()
            
    # Remove button triggered, update possible/final dates list
    def remove_date(self):
        if self.final_dates_focus == True and self.possible_dates_focus == False:
            if self.final_dates.get(self.final_dates.curselection()) not in self.possible_dates_list:
                self.possible_dates_list.append(self.final_dates.get(self.final_dates.curselection()))
            self.final_dates_list.remove(self.final_dates.get(self.final_dates.curselection()))
            self.update_final_list()
            self.update_possible_list()
            self.update_statistics()
 
    # Update possible dates listbox
    def update_possible_list(self):
        self.possible_dates.delete(0, 'end')
        for date in self.possible_dates_list:
            if date not in self.final_dates_list:
                self.possible_dates.insert('end', date)
                
    # Update final dates listbox
    def update_final_list(self):
        self.final_dates.delete(0, 'end')
        for date in self.final_dates_list:
            self.final_dates.insert('end', date)

    # Send message using Vonage API in vonage_task.py
    def send_message(self):
        self.master.focus()
        # Send SMS instantly
        if (self.instant.get() == 1):
            if len(self.final_dates_list) > 0 and len(self.message.get("0.0", "end")) > 0:
                receiving_clients = []
                for file in self.final_dates_list:
                    filename = self.PATH + getSubDir(file) + file
                    receiving_clients += open(filename, "r").read().splitlines()
                response = vonage_task.send_sms(receiving_clients, self.message.get("0.0", "end"))
        # Send SMS at given date 
        else:
            pass
        
    # Triggered upon date selection month changed, update date
    def month_changed(self, event):
        time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if str(event) != str(datetime.datetime.now().strftime("%B")):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if int(self.day.get()) == int(datetime.datetime.now().day) and int(self.year.get()) == int(datetime.datetime.now().year and str(self.time.get()) == str(time.strftime("%I:%M")) and str(self.am_pm.get()) == str(time.strftime("%p"))):
                self.instant_switch.select()
                self.instant.set(1)            

    # Triggered upon date selection day changed, update date
    def day_changed(self, event):
        time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if int(event) != int(datetime.datetime.now().day):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if str(self.month.get()) == str(datetime.datetime.now().strftime("%B")) and int(self.year.get()) == int(datetime.datetime.now().year and str(self.time.get()) == str(time.strftime("%I:%M")) and str(self.am_pm.get()) == str(time.strftime("%p"))):
                self.instant_switch.select()
                self.instant.set(1)
    
    # Triggered upon date selection year changed, update date
    def year_changed(self, event):
        time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if int(event) != int(datetime.datetime.now().year):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if str(self.month.get()) == str(datetime.datetime.now().strftime("%B")) and int(self.day.get()) == int(datetime.datetime.now().day and str(self.time.get()) == str(time.strftime("%I:%M")) and str(self.am_pm.get()) == str(time.strftime("%p"))):
                self.instant_switch.select()
                self.instant.set(1)

    # Triggered upon date selection time changed, update date
    def time_changed(self, *args):
        time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if str(self.time.get()) != str(time.strftime("%I%M")):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if str(self.month.get()) == str(datetime.datetime.now().strftime("%B")) and int(self.day.get()) == int(datetime.datetime.now().day) and int(self.year.get()) == int(datetime.datetime.now().year) and str(self.am_pm.get()) == str(time.strftime("%p")):
                self.instant_switch.select()
                self.instant.set(1)

    # Triggered upon date selection am/pm changed, update date
    def am_pm_changed(self, event):
        time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
        if str(event) != str(time.strftime("%p")):
            self.instant_switch.deselect()
            self.instant.set(0)
        else:
            if str(self.month.get()) == str(datetime.datetime.now().strftime("%B")) and int(self.day.get()) == int(datetime.datetime.now().day) and int(self.year.get()) == int(datetime.datetime.now().year) and str(self.time.get()) == str(time.strftime("%I:%M")):
                self.instant_switch.select()
                self.instant.set(1)

    # Show error message upon invalid data entry
    def show_message(self, error = ''):
        self.error_label.configure(text = error)
        if (error == ''):
            self.time.configure(fg_color = self.date_select_frame.bg_color)
        else:
            self.time.configure(fg_color = "#B66A58")

    # Validate time input in 12 hour format
    def validate(self, event):   
        pattern = r'^(0?[1-9]|1[0-2]):[0-5][0-9]$'
        if (re.fullmatch(pattern, event) is None):
            return False
        self.show_message()
        return True         

    # Display invalid message
    def on_invalid(self):
        self.show_message('Enter a valid time (hh:mm)')

    # Triggered upon date selection instant selection changed, update date
    def instant_changed(self):
        if self.instant.get() == 1:
            self.month.set(datetime.datetime.now().strftime("%B"))
            self.day.set(datetime.datetime.now().day)
            self.year.set(datetime.datetime.now().year)
            self.time.delete(0, "end")
            time = datetime.datetime.strptime((datetime.datetime.now().strftime("%H:%M")), "%H:%M")
            self.time.insert(0, time.strftime("%I:%M"))
            self.am_pm.set(time.strftime("%p"))
            
    # Update statistics
    def update_statistics(self):
        self.statistics.configure(state = "normal")
        self.statistics.delete("0.0", "end")
        message_length = len(self.message.get("0.0", "end")) - 1
        total_files = len(self.final_dates_list)
        total_clients = 0
        for file in self.final_dates_list:
            filename = self.PATH + getSubDir(file) + file
            total_clients += len(open(filename, "r").read().splitlines())
        num_messages = 1 + math.floor(message_length / 160)
        message_rate = 50
        approx_time = round((num_messages * total_clients) / message_rate, 2) 
        message_price = 0.0078
        approx_price = round((num_messages * total_clients) * message_price, 2)
        message = "Message Length:\n- {} characters\n\nTotal Recieving Clients:\n- {} clients ({} files)\n\nApproximate Send Time:\n- {} seconds\n\nApproximate Price:\n- ${}".format(message_length, total_clients, total_files, approx_time, approx_price)
        self.statistics.insert("0.0", message)
        self.statistics.configure(state = "disabled")
    
    def save_data(self):
        self.config["message_center"]["message"] = self.message.get("0.0", "end")
        self.config["message_center"]["possible_dates"] = self.possible_dates_list
        self.config["message_center"]["final_dates"] = self.final_dates_list
        self.config["message_center"]["master_select"] = self.filter_selection_master.get()
        self.config["message_center"]["client_select"] = self.filter_selection_client.get()
        self.config["message_center"]["month"] = self.month.get()
        self.config["message_center"]["day"] = self.day.get()
        self.config["message_center"]["year"] = self.year.get()
        self.config["message_center"]["time"] = self.time.get()
        self.config["message_center"]["am_pm"] = self.am_pm.get()
        self.config["message_center"]["instant"] = self.instant_switch.get()
        data = toml.dumps(self.config)
        with open(self.PATH + "\config.toml", "w") as f:
            f.write(data)

    def on_closing(self, event = 0):
        self.save_data()
        self.master.destroy()