"""Signed, short-lived delivery of a private image.

The file lives in ./private (git-ignored, not mounted as static) and is only
reachable through a time-limited signed URL that the page hands out. This keeps
it out of the repo, out of /static, out of crawlers' reach and out of caches.
It cannot stop a person who is looking at it from taking a screenshot.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import os
import re
import secrets
import time
from pathlib import Path
from typing import Mapping

PRIVATE_DIR = Path("private")
TTL_SECONDS = 6 * 60 * 60
HEADERS = {
    "Cache-Control": "no-store, private, max-age=0",
    "X-Robots-Tag": "noindex, noimageindex, noarchive, nosnippet, noai, noimageai",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Content-Disposition": "inline",
    "X-Content-Type-Options": "nosniff",
}

if not os.getenv("MEDIA_SECRET"):
    logging.getLogger(__name__).warning(
        "MEDIA_SECRET is not set: private image links use a per-process secret and break across workers/restarts"
    )
_SECRET = (os.getenv("MEDIA_SECRET") or secrets.token_hex(32)).encode()

# ai/scraper/automation clients; real browsers never send these ("bot", "spider" and "crawl" catch most named crawlers)
_BLOCKED_UA = re.compile(
    r"bot\b|spider|crawl|chatgpt|oai-|openai|claude|anthropic|perplexity|google-extended|cohere|meta-external|"
    r"omgili|imagesift|img2dataset|python-|aiohttp|curl|wget|go-http|node-fetch|axios|okhttp|java/|libwww|scrapy",
    re.I,
)
_NAME = re.compile(r"[a-z0-9_-]+")


def _sign(exp: int, name: str) -> str:
    return hmac.new(_SECRET, f"{name}:{exp}".encode(), hashlib.sha256).hexdigest()[:32]


def signed_url(name: str) -> str:
    exp = int(time.time()) + TTL_SECONDS
    return f"/_/p/{name}/{exp}.{_sign(exp, name)}"


def is_allowed_request(headers: Mapping[str, str]) -> bool:
    """A real browser loading the image from our own page (Sec-Fetch-* absent on very old browsers is tolerated)."""
    ua = headers.get("user-agent")
    dest, site = headers.get("sec-fetch-dest"), headers.get("sec-fetch-site")
    return bool(ua) and not _BLOCKED_UA.search(ua) and dest in (None, "image") and site in (None, "same-origin")


def _materialize_from_env(path: Path, name: str) -> None:
    """Containers can't get git-ignored files, so a private image may arrive as base64 split over
    PRIVATE_<NAME>_B64_0, _1, ... (each chunk stays under Railway's 32,768-character variable limit; 30,000 is used)."""
    chunks = []
    while chunk := os.getenv(f"PRIVATE_{name.upper()}_B64_{len(chunks)}"):
        chunks.append(chunk)
    if chunks:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(base64.b64decode("".join(chunks)))


def resolve(name: str, token: str) -> Path | None:
    """Return the file path if the token is valid and unexpired, else None."""
    if not _NAME.fullmatch(name):
        return None
    try:
        exp_s, sig = token.split(".", 1)
        exp = int(exp_s)
    except ValueError:
        return None
    if exp < time.time() or not hmac.compare_digest(sig, _sign(exp, name)):
        return None
    path = PRIVATE_DIR / f"{name}.jpg"
    if not path.is_file():
        _materialize_from_env(path, name)
    return path if path.is_file() else None
