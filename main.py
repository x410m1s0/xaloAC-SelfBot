# xaloAC-x410m1s0
"""
Discord Otomatik Cevap Self-Botu - Başlatıcı
"""

from bot import run_bot
from config import DISCORD_TOKEN

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("[HATA] Token bulunamadı.")
        print("Lütfen .env dosyasına token'ınızı ekleyin.")
        exit(1)

    run_bot(DISCORD_TOKEN)