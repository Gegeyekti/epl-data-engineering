from pathlib import Path
import os
import time
import requests
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_PATH = DATA_DIR / "E0.csv"

load_dotenv(PROJECT_DIR / ".env")

CSV_URL = os.getenv("EPL_CSV_URL")

if not CSV_URL:
    raise ValueError(
        "EPL_CSV_URL belum diatur dalam .env"
    )


def download_csv(url, attempts=3):
    for attempt in range(1, attempts + 1):
        try:
            print(f"Mengunduh CSV ({attempt}/{attempts})...")

            response = requests.get(
                url,
                timeout=(15, 60),
                headers={"User-Agent": "Mozilla/5.0"}
            )
            response.raise_for_status()

            if not response.content.strip():
                raise ValueError("CSV yang diunduh kosong.")

            first_line = response.content.splitlines()[0].decode(
                "utf-8-sig", errors="replace"
            )
            if "," not in first_line:
                raise ValueError("Respons tidak tampak seperti CSV.")

            return response.content

        except (requests.RequestException, ValueError) as exc:
            print(f"Unduhan gagal: {exc}")

            if attempt < attempts:
                wait_seconds = 5 * attempt
                print(f"Mencoba lagi dalam {wait_seconds} detik...")
                time.sleep(wait_seconds)

    return None


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    content = download_csv(CSV_URL)

    if content is not None:
        temp_path = OUTPUT_PATH.with_suffix(".tmp")
        temp_path.write_bytes(content)
        temp_path.replace(OUTPUT_PATH)

        print("Berhasil mengunduh CSV terbaru.")
    elif OUTPUT_PATH.exists():
        print("Koneksi gagal. Menggunakan CSV lokal yang tersedia.")
        print("Pastikan file lokal tersebut adalah versi terbaru.")
    else:
        raise FileNotFoundError(
            f"Unduhan gagal dan file lokal tidak ditemukan: {OUTPUT_PATH}"
        )

    print(f"File input: {OUTPUT_PATH}")
    print(f"Ukuran file: {OUTPUT_PATH.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
