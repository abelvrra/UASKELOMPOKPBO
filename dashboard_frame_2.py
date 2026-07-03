import tkinter as tk
from tkinter import font as tkfont
 
 
# ------------------------------------------------------------------
# Palet warna (disesuaikan dengan desain)
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
COLOR_RED_LIGHT = "#fdeaea"
COLOR_GOLD = "#d4a017"
 
 
class RoundedCard(tk.Frame):
    """Kartu menu dengan ikon lingkaran, judul, deskripsi, dan tombol panah."""
 
    def __init__(self, master, icon_char, icon_bg, icon_fg, title, description,
                 command=None, **kwargs):
        super().__init__(master, bg="white", highlightbackground=COLOR_BORDER,
                          highlightthickness=1, bd=0, **kwargs)
        self.command = command
        self.configure(cursor="hand2")
 
        content = tk.Frame(self, bg="white")
        content.pack(fill="both", expand=True, padx=22, pady=20)
 
        # Ikon lingkaran
        icon_canvas = tk.Canvas(content, width=64, height=64, bg="white",
                                 highlightthickness=0)
        icon_canvas.grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 18))
        icon_canvas.create_oval(2, 2, 62, 62, fill=icon_bg, outline="")
        icon_canvas.create_text(32, 32, text=icon_char, font=("Segoe UI Emoji", 20),
                                 fill=icon_fg)
 
        # Judul
        title_lbl = tk.Label(content, text=title, font=("Segoe UI", 14, "bold"),
                              bg="white", fg=COLOR_TEXT_DARK, anchor="w")
        title_lbl.grid(row=0, column=1, sticky="w")
 
        # Deskripsi
        desc_lbl = tk.Label(content, text=description, font=("Segoe UI", 10),
                             bg="white", fg=COLOR_TEXT_GRAY, anchor="w",
                             justify="left", wraplength=230)
        desc_lbl.grid(row=1, column=1, sticky="w", pady=(4, 0))
 
        content.grid_columnconfigure(1, weight=1)
 
        # Tombol panah
        arrow_canvas = tk.Canvas(content, width=36, height=36, bg="white",
                                  highlightthickness=0)
        arrow_canvas.grid(row=0, column=2, rowspan=2, sticky="e")
        arrow_canvas.create_oval(2, 2, 34, 34, fill=COLOR_GREEN_LIGHT, outline="")
        arrow_canvas.create_text(18, 18, text="\u203a", font=("Segoe UI", 14, "bold"),
                                  fill=COLOR_GREEN)
 
        # Bind klik ke seluruh kartu
        for widget in (self, content, icon_canvas, title_lbl, desc_lbl, arrow_canvas):
            widget.bind("<Button-1>", self._on_click)
 
    def _on_click(self, event=None):
        if self.command:
            self.command()
 
 
class SidebarItem(tk.Frame):
    """Item navigasi di sidebar (bisa aktif/tidak aktif)."""
 
    def __init__(self, master, icon_char, label, active=False, danger=False,
                 command=None, **kwargs):
        bg = COLOR_GREEN_LIGHT if active else COLOR_SIDEBAR
        fg = COLOR_GREEN_DARK if active else (COLOR_RED if danger else "#333333")
        super().__init__(master, bg=bg, cursor="hand2", **kwargs)
        self.command = command
 
        inner = tk.Frame(self, bg=bg)
        inner.pack(fill="x", padx=14, pady=10)
 
        icon_lbl = tk.Label(inner, text=icon_char, font=("Segoe UI Emoji", 12),
                             bg=bg, fg=fg)
        icon_lbl.pack(side="left")
 
        weight = "bold" if active else "normal"
        text_lbl = tk.Label(inner, text=label, font=("Segoe UI", 11, weight),
                             bg=bg, fg=fg)
        text_lbl.pack(side="left", padx=(10, 0))
 
        for widget in (self, inner, icon_lbl, text_lbl):
            widget.bind("<Button-1>", self._on_click)
 
    def _on_click(self, event=None):
        if self.command:
            self.command()
 
 
class StatItem(tk.Frame):
    """Satu blok statistik pada bar bawah (ikon + judul + subjudul)."""
 
    def __init__(self, master, icon_char, icon_fg, title, subtitle, **kwargs):
        super().__init__(master, bg=COLOR_GREEN_LIGHT, **kwargs)
        icon_lbl = tk.Label(self, text=icon_char, font=("Segoe UI Emoji", 16),
                             bg=COLOR_GREEN_LIGHT, fg=icon_fg)
        icon_lbl.pack(side="left", padx=(0, 10))
 
        text_frame = tk.Frame(self, bg=COLOR_GREEN_LIGHT)
        text_frame.pack(side="left")
 
        tk.Label(text_frame, text=title, font=("Segoe UI", 11, "bold"),
                 bg=COLOR_GREEN_LIGHT, fg=COLOR_TEXT_DARK, anchor="w").pack(anchor="w")
        tk.Label(text_frame, text=subtitle, font=("Segoe UI", 10),
                 bg=COLOR_GREEN_LIGHT, fg=COLOR_TEXT_GRAY, anchor="w").pack(anchor="w")
 
 
