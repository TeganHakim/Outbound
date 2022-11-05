# Author: Outward Industries

# Import libraries for tkinter GUI and system utilities
import customtkinter
import message_center, client_manager

# Set the system appearance to Dark mode by default
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# ==================== #
#     Tkinter App      #
# ==================== #
class App(customtkinter.CTk):
    # Window dimensions
    WIDTH = 1350
    HEIGHT = 850

    # Minimum window dimensions
    MINWIDTH = 1100
    MINHEIGHT = 800

    # Initiliaze tkinter GUI window application
    def __init__(self):
        super().__init__()

        # Basic window setup
        self.title("Outbound v1.0")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(App.MINWIDTH, App.MINHEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  

        # Configure grid layout for base app
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        
        # Configure left frame (static sidebar frame)
        self.frame_left = customtkinter.CTkFrame(master = self, width = 180, corner_radius = 0)
        self.frame_left.grid(row = 0, column = 0, sticky = "nsew")

        # Configure right frame (changing application frame)
        self.frame_right = customtkinter.CTkFrame(master = self)

        # Switch right frame data upon request
        self.switch_frame(message_center.MessageCenter)

        # Configure right frame's grid layout
        self.frame_left.grid_rowconfigure(5, weight = 1) 
        self.frame_left.grid_rowconfigure(8, minsize = 20)   
        self.frame_left.grid_rowconfigure(11, minsize = 10)

        # Sidebar title
        self.title = customtkinter.CTkLabel(master = self.frame_left, text = "Outbound SMS", text_font = ("Roboto Medium", -22, "bold")) 
        self.title.grid(row = 0, column = 0, pady = (10, 0), padx = 10)

        # Sidebar subtitle
        self.subtitle = customtkinter.CTkLabel(master = self.frame_left, text = "Top Notch Sports", text_font = ("Roboto Medium", -15, "italic"))
        self.subtitle.grid(row = 1, column = 0, pady = (0, 10), padx = 10)

        # Sidebar frame for Message Center button
        self.message_center_frame = customtkinter.CTkFrame(master = self.frame_left, width = 180, corner_radius = 0, fg_color = self.frame_right.bg_color)
        self.message_center_frame.grid(row = 2, column = 0, sticky = "nsew")

        # Sidebar Message Center button
        self.message_center_button = customtkinter.CTkButton(master=self.message_center_frame, text="Message Center", command = self.message_center)
        self.message_center_button.grid(row=2, column=0, pady=10, padx=20)
        
        # Sidebar frame for Client Manager button
        self.client_manager_frame = customtkinter.CTkFrame(master = self.frame_left, width = 180, corner_radius = 0, fg_color = self.frame_left.fg_color)
        self.client_manager_frame.grid(row = 3, column = 0, sticky = "nswe")
        
        # Sidebar Client Manager button
        self.client_manager_button = customtkinter.CTkButton(master = self.client_manager_frame, text = "Client Manager", command = self.client_manager)
        self.client_manager_button.grid(row = 3, column = 0, pady = 10, padx = 20)

    # ==================== #
    #     App Functions    #
    # ==================== #
    
    # Switch the right frame's content to the specified frame
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame_right is not None:
            self.frame_right.destroy()
        self.frame_right = new_frame
        self.frame_right.grid(row = 0, column = 1, sticky = "nsew", padx = 20, pady = 20)
    
    # Destroy app upon clicking X button
    def on_closing(self, event = 0):
        self.destroy()

    # Switch frame to Message Center
    def message_center(self):
        self.switch_frame(message_center.MessageCenter)
        self.message_center_frame.configure(fg_color = self.frame_right.bg_color)
        self.client_manager_frame.configure(fg_color = self.frame_left.fg_color)
        
    # Switch frame to Client Manager
    def client_manager(self):
        self.switch_frame(client_manager.ClientManager)
        self.message_center_frame.configure(fg_color=self.frame_left.fg_color)
        self.client_manager_frame.configure(fg_color=self.frame_right.bg_color)   

# Run App mainloop()
if __name__ == "__main__":
    app = App()
    app.mainloop()