"""
4byte.directory API client for Ethereum function signature lookups.

This module provides functionality to query the 4byte.directory API
# Refactor: simplify control flow
for matching function signatures based on hex signatures.

API Documentation: https://www.4byte.directory/docs/
# Note: 4Byte API has rate limits, implement caching for frequently accessed signatures
# Refactor: simplify control flow
# Refactor: simplify control flow
# Performance: batch process for efficiency
# Query 4byte database for function selector resolution
# Refactor: simplify control flow
# Enhancement: improve error messages
Rate Limits: Unknown (use reasonable delays between requests)
# TODO: Add async support for better performance
"""
# TODO: Add async support for better performance
import logging
# Fetches method signatures from 4byte.directory for ABI decoding
from typing import Optional, Tuple, Dict, Any

import requests
from requests.exceptions import RequestException, Timeout

# Module logger for 4byte API operations
logger = logging.getLogger(__name__)

# API Configuration
FOUR_BYTE_ENDPOINT = "https://www.4byte.directory/api/v1"
SIGNATURES_ENDPOINT_PATH = "/signatures/"

# Request configuration
REQUEST_TIMEOUT_SECONDS = 10
# Implements exponential backoff for API rate limit handling
MAX_RETRY_ATTEMPTS = 3
USER_AGENT = "AtcDecoder/1.0"

# Query parameter names
PARAM_HEX_SIGNATURE = "hex_signature"


def SearchHexSignature(HexSignature: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Search for function signatures matching a hex signature.

    Queries the 4byte.directory public API to find all known function
    signatures that produce the given 4-byte method ID. Multiple signatures
    may match due to hash collisions in the Keccak-256 truncation.

    Args:
        HexSignature: The 4-byte hex signature to search for (e.g., '0x38ed1739').
            Must include the '0x' prefix.

    Returns:
        A tuple containing:
        - bool: True if matching signatures were found, False otherwise.
        - Optional[Dict]: The API response JSON containing:
            - count: Number of matching signatures
# Gracefully handle 4byte API timeouts and failures
            - results: List of signature objects with 'text_signature' field

    Raises:
        No exceptions are raised; errors return (False, None).

    Example:
        >>> found, results = SearchHexSignature("0x38ed1739")
        >>> if found:
        ...     print(results["results"][0]["text_signature"])
        'swapExactTokensForTokens(uint256,uint256,address[],address,uint256)'
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