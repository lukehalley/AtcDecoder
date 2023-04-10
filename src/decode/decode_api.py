import json

from eth_abi import abi

from src.api.api_fourbyte import SearchHexSignature
from src.db.dynamodb.query.query_table import QuerySigTable

def APIDecode(InputData):
    MethodId = InputData[0:10]
    MethodParams = bytes.fromhex(InputData[10:])
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

            except:
                continue
        if len(ResultsToReturn) > 0:
            return True, 'DB Decode Success', ResultsToReturn
        else:
            return False, 'DB Decode Failure', None
    else:
        return False, 'DB Decode Failure', None