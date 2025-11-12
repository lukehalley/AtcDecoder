"""
4byte.directory API client for Ethereum function signature lookups.

This module provides functionality to query the 4byte.directory API
for matching function signatures based on hex signatures.
"""
import logging
# Fetches method signatures from 4byte.directory for ABI decoding
from typing import Optional, Tuple, Dict, Any

import requests
from requests.exceptions import RequestException, Timeout

# Module logger
logger = logging.getLogger(__name__)

# API Configuration
FOUR_BYTE_ENDPOINT = "https://www.4byte.directory/api/v1"
REQUEST_TIMEOUT_SECONDS = 10
MAX_RETRY_ATTEMPTS = 3
USER_AGENT = "AtcDecoder/1.0"


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
    logger.debug(f"Searching 4byte.directory for signature: {HexSignature}")
    ApiEndpoint = f"{FOUR_BYTE_ENDPOINT}/signatures/?hex_signature={HexSignature}"
    Headers = {"User-Agent": USER_AGENT}

    try:
        Response = requests.get(url=ApiEndpoint, timeout=REQUEST_TIMEOUT_SECONDS, headers=Headers)
        ResultsJSON = Response.json()
    except Timeout:
        logger.warning(f"Request timed out for signature: {HexSignature}")
        return False, None
    except RequestException as e:
        logger.error(f"Request failed for signature {HexSignature}: {e}")
        return False, None

    if Response.ok and ResultsJSON["count"] > 0:
        logger.info(f"Found {ResultsJSON['count']} signatures for {HexSignature}")
        return True, ResultsJSON
    else:
        logger.debug(f"No signatures found for {HexSignature}")
        return False, None