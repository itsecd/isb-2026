"""
Utilities for file hashing, checksum storage, integrity verification,
verification result export, and collision demonstration.
"""

import hashlib
import os
import random
import string
from tqdm import tqdm


def sha256_file(path, chunk_size=8192):
    """
    Compute SHA-256 hash for a file with a progress bar.

    Args:
        path (str): Path to the file.
        chunk_size (int): Read chunk size in bytes.

    Returns:
        str: Hex digest of the file.
    """
    hasher = hashlib.sha256()
    total = os.path.getsize(path)

    with tqdm(total=total, unit="B", unit_scale=True, desc="Hashing") as pbar:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
                pbar.update(len(chunk))

    return hasher.hexdigest()


def save_checksum(source_path, checksum, checksum_path=None):
    """
    Save checksum to a separate file.

    Args:
        source_path (str): Original file path.
        checksum (str): Hex digest string.
        checksum_path (str | None): Output checksum path.

    Returns:
        str: Path to checksum file.
    """
    if checksum_path is None:
        checksum_path = source_path + ".sha256"

    with open(checksum_path, "w", encoding="utf-8") as f:
        f.write(f"{checksum}  {os.path.basename(source_path)}\n")

    return checksum_path


def load_checksum(checksum_path):
    """
    Load checksum from file.

    Args:
        checksum_path (str): Path to checksum file.

    Returns:
        str: Stored checksum.
    """
    with open(checksum_path, "r", encoding="utf-8") as f:
        line = f.readline().strip()

    if not line:
        raise ValueError("Checksum file is empty")

    return line.split()[0]


def verify_file(path, checksum_path=None):
    """
    Verify file integrity by comparing current and stored checksum.

    Args:
        path (str): File path.
        checksum_path (str | None): Path to checksum file.

    Returns:
        tuple[bool, str, str]: (is_valid, current_hash, saved_hash)
    """
    if checksum_path is None:
        checksum_path = path + ".sha256"

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if not os.path.exists(checksum_path):
        raise FileNotFoundError(f"Checksum file not found: {checksum_path}")

    current = sha256_file(path)
    saved = load_checksum(checksum_path)
    return current == saved, current, saved


def write_verification_result(ok, current, saved, result_path="verify_result.txt"):
    """
    Write verification result to a text file.

    Args:
        ok (bool): Verification status.
        current (str): Current checksum.
        saved (str): Stored checksum.
        result_path (str): Output file path.

    Returns:
        str: Result file path.
    """
    with open(result_path, "w", encoding="utf-8") as f:
        f.write(f"Current: {current}\n")
        f.write(f"Saved:   {saved}\n")
        f.write("OK\n" if ok else "FAILED\n")

    return result_path


def collision_demo(max_attempts=10000, prefix_len=8):
    """
    Demonstrate collision search on a truncated SHA-256 prefix.

    Args:
        max_attempts (int): Maximum random attempts.
        prefix_len (int): Number of hex digits to compare.

    Returns:
        dict: Search result.
    """
    seen = {}

    for i in tqdm(range(max_attempts), desc="Collision search"):
        msg = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        h = hashlib.sha256(msg.encode()).hexdigest()[:prefix_len]

        if h in seen:
            return {
                "found": True,
                "attempts": i + 1,
                "first": seen[h],
                "second": msg,
                "hash": h,
            }

        seen[h] = msg

    return {"found": False, "attempts": max_attempts}