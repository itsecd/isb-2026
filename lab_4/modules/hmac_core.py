# -*- coding: utf-8 -*-
"""Core HMAC operations: generation, verification, tamper detection."""

import hashlib
import hmac
import json
from pathlib import Path

import modules.logger as logger

log = logger.app_logger

# Algorithms supported by this module.
SUPPORTED_ALGORITHMS = {"sha256", "sha512", "sha3_256", "sha3_512"}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _encode(value: str) -> bytes:
    """Encode *value* to UTF-8 bytes.

    Args:
        value: Plain-text string to encode.

    Returns:
        UTF-8 encoded bytes.
    """
    return value.encode("utf-8")


def _validate_algo(algo: str) -> str:
    """Validate and normalise the algorithm name.

    Args:
        algo: Algorithm name supplied by the caller.

    Returns:
        Lower-cased algorithm name.

    Raises:
        ValueError: If *algo* is not in :data:`SUPPORTED_ALGORITHMS`.
    """
    algo = algo.lower()
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported algorithm '{algo}'. "
            f"Choose from: {', '.join(sorted(SUPPORTED_ALGORITHMS))}"
        )
    return algo


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_hmac(message: str, secret_key: str, algo: str = "sha256") -> str:
    """Compute an HMAC tag for *message* using *secret_key*.

    Args:
        message: Plain-text message to authenticate.
        secret_key: Secret key shared between sender and receiver.
        algo: Hash algorithm (default ``"sha256"``).

    Returns:
        Hex-encoded HMAC digest string.

    Raises:
        ValueError: If *algo* is not supported.
        TypeError: If *message* or *secret_key* are not strings.
    """
    if not isinstance(message, str) or not isinstance(secret_key, str):
        raise TypeError("message and secret_key must be str")

    algo = _validate_algo(algo)
    tag = hmac.new(_encode(secret_key), _encode(message), algo)
    digest = tag.hexdigest()
    log.debug("HMAC computed for message (algo=%s): %s", algo, digest)
    return digest


def verify_hmac(
    message: str,
    secret_key: str,
    expected_tag: str,
    algo: str = "sha256",
) -> bool:
    """Verify that *expected_tag* matches the HMAC of *message*.

    Uses :func:`hmac.compare_digest` to prevent timing attacks.

    Args:
        message: Message whose authenticity is being checked.
        secret_key: Shared secret key.
        expected_tag: Hex-encoded HMAC tag to compare against.
        algo: Hash algorithm (default ``"sha256"``).

    Returns:
        ``True`` if the tag is valid, ``False`` otherwise.

    Raises:
        ValueError: If *algo* is not supported.
    """
    actual_tag = compute_hmac(message, secret_key, algo)
    result = hmac.compare_digest(actual_tag, expected_tag)
    log.info("HMAC verification result: %s", "PASS" if result else "FAIL")
    return result


def sign_and_save(
    message: str,
    secret_key: str,
    output_path: str,
    algo: str = "sha256",
) -> dict:
    """Compute an HMAC tag and persist a signed envelope to *output_path*.

    The envelope JSON has the shape::

        {"message": "...", "hmac": "...", "algo": "sha256"}

    Args:
        message: Message to sign.
        secret_key: Shared secret key.
        output_path: File path for the signed JSON envelope.
        algo: Hash algorithm (default ``"sha256"``).

    Returns:
        The signed envelope as a dictionary.

    Raises:
        OSError: If the file cannot be written.
    """
    tag = compute_hmac(message, secret_key, algo)
    envelope = {"message": message, "hmac": tag, "algo": algo}

    path = Path(output_path)
    path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Signed envelope saved → %s", path)
    return envelope


def load_and_verify(
    input_path: str,
    secret_key: str,
) -> tuple[bool, dict]:
    """Load a signed envelope from *input_path* and verify its HMAC.

    Args:
        input_path: Path to the JSON envelope file.
        secret_key: Shared secret key for verification.

    Returns:
        A tuple ``(is_valid, envelope)`` where *is_valid* is ``True`` when
        the stored HMAC matches the re-computed one.

    Raises:
        FileNotFoundError: If *input_path* does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        KeyError: If required fields are missing from the envelope.
    """
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Envelope file not found: {input_path}")

    envelope = json.loads(path.read_text(encoding="utf-8"))
    for field in ("message", "hmac", "algo"):
        if field not in envelope:
            raise KeyError(f"Missing field '{field}' in envelope")

    is_valid = verify_hmac(
        envelope["message"],
        secret_key,
        envelope["hmac"],
        envelope["algo"],
    )
    return is_valid, envelope


def tamper_and_verify(
    input_path: str,
    secret_key: str,
    tampered_message: str,
) -> bool:
    """Demonstrate tamper detection by verifying a *tampered_message*
    against the HMAC stored in *input_path*.

    Args:
        input_path: Path to the original signed JSON envelope.
        secret_key: Shared secret key.
        tampered_message: The modified message to test.

    Returns:
        ``False`` when tampering is successfully detected (expected behaviour),
        ``True`` only if the tampered message accidentally matches.

    Raises:
        FileNotFoundError: If *input_path* does not exist.
        KeyError: If required envelope fields are missing.
    """
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Envelope file not found: {input_path}")

    envelope = json.loads(path.read_text(encoding="utf-8"))
    result = verify_hmac(
        tampered_message,
        secret_key,
        envelope["hmac"],
        envelope.get("algo", "sha256"),
    )
    log.info(
        "Tamper check: original_hmac=%s | tampered_valid=%s",
        envelope["hmac"][:16] + "…",
        result,
    )
    return result
