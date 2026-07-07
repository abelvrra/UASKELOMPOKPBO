#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GoTravel - Sistem Pemesanan Tiket Wisata dan Homestay
Main Application File
"""

import tkinter as tk
from tkinter import ttk

# Import semua frame
from login_frame_2 import LoginFrame
from register_frame_2 import RegisterFrame
from dashboard_frame_2 import DashboardFrame
from ticket_frame_2 import TicketFrame
from homestay_frame_2 import HomestayFrame
from route_frame_2 import RouteFrame2
from cancellation_frame_2 import CancellationFrame
from my_tickets_frame_2 import MyTicketsFrame


class GoTravelApp(tk.Tk):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        self.title("GoTravel - Sistem Pemesanan Tiket Wisata")
        self.geometry("1000x650")
        self.resizable(True, True)
        self.minsize(900, 600)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Application state
        self.active_user = None
        self.user_id = None
        
        # Setup main container
        self._setup_container()
        
        # Register all frames
        self._register_frames()
        
        # Show login page first
        self.show_frame("LoginFrame")
    
    def _setup_container(self):
        """Setup main container frame"""
        container = tk.Frame(self, bg="#ffffff")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.container = container
        self.frames = {}
    
    def _register_frames(self):
        """Register all frame classes"""
        frame_classes = [
            ("LoginFrame", LoginFrame),
            ("RegisterFrame", RegisterFrame),
            ("DashboardFrame", DashboardFrame),
            ("TicketFrame", TicketFrame),
            ("HomestayFrame", HomestayFrame),
            ("RouteFrame2", RouteFrame2),
            ("CancellationFrame", CancellationFrame),
            ("MyTicketsFrame", MyTicketsFrame),
        ]
        
        for frame_name, frame_class in frame_classes:
            frame = frame_class(self.container, self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, frame_name):
        """
        Display a specific frame and raise it to the top
        
        Args:
            frame_name (str): Name of the frame to display
        """
        if frame_name in self.frames:
            frame = self.frames[frame_name]
            frame.tkraise()
            
            # Refresh frame if it has a refresh method
            if hasattr(frame, 'refresh'):
                frame.refresh()
        else:
            print(f"Warning: Frame '{frame_name}' not found!")


def main():
    """Main entry point"""
    app = GoTravelApp()
    app.mainloop()


if __name__ == "__main__":
    main()