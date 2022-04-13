from eth_abi import abi

from src.api.api_fourbyte import SearchHexSignature
from src.db.dynamodb.query.query_table import QuerySigTable

def APIDecode(InputData):
    MethodId = InputData[0:10]
    MethodParams = bytes.fromhex(InputData[10:])
    HexFound, APIResults = SearchHexSignature(MethodId)
    if HexFound and len(APIResults) > 0:
        for Signature in APIResults["results"]:
            SplitFunction = Signature["text_signature"].split("(")
            FunctionName = SplitFunction[0]
            FunctionDef = SplitFunction[1].replace(")", "").split(",")
            try:
                DecodedInput = abi.decode(FunctionDef, MethodParams)
                return True, 'DB Decode Success', FunctionName, DecodedInput
            except:
                return False, 'DB Decode Failure', None, None