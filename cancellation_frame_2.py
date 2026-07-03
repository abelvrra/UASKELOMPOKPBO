import tkinter as tk
from tkinter import messagebox
from data_store_2 import DataStore
from sidebar_common import build_sidebar
from scroll_utils import enable_mousewheel_scroll

COLOR_BG = "#f7f8fa"
COLOR_BORDER = "#e6e8eb"
COLOR_GREEN_DARK = "#1f7a35"
COLOR_GREEN = "#2f9e44"
COLOR_GREEN_LIGHT = "#e8f5e9"
COLOR_TEXT_DARK = "#1a1a1a"
COLOR_TEXT_GRAY = "#6b7280"
COLOR_WHITE = "#ffffff"
COLOR_RED = "#e03131"
COLOR_RED_LIGHT = "#fdeaea"
COLOR_WARN_BG = "#fbeed4"
COLOR_WARN_BORDER = "#f0dcb0"


def _format_rupiah(angka):
    return "Rp " + f"{angka:,.0f}".replace(",", ".")


class BookingRow(tk.Frame):
    """Satu baris booking pada daftar Pembatalan (tiket wisata / homestay)."""

    def __init__(self, master, icon_char, title, subtitle, kode, harga,
                 cancellable, on_cancel=None, **kwargs):
        super().__init__(master, bg=COLOR_WHITE, **kwargs)

        content = tk.Frame(self, bg=COLOR_WHITE)
        content.pack(fill="x", padx=4, pady=18)
        content.grid_columnconfigure(1, weight=1)

        icon_canvas = tk.Canvas(content, width=64, height=64, bg=COLOR_WHITE,
                                 highlightthickness=0)
        icon_canvas.grid(row=0, column=0, rowspan=3, sticky="n", padx=(0, 18))
        icon_canvas.create_oval(2, 2, 62, 62, fill=COLOR_GREEN_LIGHT, outline="")
        icon_canvas.create_text(32, 32, text=icon_char, font=("Segoe UI Emoji", 20))

        tk.Label(content, text=title, font=("Segoe UI", 13, "bold"), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK, anchor="w").grid(row=0, column=1, sticky="w")
        tk.Label(content, text=subtitle, font=("Segoe UI", 10), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY, anchor="w").grid(row=1, column=1, sticky="w", pady=(3, 0))
        tk.Label(content, text=f"Kode Booking:  {kode}", font=("Segoe UI", 9), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY, anchor="w").grid(row=2, column=1, sticky="w", pady=(3, 0))

        right = tk.Frame(content, bg=COLOR_WHITE)
        right.grid(row=0, column=2, rowspan=3, sticky="e")

        tk.Label(right, text=_format_rupiah(harga), font=("Segoe UI", 13, "bold"),
                 bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, anchor="e").pack(anchor="e")

        if cancellable:
            tk.Button(
                right, text="Batalkan", font=("Segoe UI", 10, "bold"), bg=COLOR_WHITE,
                fg=COLOR_RED, highlightbackground=COLOR_RED, highlightthickness=1, bd=0,
                relief="flat", padx=16, pady=7, cursor="hand2",
                command=on_cancel if on_cancel else None,
            ).pack(anchor="e", pady=(8, 0))
        else:
            note = tk.Frame(right, bg="#eef0f2")
            note.pack(anchor="e", pady=(8, 0))
            tk.Label(note, text="Tiket dapat tidak\ndibatalkan.", font=("Segoe UI", 8),
                     bg="#eef0f2", fg=COLOR_TEXT_GRAY, justify="right",
                     padx=12, pady=8).pack()

        tk.Frame(self, bg=COLOR_BORDER, height=1).pack(fill="x", side="bottom")


