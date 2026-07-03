"""
sidebar_common.py
Komponen sidebar navigasi yang dipakai bersama oleh semua halaman
(DashboardFrame, TicketFrame, HomestayFrame, RouteFrame2, CancellationFrame).

Dibuat sebagai modul terpisah supaya sidebar tidak perlu ditulis ulang di
setiap file frame -- ini juga yang menyebabkan bug duplikasi method
_on_nav_click sebelumnya. Palet warna SENGAJA disamakan dengan
dashboard_frame_2.py supaya semua halaman terasa satu kesatuan.
"""

import tkinter as tk

COLOR_SIDEBAR = "#ffffff"
COLOR_BORDER = "#e6e8eb"
COLOR_GREEN_DARK = "#1f7a35"
COLOR_GREEN = "#2f9e44"
COLOR_GREEN_LIGHT = "#e8f5e9"
COLOR_TEXT_DARK = "#1a1a1a"
COLOR_TEXT_GRAY = "#6b7280"
COLOR_RED = "#e03131"

# (icon, label, frame_name_di_main_2)
MENU_ITEMS = [
    ("\U0001F3E0", "Beranda", "DashboardFrame"),
    ("\U0001F3AB", "Beli Tiket Wisata", "TicketFrame"),
    ("\U0001F3E1", "Booking Homestay", "HomestayFrame"),
    ("\U0001F5FA", "Cek Rute & Cuaca", "RouteFrame2"),
    ("\u2716", "Pembatalan Booking", "CancellationFrame"),
]


class SidebarItem(tk.Frame):
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


def build_sidebar(parent_frame, controller, active_frame_name):
    """Bangun sidebar lengkap (logo + menu + logout) di dalam parent_frame.
    active_frame_name: nama frame (sesuai key di main_2.py) yang sedang aktif,
    mis. "TicketFrame", supaya menu terkait ter-highlight otomatis."""
    sidebar = tk.Frame(parent_frame, bg=COLOR_SIDEBAR, width=270,
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

    for icon, label, frame_name in MENU_ITEMS:
        item = SidebarItem(
            nav_frame, icon, label, active=(frame_name == active_frame_name),
            command=lambda fn=frame_name: controller.show_frame(fn),
        )
        item.pack(fill="x", pady=3)

    logout_frame = tk.Frame(sidebar, bg=COLOR_SIDEBAR)
    logout_frame.pack(side="bottom", fill="x", padx=12, pady=30)

    def _do_logout():
        if hasattr(controller, "logout_action"):
            controller.logout_action()
        else:
            controller.show_frame("LoginFrame")

    logout_item = SidebarItem(
        logout_frame, "\u2192", "Logout", danger=True,
        command=_do_logout,
    )
    logout_item.pack(fill="x")

    return sidebar