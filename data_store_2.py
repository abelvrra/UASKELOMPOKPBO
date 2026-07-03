class DataStore:
    """
    Penyimpanan data sederhana di memori (in-memory) untuk seluruh aplikasi.

    Struktur item tickets  : {"username", "destinasi", "tanggal", "jumlah", "kode", "harga"}
      - harga = TOTAL harga tiket (bukan per-orang), Rp 0 berarti tiket gratis
      - tiket dengan harga Rp 0 tidak bisa dibatalkan (lihat cancellation_frame_2.py)

    Struktur item homestays: {"username", "nama_homestay", "alamat", "harga",
                               "checkin", "checkout", "kode"}
      - harga = harga per malam
    """

    users = {"admin": "123"}
    active_user = None

    # Data contoh (seed) supaya saat login sebagai 'admin', halaman
    # Pembatalan Booking langsung terisi seperti pada desain.
    tickets = [
        {"username": "admin", "destinasi": "Suncity Waterpark", "tanggal": "20 Mei 2024",
         "jumlah": 2, "kode": "GT24052000123", "harga": 70000},
        {"username": "admin", "destinasi": "Wana Wisata Grape", "tanggal": "18 Mei 2024",
         "jumlah": 1, "kode": "GT24051800098", "harga": 10000},
        {"username": "admin", "destinasi": "Pahlawan Street Center", "tanggal": "10 Mei 2024",
         "jumlah": 2, "kode": "GT24051000077", "harga": 0},
    ]

    homestays = [
        {"username": "admin", "nama_homestay": "Homestay Madiun City",
         "alamat": "Jl. Pahlawan No. 45, Madiun", "harga": 200000,
         "checkin": "20/05/2024", "checkout": "21/05/2024", "kode": "GTH24052000001"},
    ]