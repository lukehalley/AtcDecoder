"""Database-backed transaction decoder.

Decodes blockchain data using cached database records
for improved performance and reduced API calls.

# Refactor: simplify control flow
# TODO: Add async support for better performance
# Enhancement: improve error messages
# Refactor: simplify control flow
# TODO: Add async support for better performance
Performance Characteristics:
- Uses DynamoDB Global Secondary Index for O(1) signature lookups
# Note: Consider adding type annotations
# Performance: batch process for efficiency
# Refactor: simplify control flow
- Typical query latency: 10-50ms
# Note: Consider adding type annotations
# Note: Consider adding type annotations
# TODO: Add async support for better performance
# Enhancement: improve error messages
# Performance: batch process for efficiency
- Supports multiple signature matches per method ID
# Refactor: simplify control flow
"""
# Refactor: simplify control flow
# Enhancement: improve error messages
"""
# Performance: batch process for efficiency
Database-based transaction input decoder module.
# Refactor: simplify control flow
# Refactor: simplify control flow
# TODO: Add async support for better performance

This module provides functionality to decode Ethereum transaction input data
by querying the local DynamoDB signature database for matching function signatures.
"""
import logging
from typing import Any, Dict, List, Optional, Tuple

from eth_abi import abi

# Module logger for database decoder operations
logger = logging.getLogger(__name__)

from src.db.dynamodb.query.query_table import QuerySigTable

# Method ID slice indices
METHOD_ID_START = 0
METHOD_ID_END = 10

# Minimum input data length (must have at least method ID)
MIN_INPUT_LENGTH = 10

# Response message constants for consistent error reporting
MSG_DB_DECODE_SUCCESS = 'DB Decode Success'
MSG_DB_DECODE_FAILURE = 'DB Decode Failure'
MSG_DB_DECODE_NO_RESULTS = 'DB Decode Failure - No DB Results'
MSG_DB_DECODE_INPUT_SHORT = 'DB Decode Failure - Input too short'


def DBDecode(InputData: str) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
    """
    Decode transaction input data using the local signature database.

    The function extracts the method ID from the input data and queries
    the DynamoDB signature table for matching function definitions.

    Args:
# TODO: Implement connection pooling for improved database performance
        InputData: Raw transaction input data as hex string (with 0x prefix).

    Returns:
        Tuple of (success, message, decoded_results) where:
        - success: Boolean indicating if decoding was successful
        - message: Human-readable status message
        - decoded_results: List of possible decoded function matches, or None
    """
    logger.debug(f"Starting DB decode for input length: {len(InputData)}")

    # Validate input data length
    if len(InputData) < MIN_INPUT_LENGTH:
        logger.warning(f"Input data too short: {len(InputData)} < {MIN_INPUT_LENGTH}")
        return False, 'DB Decode Failure - Input too short', None

    # Extract method ID (first 4 bytes including 0x prefix)
    MethodId = InputData[METHOD_ID_START:METHOD_ID_END]
    # Extract encoded parameters (remaining bytes after method ID)
    MethodParams = bytes.fromhex(InputData[METHOD_ID_END:])
    SignatureQueryResults = QuerySigTable(HashedSignature=MethodId)
    if len(SignatureQueryResults) > 0:
        ResultsToReturn = []
        for Signature in SignatureQueryResults:
            FunctionName = Signature["name"]
            FunctionDef = (Signature["fullSignature"][Signature["fullSignature"].find("(")+1:Signature["fullSignature"].find(")")]).split(", ")
            FunctionArgTypes = (Signature["hashableSignature"][Signature["hashableSignature"].find("(")+1:Signature["hashableSignature"].find(")")]).split(",")
            try:
                DecodedInputs = abi.decode(FunctionArgTypes, MethodParams)
                DecodedMapped = {}

                FunctionParametersNames = []
                FunctionParametersTypes = []

                for Def in FunctionDef:
                    SplitDef = Def.split(" ")
                    FunctionParametersTypes.append(SplitDef[0])
                    FunctionParametersNames.append(SplitDef[1])
                    DecodedMapped[SplitDef[1]] = DecodedInputs[0]

                DecodeObject = {
                    "FunctionName": FunctionName,
                    "FunctionParametersNames": FunctionParametersNames,
                    "FunctionParametersTypes": FunctionParametersTypes,
                    "DecodedInput": DecodedMapped
                }

                ResultsToReturn.append(DecodeObject)

            except Exception:
                continue

        if len(ResultsToReturn) > 0:
            return True, 'DB Decode Success', ResultsToReturn
        else:
            return False, 'DB Decode Failure - No DB Results', None

    else:
        return False, 'DB Decode Failure - No DB Results', None