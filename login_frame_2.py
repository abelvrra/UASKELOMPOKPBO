import tkinter as tk
from tkinter import messagebox
from data_store_2 import DataStore
from colors import BACKGROUND, PRIMARY, CARD, TEXT

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        
        # Container Login Tengah
        login_box = tk.Frame(self, bg=CARD, padx=40, pady=40, highlightbackground="#E5E7EB", highlightthickness=1)
        login_box.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(login_box, text="Login GoTravel", font=("Arial", 20, "bold"), bg=CARD).pack(pady=20)
        
        tk.Label(login_box, text="Username:", bg=CARD).pack(anchor="w")
        self.entry_user = tk.Entry(login_box, width=30)
        self.entry_user.pack(pady=5)
        
        tk.Label(login_box, text="Password:", bg=CARD).pack(anchor="w")
        self.entry_pass = tk.Entry(login_box, width=30, show="*")
        self.entry_pass.pack(pady=5)
        
        tk.Button(login_box, text="LOGIN", bg=PRIMARY, fg="white", width=25, 
                  command=self.login_action).pack(pady=20)
        
        tk.Button(login_box, text="Belum punya akun? Register", borderwidth=0, bg=CARD, fg=PRIMARY,
                  command=lambda: controller.show_frame("RegisterFrame")).pack()

    def login_action(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        if u in DataStore.users and DataStore.users[u] == p:
            DataStore.active_user = u
            self.controller.active_user = u
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Error", "Login Gagal!")