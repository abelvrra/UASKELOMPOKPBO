import tkinter as tk
import random
from tkinter import messagebox
from data_store_2 import DataStore
from scroll_utils import enable_mousewheel_scroll

# ------------------------------------------------------------------
# Palet warna -- SENGAJA disamakan persis dengan dashboard_frame_2.py
# (bukan colors.py yang bertema ungu) supaya halaman ini tetap
# berkesinambungan secara visual dengan Beranda.
# ------------------------------------------------------------------
COLOR_BG = "#f7f8fa"
COLOR_SIDEBAR = "#ffffff"
COLOR_BORDER = "#e6e8eb"
COLOR_GREEN_DARK = "#1f7a35"
COLOR_GREEN = "#2f9e44"
COLOR_GREEN_LIGHT = "#e8f5e9"
COLOR_TEXT_DARK = "#1a1a1a"
COLOR_TEXT_GRAY = "#6b7280"
COLOR_RED = "#e03131"
COLOR_STAR = "#f5a623"
COLOR_WHITE = "#ffffff"


class SidebarItem(tk.Frame):
    """Item navigasi sidebar -- identik dengan yang ada di dashboard_frame_2.py
    supaya perilaku & tampilan sidebar sama persis di semua halaman."""

    def __init__(self, master, icon_char, label, active=False, danger=False,
                 command=None, **kwargs):
        bg = COLOR_GREEN_LIGHT if active else COLOR_SIDEBAR
        fg = COLOR_GREEN_DARK if active else (COLOR_RED if danger else "#333333")
        super().__init__(master, bg=bg, cursor="hand2", **kwargs)
        self.command = command

        inner = tk.Frame(self, bg=bg)
        inner.pack(fill="x", padx=14, pady=10)

        icon_lbl = tk.Label(inner, text=icon_char, font=("Segoe UI Emoji", 12), bg=bg, fg=fg)
        icon_lbl.pack(side="left")

        weight = "bold" if active else "normal"
        text_lbl = tk.Label(inner, text=label, font=("Segoe UI", 11, weight), bg=bg, fg=fg)
        text_lbl.pack(side="left", padx=(10, 0))

        for widget in (self, inner, icon_lbl, text_lbl):
            widget.bind("<Button-1>", self._on_click)

    def _on_click(self, event=None):
        if self.command:
            self.command()


