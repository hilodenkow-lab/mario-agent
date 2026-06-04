import asyncio
from playwright.async_api import async_playwright

async def jalankan_browser(perintah_url):
	print(f"[TANGAN] membuka browser untuk menuju ke: {perintah_url}")

	async with async_playwright() as p:

		browser = await p.chromium.launch(headless=False)
		page = await browser.new_page()

		await page.goto(perintah_url)

		judul_web = await page.title()
		print(f"[TANGAN] sukses membuka: {judul_web}")

		await asyncio.sleep(5)
		await browser.close()

		return judul_web

async def main():
    # Menguji fungsi yang kita buat di atas
    hasil = await jalankan_browser("https://google.com")
    print(f"[MAIN] Laporan dari modul tangan: {hasil}")

if __name__ == "__main__":
    # Menjalankan fungsi asynchronous 'main' lewat generator asyncio
    asyncio.run(main())