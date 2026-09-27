# xaloAC-x410m1s0
"""
Discord Otomatik Cevap Self-Botu - Yapılandırma
"""

import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "token buraya örnek MTUwOTk5NzM2NDAyMTE2NjI5Mg...")

# Cooldown (saniye)
DM_COOLDOWN: int = 30
MENTION_COOLDOWN: int = 15
GLOBAL_COOLDOWN: int = 2

# Gecikme (saniye)
DM_DELAY_MIN: float = 3.0
DM_DELAY_MAX: float = 6.0
MENTION_DELAY_MIN: float = 6.0
MENTION_DELAY_MAX: float = 6.0

# Spam koruması
MAX_MENTIONS: int = 3

# Sunucu whitelist (boş = tüm sunucularda çalışır)
ALLOWED_GUILD_IDS: list[int] = []

# Cevaplar
DM_REPLIES: list[str] = [
    "Yazma la bi dur yarram",
    "Bi dur amk işim var",

]

MENTION_REPLIES: list[str] = [
    "müsait değilim brrreemin aliminyumfolyo bekle yazacam",
    "etiketini gördüm, az sonra bakıyorum",
    "gördüm, birazdan ilgilenicem",
    "yazdığını okudum, dönüş yapıcam",
    "şimdi denk geldi, 5dk sonra dönerim",
    "not aldım, birazdan cevap vericem",
]