import tkinter as tk
from data_store_2 import DataStore
from colors import BACKGROUND, CARD, PRIMARY, TEXT

class MyTicketsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        
        tk.Label(self, text="Tiket & Booking Saya", font=("Arial", 22, "bold"), bg=BACKGROUND, fg=TEXT).pack(pady=30, padx=40, anchor="w")
        
        self.canvas = tk.Canvas(self, bg=BACKGROUND, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=40)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=BACKGROUND)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def refresh(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        for t in DataStore.tickets:
            if t["username"] == DataStore.active_user:
                card = tk.Frame(self.scrollable_frame, bg=CARD, padx=25, pady=20, highlightbackground="#E5E7EB", highlightthickness=1)
                card.pack(fill="x", pady=10, padx=5)
                
                tk.Label(card, text="🎟️ E-TICKET WISATA", font=("Arial", 10, "bold"), bg=CARD, fg=PRIMARY).pack(anchor="w")
                tk.Label(card, text=f"KODE: {t['kode']}", font=("Arial", 16, "bold"), bg=CARD).pack(anchor="w", pady=5)
                tk.Label(card, text=f"Destinasi: {t['destinasi']}", font=("Arial", 11), bg=CARD).pack(anchor="w")
                tk.Label(card, text=f"Jumlah: {t['jumlah']} Orang", font=("Arial", 11), bg=CARD, fg="#6B7280").pack(anchor="w")