import tkinter as tk
from sidebar_common import build_sidebar

COLOR_BG = "#f7f8fa"
COLOR_BORDER = "#e6e8eb"
COLOR_GREEN_DARK = "#1f7a35"
COLOR_GREEN = "#2f9e44"
COLOR_GREEN_LIGHT = "#e8f5e9"
COLOR_TEXT_DARK = "#1a1a1a"
COLOR_TEXT_GRAY = "#6b7280"
COLOR_WHITE = "#ffffff"
COLOR_RED = "#e03131"
COLOR_GOLD = "#f5a623"
COLOR_BLUE = "#4a90d9"
COLOR_MAP_BG = "#eef1ef"
COLOR_MAP_PARK = "#dfeee1"
COLOR_MAP_RIVER = "#cfe3f2"

DESTINATIONS = [
    "Alun-Alun Kota Madiun", "Pahlawan Street Center", "Suncity Waterpark",
    "Wana Wisata Grape", "Cemoro Sewu", "Museum Kretek Madiun",
]
LOKASI_SAYA = ["Stasiun Madiun", "Terminal Purbaya", "Alun-Alun Kota Madiun"]

# Data rute contoh per destinasi (durasi & jarak perkiraan dari lokasi umum di Madiun)
ROUTE_INFO = {
    "Alun-Alun Kota Madiun": {"durasi": "15 menit", "jarak": "5.2 km"},
    "Pahlawan Street Center": {"durasi": "12 menit", "jarak": "4.0 km"},
    "Suncity Waterpark": {"durasi": "20 menit", "jarak": "7.8 km"},
    "Wana Wisata Grape": {"durasi": "35 menit", "jarak": "15.4 km"},
    "Cemoro Sewu": {"durasi": "40 menit", "jarak": "18.1 km"},
    "Museum Kretek Madiun": {"durasi": "14 menit", "jarak": "4.6 km"},
}

# Data cuaca contoh -- disamakan dengan widget cuaca di Beranda agar konsisten
WEATHER = {
    "suhu": "28\u00b0C", "kondisi": "Cerah", "kelembapan": "65%",
    "angin": "10 km/jam", "prakiraan": "Cerah sepanjang hari", "sumber": "BMKG",
}


