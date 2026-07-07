import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None
from data_store_2 import DataStore
from scroll_utils import enable_mousewheel_scroll

# Warna tema (di-inline langsung di file ini, tidak lagi dari colors.py)
COLOR_BG = "#f7f8fa"
COLOR_BORDER = "#e6e8eb"
COLOR_GREEN = "#2f9e44"
COLOR_TEXT_DARK = "#1a1a1a"
COLOR_TEXT_GRAY = "#6b7280"
COLOR_WHITE = "#ffffff"
COLOR_GOLD = "#f5a623"

# Katalog homestay (data statis, tidak disimpan di DataStore
# karena DataStore hanya menyimpan booking, bukan katalog produk)
HOMESTAY_CATALOG = [
    {
        "icon": "🏠", "nama": "Homestay Madiun City",
        "alamat": "Jl. Pahlawan No. 45, Madiun", "harga": 200000,
        "rating": 4.8, "review_count": 120,
        "fasilitas": "AC, WiFi, sarapan, parkir luas",
    },
    {
        "icon": "🏡", "nama": "Villa Kare Asri",
        "alamat": "Kare, Madiun", "harga": 350000,
        "rating": 4.9, "review_count": 87,
        "fasilitas": "Kolam renang, dapur, BBQ area, WiFi",
    },
    {
        "icon": "🛖", "nama": "Griya Wisata Sederhana",
        "alamat": "Jl. Diponegoro, Madiun", "harga": 120000,
        "rating": 4.5, "review_count": 54,
        "fasilitas": "Kipas angin, kamar mandi dalam, dapur bersama",
    },
    {
        "icon": "🏘️", "nama": "Omah Asri Guesthouse",
        "alamat": "Jl. Mayjend Sungkono, Madiun", "harga": 175000,
        "rating": 4.6, "review_count": 63,
        "fasilitas": "AC, WiFi, dapur bersama, teras",
    },
    {
        "icon": "🏨", "nama": "Madiun Heritage Homestay",
        "alamat": "Jl. Kompol Sunaryo, Madiun", "harga": 280000,
        "rating": 4.7, "review_count": 95,
        "fasilitas": "AC, WiFi, sarapan, ruang tamu bersama",
    },
    {
        "icon": "🌾", "nama": "Sawah View Cottage",
        "alamat": "Geger, Madiun", "harga": 150000,
        "rating": 4.6, "review_count": 41,
        "fasilitas": "Pemandangan sawah, gazebo, kipas angin",
    },
    {
        "icon": "🏕️", "nama": "Kare Hill Homestay",
        "alamat": "Kare, Madiun", "harga": 225000,
        "rating": 4.7, "review_count": 58,
        "fasilitas": "Udara sejuk, api unggun, parkir luas",
    },
    {
        "icon": "🏩", "nama": "Pahlawan Residence",
        "alamat": "Jl. Pahlawan, Madiun", "harga": 260000,
        "rating": 4.4, "review_count": 39,
        "fasilitas": "AC, WiFi, dekat pusat kota, parkir",
    },
    {
        "icon": "🛌", "nama": "Simple Stay Madiun",
        "alamat": "Jl. Mangga, Madiun", "harga": 95000,
        "rating": 4.3, "review_count": 27,
        "fasilitas": "Kipas angin, kamar mandi dalam",
    },
]

BULAN_ID = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"]


