# xaloAC-x410m1s0

# Discord Otomatik Cevap Self-Botu

DM ve mention mesajlarına otomatik cevap veren self-bot.

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Çalıştırma
bash
python bot.py
Ayarlar
Tüm ayarlar config.py içinde.

text

```text
main.py
python
from bot import run_bot
from config import DISCORD_TOKEN

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("[HATA] Token bulunamadı.")
        exit(1)
    run_bot(DISCORD_TOKEN)