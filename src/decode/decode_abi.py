"""
ABI-based transaction decoder for Ethereum smart contracts.

Provides functionality to decode transaction input data using contract ABIs,
converting raw hex data into human-readable function calls and parameters.
"""
import json
import sys
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple, Union

from eth_utils import to_hex
from web3 import Web3
from web3.auto import w3


def decode_tuple(t: tuple, target_field: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Recursively decode a tuple structure into a dictionary.

    Args:
        t: The tuple to decode.
        target_field: The ABI field definition describing the tuple structure.

    Returns:
        A dictionary with decoded values mapped to their field names.
    """
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

    Args:
        l: The list of tuples to decode.
        target_field: The ABI field definition for tuple elements.

    Returns:
        A list with each tuple decoded into a dictionary.
    """
    output = l
    for i in range(len(l)):
        output[i] = decode_tuple(l[i], target_field)
    return output


def decode_list(l: List[Any]) -> List[Any]:
    """
    Decode a list, converting any bytes elements to hex strings.

    Args:
        l: The list to decode.

    Returns:
        A list with bytes converted to hex strings.
    """
    output = l
    for i in range(len(l)):
        if isinstance(l[i], (bytes, bytearray)):
            output[i] = to_hex(l[i])
        else:
            output[i] = l[i]
    return output


def convert_to_hex(arg, target_schema):
    """
    utility function to convert byte codes into human readable and json serializable data structures
    """
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
def _get_contract(address, abi):
    """
    This helps speed up execution of decoding across a large dataset by caching the contract object
    It assumes that we are decoding a small set, on the order of thousands, of target smart contracts
    """
    if isinstance(abi, str):
        abi = json.loads(abi)

    contract = w3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)
    return contract, abi


def decode_tx(address, input_data, abi):
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