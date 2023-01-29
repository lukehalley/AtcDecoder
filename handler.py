from web3 import Web3

from src.db.querys.querys_Abi import getAbiByDbId
from src.decode.decode import decode_tx


def invoke(event, context):

    # Collect Args
    RPCUrl = event["rpc_url"]
    TxHash = event["tx_hash"]
    ContractHash = event["contract_hash"]
    ContractAbiDbId = int(event["contract_db_id"])

    # Get ABI From DB
    AbiFromDB = getAbiByDbId(ContractAbiDbId)
    Abi = AbiFromDB["abi"]

    # Connect To RPC
    web3Instance = Web3(Web3.HTTPProvider(RPCUrl))

    # Get Transaction
    TransactionDetails = web3Instance.eth.get_transaction(TxHash)

    # Invoke Decode
    DecodeSuccessful, DecodeMsg, FunctionName, FunctionParams, TargetSchema = decode_tx(ContractHash, TransactionDetails["input"], Abi)

    # Collect Results
    if DecodeSuccessful:

        DecodeBody = {
            "function": FunctionName,
            "args": FunctionParams,
            "schema": TargetSchema
        }

        ReturnBody = {"statusCode": 200, "msg": DecodeMsg, "body": DecodeBody}

    else:

        ReturnBody = {"statusCode": 400, "msg": DecodeMsg, "body": {}}


    return ReturnBody

# args = {
#   "rpc_url": "https://rpc.ankr.com/eth",
#   "tx_hash": "0xe71ee019cf81ae09fa237b0a1f066695b4757e3bceca4da0f524b55d5ba4aefa",
#   "contract_hash": "0xEfF92A263d31888d860bD50809A8D171709b7b1c",
#   "contract_db_id": 339
# }
#
# invoke(event=args, context="")