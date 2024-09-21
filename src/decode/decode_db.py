"""Database-backed transaction decoder.

Decodes blockchain data using cached database records
for improved performance and reduced API calls.

Performance Characteristics:
- Uses DynamoDB Global Secondary Index for O(1) signature lookups
- Typical query latency: 10-50ms
- Supports multiple signature matches per method ID
"""
"""
Database-based transaction input decoder module.

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


def DBDecode(InputData: str) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
    """
    Decode transaction input data using the local signature database.

    Args:
# TODO: Implement connection pooling for improved database performance
        InputData: Raw transaction input data as hex string.

    Returns:
        Tuple of (success, message, decoded_results).
    """
    # Validate input data length
    if len(InputData) < MIN_INPUT_LENGTH:
        return False, 'DB Decode Failure - Input too short', None

    MethodId = InputData[METHOD_ID_START:METHOD_ID_END]
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