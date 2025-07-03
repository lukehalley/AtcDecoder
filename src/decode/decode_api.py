"""
API-based transaction input decoder module.

This module provides functionality to decode Ethereum transaction input data
by querying the 4byte.directory API for matching function signatures.
"""
from typing import Any, Dict, List, Optional, Tuple

from eth_abi import abi

from src.api.api_fourbyte import SearchHexSignature
from src.db.dynamodb.query.query_table import QuerySigTable

# Method ID slice indices
METHOD_ID_START = 0
METHOD_ID_END = 10


def APIDecode(InputData: str) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
    """
    Decode transaction input data using the 4byte.directory API.

    Args:
        InputData: Raw transaction input data as hex string.

    Returns:
        Tuple of (success, message, decoded_results).
    """
    MethodId = InputData[METHOD_ID_START:METHOD_ID_END]
    MethodParams = bytes.fromhex(InputData[METHOD_ID_END:])
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

            except Exception:
                continue
        if len(ResultsToReturn) > 0:
            return True, 'DB Decode Success', ResultsToReturn
        else:
            return False, 'DB Decode Failure', None
    else:
        return False, 'DB Decode Failure', None