import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from colors import COLOR_BG, COLOR_GREEN, COLOR_TEXT_DARK, COLOR_TEXT_GRAY, COLOR_WHITE, COLOR_BORDER
from data_store_2 import DataStore

class DestinationCard(tk.Frame):
    """Card untuk menampilkan destinasi wisata"""
    
    def __init__(self, master, destination, on_select=None, **kwargs):
        super().__init__(master, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                        highlightthickness=1, **kwargs)
        self.destination = destination
        self.on_select = on_select
        self.configure(cursor="hand2")
        
        # Content
        content = tk.Frame(self, bg=COLOR_WHITE)
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Icon & Name
        header = tk.Frame(content, bg=COLOR_WHITE)
        header.pack(fill="x", pady=(0, 10))
        
        tk.Label(header, text=destination["icon"], font=("Arial", 24),
                bg=COLOR_WHITE).pack(side="left", padx=(0, 10))
        
        tk.Label(header, text=destination["nama"], font=("Segoe UI", 12, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")
        
        # Description
        tk.Label(content, text=destination["desc"], font=("Segoe UI", 9),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY, wraplength=250, justify="left").pack(anchor="w", pady=(0, 10))
        
        # Price & Button
        footer = tk.Frame(content, bg=COLOR_WHITE)
        footer.pack(fill="x", pady=(10, 0))
        
        if destination["harga"] > 0:
            price_text = f"Rp {destination['harga']:,}".replace(",", ".")
            tk.Label(footer, text=price_text, font=("Segoe UI", 11, "bold"),
                    bg=COLOR_WHITE, fg=COLOR_GREEN).pack(side="left")
        else:
            tk.Label(footer, text="Gratis", font=("Segoe UI", 11, "bold"),
                    bg=COLOR_WHITE, fg=COLOR_GREEN).pack(side="left")
        
        # Pilih button
        btn = tk.Button(footer, text="Pilih", bg=COLOR_GREEN, fg="white",
                       font=("Segoe UI", 9, "bold"), width=8, relief="flat",
                       command=self._on_click)
        btn.pack(side="right")
        
        # Bind click
        for widget in (self, content, header):
            widget.bind("<Button-1>", lambda e: self._on_click())
    
    def _on_click(self):
        if self.on_select:
            self.on_select(self.destination)


class TicketFrame(tk.Frame):
    """Frame untuk membeli tiket wisata"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.selected_destination = None
        self.build_layout()
    
    def build_layout(self):
        """Membangun layout ticket page"""
        # Back button & Title
        header_frame = tk.Frame(self, bg=COLOR_BG)
        header_frame.pack(fill="x", padx=30, pady=20)
        
        tk.Button(header_frame, text="← Beli Tiket Wisata", bg=COLOR_BG, fg=COLOR_GREEN,
                 font=("Segoe UI", 16, "bold"), bd=0, relief="flat",
                 command=lambda: self.controller.show_frame("DashboardFrame")).pack(anchor="w")
        
        tk.Label(header_frame, text="Pilih destinasi wisata favorit Anda",
                font=("Segoe UI", 11), bg=COLOR_BG, fg=COLOR_TEXT_GRAY).pack(anchor="w")
        
        # Scrollable content
        canvas_frame = tk.Frame(self, bg=COLOR_BG)
        canvas_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mousewheel untuk scroll smooth
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Grid layout untuk destinasi (3 columns)
        col = 0
        row = 0
        for dest in DataStore.destinations:
            card = DestinationCard(scrollable_frame, dest, on_select=self._on_select_destination)
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
            
            scrollable_frame.grid_columnconfigure(col, weight=1)
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _on_select_destination(self, destination):
        """Handle destinasi dipilih"""
        self.selected_destination = destination
        # Show booking window
        self._show_booking_dialog(destination)
    
    def _show_booking_dialog(self, destination):
        """Menampilkan dialog untuk booking tiket"""
        dialog = tk.Toplevel(self)
        dialog.title(f"Pesan Tiket - {destination['nama']}")
        dialog.geometry("500x500")
        dialog.resizable(True, True)
        
        # Main frame dengan scrollbar
        main_frame = tk.Frame(dialog, bg=COLOR_WHITE)
        main_frame.pack(fill="both", expand=True)
        
        # Canvas dan scrollbar
        canvas = tk.Canvas(main_frame, bg=COLOR_WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_WHITE)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content di dalam scrollable frame
        content = tk.Frame(scrollable_frame, bg=COLOR_WHITE)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content, text=destination["icon"], font=("Arial", 30),
                bg=COLOR_WHITE).pack(pady=(0, 10))
        
        tk.Label(content, text=destination["nama"], font=("Segoe UI", 16, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack()
        
        tk.Label(content, text=f"📍 Lokasi: {destination['lokasi']}", 
                font=("Segoe UI", 10), bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY, wraplength=400).pack(pady=5)
        tk.Label(content, text=f"🕐 Jam Buka: {destination['jam_buka']}", 
                font=("Segoe UI", 10), bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack(pady=5)
        tk.Label(content, text=f"🏗️ Fasilitas: {destination['fasilitas']}", 
                font=("Segoe UI", 10), bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY, wraplength=400, justify="left").pack(pady=10)
        
        # Separator
        separator = tk.Frame(content, bg="#e0e0e0", height=1)
        separator.pack(fill="x", pady=15)
        
        # Quantity input
        input_frame = tk.Frame(content, bg=COLOR_WHITE)
        input_frame.pack(pady=15, fill="x")
        
        tk.Label(input_frame, text="Jumlah Tiket:", font=("Segoe UI", 11, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left", padx=(0, 10))
        
        qty_var = tk.IntVar(value=1)
        qty_spin = tk.Spinbox(input_frame, from_=1, to=10, textvariable=qty_var,
                             width=8, font=("Segoe UI", 11), justify="center")
        qty_spin.pack(side="left", padx=(0, 20))
        
        # Harga
        harga_frame = tk.Frame(content, bg=COLOR_WHITE)
        harga_frame.pack(pady=10, fill="x")
        
        tk.Label(harga_frame, text="Harga per Tiket:", font=("Segoe UI", 10),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack(side="left")
        
        if destination["harga"] > 0:
            price_text = f"Rp {destination['harga']:,}".replace(",", ".")
            tk.Label(harga_frame, text=price_text, font=("Segoe UI", 11, "bold"),
                    bg=COLOR_WHITE, fg=COLOR_GREEN).pack(side="right")
        else:
            tk.Label(harga_frame, text="Gratis", font=("Segoe UI", 11, "bold"),
                    bg=COLOR_WHITE, fg=COLOR_GREEN).pack(side="right")
        
        # Total Price
        price_frame = tk.Frame(content, bg=COLOR_WHITE)
        price_frame.pack(pady=15, fill="x")
        
        tk.Label(price_frame, text="Total:", font=("Segoe UI", 12, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")
        
        price_label = tk.Label(price_frame, text="Rp 0", font=("Segoe UI", 14, "bold"),
                              bg=COLOR_WHITE, fg=COLOR_GREEN)
        price_label.pack(side="right")
        
        def update_price(*args):
            qty = qty_var.get()
            total = destination["harga"] * qty
            price_text = f"Rp {total:,}".replace(",", ".")
            price_label.config(text=price_text)
        
        qty_var.trace("w", update_price)
        update_price()
        
        # Separator
        separator2 = tk.Frame(content, bg="#e0e0e0", height=1)
        separator2.pack(fill="x", pady=15)
        
        # Buttons
        btn_frame = tk.Frame(content, bg=COLOR_WHITE)
        btn_frame.pack(fill="x", pady=20)
        
        def confirm_booking():
            qty = qty_var.get()
            total = destination["harga"] * qty
            booking = DataStore.add_booking("ticket", destination["id"], None, None, qty, total)
            messagebox.showinfo("Sukses", f"Booking berhasil!\nKode Booking: {booking['id']}\nTotal: Rp {total:,}".replace(",", "."))
            dialog.destroy()
        
        tk.Button(btn_frame, text="Pesan Sekarang", bg=COLOR_GREEN, fg="white",
                 font=("Segoe UI", 11, "bold"), command=confirm_booking, padx=20).pack(side="right", padx=(10, 0))
        tk.Button(btn_frame, text="Batal", bg="#cccccc", fg="#333",
                 font=("Segoe UI", 11, "bold"), command=dialog.destroy, padx=20).pack(side="right")
        
        # Pack canvas dan scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def refresh(self):
        """Refresh frame"""
        pass