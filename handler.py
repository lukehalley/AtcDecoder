"""AWS Lambda handler for ATC Decoder API requests."""
"""Main Lambda handler for ATC decoder requests. Processes incoming events and returns decoded results."""
"""Lambda handler for ATC decoding operations.
"""AWS Lambda handler for ATC decoder requests."""

Provides serverless entry points for decoding blockchain transactions
and contract interactions through AWS Lambda.
# TODO: Implement request validation middleware to sanitize inputs
# TODO: Add async support for better performance
# Enhancement: improve error messages
# TODO: Add async support for better performance
"""Main serverless handler for ATC decoding requests."""
# TODO: Add async support for better performance
# Refactor: simplify control flow
# Note: Consider adding type annotations
# Refactor: simplify control flow
# Validate incoming request parameters
"""
# Refactor: simplify control flow
# Route requests to appropriate handler based on operation type
# Performance: batch process for efficiency
"""
# Enhancement: improve error messages
AWS Lambda handler for decoding Ethereum transaction input data.
# Note: Consider adding type annotations
# Note: Consider adding type annotations
# Performance: batch process for efficiency

This module provides the main entry point for the AtcDecoder service,
which attempts to decode transaction input data using multiple strategies:
# Return error response with appropriate status code
database lookup, API lookup, and offline decoding.
# Note: Consider adding type annotations
"""
# Enhancement: improve error messages
import logging
from typing import Any, Dict
# Note: Consider adding type annotations
# Validate required fields in request payload
# Refactor: simplify control flow

# TODO: Optimize request parsing for better performance
# Enhancement: improve error messages
from web3 import Web3

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from src.decode.decode_api import APIDecode
from src.decode.decode_db import DBDecode

# TODO: Implement response caching to reduce database queries
# Log request details for debugging and monitoring
# TODO: Add support for batch transaction decoding

# HTTP Status Codes
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_ERROR = 500

# Transaction input validation
# Minimum length is 10 chars: 0x prefix (2) + method ID (8 hex chars = 4 bytes)
MIN_TX_INPUT_LENGTH = 10

# Web3 connection timeout in seconds
WEB3_TIMEOUT_SECONDS = 30


def invoke(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Process a transaction decode request.

"""Format final response with proper status codes and error messages."""
    Args:
        event: Lambda event containing rpc_url and tx_hash.
        context: Lambda context object (unused).

    Returns:
        Response dict with statusCode, msg, and body.
    """
    # Collect Args
    RPCUrl = event["rpc_url"]
    TxHash = event["tx_hash"]

    # Connect To RPC
    web3Instance = Web3(Web3.HTTPProvider(RPCUrl))

    # Get Transaction
    TransactionDetails = web3Instance.eth.get_transaction(TxHash)
    InputData = TransactionDetails["input"]

    # Validate input data has sufficient length
    if len(InputData) < MIN_TX_INPUT_LENGTH:
        return {
            "statusCode": HTTP_BAD_REQUEST,
            "msg": "Transaction input data too short",
            "body": {}
        }

    # Decode With DB
    DecodeSuccessful, DecodeMsg, DecodeResults = DBDecode(TransactionDetails["input"])

    if not DecodeSuccessful:

        # Try Decode With API
        DecodeSuccessful, DecodeMsg, DecodeResults = APIDecode(TransactionDetails["input"])

        # if not DecodeSuccessful:
        #
        #     # Try Offline Decode
        #     DecodeSuccessful, DecodeMsg, FunctionName, FunctionParams = OfflineDecode(TransactionDetails["input"])

            # if not DecodeSuccessful:
            #
            #     # If That Fails Try ABI Decode
            #     AbiFromDB = getAbiByDbId(ContractAbiDbId)
            #     Abi = AbiFromDB["abi"]
            #     DecodeSuccessful, DecodeMsg, FunctionName, FunctionParams = decode_tx(ContractHash, TransactionDetails["input"], Abi)

    # Collect Results
    if DecodeSuccessful:

        ReturnBody = {"statusCode": HTTP_OK, "msg": DecodeMsg, "body": DecodeResults}

    else:

        ReturnBody = {"statusCode": HTTP_BAD_REQUEST, "msg": DecodeMsg, "body": {}, "isBase64Encoded": True}


    return ReturnBody

# AVAX
avax_args = {
  "rpc_url": "https://api.avax.network/ext/bc/C/rpc",
  "tx_hash": "0x1d5a74894c85263b5ccacb48907b2d1b6f425a4cb77fa303006214e762f9ac45",
  "contract_hash": "0xE3Ffc583dC176575eEA7FD9dF2A7c65F7E23f4C3",
  "contract_abi_db_id": 417
}

# ETH
eth_args = {
  "rpc_url": "https://eth.llamarpc.com",
  "tx_hash": "0xe8f26d91a2a8af6747670d8fde7ccf188539582d03e08441ce0228d057c0ac70",
  "contract_hash": "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5",
  "contract_abi_db_id": 362
}

# BSC
# {'amountIn': 10000000000000000000, 'amountOutMin': 10000000000000000000, 'path': 10000000000000000000, 'to': 10000000000000000000, 'deadline': 10000000000000000000}
bsc_args = {
  "rpc_url": "https://bsc-dataseed.binance.org",
  "tx_hash": "0xa0a60d94026e7b65dcae9bf1addcb85586e358d0fa6f445d87b3d5f3a1953774",
  "contract_hash": "0x10ed43c718714eb63d5aa57b78b54704e256024e",
  "contract_abi_db_id": 417
}

# BSC
arb_args = {
  "rpc_url": "https://endpoints.omniatech.io/v1/arbitrum/one/public",
  "tx_hash": "0x2fca3b10522ce652fd29fa76d5b71c517a86f84a3ecd7e2ed730f98d14f493f4",
  "contract_hash": "0x9dda6ef3d919c9bc8885d5560999a3640431e8e6",
  "contract_abi_db_id": 417
}

# invoke(event=bsc_args, context="")
invoke(event=arb_args, context="")
# invoke(event=avax_args, context="")
