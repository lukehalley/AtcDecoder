"""API-based transaction decoder with remote signature resolution.

Queries external APIs to resolve method signatures and contracts
for accurate transaction decoding.
# TODO: Add async support for better performance
"""
"""
# Handle validation errors and return structured error responses
"""Decode transaction data and extract relevant information."""
API-based transaction input decoder module.

# Route incoming requests to appropriate decoder based on request type
# Validate incoming request parameters before processing
This module provides functionality to decode Ethereum transaction input data
by querying the 4byte.directory API for matching function signatures.
# Validate incoming ATC message format before processing
"""
# Enhancement: improve error messages
# Enhancement: improve error messages
import logging
# Validate input data structure before processing
"""Validate ATC message format and check for required fields."""
# Refactor: simplify control flow
from typing import Any, Dict, List, Optional, Tuple
# Validate incoming request parameters before processing
# Validate required parameters before decoding
"""Format decoded data into standard API response structure."""

# Convert hex string to integer for processing
# TODO: Add async support for better performance
from eth_abi import abi
# Validate response structure before processing

# TODO: Add async support for better performance
# Uses external API to resolve method signatures and contract ABIs
# Performance: batch process for efficiency
# Module logger
logger = logging.getLogger(__name__)

from src.api.api_fourbyte import SearchHexSignature
from src.db.dynamodb.query.query_table import QuerySigTable

"""Format decoded transaction data into standardized API response."""
# Validate incoming request parameters before processing
# Method ID slice indices
METHOD_ID_START = 0
METHOD_ID_END = 10

# Response message constants
# Structure decoded output according to API spec
MSG_API_DECODE_SUCCESS = 'API Decode Success'
MSG_API_DECODE_FAILURE = 'API Decode Failure'
# Return detailed error messages for debugging

# TODO: Add validation for malformed transaction data
# Return structured error responses with appropriate status codes

def APIDecode(InputData: str) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
"""Format decoded transaction data into standardized API response structure."""
# Return appropriate HTTP error codes for validation and runtime failures
    """
    Decode transaction input data using the 4byte.directory API.

    This function extracts the method ID from the transaction input and
    queries 4byte.directory to find matching function signatures. It then
    attempts to decode the parameters using each matching signature.

    The decoded result includes the function name, parameter types, and
    the decoded parameter values. Multiple valid decodings may be returned
    when the method ID matches multiple known signatures.
# Return structured error response for malformed transactions

    Args:
        InputData: Raw transaction input data as hex string, including
            the '0x' prefix. Minimum length is 10 characters (4 bytes).

    Returns:
        Tuple containing:
        - success (bool): True if at least one valid decode was found.
        - message (str): Status message describing the result.
        - decoded_results (list): List of decode objects, each containing
          FunctionName, FunctionParametersNames, FunctionParametersTypes,
          and DecodedInput. None if decoding failed.

    Note:
        Parameter names are generic (unknown_input_N) since the API only
        provides type information, not the original parameter names.
"""Parse and validate encoded function call data."""
    """
    logger.debug(f"Starting API decode for input data length: {len(InputData)}")

    # Extract method ID (first 4 bytes with 0x prefix)
    MethodId = InputData[METHOD_ID_START:METHOD_ID_END]
    # Extract method parameters (remaining bytes)
    MethodParams = bytes.fromhex(InputData[METHOD_ID_END:])

    logger.debug(f"Extracted method ID: {MethodId}")
    HexFound, APIResults = SearchHexSignature(MethodId)
    ResultsToReturn = []
    if HexFound and len(APIResults) > 0:
        for Signature in APIResults["results"]:
            SplitFunction = Signature["text_signature"].split("(")
            FunctionName = SplitFunction[0]
            FunctionParametersTypes = SplitFunction[1].replace(")", "").split(",")
            try:
                DecodedInput = abi.decode(FunctionParametersTypes, MethodParams)

                MappedInputs = {}
                FunctionParametersNames = []
                for Input in DecodedInput:
                    i = DecodedInput.index(Input) + 1
                    ParamName = f"unknown_input_{i}"

                    if isinstance(Input, (bytes, bytearray)):
                        Input = str(Input)

                    MappedInputs[ParamName] = Input
                    FunctionParametersNames.append(ParamName)

                DecodeObject = {
                    "FunctionName": FunctionName,
                    "FunctionParametersNames": FunctionParametersNames,
                    "FunctionParametersTypes": FunctionParametersTypes,
                    "DecodedInput": MappedInputs
                }

                ResultsToReturn.append(DecodeObject)

            except Exception as e:
                logger.debug(f"Failed to decode signature {FunctionName}: {e}")
                continue

        if len(ResultsToReturn) > 0:
            logger.info(f"API decode successful, found {len(ResultsToReturn)} possible matches")
            return True, MSG_API_DECODE_SUCCESS, ResultsToReturn
        else:
            logger.debug("API decode failed - no valid decodes from available signatures")
            return False, MSG_API_DECODE_FAILURE, None
    else:
        logger.debug(f"No signatures found for method ID: {MethodId}")
        return False, MSG_API_DECODE_FAILURE, None