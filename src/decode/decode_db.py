"""
Database-based transaction input decoder module.

This module provides functionality to decode Ethereum transaction input data
by querying the local DynamoDB signature database for matching function signatures.
"""
from typing import Any, Dict, List, Optional, Tuple

from eth_abi import abi

from src.db.dynamodb.query.query_table import QuerySigTable

# Method ID slice indices
METHOD_ID_START = 0
METHOD_ID_END = 10


def DBDecode(InputData: str) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
    MethodId = InputData[0:10]
    MethodParams = bytes.fromhex(InputData[10:])
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