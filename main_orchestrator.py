import time
from playwright.sync_api import sync_playwright, Page, BrowserContext
from agent_brain import pikirkan_perintah

# ─────────────────────────────────────────────
#  State global — satu instance browser buat
#  seluruh sesi Streamlit
# ─────────────────────────────────────────────
_playwright  = None
_context: BrowserContext = None
_page: Page  = None

def _pastikan_browser_hidup():
    """Nyalain browser kalau belum jalan."""
    global _playwright, _context, _page

    if _page is not None:
        return  # sudah hidup

    print("[MARIO] Meluncurkan browser...")
    _playwright = sync_playwright().start()
    _context = _playwright.chromium.launch_persistent_context(
        user_data_dir="./user_data",
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )
    _page = _context.new_page()
    print("[MARIO] Browser siap.")

def _baca_halaman() -> str:
    """Ambil teks halaman yang lagi kebuka (maks 4000 karakter)."""
    try:
        return _page.locator("body").inner_text()[:4000]
    except Exception:
        return "Browser baru dibuka, belum ada halaman aktif."

def _perbaiki_url(url: str) -> str:
    """Pastiin URL punya skema http/https."""
    if url.startswith("www."):
        return "https://" + url
    if not url.startswith("http"):
        return f"https://www.google.com/search?q={url}"
    return url

# ─────────────────────────────────────────────
#  FUNGSI UTAMA — dipanggil dari app_ui.py
# ─────────────────────────────────────────────
def jalankan_perintah(perintah: str) -> str:
    """
    Terima perintah teks dari UI, proses lewat Gemini,
    eksekusi di browser, kembalikan laporan ke UI.

    Returns:
        str — teks laporan yang ditampilkan di chat bubble
    """
    _pastikan_browser_hidup()

    # 1. Baca konteks halaman saat ini
    konteks = _baca_halaman()

    # 2. Tanya Gemini (retry 3x kalau 503)
    hasil_otak = None
    for percobaan in range(3):
        try:
            print(f"[MARIO] Menghubungi Gemini... (percobaan {percobaan+1}/3)")
            hasil_otak = pikirkan_perintah(perintah, konteks)
            break
        except Exception as e:
            if "503" in str(e) and percobaan < 2:
                print("[MARIO] Gemini sibuk, coba lagi dalam 2 detik...")
                time.sleep(2)
            else:
                return f"Gemini error: {e}"

    if not hasil_otak:
        return "Tidak bisa menghubungi Gemini setelah 3 percobaan."

    # 3. Navigasi browser
    url = _perbaiki_url(hasil_otak.url_tujuan)
    print(f"[MARIO] Menuju → {url}")

    try:
        _page.goto(url, timeout=15000)
        judul = _page.title()
        return (
            f"Oke, gw udah buka **{judul}**\n\n"
            f"Alasan: {hasil_otak.alasan}\n"
            f"URL: {url}"
        )
    except Exception as e:
        return f"Gagal navigasi ke {url}: {e}"

def tutup_browser():
    """Panggil ini waktu app Streamlit ditutup."""
    global _playwright, _context, _page
    try:
        if _context:
            _context.close()
        if _playwright:
            _playwright.stop()
    except Exception:
        pass
    _playwright = _context = _page = None