class CancellationFrame(tk.Frame):
    """Halaman Pembatalan Booking dengan tab Tiket Wisata / Homestay."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.active_tab = "tiket"

        build_sidebar(self, controller, active_frame_name="CancellationFrame")

        main = tk.Frame(self, bg=COLOR_BG)
        main.pack(side="left", fill="both", expand=True)

        content = tk.Frame(main, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=40, pady=40)

        self._build_header(content)
        self._build_tabs(content)

        self.list_wrap = tk.Frame(content, bg=COLOR_BG)
        self.list_wrap.pack(fill="both", expand=True, pady=(0, 20))

        self._build_policy_box(content)

        self._render_list()

    # ----------------------------------------------------------
    def _build_header(self, parent):
        header = tk.Frame(parent, bg=COLOR_BG)
        header.pack(anchor="w", fill="x", pady=(0, 24))

        back_canvas = tk.Canvas(header, width=44, height=44, bg=COLOR_BG,
                                 highlightthickness=0, cursor="hand2")
        back_canvas.grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 16))
        back_canvas.create_oval(2, 2, 42, 42, fill=COLOR_GREEN_LIGHT, outline="")
        back_canvas.create_text(22, 22, text="\u2190", font=("Segoe UI", 15, "bold"),
                                 fill=COLOR_GREEN)
        back_canvas.bind("<Button-1>", lambda e: self.controller.show_frame("DashboardFrame"))

        tk.Label(header, text="Pembatalan Booking", font=("Segoe UI", 20, "bold"),
                 bg=COLOR_BG, fg=COLOR_TEXT_DARK, anchor="w").grid(row=0, column=1, sticky="w")
        tk.Label(header, text="Pilih booking yang ingin dibatalkan.", font=("Segoe UI", 11),
                 bg=COLOR_BG, fg=COLOR_TEXT_GRAY, anchor="w").grid(row=1, column=1, sticky="w",
                                                                     pady=(2, 0))

    def _build_tabs(self, parent):
        tabs_frame = tk.Frame(parent, bg=COLOR_BG)
        tabs_frame.pack(anchor="w", fill="x", pady=(0, 4))

        self.tab_buttons = {}
        for key, label in (("tiket", "Tiket Wisata"), ("homestay", "Homestay")):
            wrap = tk.Frame(tabs_frame, bg=COLOR_BG)
            wrap.pack(side="left", padx=(0, 26))
            btn = tk.Label(wrap, text=label, font=("Segoe UI", 12, "bold"), bg=COLOR_BG,
                            fg=COLOR_TEXT_GRAY, cursor="hand2")
            btn.pack()
            underline = tk.Frame(wrap, bg=COLOR_BG, height=3)
            underline.pack(fill="x", pady=(6, 0))
            btn.bind("<Button-1>", lambda e, k=key: self._switch_tab(k))
            self.tab_buttons[key] = (btn, underline)

        tk.Frame(parent, bg=COLOR_BORDER, height=1).pack(fill="x", pady=(0, 4))
        self._update_tab_style()

    def _update_tab_style(self):
        for key, (btn, underline) in self.tab_buttons.items():
            if key == self.active_tab:
                btn.configure(fg=COLOR_GREEN_DARK)
                underline.configure(bg=COLOR_GREEN_DARK)
            else:
                btn.configure(fg=COLOR_TEXT_GRAY)
                underline.configure(bg=COLOR_BG)

    def _switch_tab(self, key):
        self.active_tab = key
        self._update_tab_style()
        self._render_list()

    # ----------------------------------------------------------
    def _build_policy_box(self, parent):
        box = tk.Frame(parent, bg=COLOR_GREEN_LIGHT)
        box.pack(fill="x")
        inner = tk.Frame(box, bg=COLOR_GREEN_LIGHT)
        inner.pack(fill="x", padx=24, pady=18)
        tk.Label(inner, text="Kebijakan Pembatalan", font=("Segoe UI", 11, "bold"),
                 bg=COLOR_GREEN_LIGHT, fg=COLOR_TEXT_DARK, anchor="w").pack(anchor="w")
        tk.Label(inner, text="Pembatalan dapat dilakukan maksimal 1 hari sebelum kunjungan.",
                 font=("Segoe UI", 9), bg=COLOR_GREEN_LIGHT, fg=COLOR_TEXT_GRAY,
                 anchor="w").pack(anchor="w", pady=(4, 0))

    # ----------------------------------------------------------
    def _render_list(self):
        for widget in self.list_wrap.winfo_children():
            widget.destroy()

        card = tk.Frame(self.list_wrap, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                         highlightthickness=1)
        card.pack(fill="both", expand=True)

        canvas = tk.Canvas(card, bg=COLOR_WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(card, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=COLOR_WHITE)

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        scrollbar.pack(side="right", fill="y")

        enable_mousewheel_scroll(canvas)

        username = DataStore.active_user
        if self.active_tab == "tiket":
            items = [t for t in DataStore.tickets if t["username"] == username]
        else:
            items = [h for h in DataStore.homestays if h["username"] == username]

        if not items:
            tk.Label(inner, text="Belum ada booking di kategori ini.", font=("Segoe UI", 10),
                     bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack(pady=40)
            return

        for item in items:
            if self.active_tab == "tiket":
                subtitle = f"{item['tanggal']}   \u2022   {item['jumlah']} Tiket"
                row = BookingRow(
                    inner, "\U0001F3AB", item["destinasi"], subtitle, item["kode"],
                    item["harga"], cancellable=(item["harga"] > 0),
                    on_cancel=lambda it=item: self._confirm_cancel_ticket(it),
                )
            else:
                subtitle = f"{item.get('checkin', '-')} \u2013 {item.get('checkout', '-')}"
                row = BookingRow(
                    inner, "\U0001F3E0", item["nama_homestay"], subtitle,
                    item.get("kode", "-"), item["harga"], cancellable=True,
                    on_cancel=lambda it=item: self._confirm_cancel_homestay(it),
                )
            row.pack(fill="x")

    # ----------------------------------------------------------
    def _confirm_cancel_ticket(self, item):
        subtitle = f"{item['tanggal']}  \u2022  {item['jumlah']} Tiket"
        self._open_confirm_dialog(
            title=item["destinasi"], subtitle=subtitle, kode=item["kode"],
            total=item["harga"],
            on_confirm=lambda: self._do_cancel(DataStore.tickets, item),
        )

    def _confirm_cancel_homestay(self, item):
        subtitle = f"{item.get('checkin', '-')} \u2013 {item.get('checkout', '-')}"
        self._open_confirm_dialog(
            title=item["nama_homestay"], subtitle=subtitle, kode=item.get("kode", "-"),
            total=item["harga"],
            on_confirm=lambda: self._do_cancel(DataStore.homestays, item),
        )

    def _open_confirm_dialog(self, title, subtitle, kode, total, on_confirm):
        popup = tk.Toplevel(self)
        popup.title("Konfirmasi Pembatalan")
        popup.configure(bg=COLOR_BG)
        popup.resizable(False, False)
        popup.transient(self.winfo_toplevel())

        # Posisikan di tengah jendela utama
        w, h = 520, 560
        root = self.winfo_toplevel()
        root.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (w // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")
        popup.grab_set()

        tk.Label(popup, text="Konfirmasi Pembatalan", font=("Segoe UI", 16, "bold"),
                 bg=COLOR_BG, fg=COLOR_TEXT_DARK).pack(pady=(28, 20))

        card = tk.Frame(popup, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                         highlightthickness=1)
        card.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        inner = tk.Frame(card, bg=COLOR_WHITE)
        inner.pack(expand=True, pady=30, padx=30)

        icon_canvas = tk.Canvas(inner, width=100, height=100, bg=COLOR_WHITE,
                                 highlightthickness=0)
        icon_canvas.pack(pady=(0, 18))
        icon_canvas.create_oval(4, 4, 96, 96, fill=COLOR_RED_LIGHT, outline="")
        icon_canvas.create_line(35, 35, 65, 65, fill=COLOR_RED, width=6, capstyle="round")
        icon_canvas.create_line(65, 35, 35, 65, fill=COLOR_RED, width=6, capstyle="round")

        tk.Label(inner, text="Batalkan Booking Ini?", font=("Segoe UI", 17, "bold"),
                 bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(pady=(0, 14))

        tk.Label(inner, text=title, font=("Segoe UI", 12, "bold"), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_DARK).pack()
        tk.Label(inner, text=subtitle, font=("Segoe UI", 10), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY).pack(pady=(2, 2))
        tk.Label(inner, text=f"Kode Booking: {kode}", font=("Segoe UI", 10), bg=COLOR_WHITE,
                 fg=COLOR_TEXT_GRAY).pack(pady=(0, 18))

        warn_box = tk.Frame(inner, bg=COLOR_WARN_BG, highlightbackground=COLOR_WARN_BORDER,
                             highlightthickness=1)
        warn_box.pack(fill="x", pady=(0, 22))
        warn_inner = tk.Frame(warn_box, bg=COLOR_WARN_BG)
        warn_inner.pack(fill="x", padx=18, pady=14)

        top_row = tk.Frame(warn_inner, bg=COLOR_WARN_BG)
        top_row.pack(fill="x")
        tk.Label(top_row, text="Total Pembayaran", font=("Segoe UI", 10, "bold"),
                 bg=COLOR_WARN_BG, fg=COLOR_TEXT_DARK, anchor="w").pack(side="left")
        tk.Label(top_row, text=_format_rupiah(total), font=("Segoe UI", 11, "bold"),
                 bg=COLOR_WARN_BG, fg=COLOR_TEXT_DARK, anchor="e").pack(side="right")
        tk.Label(warn_inner, text="Dana akan dikembalikan sesuai metode pembayaran.",
                 font=("Segoe UI", 9), bg=COLOR_WARN_BG, fg=COLOR_TEXT_GRAY,
                 anchor="w", justify="left", wraplength=380).pack(anchor="w", pady=(8, 0))

        btn_row = tk.Frame(inner, bg=COLOR_WHITE)
        btn_row.pack(fill="x")
        btn_row.grid_columnconfigure(0, weight=1)
        btn_row.grid_columnconfigure(1, weight=1)

        tk.Button(
            btn_row, text="Kembali", font=("Segoe UI", 11, "bold"), bg=COLOR_WHITE,
            fg=COLOR_GREEN_DARK, highlightbackground=COLOR_GREEN_DARK, highlightthickness=1,
            bd=0, relief="flat", pady=12, cursor="hand2", command=popup.destroy,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        def _confirm_and_close():
            popup.destroy()
            on_confirm()

        tk.Button(
            btn_row, text="Ya, Batalkan", font=("Segoe UI", 11, "bold"), bg=COLOR_RED,
            fg=COLOR_WHITE, activebackground="#c92a2a", activeforeground=COLOR_WHITE,
            relief="flat", pady=12, cursor="hand2", command=_confirm_and_close,
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

    def _do_cancel(self, data_list, item):
        if item in data_list:
            data_list.remove(item)
        messagebox.showinfo("Berhasil", "Booking berhasil dibatalkan.")
        self._render_list()

    # ----------------------------------------------------------
    def refresh(self):
        """Dipanggil otomatis oleh main_2.py tiap kali halaman ini dibuka."""
        self._render_list()