class HomestayCard(tk.Frame):
    """Kartu satu homestay: ikon rumah, nama, alamat, harga/malam,
    rating bintang, dan tombol 'Lihat Detail'."""

    def __init__(self, master, data, on_detail=None, **kwargs):
        super().__init__(master, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                          highlightthickness=1, bd=0, **kwargs)

        content = tk.Frame(self, bg=COLOR_WHITE)
        content.pack(fill="both", expand=True, padx=24, pady=22)
        content.grid_columnconfigure(1, weight=1)

        icon_canvas = tk.Canvas(content, width=76, height=76, bg=COLOR_WHITE,
                                 highlightthickness=0)
        icon_canvas.grid(row=0, column=0, rowspan=3, sticky="n", padx=(0, 20))
        icon_canvas.create_oval(2, 2, 74, 74, fill=COLOR_GREEN_LIGHT, outline="")
        icon_canvas.create_text(38, 38, text="\U0001F3E0", font=("Segoe UI Emoji", 26))

        tk.Label(content, text=data["nama"], font=("Segoe UI", 15, "bold"), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK, anchor="w").grid(row=0, column=1, sticky="w")
        tk.Label(content, text=data["alamat"], font=("Segoe UI", 10), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY, anchor="w").grid(row=1, column=1, sticky="w", pady=(2, 0))

        price_frame = tk.Frame(content, bg=COLOR_WHITE)
        price_frame.grid(row=2, column=1, sticky="w", pady=(10, 0))
        harga_fmt = f"Rp {data['harga']:,.0f}".replace(",", ".")
        tk.Label(price_frame, text=harga_fmt, font=("Segoe UI", 14, "bold"),
                 bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")
        tk.Label(price_frame, text=" /malam", font=("Segoe UI", 10), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY).pack(side="left")

        rating_frame = tk.Frame(content, bg=COLOR_WHITE)
        rating_frame.grid(row=0, column=2, rowspan=3, sticky="e", padx=(20, 20))
        tk.Label(rating_frame, text="\u2605", font=("Segoe UI", 14), bg=COLOR_WHITE,
                 fg=COLOR_STAR).pack(side="left")
        tk.Label(rating_frame, text=f" {data['rating']}", font=("Segoe UI", 12, "bold"),
                 bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")

        detail_btn = tk.Button(
            content, text="Lihat Detail", font=("Segoe UI", 11, "bold"), bg=COLOR_GREEN_DARK,
            fg=COLOR_WHITE, activebackground=COLOR_GREEN, activeforeground=COLOR_WHITE,
            relief="flat", padx=20, pady=8, cursor="hand2",
            command=lambda: on_detail(data) if on_detail else None,
        )
        detail_btn.grid(row=0, column=3, rowspan=3, sticky="e")


class HomestayFrame(tk.Frame):
    """Halaman Booking Homestay -- selaras dengan sidebar & tema DashboardFrame."""

    # Data contoh homestay. Bisa diganti/ditambah, atau nanti disambungkan ke DataStore/DB.
    HOMESTAYS = [
        {"nama": "Homestay Madiun City", "alamat": "Jl. Pahlawan No. 45, Madiun",
         "harga": 200000, "rating": 4.6},
        {"nama": "Ndalem Habibah Homestay", "alamat": "Jl. Yos Sudarso No. 12, Madiun",
         "harga": 250000, "rating": 4.5},
        {"nama": "Griya Madiun Syariah", "alamat": "Jl. Setiabudi No. 8, Madiun",
         "harga": 180000, "rating": 4.4},
    ]

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self._build_layout()

    # ----------------------------------------------------------
    def _build_layout(self):
        # ---------------- SIDEBAR ----------------
        sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=270,
                            highlightbackground=COLOR_BORDER, highlightthickness=1)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_frame = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
        logo_frame.pack(pady=(36, 10))

        logo_canvas = tk.Canvas(logo_frame, width=60, height=60, bg=COLOR_SIDEBAR,
                                 highlightthickness=0)
        logo_canvas.pack()
        logo_canvas.create_polygon(30, 5, 45, 40, 15, 40, fill="", outline=COLOR_GREEN, width=2)
        logo_canvas.create_line(30, 5, 30, 40, fill=COLOR_GREEN, width=2)
        logo_canvas.create_oval(26, 2, 34, 10, outline=COLOR_GREEN, width=2)
        logo_canvas.create_line(10, 45, 50, 45, fill=COLOR_GREEN, width=2)

        tk.Label(logo_frame, text="GoTravel", font=("Segoe UI", 16, "bold"),
                 bg=COLOR_SIDEBAR, fg=COLOR_GREEN_DARK).pack(pady=(6, 0))
        tk.Label(logo_frame, text="Kota Madiun", font=("Segoe UI", 10),
                 bg=COLOR_SIDEBAR, fg=COLOR_TEXT_GRAY).pack()

        nav_frame = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
        nav_frame.pack(fill="x", pady=(24, 0), padx=12)

        menu_items = [
            ("\U0001F3E0", "Beranda", False, False, "DashboardFrame"),
            ("\U0001F3AB", "Beli Tiket Wisata", False, False, "TicketFrame"),
            ("\U0001F3E1", "Booking Homestay", True, False, "HomestayFrame"),
            ("\U0001F5FA", "Cek Rute & Cuaca", False, False, "RouteFrame2"),
            ("\u2716", "Pembatalan Booking", False, False, "CancellationFrame"),
        ]
        for icon, label, active, danger, frame_name in menu_items:
            item = SidebarItem(nav_frame, icon, label, active=active, danger=danger,
                                command=lambda fn=frame_name: self.controller.show_frame(fn))
            item.pack(fill="x", pady=3)

        logout_frame = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
        logout_frame.pack(side="bottom", fill="x", padx=12, pady=30)
        logout_item = SidebarItem(logout_frame, "\u2192", "Logout", danger=True,
                                   command=self._on_logout)
        logout_item.pack(fill="x")

        # ---------------- MAIN CONTENT ----------------
        main = tk.Frame(self, bg=COLOR_BG)
        main.pack(side="left", fill="both", expand=True)

        content = tk.Frame(main, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=50, pady=45)

        # Header: tombol back + judul + subjudul
        header = tk.Frame(content, bg=COLOR_BG)
        header.pack(anchor="w", fill="x", pady=(0, 26))

        back_canvas = tk.Canvas(header, width=48, height=48, bg=COLOR_BG,
                                 highlightthickness=0, cursor="hand2")
        back_canvas.grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 18))
        back_canvas.create_oval(2, 2, 46, 46, fill=COLOR_GREEN_LIGHT, outline="")
        back_canvas.create_text(24, 24, text="\u2190", font=("Segoe UI", 16, "bold"),
                                 fill=COLOR_GREEN)
        back_canvas.bind("<Button-1>", lambda e: self.controller.show_frame("DashboardFrame"))

        tk.Label(header, text="Booking Homestay", font=("Segoe UI", 22, "bold"),
                 bg=COLOR_BG, fg=COLOR_TEXT_DARK, anchor="w").grid(row=0, column=1, sticky="w")
        tk.Label(header, text="Temukan homestay terbaik di Kota Madiun", font=("Segoe UI", 12),
                 bg=COLOR_BG, fg=COLOR_TEXT_GRAY, anchor="w").grid(row=1, column=1, sticky="w",
                                                                     pady=(4, 0))

        # Kotak filter pencarian
        self._build_filter_box(content)

        # Daftar homestay (scrollable)
        self._build_homestay_list(content)

    # ----------------------------------------------------------
    def _build_filter_box(self, parent):
        box = tk.Frame(parent, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                        highlightthickness=1)
        box.pack(fill="x", pady=(0, 22))

        inner = tk.Frame(box, bg=COLOR_WHITE)
        inner.pack(fill="x", padx=28, pady=26)
        inner.grid_columnconfigure(0, weight=2)
        inner.grid_columnconfigure(1, weight=2)
        inner.grid_columnconfigure(2, weight=1)
        inner.grid_columnconfigure(3, weight=0)

        self.checkin_var = self._date_field(inner, "Check-in", "20/05/2024", col=0)
        self.checkout_var = self._date_field(inner, "Check-out", "21/05/2024", col=1)

        # Dropdown Tamu
        tamu_frame = tk.Frame(inner, bg=COLOR_WHITE)
        tamu_frame.grid(row=0, column=2, sticky="ew", padx=(0, 20))
        tk.Label(tamu_frame, text="Tamu", font=("Segoe UI", 10), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK, anchor="w").pack(anchor="w", pady=(0, 6))
        tamu_box = tk.Frame(tamu_frame, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                             highlightthickness=1)
        tamu_box.pack(fill="x")
        self.tamu_var = tk.StringVar(value="2")
        tamu_menu = tk.OptionMenu(tamu_box, self.tamu_var, "1", "2", "3", "4", "5", "6+")
        tamu_menu.configure(font=("Segoe UI", 11), bg=COLOR_WHITE, fg=COLOR_TEXT_DARK,
                             bd=0, relief="flat", highlightthickness=0, anchor="w")
        tamu_menu["menu"].configure(font=("Segoe UI", 11))
        tamu_menu.pack(fill="both", expand=True, padx=8, pady=6)

        cari_btn = tk.Button(
            inner, text="Cari", font=("Segoe UI", 11, "bold"), bg=COLOR_GREEN_DARK,
            fg=COLOR_WHITE, activebackground=COLOR_GREEN, activeforeground=COLOR_WHITE,
            relief="flat", padx=28, pady=12, cursor="hand2", command=self._on_cari,
        )
        cari_btn.grid(row=0, column=3, sticky="s")

    def _date_field(self, parent, label_text, default_value, col):
        wrap = tk.Frame(parent, bg=COLOR_WHITE)
        wrap.grid(row=0, column=col, sticky="ew", padx=(0, 20))

        tk.Label(wrap, text=label_text, font=("Segoe UI", 10), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK, anchor="w").pack(anchor="w", pady=(0, 6))

        field_box = tk.Frame(wrap, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                              highlightthickness=1)
        field_box.pack(fill="x")

        var = tk.StringVar(value=default_value)
        entry = tk.Entry(field_box, textvariable=var, font=("Segoe UI", 11), bd=0,
                          bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, relief="flat",
                          insertbackground=COLOR_TEXT_DARK)
        entry.pack(side="left", fill="both", expand=True, padx=12, pady=10)

        tk.Label(field_box, text="\U0001F4C5", font=("Segoe UI", 12), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY).pack(side="right", padx=12)
        return var

    def _on_cari(self):
        # TODO: hubungkan ke sumber data nyata (DB/API) sesuai filter tanggal & jumlah tamu.
        checkin = self.checkin_var.get()
        checkout = self.checkout_var.get()
        tamu = self.tamu_var.get()
        print(f"Mencari homestay: check-in={checkin}, check-out={checkout}, tamu={tamu}")
        self._render_list(self.HOMESTAYS)

    # ----------------------------------------------------------
    def _build_homestay_list(self, parent):
        scroll_wrap = tk.Frame(parent, bg=COLOR_BG)
        scroll_wrap.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_wrap, bg=COLOR_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_wrap, orient="vertical", command=canvas.yview)
        self.list_container = tk.Frame(canvas, bg=COLOR_BG)

        self.list_container.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((0, 0), window=self.list_container, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        enable_mousewheel_scroll(canvas)

        self._render_list(self.HOMESTAYS)

    def _render_list(self, homestays):
        for widget in self.list_container.winfo_children():
            widget.destroy()
        for data in homestays:
            card = HomestayCard(self.list_container, data, on_detail=self._open_detail)
            card.pack(fill="x", pady=(0, 18))

    # ----------------------------------------------------------
    def _open_detail(self, data):
        """Dialog detail homestay + tombol booking."""
        popup = tk.Toplevel(self)
        popup.title(data["nama"])
        popup.configure(bg=COLOR_WHITE)
        popup.resizable(False, False)
        popup.transient(self.winfo_toplevel())

        w, h = 420, 360
        root = self.winfo_toplevel()
        root.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (w // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")
        popup.grab_set()

        wrap = tk.Frame(popup, bg=COLOR_WHITE)
        wrap.pack(fill="both", expand=True, padx=28, pady=26)

        icon_canvas = tk.Canvas(wrap, width=72, height=72, bg=COLOR_WHITE, highlightthickness=0)
        icon_canvas.pack(pady=(0, 14))
        icon_canvas.create_oval(2, 2, 70, 70, fill=COLOR_GREEN_LIGHT, outline="")
        icon_canvas.create_text(36, 36, text="\U0001F3E0", font=("Segoe UI Emoji", 26))

        tk.Label(wrap, text=data["nama"], font=("Segoe UI", 16, "bold"), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK).pack()
        tk.Label(wrap, text=data["alamat"], font=("Segoe UI", 10), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY).pack(pady=(2, 14))

        info_frame = tk.Frame(wrap, bg=COLOR_WHITE)
        info_frame.pack(fill="x", pady=(0, 18))

        harga_fmt = f"Rp {data['harga']:,.0f}".replace(",", ".")
        tk.Label(info_frame, text=f"{harga_fmt} /malam", font=("Segoe UI", 14, "bold"),
                 bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")

        rating_frame = tk.Frame(info_frame, bg=COLOR_WHITE)
        rating_frame.pack(side="right")
        tk.Label(rating_frame, text="\u2605", font=("Segoe UI", 13), bg=COLOR_WHITE,
                 fg=COLOR_STAR).pack(side="left")
        tk.Label(rating_frame, text=f" {data['rating']}", font=("Segoe UI", 12, "bold"),
                 bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")

        tk.Button(
            wrap, text="Booking Sekarang", font=("Segoe UI", 11, "bold"), bg=COLOR_GREEN_DARK,
            fg=COLOR_WHITE, activebackground=COLOR_GREEN, activeforeground=COLOR_WHITE,
            relief="flat", pady=12, cursor="hand2",
            command=lambda: self._pesan_homestay(data, popup),
        ).pack(fill="x", pady=(10, 0))

    def _pesan_homestay(self, data, popup=None):
        """Simpan booking ke DataStore. Struktur data dijaga kompatibel dengan
        cancellation_frame_2.py (butuh key 'username', 'nama_homestay', 'kode', dst)."""
        if not DataStore.active_user:
            messagebox.showwarning("Peringatan", "Silakan login terlebih dahulu!")
            self.controller.show_frame("LoginFrame")
            if popup:
                popup.destroy()
            return

        kode = f"GTH{random.randint(10**10, 10**11 - 1)}"
        DataStore.homestays.append({
            "username": DataStore.active_user,
            "nama_homestay": data["nama"],
            "alamat": data["alamat"],
            "harga": data["harga"],
            "checkin": self.checkin_var.get(),
            "checkout": self.checkout_var.get(),
            "kode": kode,
        })
        messagebox.showinfo("Sukses", f"Berhasil booking {data['nama']}!")
        if popup:
            popup.destroy()

    # ----------------------------------------------------------
    def _on_logout(self):
        if hasattr(self.controller, "logout_action"):
            self.controller.logout_action()
        else:
            self.controller.show_frame("LoginFrame")

    def refresh(self):
        """Dipanggil otomatis oleh main_2.py (show_frame) tiap kali halaman ini dibuka."""
        self._render_list(self.HOMESTAYS)