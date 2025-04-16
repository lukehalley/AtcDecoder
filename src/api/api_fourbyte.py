"""
4byte.directory API client for Ethereum function signature lookups.

This module provides functionality to query the 4byte.directory API
for matching function signatures based on hex signatures.
"""
from typing import Optional, Tuple, Dict, Any

import requests

FOUR_BYTE_ENDPOINT = "https://www.4byte.directory/api/v1"


def SearchHexSignature(HexSignature: str) -> Tuple[bool, Optional[Dict[str, Any]]]:

    ApiEndpoint = f"{FOUR_BYTE_ENDPOINT}/signatures/?hex_signature={HexSignature}"

    Response = requests.get(url=ApiEndpoint)

    ResultsJSON = Response.json()

    if Response.ok and ResultsJSON["count"] > 0:
        return True, ResultsJSON
    else:
        return False, None