def _generate_kode():
    now = datetime.datetime.now()
    return "GTH" + now.strftime("%y%m%d%H%M%S") + str(random.randint(0, 9))


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
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack(anchor="w")

        price_text = f"Rp {homestay['harga']:,}/malam".replace(",", ".")
        tk.Label(info_frame, text=price_text, font=("Segoe UI", 11, "bold"),
                bg=COLOR_WHITE, fg=COLOR_GREEN).pack(anchor="w", pady=(2, 0))

        # Facilities
        tk.Label(content, text=f"Fasilitas: {homestay['fasilitas']}", font=("Segoe UI", 8),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY, wraplength=230, justify="left").pack(anchor="w")

        # Button
        btn = tk.Button(content, text="Lihat Detail", bg=COLOR_GREEN, fg="white",
                       font=("Segoe UI", 9, "bold"), relief="flat",
                       command=self._on_click)
        btn.pack(anchor="e", pady=(10, 0))

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

        # Add homestay cards dalam grid 3 kolom (ke samping, hemat tempat)
        col = 0
        row = 0
        for homestay in HOMESTAY_CATALOG:
            card = HomestayCard(scrollable_frame, homestay, on_book=self._on_book_homestay)
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

            scrollable_frame.grid_columnconfigure(col, weight=1)

            col += 1
            if col >= 3:
                col = 0
                row += 1

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _on_book_homestay(self, homestay):
        """Handle booking homestay"""
        if not self.controller.active_user:
            messagebox.showwarning("Peringatan", "Silakan login terlebih dahulu.")
            return
        self._show_booking_dialog(homestay)

    def _show_booking_dialog(self, homestay):
        """Menampilkan dialog untuk booking homestay"""
        dialog = tk.Toplevel(self)
        dialog.title(f"Booking - {homestay['nama']}")
        dialog.geometry("600x550")
        dialog.resizable(True, True)

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

        if DateEntry is not None:
            checkin_date = DateEntry(date_frame, width=15, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy")
            checkin_date.pack(side="left", padx=(10, 20))
        else:
            checkin_var = tk.StringVar(value=datetime.date.today().strftime("%d/%m/%Y"))
            checkin_date = tk.Entry(date_frame, width=15, textvariable=checkin_var)
            checkin_date.pack(side="left", padx=(10, 20))

        tk.Label(date_frame, text="Check-out:", font=("Segoe UI", 10),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")

        if DateEntry is not None:
            checkout_date = DateEntry(date_frame, width=15, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy")
            checkout_date.pack(side="left", padx=(10, 0))
        else:
            checkout_var = tk.StringVar(
                value=(datetime.date.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
            )
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

        # Total price preview
        price_frame = tk.Frame(content, bg=COLOR_WHITE)
        price_frame.pack(pady=15, fill="x")

        tk.Label(price_frame, text="Total:", font=("Segoe UI", 12, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")

        price_label = tk.Label(price_frame, text="Rp 0", font=("Segoe UI", 14, "bold"),
                              bg=COLOR_WHITE, fg=COLOR_GREEN)
        price_label.pack(side="right")

        def _get_dates():
            checkin = str(checkin_date.get_date().strftime("%d/%m/%Y")) if hasattr(checkin_date, 'get_date') else checkin_date.get()
            checkout = str(checkout_date.get_date().strftime("%d/%m/%Y")) if hasattr(checkout_date, 'get_date') else checkout_date.get()
            return checkin, checkout

        def _hitung_malam(checkin, checkout):
            try:
                d1 = datetime.datetime.strptime(checkin, "%d/%m/%Y").date()
                d2 = datetime.datetime.strptime(checkout, "%d/%m/%Y").date()
                malam = (d2 - d1).days
                return malam if malam > 0 else 1
            except ValueError:
                return 1

        def update_price(*args):
            checkin, checkout = _get_dates()
            malam = _hitung_malam(checkin, checkout)
            total = homestay["harga"] * qty_var.get() * malam
            price_label.config(text=f"Rp {total:,}".replace(",", "."))

        qty_var.trace("w", update_price)
        update_price()

        # Separator
        separator2 = tk.Frame(content, bg="#e0e0e0", height=1)
        separator2.pack(fill="x", pady=15)

        # Buttons
        btn_frame = tk.Frame(content, bg=COLOR_WHITE)
        btn_frame.pack(fill="x", pady=20)

        def confirm_booking():
            try:
                qty = qty_var.get()
                checkin, checkout = _get_dates()

                if not checkin or not checkout:
                    messagebox.showwarning("Peringatan", "Silakan pilih tanggal!")
                    return

                malam = _hitung_malam(checkin, checkout)
                total = homestay["harga"] * qty * malam
                kode = _generate_kode()

                DataStore.homestays.append({
                    "username": self.controller.active_user,
                    "nama_homestay": homestay["nama"],
                    "alamat": homestay["alamat"],
                    "harga": total,
                    "checkin": checkin,
                    "checkout": checkout,
                    "kode": kode,
                })

                messagebox.showinfo(
                    "Sukses",
                    f"Booking berhasil!\nKode Booking: {kode}\nTotal: Rp {total:,}".replace(",", ".")
                )
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