import tkinter as tk
from tkinter import messagebox
from data_store_2 import DataStore
from colors import BACKGROUND, PRIMARY, CARD

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        
        reg_box = tk.Frame(self, bg=CARD, padx=40, pady=40, highlightbackground="#E5E7EB", highlightthickness=1)
        reg_box.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(reg_box, text="Register Akun", font=("Arial", 20, "bold"), bg=CARD).pack(pady=20)
        
        tk.Label(reg_box, text="Username:", bg=CARD).pack(anchor="w")
        self.entry_user = tk.Entry(reg_box, width=30)
        self.entry_user.pack(pady=5)
        
        tk.Label(reg_box, text="Password:", bg=CARD).pack(anchor="w")
        self.entry_pass = tk.Entry(reg_box, width=30, show="*")
        self.entry_pass.pack(pady=5)
        
        tk.Button(reg_box, text="DAFTAR", bg=PRIMARY, fg="white", width=25, 
                  command=self.register_action).pack(pady=20)
        
        tk.Button(reg_box, text="Kembali ke Login", borderwidth=0, bg=CARD, fg=PRIMARY,
                  command=lambda: controller.show_frame("LoginFrame")).pack()

    def register_action(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        if u and p:
            DataStore.users[u] = p
            messagebox.showinfo("Sukses", "Berhasil Register!")
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showwarning("Peringatan", "Field tidak boleh kosong!")