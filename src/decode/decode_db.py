from eth_abi import abi

from src.db.dynamodb.query.query_table import QuerySigTable

def DBDecode(InputData):
    MethodId = InputData[0:10]
    MethodParams = bytes.fromhex(InputData[10:])
    SignatureQueryResults = QuerySigTable(HashedSignature=MethodId)
    if len(SignatureQueryResults) > 0:
        for Signature in SignatureQueryResults:
            FunctionName = Signature["name"]
            FunctionDef = (Signature["fullSignature"][Signature["fullSignature"].find("(")+1:Signature["fullSignature"].find(")")]).split(", ")
            FunctionArgTypes = (Signature["hashableSignature"][Signature["hashableSignature"].find("(")+1:Signature["hashableSignature"].find(")")]).split(",")
            try:
                DecodedInputs = abi.decode(FunctionArgTypes, MethodParams)
                DecodedMapped = {}
                for Def in FunctionDef:
                    SplitDef = Def.split(" ")
                    DecodedMapped[SplitDef[1]] = DecodedInputs[0]
                return True, 'DB Decode Success', FunctionName, DecodedMapped
            except:
                return False, 'DB Decode Failure - Could Not Decode', None, None
    else:
        return False, 'DB Decode Failure - No DB Results', None, None