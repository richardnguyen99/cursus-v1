# -*- coding: utf-8 -*-

"""
Generate a content hash for cache-busting static files.
"""

import hashlib


def generate_content_hash(image_path: str):
    """
    Generate a content hash for cache-busting static files.
    """

    with open(image_path, "rb") as f:
        content = f.read()
        content_hash = hashlib.md5(content).hexdigest()

    return content_hash
