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
        
        tk.Button(header_frame, text="← Pembatalan Booking", bg=COLOR_BG, fg=COLOR_GREEN,
                 font=("Segoe UI", 16, "bold"), bd=0, relief="flat",
                 command=lambda: self.controller.show_frame("DashboardFrame")).pack(anchor="w")
        
        tk.Label(header_frame, text="Batalkan atau ubah pesanan dengan mudah",
                font=("Segoe UI", 11), bg=COLOR_BG, fg=COLOR_TEXT_GRAY).pack(anchor="w")
        
        # Content area untuk booking list
        self.content_frame = tk.Frame(self, bg=COLOR_BG)
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        self.refresh()
    
    def refresh(self):
        """Refresh dan tampilkan booking list"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get user bookings
        if not self.controller.active_user:
            tk.Label(self.content_frame, text="Silakan login terlebih dahulu",
                    font=("Segoe UI", 12), bg=COLOR_BG, fg=COLOR_TEXT_GRAY).pack(pady=50)
            return
        
        user_bookings = DataStore.get_user_bookings(self.controller.active_user)
        
        if not user_bookings:
            tk.Label(self.content_frame, text="Anda belum memiliki booking",
                    font=("Segoe UI", 12), bg=COLOR_BG, fg=COLOR_TEXT_GRAY).pack(pady=50)
            return
        
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
        
        # Display bookings
        for booking in user_bookings:
            self._create_booking_card(scrollable_frame, booking)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_booking_card(self, parent, booking):
        """Buat card untuk satu booking"""
        card = tk.Frame(parent, bg=COLOR_WHITE, highlightbackground=COLOR_BORDER,
                       highlightthickness=1)
        card.pack(fill="x", pady=10)
        
        content = tk.Frame(card, bg=COLOR_WHITE)
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Booking ID & Status
        header = tk.Frame(content, bg=COLOR_WHITE)
        header.pack(fill="x", pady=(0, 10))
        
        tk.Label(header, text=f"Kode Booking: {booking['id']}", font=("Segoe UI", 11, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(side="left")
        
        status_color = COLOR_GREEN if booking['status'] == 'confirmed' else COLOR_RED
        status_text = "✓ Dikonfirmasi" if booking['status'] == 'confirmed' else "✗ Dibatalkan"
        tk.Label(header, text=status_text, font=("Segoe UI", 10, "bold"),
                bg=COLOR_WHITE, fg=status_color).pack(side="right")
        
        # Item details
        if booking["type"] == "ticket":
            dest = DataStore.get_destination(booking["item_id"])
            if dest:
                tk.Label(content, text=f"🎫 {dest['nama']}", font=("Segoe UI", 11),
                        bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(anchor="w")
        else:
            homestay = DataStore.get_homestay(booking["item_id"])
            if homestay:
                tk.Label(content, text=f"🏠 {homestay['nama']}", font=("Segoe UI", 11),
                        bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(anchor="w")
        
        # Details
        detail_text = f"Tanggal: {booking['created_at']} | Qty: {booking['qty']} | Total: Rp {booking['total_price']:,}".replace(",", ".")
        tk.Label(content, text=detail_text, font=("Segoe UI", 9),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack(anchor="w", pady=(5, 10))
        
        # Buttons
        btn_frame = tk.Frame(content, bg=COLOR_WHITE)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        if booking['status'] == 'confirmed':
            tk.Button(btn_frame, text="Batalkan", bg=COLOR_RED, fg="white",
                     font=("Segoe UI", 9, "bold"), relief="flat",
                     command=lambda: self._confirm_cancellation(booking['id'])).pack(side="right", padx=(10, 0))
        
        tk.Button(btn_frame, text="Lihat Detail", bg=COLOR_GREEN, fg="white",
                 font=("Segoe UI", 9, "bold"), relief="flat",
                 command=lambda: self._show_detail(booking)).pack(side="right")
    
    def _confirm_cancellation(self, booking_id):
        """Tampilkan konfirmasi pembatalan"""
        booking = DataStore.get_booking(booking_id)
        if not booking:
            return
        
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
        
        # Item info
        if booking["type"] == "ticket":
            dest = DataStore.get_destination(booking["item_id"])
            item_name = dest['nama'] if dest else "Destinasi"
        else:
            homestay = DataStore.get_homestay(booking["item_id"])
            item_name = homestay['nama'] if homestay else "Homestay"
        
        tk.Label(content, text=item_name, font=("Segoe UI", 12, "bold"),
                bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(pady=5)
        tk.Label(content, text=f"Kode Booking: {booking_id}", font=("Segoe UI", 10),
                bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack()
        tk.Label(content, text=f"Total Pembayaran: Rp {booking['total_price']:,}".replace(",", "."),
                font=("Segoe UI", 11, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_DARK).pack(pady=10)
        
        tk.Label(content, text="Dana akan dikembalikan sesuai metode pembayaran",
                font=("Segoe UI", 9), bg=COLOR_WHITE, fg=COLOR_TEXT_GRAY).pack()
        
        # Buttons
        btn_frame = tk.Frame(content, bg=COLOR_WHITE)
        btn_frame.pack(fill="x", pady=30)
        
        def cancel():
            DataStore.cancel_booking(booking_id)
            messagebox.showinfo("Sukses", "Booking berhasil dibatalkan!\nDana akan dikembalikan dalam 3-5 hari kerja.")
            dialog.destroy()
            self.refresh()
        
        tk.Button(btn_frame, text="Ya, Batalkan", bg=COLOR_RED, fg="white",
                 font=("Segoe UI", 11, "bold"), width=15, relief="flat",
                 command=cancel).pack(side="right", padx=(10, 0))
        tk.Button(btn_frame, text="Tidak, Jangan", bg="#cccccc", fg="#333",
                 font=("Segoe UI", 11, "bold"), width=15, relief="flat",
                 command=dialog.destroy).pack(side="right")
    
    def _show_detail(self, booking):
        """Tampilkan detail booking"""
        booking_item = None
        if booking["type"] == "ticket":
            booking_item = DataStore.get_destination(booking["item_id"])
        else:
            booking_item = DataStore.get_homestay(booking["item_id"])
        
        if not booking_item:
            messagebox.showerror("Error", "Item tidak ditemukan")
            return
        
        message = f"""
Kode Booking: {booking['id']}
Tipe: {'Tiket Wisata' if booking['type'] == 'ticket' else 'Homestay'}
Nama: {booking_item['nama']}
Jumlah: {booking['qty']}
Total Harga: Rp {booking['total_price']:,}
Status: {booking['status']}
Tanggal Booking: {booking['created_at']}
        """.replace(",", ".")
        
        messagebox.showinfo("Detail Booking", message)