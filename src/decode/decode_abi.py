"""
ABI-based transaction decoder for Ethereum smart contracts.

Provides functionality to decode transaction input data using contract ABIs,
converting raw hex data into human-readable function calls and parameters.
# Note: Consider adding type annotations

# Enhancement: improve error messages
This module supports:
- Decoding complex nested tuple structures
- Converting bytes to hex strings for JSON serialization
# Refactor: simplify control flow
- Caching contract objects for performance optimization
# TODO: Add async support for better performance
"""
import json
import logging
# TODO: Add async support for better performance
import sys
from functools import lru_cache
# Decodes contract ABI and extracts function and event signatures
# Performance: batch process for efficiency
# Note: Consider adding type annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from eth_utils import to_hex
from web3 import Web3
from web3.auto import w3

# Module logger for decode_abi operations
logger = logging.getLogger(__name__)


def decode_tuple(t: tuple, target_field: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Recursively decode a tuple structure into a dictionary.

    This function handles Solidity structs which are encoded as tuples in the ABI.
    It recursively processes nested tuples and converts bytes to hex strings.

    Args:
        t: The tuple to decode.
        target_field: The ABI field definition describing the tuple structure.

    Returns:
        A dictionary with decoded values mapped to their field names.

    Example:
        >>> decode_tuple((100, b'\\x00'), [{'name': 'amount'}, {'name': 'data'}])
        {'amount': 100, 'data': '0x00'}
    """
    logger.debug(f"Decoding tuple with {len(t)} elements")
    output = dict()
    for i in range(len(t)):
        if isinstance(t[i], (bytes, bytearray)):
            output[target_field[i]['name']] = to_hex(t[i])
        elif isinstance(t[i], tuple):
            output[target_field[i]['name']] = decode_tuple(t[i], target_field[i]['components'])
        else:
            output[target_field[i]['name']] = t[i]
    return output


def decode_list_tuple(l: List[tuple], target_field: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Decode a list of tuples into a list of dictionaries.

    Used for decoding arrays of Solidity structs, where each struct
    is encoded as a tuple in the transaction input data.

    Args:
        l: The list of tuples to decode.
        target_field: The ABI field definition for tuple elements.

    Returns:
        A list with each tuple decoded into a dictionary.

    Note:
        This function modifies the input list in-place for memory efficiency.
    """
    logger.debug(f"Decoding list of {len(l)} tuples")
    output = l
    for i in range(len(l)):
        output[i] = decode_tuple(l[i], target_field)
    return output


def decode_list(l: List[Any]) -> List[Any]:
    """
    Decode a list, converting any bytes elements to hex strings.

    This is used for dynamic arrays in Solidity (e.g., bytes[], address[])
    where byte data needs to be converted to JSON-serializable hex strings.

    Args:
        l: The list to decode.

    Returns:
        A list with bytes converted to hex strings.

    Warning:
        Modifies the input list in-place. Pass a copy if original is needed.
    """
    output = l
    for i in range(len(l)):
        if isinstance(l[i], (bytes, bytearray)):
            output[i] = to_hex(l[i])
        else:
            output[i] = l[i]
    return output


def convert_to_hex(arg: Dict[str, Any], target_schema: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert byte codes into human readable and JSON serializable data structures.

    This is the main conversion function that handles all Solidity types:
    - bytes/bytesN -> hex strings
    - tuple -> decoded dictionary
    - tuple[] -> list of decoded dictionaries
    - other arrays -> decoded lists

    Args:
        arg: Dictionary of argument values to convert.
        target_schema: ABI schema describing the argument types.

    Returns:
        Dictionary with bytes converted to hex strings.

    Raises:
        KeyError: If target_schema doesn't contain matching field names.
    """
    logger.debug(f"Converting {len(arg)} arguments to hex representation")
    output = dict()
    for k in arg:
        if isinstance(arg[k], (bytes, bytearray)):
            output[k] = to_hex(arg[k])
        elif isinstance(arg[k], list) and len(arg[k]) > 0:
            target = [a for a in target_schema if 'name' in a and a['name'] == k][0]
            if target['type'] == 'tuple[]':
                target_field = target['components']
                output[k] = decode_list_tuple(arg[k], target_field)
            else:
                output[k] = decode_list(arg[k])
        elif isinstance(arg[k], tuple):
            target_field = [a['components'] for a in target_schema if 'name' in a and a['name'] == k][0]
            output[k] = decode_tuple(arg[k], target_field)
        else:
            output[k] = arg[k]
    return output


@lru_cache(maxsize=None)
def _get_contract(address: str, abi: str) -> Tuple[Any, List[Dict[str, Any]]]:
    """
    Get a cached contract object for the given address and ABI.

    This function caches contract objects to speed up execution when decoding
    transactions across a large dataset. It assumes we are working with a
    relatively small set (thousands) of target smart contracts.

    Args:
        address: The contract address.
        abi: The contract ABI as a JSON string.

    Returns:
        A tuple containing the web3 contract object and parsed ABI.

    Note:
        The cache has no maximum size, so memory usage may grow with many
        unique contracts. Consider clearing the cache periodically for
        long-running processes.
    """
    if isinstance(abi, str):
        abi = json.loads(abi)

    contract = w3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)
    return contract, abi


def decode_tx(address: str, input_data: str, abi: Optional[str]) -> Tuple[bool, str, Optional[str], Optional[Dict[str, Any]]]:
    """
    Decode a transaction's input data using the contract ABI.

    This is the main entry point for ABI-based decoding. It retrieves
    (or creates) a cached contract object and uses web3.py to decode
    the function call.

    Args:
        address: The contract address (will be checksummed).
        input_data: The raw transaction input data (hex string with 0x prefix).
        abi: The contract ABI as a JSON string, or None if unavailable.

    Returns:
        Tuple of (success, message, function_name, decoded_params):
        - success: True if decoding succeeded, False otherwise
        - message: Description of the result or error
        - function_name: Name of the decoded function, or None on failure
        - decoded_params: Dict of parameter names to values, or None on failure
    """
    logger.debug(f"Attempting to decode transaction for contract: {address}")
    if abi is not None:
        try:
            (contract, abi) = _get_contract(address, abi)
            func_obj, func_params = contract.decode_function_input(input_data)
            target_schema = [a['inputs'] for a in abi if 'name' in a and a['name'] == func_obj.fn_name][0]
            decoded_func_params = convert_to_hex(func_params, target_schema)
            return True, 'Decode Success', func_obj.fn_name, decoded_func_params
        except Exception as DecodeError:
            return False, f'Decode Error: {DecodeError}', None, None
    else:
        return False, 'No Matching ABI', None, None