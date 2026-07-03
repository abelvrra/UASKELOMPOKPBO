"""
scroll_utils.py
Helper untuk membuat area yang bisa di-scroll dengan mouse wheel, dipakai
bersama oleh ticket_frame_2.py dan homestay_frame_2.py.

Kenapa dibuat terpisah:
- Sebelumnya tiap halaman memakai canvas.bind_all("<MouseWheel>", ...).
  bind_all() itu GLOBAL untuk seluruh aplikasi, jadi kalau ada 2 halaman
  yang sama-sama melakukan ini, halaman yang dibuat PALING TERAKHIR akan
  menimpa binding halaman lain -- akibatnya scroll di halaman lain berhenti
  berfungsi.
- Fix di sini: mouse wheel hanya di-bind saat kursor benar-benar berada di
  atas canvas tsb (event <Enter>/<Leave>), dan langsung di-unbind saat
  kursor keluar. Jadi tidak ada dua canvas yang berebut binding global.
- Linux mengirim event <Button-4>/<Button-5> untuk scroll (bukan
  <MouseWheel> seperti Windows/Mac), jadi keduanya di-handle di sini
  supaya aplikasi tetap bisa di-scroll di platform manapun.
"""


def enable_mousewheel_scroll(canvas):
    """Aktifkan scroll mouse wheel pada `canvas` hanya saat kursor berada
    di atasnya. Aman dipakai di banyak halaman/canvas sekaligus."""

    def _on_mousewheel(event):
        if getattr(event, "num", None) == 4:          # Linux: scroll up
            canvas.yview_scroll(-1, "units")
        elif getattr(event, "num", None) == 5:          # Linux: scroll down
            canvas.yview_scroll(1, "units")
        elif getattr(event, "delta", 0):                # Windows / Mac
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)

    def _unbind(event):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", _bind)
    canvas.bind("<Leave>", _unbind)