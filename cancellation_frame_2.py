import tkinter as tk
from tkinter import ttk, messagebox
from data_store_2 import DataStore
from scroll_utils import enable_mousewheel_scroll

# Warna tema (di-inline langsung di file ini, tidak lagi dari colors.py)
COLOR_BG = "#f7f8fa"
COLOR_BORDER = "#e6e8eb"
COLOR_GREEN = "#2f9e44"
COLOR_RED = "#e03131"
COLOR_TEXT_DARK = "#1a1a1a"
COLOR_TEXT_GRAY = "#6b7280"
COLOR_WHITE = "#ffffff"


class CancellationFrame(tk.Frame):
    """Frame untuk pembatalan booking"""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.build_layout()

    def build_layout(self):
        """Membangun layout cancellation page"""
        # Back button & Title
        header_frame = tk.Frame(self, bg=COLOR_BG)
        header_frame.pack(fill="x", padx=30, pady=20)

        top_row = tk.Frame(header_frame, bg=COLOR_BG)
        top_row.pack(fill="x")

        tk.Button(top_row, text="← Pembatalan Booking", bg=COLOR_BG, fg=COLOR_GREEN,
                 font=("Segoe UI", 16, "bold"), bd=0, relief="flat",
                 command=lambda: self.controller.show_frame("DashboardFrame")).pack(side="left")

        tk.Button(top_row, text="🔄 Refresh", bg=COLOR_BG, fg=COLOR_TEXT_GRAY,
                 font=("Segoe UI", 9, "bold"), bd=0, relief="flat", cursor="hand2",
                 command=self.refresh).pack(side="right")

        tk.Label(header_frame, text="Batalkan atau lihat detail pesanan dengan mudah",
                font=("Segoe UI", 11), bg=COLOR_BG, fg=COLOR_TEXT_GRAY).pack(anchor="w")

        self.summary_label = tk.Label(header_frame, text="", font=("Segoe UI", 9, "bold"),
                                       bg=COLOR_BG, fg=COLOR_GREEN)
        self.summary_label.pack(anchor="w", pady=(6, 0))

        # Content area untuk booking list
        self.content_frame = tk.Frame(self, bg=COLOR_BG)
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        self.refresh()

    def _get_user_bookings(self):
        """Gabungkan tickets & homestays milik active_user jadi satu list booking
        dengan tag 'type' supaya bisa ditampilkan seragam."""
        username = self.controller.active_user
        bookings = []

        for t in DataStore.tickets:
            if t["username"] == username:
                bookings.append({"type": "ticket", "data": t})

        for h in DataStore.homestays:
            if h["username"] == username:
                bookings.append({"type": "homestay", "data": h})

        return bookings

    def refresh(self):
        """Refresh dan tampilkan booking list"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Get user bookings
        if not self.controller.active_user:
            self.summary_label.config(text="")
            tk.Label(self.content_frame, text="🔒", font=("Arial", 40),
                    bg=COLOR_BG).pack(pady=(60, 10))
            tk.Label(self.content_frame, text="Silakan login terlebih dahulu",
                    font=("Segoe UI", 12), bg=COLOR_BG, fg=COLOR_TEXT_GRAY).pack()
            return

        user_bookings = self._get_user_bookings()

        if not user_bookings:
            self.summary_label.config(text="")
            tk.Label(self.content_frame, text="📭", font=("Arial", 40),
                    bg=COLOR_BG).pack(pady=(60, 10))
            tk.Label(self.content_frame, text="Anda belum memiliki booking",
                    font=("Segoe UI", 12), bg=COLOR_BG, fg=COLOR_TEXT_GRAY).pack()
            return

        total_bookings = len(user_bookings)
        total_bayar = sum(b["data"]["harga"] for b in user_bookings)
        self.summary_label.config(
            text=f"{total_bookings} booking aktif  •  Total nilai: Rp {total_bayar:,}".replace(",", ".")
        )

        # Scrollable frame dengan scroll yang lebih baik
        canvas_frame = tk.Frame(self.content_frame, bg=COLOR_BG)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_BG)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind mousewheel untuk scroll yang lebih smooth (aman dipakai di banyak halaman)
        enable_mousewheel_scroll(canvas)

        # Display bookings (terbaru di atas)
        for booking in reversed(user_bookings):
            self._create_booking_card(scrollable_frame, booking)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _create_booking_card(self, parent, booking):
        """Buat card untuk satu booking (tiket atau homestay)"""
        btype = booking["type"]
        data = booking["data"]

        card = tk.Frame(parent, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                       highlightthickness=1)
        card.pack(fill="x", pady=10)

        content = tk.Frame(card, bg=COLOR_WHITE)
        content.pack(fill="both", expand=True, padx=15, pady=15)

        # Booking ID & jenis
        header = tk.Frame(content, bg=COLOR_WHITE)
        header.pack(fill="x", pady=(0, 10))

        tk.Label(header, text=f"Kode Booking: {data['kode']}", font=("Segoe UI", 11, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")

        jenis_text = "🎫 Tiket Wisata" if btype == "ticket" else "🏠 Homestay"
        tk.Label(header, text=jenis_text, font=("Segoe UI", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_GREEN).pack(side="right")

        # Item details
        if btype == "ticket":
            tk.Label(content, text=f"Destinasi: {data['destinasi']}", font=("Segoe UI", 11),
                    bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(anchor="w")
            detail_text = (f"Tanggal: {data['tanggal']} | Jumlah: {data['jumlah']} | "
                          f"Total: Rp {data['harga']:,}").replace(",", ".")
        else:
            tk.Label(content, text=f"Homestay: {data['nama_homestay']}", font=("Segoe UI", 11),
                    bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(anchor="w")
            detail_text = (f"Check-in: {data['checkin']} | Check-out: {data['checkout']} | "
                          f"Total: Rp {data['harga']:,}").replace(",", ".")

        tk.Label(content, text=detail_text, font=("Segoe UI", 9),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack(anchor="w", pady=(5, 10))

        # Buttons
        btn_frame = tk.Frame(content, bg=COLOR_WHITE)
        btn_frame.pack(fill="x", pady=(10, 0))

        bisa_dibatalkan = data["harga"] > 0

        if bisa_dibatalkan:
            tk.Button(btn_frame, text="Batalkan", bg=COLOR_RED, fg="white",
                     font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
                     command=lambda: self._confirm_cancellation(booking)).pack(side="right", padx=(10, 0))
        else:
            tk.Label(btn_frame, text="Gratis - tidak bisa dibatalkan", font=("Segoe UI", 8, "italic"),
                    bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack(side="right", padx=(10, 0))

        tk.Button(btn_frame, text="Lihat Detail", bg=COLOR_GREEN, fg="white",
                 font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
                 command=lambda: self._show_detail(booking)).pack(side="right")

    def _show_detail(self, booking):
        """Tampilkan detail lengkap booking"""
        btype = booking["type"]
        data = booking["data"]

        if btype == "ticket":
            message = f"""Kode Booking: {data['kode']}
