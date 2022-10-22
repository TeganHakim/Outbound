import tkinter
from tkinter.font import Font
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")
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
        self.selected_groups_label.grid(row=0, column=2, columnspan=1, pady=(20, 0), padx=(0, 15), sticky="")

        self.selected_groups_frame = customtkinter.CTkFrame(master=self.frame_right)
        self.selected_groups_frame.grid(row=1, column=2, pady=10, padx=(0, 15), sticky="nsew")
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

        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="CTkSwitch")
        self.switch_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="CTkSwitch")
        self.switch_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
                                                    values=["Value 1", "Value 2"])
        self.combobox_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="CTkCheckBox")
        self.check_box_1.grid(row=6, column=0, pady=10, padx=20, sticky="w")

        self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="CTkCheckBox")
        self.check_box_2.grid(row=6, column=1, pady=10, padx=20, sticky="w")

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="CTkEntry")
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="CTkButton",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.button_event)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.combobox_1.set("CTkCombobox")
        self.switch_2.select()
        self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
        self.check_box_2.select()

    def button_event(self):
        print(self.master.winfo_width())

class ClientManager(customtkinter.CTkFrame):
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
        self.frame_info.rowconfigure(1, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.message_label = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="Client Manager:",
                                                    text_font=("Roboto Medium", -18, "bold"))
        self.message_label.grid(column=0, row=0, sticky="nwe", padx=15, pady=(10, 0))
        self.message = customtkinter.CTkTextbox(master=self.frame_info,
                                                height=200,
                                                corner_radius=10,
                                                fg_color=("white", "gray38"),
                                                text_font=("Roboto", -14))
        self.message.grid(column=0, row=1, sticky="nsew", padx=15, pady=(10, 15))
        # ============ frame_right ============

        self.radio_var = tkinter.IntVar(value=0)

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
                                                from_=0,
                                                to=1,
                                                number_of_steps=3)
        self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.slider_2 = customtkinter.CTkSlider(master=self.frame_right)
        self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="CTkSwitch")
        self.switch_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="CTkSwitch")
        self.switch_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
                                                    values=["Value 1", "Value 2"])
        self.combobox_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="CTkCheckBox")
        self.check_box_1.grid(row=6, column=0, pady=10, padx=20, sticky="w")

        self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="CTkCheckBox")
        self.check_box_2.grid(row=6, column=1, pady=10, padx=20, sticky="w")

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="CTkEntry")
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="CTkButton",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.button_event)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.combobox_1.set("CTkCombobox")
        self.radio_button_1.select()
        self.slider_1.set(0.2)
        self.slider_2.set(0.7)
        self.switch_2.select()
        self.radio_button_3.configure(state=tkinter.DISABLED)
        self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
        self.check_box_2.select()

    def button_event(self):
        print("Button pressed")

# def resize(event):
#     if (event.width > 500):
#         app.title.configure(font=("Roboto Medium", -30, "bold"))
#         app.subtitle.configure(font=("Roboto Medium", -23, "italic"))
#         app.frame_right.message_label.configure(font=("Roboto Medium", -25, "bold"))
    

if __name__ == "__main__":
    app = App()
    # app.bind('<Configure>', resize)
    app.mainloop()