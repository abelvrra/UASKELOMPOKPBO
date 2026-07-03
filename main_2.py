import tkinter as tk
from data_store_2 import DataStore
from login_frame_2 import LoginFrame
from register_frame_2 import RegisterFrame
from dashboard_frame_2 import DashboardFrame
from ticket_frame_2 import TicketFrame
from homestay_frame_2 import HomestayFrame
from cancellation_frame_2 import CancellationFrame
from route_frame_2 import RouteFrame2
from my_tickets_frame_2 import MyTicketsFrame

class GoTravelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GoTravel - Sistem Pemesanan Tiket Wisata")
        self.geometry("1400x900")
        self.configure(bg="#f7f8fa")

        # Container utama
        self.container = tk.Frame(self, bg="#f7f8fa")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        # Registrasi semua frame
        for F in (LoginFrame, RegisterFrame, DashboardFrame, TicketFrame, 
                  HomestayFrame, CancellationFrame, RouteFrame2, MyTicketsFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.show_frame("LoginFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, 'refresh'):
            frame.refresh()

    def logout_action(self):
        DataStore.active_user = None
        self.show_frame("LoginFrame")

if __name__ == "__main__":
    app = GoTravelApp()
    app.mainloop()