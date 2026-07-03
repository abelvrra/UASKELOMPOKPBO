import tkinter as tk
import random
from tkinter import messagebox
from data_store_2 import DataStore
from sidebar_common import build_sidebar
from scroll_utils import enable_mousewheel_scroll

# ------------------------------------------------------------------
# Palet warna -- disamakan dengan dashboard_frame_2.py / homestay_frame_2.py
# ------------------------------------------------------------------
COLOR_BG = "#f7f8fa"
COLOR_BORDER = "#e6e8eb"
COLOR_GREEN_DARK = "#1f7a35"
COLOR_GREEN = "#2f9e44"
COLOR_GREEN_LIGHT = "#e8f5e9"
COLOR_TEXT_DARK = "#1a1a1a"
COLOR_TEXT_GRAY = "#6b7280"
COLOR_WHITE = "#ffffff"
COLOR_DISABLED_BG = "#d9ecdc"
COLOR_DISABLED_FG = "#8fbf9a"

# Data destinasi wisata -- sesuai desain "Beli Tiket Wisata"
DESTINATIONS = [
    {"icon": "\u26E9", "nama": "Alun-Alun Kota Madiun",
     "desc": "Taman kota yang asri dan ikon kota Madiun.", "harga": 0,
     "jam_buka": "24 Jam", "lokasi": "Jl. Pahlawan, Kota Madiun",
     "fasilitas": "Taman, Area Bermain, Kuliner"},
    {"icon": "\U0001F3E2", "nama": "Pahlawan Street Center",
     "desc": "Pusat kuliner & oleh-oleh khas Madiun.", "harga": 0,
     "jam_buka": "10.00 - 22.00", "lokasi": "Jl. Pahlawan, Kota Madiun",
     "fasilitas": "Foodcourt, Parkir, Toilet"},
    {"icon": "\U0001F30A", "nama": "Suncity Waterpark",
     "desc": "Wahana air seru untuk semua usia.", "harga": 35000,
     "jam_buka": "08.00 - 17.00", "lokasi": "Jl. Yos Sudarso, Kota Madiun",
     "fasilitas": "Kolam Renang, Wahana Air, Kafe"},
    {"icon": "\U0001F347", "nama": "Wana Wisata Grape",
     "desc": "Wisata alam dan edukasi perkebunan anggur.", "harga": 10000,
     "jam_buka": "07.00 - 16.00", "lokasi": "Kec. Dagangan, Kab. Madiun",
     "fasilitas": "Kebun Anggur, Spot Foto, Musholla"},
    {"icon": "\U0001F333", "nama": "Cemoro Sewu",
     "desc": "Hutan pinus dengan udara sejuk dan pemandangan indah.", "harga": 10000,
     "jam_buka": "06.00 - 18.00", "lokasi": "Kec. Kare, Kab. Madiun",
     "fasilitas": "Hutan Pinus, Camping Ground, Gazebo"},
    {"icon": "\U0001F3DB", "nama": "Museum Kretek Madiun",
     "desc": "Museum yang menyimpan sejarah rokok kretek.", "harga": 5000,
     "jam_buka": "08.00 - 15.00", "lokasi": "Jl. Yos Sudarso, Kota Madiun",
     "fasilitas": "Ruang Pameran, Pemandu, Parkir"},
]


def _format_rupiah(angka):
    return "Rp " + f"{angka:,.0f}".replace(",", ".")


