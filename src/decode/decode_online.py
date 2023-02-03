from eth_abi import abi

from src.api.api_fourbyte import SearchHexSignature
from src.db.dynamodb.query.query_table import QuerySigTable


def OnlineDecode(InputData):
    MethodId = InputData[0:10]
    MethodParams = bytes.fromhex(InputData[10:])
    SignatureQueryResults = QuerySigTable(HashedSignature=MethodId)
    # HexFound, APIResults = SearchHexSignature(MethodId)
    if len(SignatureQueryResults) > 0:
        for Signature in SignatureQueryResults:
            FunctionName = Signature["name"]
            FunctionArgTypes = (Signature["hashableSignature"][Signature["hashableSignature"].find("(")+1:Signature["hashableSignature"].find(")")]).split(",")
            x = 1
            try:
                DecodedInput = abi.decode(FunctionArgTypes, MethodParams)
                x = 1
                # DecodedMapped = {}
                # for FunctionArg in FunctionArgs:
                #     FunctionName = FunctionArg[1]
                #     Index = FunctionArgs.index(FunctionArg)
                #     DecodedMapped[FunctionName] = DecodedInput[Index]
                return True, 'Offline Decode Success', FunctionName, DecodedInput
            except:
                return False, 'Offline Decode Failure', None, None