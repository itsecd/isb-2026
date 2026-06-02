from errors import HashError
from hash_utils import generate_string, get_short_hash


def find_single_collision(length: int) -> tuple[str, str, int, int]:
    """
    Find single collision.
    :param length: length of shat hash value to check
    :return: string 1, string 2, hash value, attempts to find
    """
    seen_hashes = {}
    attempts = 0
    limit = 100000

    while attempts < limit:
        attempts += 1
        curr_str = generate_string()
        curr_hash = get_short_hash(curr_str, length)
        if curr_hash in seen_hashes:
            if seen_hashes[curr_hash] != curr_str:
                return seen_hashes[curr_hash], curr_str, curr_hash, attempts
        else:
            seen_hashes[curr_hash] = curr_str

    raise HashError("No collisions were found.")