class DestinationCard(tk.Frame):
    """Kartu destinasi wisata di grid kiri (ikon, nama, deskripsi, harga, tombol Pilih)."""

    def __init__(self, master, data, on_select=None, **kwargs):
        super().__init__(master, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                          highlightthickness=1, bd=0, **kwargs)
        content = tk.Frame(self, bg=COLOR_WHITE)
        content.pack(fill="both", expand=True, padx=20, pady=18)

        icon_canvas = tk.Canvas(content, width=52, height=52, bg=COLOR_WHITE,
                                 highlightthickness=0)
        icon_canvas.pack(anchor="w")
        icon_canvas.create_oval(2, 2, 50, 50, fill=COLOR_GREEN_LIGHT, outline="")
        icon_canvas.create_text(26, 26, text=data["icon"], font=("Segoe UI Emoji", 18))

        tk.Label(content, text=data["nama"], font=("Segoe UI", 12, "bold"), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK, anchor="w", justify="left").pack(anchor="w", pady=(10, 4))
        tk.Label(content, text=data["desc"], font=("Segoe UI", 9), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY, anchor="w", justify="left",
                 wraplength=230).pack(anchor="w")

        bottom = tk.Frame(content, bg=COLOR_WHITE)
        bottom.pack(fill="x", pady=(16, 0))

        tk.Label(bottom, text=_format_rupiah(data["harga"]), font=("Segoe UI", 11, "bold"),
                 bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")

        tk.Button(
            bottom, text="Pilih", font=("Segoe UI", 10, "bold"), bg=COLOR_GREEN_DARK,
            fg=COLOR_WHITE, activebackground=COLOR_GREEN, activeforeground=COLOR_WHITE,
            relief="flat", padx=18, pady=6, cursor="hand2",
            command=lambda: on_select(data) if on_select else None,
        ).pack(side="right")


class TicketFrame(tk.Frame):
    """Halaman Beli Tiket Wisata."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.selected_destination = None
        self.jumlah_tiket = tk.IntVar(value=1)
        self.current_page = 1

        build_sidebar(self, controller, active_frame_name="TicketFrame")

        main = tk.Frame(self, bg=COLOR_BG)
        main.pack(side="left", fill="both", expand=True)

        content = tk.Frame(main, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=40, pady=40)

        self._build_header(content)
        self._build_search(content)

        body = tk.Frame(content, bg=COLOR_BG)
        body.pack(fill="both", expand=True, pady=(20, 0))

        self._build_grid_area(body)
        self._build_detail_panel(body)

        self._build_pagination(content)

    # ----------------------------------------------------------
    def _build_header(self, parent):
        header = tk.Frame(parent, bg=COLOR_BG)
        header.pack(anchor="w", fill="x")

        back_canvas = tk.Canvas(header, width=44, height=44, bg=COLOR_BG,
                                 highlightthickness=0, cursor="hand2")
        back_canvas.grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 16))
        back_canvas.create_oval(2, 2, 42, 42, fill=COLOR_GREEN_LIGHT, outline="")
        back_canvas.create_text(22, 22, text="\u2190", font=("Segoe UI", 15, "bold"),
                                 fill=COLOR_GREEN)
        back_canvas.bind("<Button-1>", lambda e: self.controller.show_frame("DashboardFrame"))

        tk.Label(header, text="Beli Tiket Wisata", font=("Segoe UI", 20, "bold"),
                 bg=COLOR_BG, fg=COLOR_TEXT_DARK, anchor="w").grid(row=0, column=1, sticky="w")
        tk.Label(header, text="Pilih destinasi wisata yang ingin kamu kunjungi",
                 font=("Segoe UI", 11), bg=COLOR_BG, fg=COLOR_TEXT_GRAY,
                 anchor="w").grid(row=1, column=1, sticky="w", pady=(2, 0))

    def _build_search(self, parent):
        search_frame = tk.Frame(parent, bg=COLOR_BG)
        search_frame.pack(fill="x", pady=(20, 0))

        search_box = tk.Frame(search_frame, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                               highlightthickness=1)
        search_box.pack(side="left", fill="x", expand=True, padx=(0, 10))

        tk.Label(search_box, text="\U0001F50D", font=("Segoe UI", 10), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY).pack(side="left", padx=(12, 4))
        self.search_var = tk.StringVar()
        entry = tk.Entry(search_box, textvariable=self.search_var, font=("Segoe UI", 10),
                          bd=0, bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, relief="flat")
        entry.pack(side="left", fill="both", expand=True, ipady=8, padx=(0, 10))
        entry.bind("<KeyRelease>", lambda e: self._apply_search())
        self._add_placeholder(entry, "Cari destinasi wisata...")

        tk.Button(search_frame, text="\U0001F53D Filter", font=("Segoe UI", 9, "bold"),
                  bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, highlightbackground=COLOR_BORDER,
                  highlightthickness=1, bd=0, relief="flat", cursor="hand2",
                  padx=16, pady=9).pack(side="left")

    def _add_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.config(fg=COLOR_TEXT_GRAY)

        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg=COLOR_TEXT_DARK)

        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=COLOR_TEXT_GRAY)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def _apply_search(self):
        query = self.search_var.get().strip().lower()
        if query == "cari destinasi wisata...":
            query = ""
        if query:
            filtered = [d for d in DESTINATIONS if query in d["nama"].lower()]
        else:
            filtered = DESTINATIONS
        self._render_grid(filtered)

    # ----------------------------------------------------------
    def _build_grid_area(self, parent):
        wrap = tk.Frame(parent, bg=COLOR_BG)
        wrap.pack(side="left", fill="both", expand=True, padx=(0, 24))

        canvas = tk.Canvas(wrap, bg=COLOR_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
        self.grid_container = tk.Frame(canvas, bg=COLOR_BG)

        self.grid_container.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((0, 0), window=self.grid_container, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        enable_mousewheel_scroll(canvas)

        self.grid_container.grid_columnconfigure(0, weight=1, uniform="c")
        self.grid_container.grid_columnconfigure(1, weight=1, uniform="c")

        self._render_grid(DESTINATIONS)

    def _render_grid(self, destinations):
        for widget in self.grid_container.winfo_children():
            widget.destroy()
        row, col = 0, 0
        for dest in destinations:
            card = DestinationCard(self.grid_container, dest, on_select=self._select_destination)
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
            col += 1
            if col == 2:
                col = 0
                row += 1
        if not destinations:
            tk.Label(self.grid_container, text="Destinasi tidak ditemukan.",
                     font=("Segoe UI", 10), bg=COLOR_BG, fg=COLOR_TEXT_GRAY).grid(
                row=0, column=0, columnspan=2, pady=30)

    # ----------------------------------------------------------
    def _build_detail_panel(self, parent):
        panel = tk.Frame(parent, bg=COLOR_WHITE, width=320,
                          highlightbackground=COLOR_BORDER, highlightthickness=1)
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)

        inner = tk.Frame(panel, bg=COLOR_WHITE)
        inner.pack(fill="both", expand=True, padx=22, pady=22)

        tk.Label(inner, text="Detail Destinasi", font=("Segoe UI", 13, "bold"),
                 bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, anchor="w").pack(anchor="w")

        # Placeholder gambar
        img_canvas = tk.Canvas(inner, height=140, bg=COLOR_GREEN_LIGHT, highlightthickness=0)
        img_canvas.pack(fill="x", pady=(14, 16))
        img_canvas.bind("<Configure>", lambda e: self._draw_placeholder_mountain(img_canvas, e))
        self._img_canvas = img_canvas

        self.detail_title = tk.Label(inner, text="Pilih destinasi untuk melihat detail",
                                      font=("Segoe UI", 13, "bold"), bg=COLOR_WHITE,
                                      fg=COLOR_TEXT_DARK, anchor="w", justify="left",
                                      wraplength=270)
        self.detail_title.pack(anchor="w")

        self.detail_subtitle = tk.Label(
            inner, text="Klik salah satu destinasi wisata untuk melihat informasi "
                        "lebih lengkap dan melakukan pemesanan.",
            font=("Segoe UI", 9), bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY, anchor="w",
            justify="left", wraplength=270)
        self.detail_subtitle.pack(anchor="w", pady=(4, 16))

        tk.Frame(inner, bg=COLOR_BORDER, height=1).pack(fill="x", pady=(0, 14))

        tk.Label(inner, text="Informasi", font=("Segoe UI", 10, "bold"), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK, anchor="w").pack(anchor="w", pady=(0, 10))

        self.info_labels = {}
        for key, icon, label in [
            ("jam_buka", "\u23F0", "Jam Buka"),
            ("lokasi", "\U0001F4CD", "Lokasi"),
            ("harga_tiket", "\U0001F3F7", "Harga Tiket"),
            ("fasilitas", "\u2728", "Fasilitas"),
        ]:
            row = tk.Frame(inner, bg=COLOR_WHITE)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=icon, font=("Segoe UI", 10), bg=COLOR_WHITE,
                     fg=COLOR_GREEN, width=3).pack(side="left")
            tk.Label(row, text=label, font=("Segoe UI", 9, "bold"), bg=COLOR_WHITE,
                     fg=COLOR_TEXT_DARK, width=10, anchor="w").pack(side="left")
            val = tk.Label(row, text="-", font=("Segoe UI", 9), bg=COLOR_WHITE,
                            fg=COLOR_TEXT_GRAY, anchor="w", justify="left", wraplength=140)
            val.pack(side="left", fill="x", expand=True)
            self.info_labels[key] = val

        # Stepper jumlah tiket
        qty_frame = tk.Frame(inner, bg=COLOR_WHITE)
        qty_frame.pack(fill="x", pady=(14, 0))
        tk.Label(qty_frame, text="Jumlah Tiket", font=("Segoe UI", 9, "bold"),
                 bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, anchor="w").pack(anchor="w")

        stepper = tk.Frame(qty_frame, bg=COLOR_WHITE)
        stepper.pack(anchor="w", pady=(6, 0))
        tk.Button(stepper, text="-", font=("Segoe UI", 10, "bold"), width=3,
                  bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, highlightbackground=COLOR_BORDER,
                  highlightthickness=1, bd=0, relief="flat", cursor="hand2",
                  command=self._decrease_qty).pack(side="left")
        self.qty_label = tk.Label(stepper, textvariable=self.jumlah_tiket, font=("Segoe UI", 10, "bold"),
                                   bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, width=4)
        self.qty_label.pack(side="left")
        tk.Button(stepper, text="+", font=("Segoe UI", 10, "bold"), width=3,
                  bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, highlightbackground=COLOR_BORDER,
                  highlightthickness=1, bd=0, relief="flat", cursor="hand2",
                  command=self._increase_qty).pack(side="left")

        self.lanjut_btn = tk.Button(
            inner, text="Lanjut ke Pemesanan  \u203a", font=("Segoe UI", 10, "bold"),
            bg=COLOR_DISABLED_BG, fg=COLOR_DISABLED_FG, relief="flat", pady=11,
            state="disabled", command=self._proceed_booking,
        )
        self.lanjut_btn.pack(fill="x", side="bottom", pady=(18, 0))

    def _draw_placeholder_mountain(self, canvas, event=None):
        canvas.delete("all")
        w = canvas.winfo_width() or 270
        h = canvas.winfo_height() or 140
        canvas.create_oval(w * 0.6, h * 0.18, w * 0.6 + 20, h * 0.18 + 20,
                            outline=COLOR_GREEN, width=2)
        canvas.create_polygon(w * 0.25, h * 0.75, w * 0.45, h * 0.4, w * 0.65, h * 0.75,
                               outline=COLOR_GREEN, width=2, fill="")
        canvas.create_polygon(w * 0.5, h * 0.75, w * 0.68, h * 0.5, w * 0.85, h * 0.75,
                               outline=COLOR_GREEN, width=2, fill="")

    # ----------------------------------------------------------
    def _build_pagination(self, parent):
        pag = tk.Frame(parent, bg=COLOR_BG)
        pag.pack(pady=(20, 0))

        self.page_buttons = {}

        tk.Button(pag, text="\u2190", font=("Segoe UI", 10), bg=COLOR_WHITE,
                  fg=COLOR_TEXT_DARK, highlightbackground=COLOR_BORDER, highlightthickness=1,
                  bd=0, width=3, cursor="hand2",
                  command=lambda: self._go_to_page(max(1, self.current_page - 1))
                  ).pack(side="left", padx=4)

        for page in (1, 2, 3):
            btn = tk.Button(pag, text=str(page), font=("Segoe UI", 9, "bold"), width=3,
                             cursor="hand2", bd=0, relief="flat",
                             command=lambda p=page: self._go_to_page(p))
            btn.pack(side="left", padx=4)
            self.page_buttons[page] = btn

        tk.Button(pag, text="\u2192", font=("Segoe UI", 10), bg=COLOR_WHITE,
                  fg=COLOR_TEXT_DARK, highlightbackground=COLOR_BORDER, highlightthickness=1,
                  bd=0, width=3, cursor="hand2",
                  command=lambda: self._go_to_page(min(3, self.current_page + 1))
                  ).pack(side="left", padx=4)

        self._update_pagination_style()

    def _update_pagination_style(self):
        for page, btn in self.page_buttons.items():
            if page == self.current_page:
                btn.configure(bg=COLOR_GREEN_DARK, fg=COLOR_WHITE)
            else:
                btn.configure(bg=COLOR_WHITE, fg=COLOR_TEXT_DARK,
                               highlightbackground=COLOR_BORDER, highlightthickness=1)

    def _go_to_page(self, page):
        self.current_page = page
        self._update_pagination_style()
        if page == 1:
            self._render_grid(DESTINATIONS)
        else:
            for widget in self.grid_container.winfo_children():
                widget.destroy()
            tk.Label(self.grid_container, text="Belum ada destinasi lain di halaman ini.",
                     font=("Segoe UI", 10), bg=COLOR_BG, fg=COLOR_TEXT_GRAY).grid(
                row=0, column=0, columnspan=2, pady=30)

    # ----------------------------------------------------------
    def _select_destination(self, dest):
        self.selected_destination = dest
        self.jumlah_tiket.set(1)

        self.detail_title.config(text=dest["nama"])
        self.detail_subtitle.config(text=dest["desc"])

        self.info_labels["jam_buka"].config(text=dest["jam_buka"])
        self.info_labels["lokasi"].config(text=dest["lokasi"])
        self.info_labels["harga_tiket"].config(text=_format_rupiah(dest["harga"]))
        self.info_labels["fasilitas"].config(text=dest["fasilitas"])

        self.lanjut_btn.configure(state="normal", bg=COLOR_GREEN_DARK, fg=COLOR_WHITE,
                                   activebackground=COLOR_GREEN, activeforeground=COLOR_WHITE,
                                   cursor="hand2")

    def _increase_qty(self):
        self.jumlah_tiket.set(self.jumlah_tiket.get() + 1)

    def _decrease_qty(self):
        if self.jumlah_tiket.get() > 1:
            self.jumlah_tiket.set(self.jumlah_tiket.get() - 1)

    def _proceed_booking(self):
        if not self.selected_destination:
            messagebox.showwarning("Peringatan", "Pilih destinasi terlebih dahulu!")
            return
        if not DataStore.active_user:
            messagebox.showwarning("Peringatan", "Silakan login terlebih dahulu!")
            self.controller.show_frame("LoginFrame")
            return

        dest = self.selected_destination
        jumlah = self.jumlah_tiket.get()
        total_harga = dest["harga"] * jumlah
        kode = f"GT{random.randint(10**10, 10**11 - 1)}"

        DataStore.tickets.append({
            "username": DataStore.active_user,
            "destinasi": dest["nama"],
            "tanggal": "Hari ini",
            "jumlah": jumlah,
            "kode": kode,
            "harga": total_harga,
        })

        messagebox.showinfo(
            "Pemesanan Berhasil",
            f"Tiket {dest['nama']} x{jumlah} berhasil dipesan!\nKode Booking: {kode}",
        )

    # ----------------------------------------------------------
    def refresh(self):
        """Dipanggil otomatis oleh main_2.py tiap kali halaman ini dibuka."""
        pass