"""
4byte.directory API client for Ethereum function signature lookups.

This module provides functionality to query the 4byte.directory API
for matching function signatures based on hex signatures.
"""
from typing import Optional, Tuple, Dict, Any

import requests

FOUR_BYTE_ENDPOINT = "https://www.4byte.directory/api/v1"
REQUEST_TIMEOUT_SECONDS = 10


def SearchHexSignature(HexSignature: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Search for function signatures matching a hex signature.

    Args:
        HexSignature: The 4-byte hex signature to search for (e.g., '0x38ed1739').

    Returns:
        A tuple containing:
        - bool: True if matching signatures were found, False otherwise.
        - Optional[Dict]: The API response JSON if found, None otherwise.
    """
    ApiEndpoint = f"{FOUR_BYTE_ENDPOINT}/signatures/?hex_signature={HexSignature}"

    Response = requests.get(url=ApiEndpoint, timeout=REQUEST_TIMEOUT_SECONDS)

    ResultsJSON = Response.json()

    if Response.ok and ResultsJSON["count"] > 0:
        return True, ResultsJSON
    else:
        return False, None