Tipe: Tiket Wisata
Destinasi: {data['destinasi']}
Tanggal Kunjungan: {data['tanggal']}
Jumlah Tiket: {data['jumlah']}
Total Harga: Rp {data['harga']:,}
Status: {'Aktif' if data['harga'] > 0 else 'Aktif (Gratis)'}""".replace(",", ".")
        else:
            message = f"""Kode Booking: {data['kode']}
Tipe: Homestay
Nama Homestay: {data['nama_homestay']}
Alamat: {data['alamat']}
Check-in: {data['checkin']}
Check-out: {data['checkout']}
Total Harga: Rp {data['harga']:,}
Status: Aktif""".replace(",", ".")

        messagebox.showinfo("Detail Booking", message)

    def _confirm_cancellation(self, booking):
        """Tampilkan konfirmasi pembatalan"""
        btype = booking["type"]
        data = booking["data"]

        # Confirmation dialog
        dialog = tk.Toplevel(self)
        dialog.title("Konfirmasi Pembatalan")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Content
        content = tk.Frame(dialog, bg=COLOR_WHITE)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Icon
        tk.Label(content, text="❌", font=("Arial", 50),
                bg=COLOR_WHITE).pack(pady=20)

        tk.Label(content, text="Batalkan Booking Ini?", font=("Segoe UI", 16, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack()

        item_name = data["destinasi"] if btype == "ticket" else data["nama_homestay"]

        tk.Label(content, text=item_name, font=("Segoe UI", 12, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(pady=5)
        tk.Label(content, text=f"Kode Booking: {data['kode']}", font=("Segoe UI", 10),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack()
        tk.Label(content, text=f"Total Pembayaran: Rp {data['harga']:,}".replace(",", "."),
                font=("Segoe UI", 11, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(pady=10)

        tk.Label(content, text="Dana akan dikembalikan sesuai metode pembayaran",
                font=("Segoe UI", 9), bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack()

        # Buttons
        btn_frame = tk.Frame(content, bg=COLOR_WHITE)
        btn_frame.pack(fill="x", pady=30)

        def cancel():
            if btype == "ticket" and data in DataStore.tickets:
                DataStore.tickets.remove(data)
            elif btype == "homestay" and data in DataStore.homestays:
                DataStore.homestays.remove(data)

            messagebox.showinfo("Sukses", "Booking berhasil dibatalkan!\nDana akan dikembalikan dalam 3-5 hari kerja.")
            dialog.destroy()
            self.refresh()

        tk.Button(btn_frame, text="Ya, Batalkan", bg=COLOR_RED, fg="white",
                 font=("Segoe UI", 11, "bold"), width=15, relief="flat", cursor="hand2",
                 command=cancel).pack(side="right", padx=(10, 0))
        tk.Button(btn_frame, text="Tidak, Jangan", bg="#cccccc", fg="#333",
                 font=("Segoe UI", 11, "bold"), width=15, relief="flat", cursor="hand2",
                 command=dialog.destroy).pack(side="right")