class DashboardFrame(tk.Frame): # Ubah dari tk.Tk ke tk.Frame
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG) # Inisialisasi Frame
        self.controller = controller # Simpan controller untuk navigasi
        
        # Panggil fungsi layout Anda
        self._build_layout()

    def _on_nav_click(self, key):
        mapping = {
            "beranda": "DashboardFrame",
            "beli_tiket": "TicketFrame",
            "booking_homestay": "HomestayFrame",
            "cek_rute": "RouteFrame2",
            "batal_booking": "CancellationFrame",
        }
        target = mapping.get(key)
        if target:
            self.controller.show_frame(target)

    def _on_logout(self):
        if hasattr(self.controller, "logout_action"):
            self.controller.logout_action()
        else:
            self.controller.show_frame("LoginFrame")
 
    # --------------------------------------------------------------
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
        # ikon sederhana berbentuk "landmark" (segitiga + garis, mewakili menara/gapura)
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
            ("\U0001F3E0", "Beranda", True, False, "beranda"),
            ("\U0001F3AB", "Beli Tiket Wisata", False, False, "beli_tiket"),
            ("\U0001F3E1", "Booking Homestay", False, False, "booking_homestay"),
            ("\U0001F5FA", "Cek Rute & Cuaca", False, False, "cek_rute"),
            ("\u2716", "Pembatalan Booking", False, False, "batal_booking"),
        ]
        self.nav_widgets = {}
        for icon, label, active, danger, key in menu_items:
            item = SidebarItem(nav_frame, icon, label, active=active, danger=danger,
                                command=lambda k=key: self._on_nav_click(k))
            item.pack(fill="x", pady=3)
            self.nav_widgets[key] = item
 
        # Logout di bagian bawah sidebar
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
 
        # Header sambutan
        tk.Label(content, text="Selamat Datang, User! \U0001F44B",
                 font=("Segoe UI", 26, "bold"), bg=COLOR_BG,
                 fg=COLOR_TEXT_DARK).pack(anchor="w")
        tk.Label(content, text="Jelajahi wisata terbaik di Kota Madiun dengan mudah.",
                 font=("Segoe UI", 12), bg=COLOR_BG, fg=COLOR_TEXT_GRAY).pack(
            anchor="w", pady=(6, 30))
 
        # Grid kartu 2x2
        grid_frame = tk.Frame(content, bg=COLOR_BG)
        grid_frame.pack(fill="both", expand=True)
        grid_frame.grid_columnconfigure(0, weight=1, uniform="col")
        grid_frame.grid_columnconfigure(1, weight=1, uniform="col")
        grid_frame.grid_rowconfigure(0, weight=1)
        grid_frame.grid_rowconfigure(1, weight=1)
 
        card_data = [
            ("\U0001F3AB", COLOR_GREEN_LIGHT, COLOR_GREEN,
             "Beli Tiket Wisata", "Pesan tiket masuk objek wisata favoritmu.", "beli_tiket"),
            ("\U0001F3E0", COLOR_GREEN_LIGHT, COLOR_GREEN,
             "Booking Homestay", "Temukan dan pesan homestay nyaman.", "booking_homestay"),
            ("\U0001F4CD", COLOR_GREEN_LIGHT, COLOR_GREEN,
             "Cek Rute & Cuaca", "Lihat rute, peta, dan prakiraan cuaca.", "cek_rute"),
            ("\u2716", COLOR_RED_LIGHT, COLOR_RED,
             "Pembatalan Booking", "Batalkan atau ubah pesanan dengan mudah.", "batal_booking"),
        ]
 
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for (icon, ibg, ifg, title, desc, key), (r, c) in zip(card_data, positions):
            card = RoundedCard(grid_frame, icon, ibg, ifg, title, desc,
                                command=lambda k=key: self._on_nav_click(k))
            card.grid(row=r, column=c, sticky="nsew",
                      padx=(0, 18) if c == 0 else (18, 0),
                      pady=(0, 18) if r == 0 else (18, 0))
 
        # ---------------- STAT BAR BAWAH ----------------
        stat_bar = tk.Frame(content, bg=COLOR_GREEN_LIGHT)
        stat_bar.pack(fill="x", pady=(30, 0))
 
        stat_inner = tk.Frame(stat_bar, bg=COLOR_GREEN_LIGHT)
        stat_inner.pack(fill="x", padx=30, pady=20)
        stat_inner.grid_columnconfigure(0, weight=1)
        stat_inner.grid_columnconfigure(1, weight=1)
        stat_inner.grid_columnconfigure(2, weight=1)
 
        StatItem(stat_inner, "\U0001F4CD", COLOR_GREEN, "Kota Madiun",
                 "Jawa Timur").grid(row=0, column=0, sticky="w")
        StatItem(stat_inner, "\u2600", COLOR_GOLD, "Cuaca Hari Ini",
                 "Cerah, 28\u00b0C").grid(row=0, column=1, sticky="w")
        StatItem(stat_inner, "\u2B50", COLOR_GREEN, "15+ Destinasi",
                 "Wisata Menarik").grid(row=0, column=2, sticky="w")