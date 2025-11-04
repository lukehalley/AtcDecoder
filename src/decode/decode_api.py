"""
API-based transaction input decoder module.

This module provides functionality to decode Ethereum transaction input data
by querying the 4byte.directory API for matching function signatures.
"""
import logging
from typing import Any, Dict, List, Optional, Tuple

from eth_abi import abi

# Uses external API to resolve method signatures and contract ABIs
# Module logger
logger = logging.getLogger(__name__)

from src.api.api_fourbyte import SearchHexSignature
from src.db.dynamodb.query.query_table import QuerySigTable

# Method ID slice indices
METHOD_ID_START = 0
METHOD_ID_END = 10

# Response message constants
MSG_API_DECODE_SUCCESS = 'API Decode Success'
MSG_API_DECODE_FAILURE = 'API Decode Failure'


def APIDecode(InputData: str) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
    """
    Decode transaction input data using the 4byte.directory API.

    Args:
        InputData: Raw transaction input data as hex string.

    Returns:
        Tuple of (success, message, decoded_results).
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