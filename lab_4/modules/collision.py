# -*- coding: utf-8 -*-
"""Partial-collision search with tqdm progress visualisation.

This module demonstrates the Birthday Problem in practice by searching for
two distinct messages whose truncated HMAC tags share a common prefix of
*n* bits.  It is intentionally limited to short prefixes so the search
finishes in seconds — full SHA-256 collisions are computationally infeasible.
"""

import hashlib
import hmac
import itertools
import random
import string
import time
from typing import Optional

from tqdm import tqdm

import modules.logger as logger

log = logger.app_logger

_DEFAULT_PREFIX_BITS = 24   # 2^24 ≈ 16 M attempts worst-case
_MAX_ATTEMPTS = 10_000_000


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _truncated_tag(message: str, secret_key: str, prefix_bits: int) -> int:
    """Return the leading *prefix_bits* of an HMAC-SHA256 tag as an integer.

    Args:
        message: Message to tag.
        secret_key: Shared secret key.
        prefix_bits: How many leading bits to keep (1–256).

    Returns:
        Integer value of the truncated tag.
    """
    raw = hmac.new(
        secret_key.encode(), message.encode(), hashlib.sha256
    ).digest()
    # Convert bytes → int, then keep only the top prefix_bits.
    full_int = int.from_bytes(raw, "big")
    shift = 256 - prefix_bits
    return full_int >> shift


def _random_message(length: int = 8) -> str:
    """Generate a random alphanumeric message of *length* characters.

    Args:
        length: Number of characters.

    Returns:
        Random string.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def find_partial_collision(
    secret_key: str,
    prefix_bits: int = _DEFAULT_PREFIX_BITS,
    max_attempts: int = _MAX_ATTEMPTS,
) -> Optional[tuple[str, str, str]]:
    """Search for two messages with the same leading *prefix_bits* HMAC tag.

    Uses a birthday-attack strategy: store tags in a dict and check for
    repeated values.  Progress is shown via :mod:`tqdm`.

    Args:
        secret_key: HMAC secret key.
        prefix_bits: Number of leading bits that must match (max 32 for speed).
        max_attempts: Hard upper limit on the number of messages to generate.

    Returns:
        ``(msg_a, msg_b, shared_prefix_hex)`` if a collision is found,
        ``None`` if *max_attempts* is exhausted first.
    """
    prefix_bits = max(1, min(prefix_bits, 64))  # safety clamp
    seen: dict[int, str] = {}

    log.info(
        "Starting partial-collision search | prefix_bits=%d | max_attempts=%d",
        prefix_bits,
        max_attempts,
    )
    start = time.perf_counter()

    with tqdm(
        total=max_attempts,
        desc=f"Collision search ({prefix_bits}-bit prefix)",
        unit="msg",
        colour="cyan",
        dynamic_ncols=True,
    ) as bar:
        for attempt in itertools.islice(itertools.count(), max_attempts):
            msg = _random_message()
            tag = _truncated_tag(msg, secret_key, prefix_bits)

            if tag in seen and seen[tag] != msg:
                elapsed = time.perf_counter() - start
                collision_hex = hex(tag)
                log.info(
                    "Collision found in %d attempts (%.2fs): '%s' vs '%s' → prefix=%s",
                    attempt + 1,
                    elapsed,
                    seen[tag],
                    msg,
                    collision_hex,
                )
                bar.update(1)
                bar.close()
                return seen[tag], msg, collision_hex

            seen[tag] = msg
            bar.update(1)

    log.warning("No collision found within %d attempts.", max_attempts)
    return None


def run_collision_demo(secret_key: str, prefix_bits: int = 24) -> None:
    """CLI entry point: run a partial-collision search and print the result.

    Args:
        secret_key: HMAC secret key.
        prefix_bits: Leading bits to match (default 24).
    """
    result = find_partial_collision(secret_key, prefix_bits)
    if result:
        msg_a, msg_b, prefix = result
        print(f"\n[✓] Collision found!")
        print(f"    Message A : {msg_a}")
        print(f"    Message B : {msg_b}")
        print(f"    Shared prefix : {prefix}")
    else:
        print("\n[✗] No collision found within the attempt limit.")
