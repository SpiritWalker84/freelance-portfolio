"""Заявки с главной витрины (GitHub Pages) → Telegram. Токен только на сервере."""

import os
import time
from collections import defaultdict

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")
_cors_raw = os.getenv("CORS_ORIGINS", "").strip()
CORS_ORIGINS = [o.strip() for o in _cors_raw.split(",") if o.strip()]

app = FastAPI(title="Portfolio Lead API")
if CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

_hits: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT = 8
RATE_WINDOW_SEC = 600


class LeadPayload(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    contact: str = Field(min_length=3, max_length=120)
    task: str = Field(min_length=3, max_length=2000)
    website: str = Field(default="", max_length=200)


def _rate_limit(ip: str) -> None:
    now = time.time()
    bucket = _hits[ip]
    _hits[ip] = [t for t in bucket if now - t < RATE_WINDOW_SEC]
    if len(_hits[ip]) >= RATE_LIMIT:
        raise HTTPException(429, "Слишком много запросов. Попробуйте позже.")
    _hits[ip].append(now)


async def _tg(text: str) -> None:
    if not BOT_TOKEN or not CHAT_ID:
        raise HTTPException(503, "Lead API не настроен")
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
        )
    if r.status_code != 200:
        raise HTTPException(502, "Telegram API error")


@app.get("/health")
async def health():
    return {"status": "ok", "telegram_configured": bool(BOT_TOKEN and CHAT_ID)}


@app.post("/api/portfolio-lead")
async def portfolio_lead(request: Request, payload: LeadPayload):
    if payload.website.strip():
        return {"ok": True}
    _rate_limit(request.client.host if request.client else "unknown")
    msg = (
        "🆕 Заявка с портфолио\n"
        f"Имя: {payload.name}\n"
        f"Контакт: {payload.contact}\n\n"
        f"Задача:\n{payload.task}"
    )
    await _tg(msg)
    return {"ok": True}