class RouteFrame2(tk.Frame):
    """Halaman Cek Rute & Cuaca."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        build_sidebar(self, controller, active_frame_name="RouteFrame2")

        main = tk.Frame(self, bg=COLOR_BG)
        main.pack(side="left", fill="both", expand=True)

        content = tk.Frame(main, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=40, pady=40)

        self._build_header(content)

        body = tk.Frame(content, bg=COLOR_BG)
        body.pack(fill="both", expand=True, pady=(24, 0))

        self.destinasi_var = tk.StringVar(value=DESTINATIONS[0])
        self.lokasi_var = tk.StringVar(value=LOKASI_SAYA[0])

        self._build_map_panel(body)
        self._build_weather_panel(body)

        # Tampilkan rute default saat pertama kali dibuka
        self._update_route_display()

    # ----------------------------------------------------------
    def _build_header(self, parent):
        header = tk.Frame(parent, bg=COLOR_BG)
        header.pack(anchor="w", fill="x")

        icon_canvas = tk.Canvas(header, width=64, height=64, bg=COLOR_BG, highlightthickness=0)
        icon_canvas.grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 18))
        icon_canvas.create_oval(2, 2, 62, 62, fill=COLOR_GREEN_LIGHT, outline="")
        icon_canvas.create_text(32, 32, text="\U0001F9ED", font=("Segoe UI Emoji", 22))

        tk.Label(header, text="Cek Rute & Cuaca", font=("Segoe UI", 22, "bold"),
                 bg=COLOR_BG, fg=COLOR_TEXT_DARK, anchor="w").grid(row=0, column=1, sticky="w")
        tk.Label(header, text="Informasi rute ke tempat wisata dan cuaca terkini di Kota Madiun.",
                 font=("Segoe UI", 11), bg=COLOR_BG, fg=COLOR_TEXT_GRAY,
                 anchor="w").grid(row=1, column=1, sticky="w", pady=(2, 0))

    # ----------------------------------------------------------

    def _build_map_panel(self, parent):
        wrap = tk.Frame(parent, bg=COLOR_BG)
        wrap.pack(side="left", fill="both", expand=True, padx=(0, 20))

        map_frame = tk.Frame(wrap, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                              highlightthickness=1)
        map_frame.pack(fill="both", expand=True)

        self.map_canvas = tk.Canvas(map_frame, bg=COLOR_MAP_BG, highlightthickness=0)
        self.map_canvas.pack(fill="both", expand=True, padx=2, pady=2)
        self.map_canvas.bind("<Configure>", lambda e: self._draw_map())

        info_bar = tk.Frame(wrap, bg=COLOR_BG)
        info_bar.pack(fill="x", pady=(14, 0))
        tk.Label(info_bar, text="\U0001F551", font=("Segoe UI", 13), bg=COLOR_BG,
                 fg=COLOR_BLUE).pack(side="left", padx=(0, 8))
        self.durasi_label = tk.Label(info_bar, text="", font=("Segoe UI", 12, "bold"),
                                      bg=COLOR_BG, fg=COLOR_TEXT_DARK)
        self.durasi_label.pack(side="left")
        self.jarak_label = tk.Label(info_bar, text="", font=("Segoe UI", 10), bg=COLOR_BG,
                                     fg=COLOR_TEXT_GRAY)
        self.jarak_label.pack(side="left", padx=(6, 0))

    def _draw_map(self):
        canvas = self.map_canvas
        canvas.delete("all")
        w = canvas.winfo_width() or 500
        h = canvas.winfo_height() or 480
        if w < 10 or h < 10:
            return

        # Dekorasi latar peta: blok taman & sungai (bukan peta nyata, sekadar ilustrasi)
        canvas.create_rectangle(w * 0.05, h * 0.08, w * 0.35, h * 0.32,
                                 fill=COLOR_MAP_PARK, outline="")
        canvas.create_rectangle(w * 0.55, h * 0.55, w * 0.9, h * 0.8,
                                 fill=COLOR_MAP_PARK, outline="")
        canvas.create_line(w * 0.7, 0, w * 0.85, h * 0.35, w * 0.75, h * 0.7, w * 0.95, h,
                            fill=COLOR_MAP_RIVER, width=14, smooth=True)

        # Titik awal (bawah) & titik tujuan (atas)
        start_x, start_y = w * 0.52, h * 0.85
        end_x, end_y = w * 0.6, h * 0.12

        # Garis rute zig-zag hijau
        points = [
            start_x, start_y,
            start_x - 15, h * 0.62,
            start_x + 25, h * 0.5,
            end_x - 10, h * 0.32,
            end_x, end_y,
        ]
        canvas.create_line(*points, fill=COLOR_GREEN, width=4, smooth=True)

        # Marker awal (lingkaran hijau berlubang)
        canvas.create_oval(start_x - 8, start_y - 8, start_x + 8, start_y + 8,
                            fill=COLOR_WHITE, outline=COLOR_GREEN, width=3)
        canvas.create_oval(start_x - 3, start_y - 3, start_x + 3, start_y + 3,
                            fill=COLOR_BLUE, outline="")

        # Marker tujuan (pin merah)
        canvas.create_oval(end_x - 10, end_y - 10, end_x + 10, end_y + 10,
                            fill=COLOR_RED, outline="")
        canvas.create_polygon(end_x - 8, end_y + 4, end_x + 8, end_y + 4, end_x, end_y + 20,
                               fill=COLOR_RED, outline="")
        canvas.create_oval(end_x - 4, end_y - 4, end_x + 4, end_y + 4, fill=COLOR_WHITE,
                            outline="")

        canvas.create_text(end_x + 14, end_y, text=self.destinasi_var.get(),
                            font=("Segoe UI", 10, "bold"), fill=COLOR_TEXT_DARK, anchor="w",
                            width=140)

    # ----------------------------------------------------------
    def _build_weather_panel(self, parent):
        panel = tk.Frame(parent, bg=COLOR_WHITE, width=260,
                          highlightbackground=COLOR_BORDER, highlightthickness=1)
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)

        inner = tk.Frame(panel, bg=COLOR_WHITE)
        inner.pack(fill="both", padx=20, pady=22)

        tk.Label(inner, text="Cuaca Saat Ini", font=("Segoe UI", 12, "bold"), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK, anchor="w").pack(anchor="w", pady=(0, 14))

        top_row = tk.Frame(inner, bg=COLOR_WHITE)
        top_row.pack(anchor="w")
        tk.Label(top_row, text="\u2600", font=("Segoe UI", 28), bg=COLOR_WHITE,
                 fg=COLOR_GOLD).pack(side="left", padx=(0, 12))
        temp_wrap = tk.Frame(top_row, bg=COLOR_WHITE)
        temp_wrap.pack(side="left")
        tk.Label(temp_wrap, text=WEATHER["suhu"], font=("Segoe UI", 20, "bold"), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK).pack(anchor="w")
        tk.Label(temp_wrap, text=WEATHER["kondisi"], font=("Segoe UI", 10), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY).pack(anchor="w")

        tk.Frame(inner, bg=COLOR_BORDER, height=1).pack(fill="x", pady=16)

        self._weather_row(inner, "Kelembapan", WEATHER["kelembapan"])
        self._weather_row(inner, "Kecepatan Angin", WEATHER["angin"])

        tk.Label(inner, text="Prakiraan", font=("Segoe UI", 9, "bold"), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK, anchor="w").pack(anchor="w", pady=(16, 2))
        tk.Label(inner, text=WEATHER["prakiraan"], font=("Segoe UI", 9), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY, anchor="w").pack(anchor="w")

        tk.Label(inner, text=f"Sumber: {WEATHER['sumber']}", font=("Segoe UI", 8),
                 bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY, anchor="w").pack(anchor="w", pady=(24, 0))

    def _weather_row(self, parent, label, value):
        row = tk.Frame(parent, bg=COLOR_WHITE)
        row.pack(fill="x", pady=4)
        tk.Label(row, text=label, font=("Segoe UI", 9), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY, anchor="w").pack(side="left")
        tk.Label(row, text=value, font=("Segoe UI", 9, "bold"), bg=COLOR_WHITE,
                 fg=COLOR_GREEN_DARK, anchor="e").pack(side="right")

    # ----------------------------------------------------------
    def _update_route_display(self):
        dest = self.destinasi_var.get()
        info = ROUTE_INFO.get(dest, {"durasi": "-", "jarak": "-"})
        self.durasi_label.config(text=info["durasi"])
        self.jarak_label.config(text=f"({info['jarak']})")
        self._draw_map()

    def refresh(self):
        """Dipanggil otomatis oleh main_2.py tiap kali halaman ini dibuka."""
        self._update_route_display()