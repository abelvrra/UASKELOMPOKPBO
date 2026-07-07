import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from colors import (COLOR_BG, COLOR_GREEN, COLOR_TEXT_DARK, COLOR_TEXT_GRAY, 
                    COLOR_WHITE, COLOR_BORDER, COLOR_GOLD)
from data_store_2 import DataStore
from scroll_utils import enable_mousewheel_scroll

class HomestayCard(tk.Frame):
    """Card untuk menampilkan homestay"""
    
    def __init__(self, master, homestay, on_book=None, **kwargs):
        super().__init__(master, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                        highlightthickness=1, **kwargs)
        self.homestay = homestay
        self.on_book = on_book
        self.configure(cursor="hand2")
        
        content = tk.Frame(self, bg=COLOR_WHITE)
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Icon & Name
        header = tk.Frame(content, bg=COLOR_WHITE)
        header.pack(fill="x", pady=(0, 5))
        
        tk.Label(header, text=homestay["icon"], font=("Arial", 20),
                bg=COLOR_WHITE).pack(side="left", padx=(0, 10))
        
        tk.Label(header, text=homestay["nama"], font=("Segoe UI", 12, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left", fill="x", expand=True)
        
        # Address
        tk.Label(content, text=f"📍 {homestay['alamat']}", font=("Segoe UI", 9),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack(anchor="w", pady=(0, 5))
        
        # Rating & Price
        info_frame = tk.Frame(content, bg=COLOR_WHITE)
        info_frame.pack(fill="x", pady=(5, 10))
        
        rating_text = f"⭐ {homestay['rating']} ({homestay['review_count']} review)"
        tk.Label(info_frame, text=rating_text, font=("Segoe UI", 9),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack(side="left")
        
        price_text = f"Rp {homestay['harga']:,}/malam".replace(",", ".")
        tk.Label(info_frame, text=price_text, font=("Segoe UI", 11, "bold"),
                bg=COLOR_WHITE, fg=COLOR_GREEN).pack(side="right")
        
        # Facilities
        tk.Label(content, text=f"Fasilitas: {homestay['fasilitas']}", font=("Segoe UI", 8),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY, wraplength=250, justify="left").pack(anchor="w")
        
        # Button
        btn = tk.Button(content, text="Lihat Detail", bg=COLOR_GREEN, fg="white",
                       font=("Segoe UI", 9, "bold"), relief="flat",
                       command=self._on_click)
        btn.pack(side="right", pady=(10, 0))
        
        for widget in (self, content, header, info_frame):
            widget.bind("<Button-1>", lambda e: self._on_click())
    
    def _on_click(self):
        if self.on_book:
            self.on_book(self.homestay)


class HomestayFrame(tk.Frame):
    """Frame untuk booking homestay"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.build_layout()
    
    def build_layout(self):
        """Membangun layout homestay page"""
        # Back button & Title
        header_frame = tk.Frame(self, bg=COLOR_BG)
        header_frame.pack(fill="x", padx=30, pady=20)
        
        tk.Button(header_frame, text="← Booking Homestay", bg=COLOR_BG, fg=COLOR_GREEN,
                 font=("Segoe UI", 16, "bold"), bd=0, relief="flat",
                 command=lambda: self.controller.show_frame("DashboardFrame")).pack(anchor="w")
        
        tk.Label(header_frame, text="Temukan dan pesan homestay nyaman di Madiun",
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
        
        # Bind mousewheel untuk scroll smooth (aman dipakai di banyak halaman)
        enable_mousewheel_scroll(canvas)
        
        # Add homestay cards
        for homestay in DataStore.homestays:
            card = HomestayCard(scrollable_frame, homestay, on_book=self._on_book_homestay)
            card.pack(fill="x", pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _on_book_homestay(self, homestay):
        """Handle booking homestay"""
        self._show_booking_dialog(homestay)
    
    def _show_booking_dialog(self, homestay):
        """Menampilkan dialog untuk booking homestay"""
        dialog = tk.Toplevel(self)
        dialog.title(f"Booking - {homestay['nama']}")
        dialog.geometry("600x500")
        dialog.resizable(False, False)
        
        # Scrollable frame
        main_frame = tk.Frame(dialog, bg=COLOR_WHITE)
        main_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_frame, bg=COLOR_WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_WHITE)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mousewheel supaya dialog ini bisa di-scroll (sebelumnya tidak ada binding)
        enable_mousewheel_scroll(canvas)
        
        # Content
        content = tk.Frame(scrollable_frame, bg=COLOR_WHITE)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title & Price
        tk.Label(content, text=homestay["nama"], font=("Segoe UI", 16, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack()
        tk.Label(content, text=f"📍 {homestay['alamat']}", font=("Segoe UI", 10),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack()
        tk.Label(content, text=f"Rp {homestay['harga']:,}/malam".replace(",", "."), 
                font=("Segoe UI", 12, "bold"), bg=COLOR_WHITE, fg=COLOR_GREEN).pack(pady=10)
        
        # Date picker
        date_frame = tk.Frame(content, bg=COLOR_WHITE)
        date_frame.pack(fill="x", pady=10)
        
        tk.Label(date_frame, text="Check-in:", font=("Segoe UI", 10),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")
        
        try:
            checkin_date = DateEntry(date_frame, width=15, background='darkblue',
                                    foreground='white', borderwidth=2)
            checkin_date.pack(side="left", padx=(10, 20))
        except:
            checkin_var = tk.StringVar()
            checkin_date = tk.Entry(date_frame, width=15, textvariable=checkin_var)
            checkin_date.pack(side="left", padx=(10, 20))
        
        tk.Label(date_frame, text="Check-out:", font=("Segoe UI", 10),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")
        
        try:
            checkout_date = DateEntry(date_frame, width=15, background='darkblue',
                                     foreground='white', borderwidth=2)
            checkout_date.pack(side="left", padx=(10, 0))
        except:
            checkout_var = tk.StringVar()
            checkout_date = tk.Entry(date_frame, width=15, textvariable=checkout_var)
            checkout_date.pack(side="left", padx=(10, 0))
        
        # Quantity of rooms
        qty_frame = tk.Frame(content, bg=COLOR_WHITE)
        qty_frame.pack(fill="x", pady=10)
        
        tk.Label(qty_frame, text="Jumlah Kamar:", font=("Segoe UI", 10),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")
        
        qty_var = tk.IntVar(value=1)
        qty_spin = tk.Spinbox(qty_frame, from_=1, to=5, textvariable=qty_var,
                             width=5, font=("Segoe UI", 10))
        qty_spin.pack(side="left", padx=10)
        
        # Calculate days and price
        price_frame = tk.Frame(content, bg=COLOR_WHITE)
        price_frame.pack(pady=15)
        
        price_label = tk.Label(price_frame, text="", font=("Segoe UI", 12, "bold"),
                              bg=COLOR_WHITE, fg=COLOR_GREEN)
        price_label.pack()
        
        # Buttons
        btn_frame = tk.Frame(content, bg=COLOR_WHITE)
        btn_frame.pack(fill="x", pady=20)
        
        def confirm_booking():
            try:
                qty = qty_var.get()
                checkin = str(checkin_date.get_date()) if hasattr(checkin_date, 'get_date') else checkin_date.get()
                checkout = str(checkout_date.get_date()) if hasattr(checkout_date, 'get_date') else checkout_date.get()
                
                if not checkin or not checkout:
                    messagebox.showwarning("Peringatan", "Silakan pilih tanggal!")
                    return
                
                # Calculate total (simplified - assume 2 nights)
                total = homestay["harga"] * qty * 2
                
                booking = DataStore.add_booking("homestay", homestay["id"], checkin, checkout, qty, total)
                messagebox.showinfo("Sukses", f"Booking berhasil!\nKode Booking: {booking['id']}\nTotal: Rp {total:,}".replace(",", "."))
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(btn_frame, text="Pesan Sekarang", bg=COLOR_GREEN, fg="white",
                 font=("Segoe UI", 11, "bold"), command=confirm_booking).pack(side="right", padx=(10, 0))
        tk.Button(btn_frame, text="Batal", bg="#cccccc", fg="#333",
                 font=("Segoe UI", 11, "bold"), command=dialog.destroy).pack(side="right")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def refresh(self):
        """Refresh frame"""
        pass