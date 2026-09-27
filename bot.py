# xaloAC-x410m1s0
"""
Discord Otomatik Cevap Self-Botu - Ana Modül
Güvenli, rate-limit uyumlu, modüler yapı
"""

import asyncio
import random
import logging
from typing import Optional

import discord

from config import (
    DM_COOLDOWN,
    MENTION_COOLDOWN,
    GLOBAL_COOLDOWN,
    DM_DELAY_MIN,
    DM_DELAY_MAX,
    MENTION_DELAY_MIN,
    MENTION_DELAY_MAX,
    MAX_MENTIONS,
    ALLOWED_GUILD_IDS,
    DM_REPLIES,
    MENTION_REPLIES,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)
logger = logging.getLogger("selfbot")


class SafeSelfBot(discord.Client):
    """Rate-limit korumalı, cooldown sistemli self-bot."""

    def __init__(self) -> None:
        # discord.py-self 2.x otomatik yönetir
        super().__init__()

        self._dm_last_reply: dict[int, float] = {}
        self._mention_last_reply: dict[int, float] = {}
        self._last_global_reply: float = 0.0
        self._processed_messages: set[int] = set()

    async def on_ready(self) -> None:
        logger.info("Bot başarıyla bağlandı.")
        logger.info("Otomatik cevap sistemi aktif.")

    async def on_connect(self) -> None:
        logger.info("Bot başlatılıyor...")

    def _is_global_cooldown(self) -> bool:
        elapsed = asyncio.get_event_loop().time() - self._last_global_reply
        return elapsed < GLOBAL_COOLDOWN

    def _is_user_cooldown(
        self, user_id: int, cooldown_map: dict[int, float], cooldown_seconds: float
    ) -> bool:
        last_time = cooldown_map.get(user_id, 0.0)
        elapsed = asyncio.get_event_loop().time() - last_time
        return elapsed < cooldown_seconds

    def _update_cooldown(self, user_id: int, cooldown_map: dict[int, float]) -> None:
        cooldown_map[user_id] = asyncio.get_event_loop().time()

    def _update_global_cooldown(self) -> None:
        self._last_global_reply = asyncio.get_event_loop().time()

    def _should_ignore_message(self, message: discord.Message) -> bool:
        if message.author.id == self.user.id:
            return True
        if message.author.bot:
            return True
        if message.webhook_id is not None:
            return True
        if message.id in self._processed_messages:
            return True
        return False

    async def _safe_typing_and_wait(
        self, channel: discord.abc.Messageable, delay_min: float, delay_max: float
    ) -> None:
        delay = random.uniform(delay_min, delay_max)
        try:
            async with channel.typing():
                await asyncio.sleep(min(delay, 5.0))
        except (discord.Forbidden, discord.HTTPException):
            await asyncio.sleep(delay)

    async def _handle_dm(self, message: discord.Message) -> None:
        user_id = message.author.id

        if self._is_user_cooldown(user_id, self._dm_last_reply, DM_COOLDOWN):
            return
        if self._is_global_cooldown():
            return

        reply = random.choice(DM_REPLIES)
        await self._safe_typing_and_wait(message.channel, DM_DELAY_MIN, DM_DELAY_MAX)

        try:
            await message.channel.send(reply)
            self._update_cooldown(user_id, self._dm_last_reply)
            self._update_global_cooldown()
            self._processed_messages.add(message.id)
        except discord.HTTPException as e:
            logger.error(f"DM cevap hatası (HTTP): {e.status}")

    async def _handle_mention(self, message: discord.Message) -> None:
        user_id = message.author.id

        if message.guild is not None and ALLOWED_GUILD_IDS and message.guild.id not in ALLOWED_GUILD_IDS:
            return

        if len(message.mentions) >= MAX_MENTIONS:
            return
        if self._is_user_cooldown(user_id, self._mention_last_reply, MENTION_COOLDOWN):
            return
        if self._is_global_cooldown():
            return

        reply = random.choice(MENTION_REPLIES)
        await self._safe_typing_and_wait(
            message.channel, MENTION_DELAY_MIN, MENTION_DELAY_MAX
        )

        try:
            await message.reply(reply)
            self._update_cooldown(user_id, self._mention_last_reply)
            self._update_global_cooldown()
            self._processed_messages.add(message.id)
        except discord.HTTPException as e:
            logger.error(f"Mention cevap hatası (HTTP): {e.status}")

    async def on_message(self, message: discord.Message) -> None:
        if self._should_ignore_message(message):
            return

        if isinstance(message.channel, discord.DMChannel):
            await self._handle_dm(message)
            return

        if self.user in message.mentions:
            await self._handle_mention(message)

    async def on_error(self, event: str, *args, **kwargs) -> None:
        logger.error(f"Beklenmeyen hata: {event}")


def run_bot(token: str) -> None:
    if not token:
        logger.error("Bot başlatılamadı: Token bulunamadı.")
        return

    bot = SafeSelfBot()
    try:
        bot.run(token, log_handler=None)
    except discord.LoginFailure:
        logger.error("Bot başlatılamadı: Discord kimlik doğrulaması başarısız.")
    except discord.HTTPException:
        logger.error("Bot başlatılamadı: Discord API bağlantı hatası.")
    except Exception:
        logger.error("Bot başlatılamadı: Beklenmeyen bir hata oluştu.")