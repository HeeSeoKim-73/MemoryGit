import hashlib


def make_memory_hash(content):
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()