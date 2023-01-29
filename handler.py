from web3 import Web3

from src.db.querys.querys_Abi import getAbiByDbId
from src.decode.decode import decode_tx

def invoke(event, context):

    # Collect Args
    RPCUrl = event["rpc_url"]
    TxHash = event["tx_hash"]
    ContractHash = event["contract_hash"]
    ContractAbiDbId = int(event["contract_abi_db_id"])

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
#   "rpc_url": "https://eth.llamarpc.com",
#   "tx_hash": "0xe8f26d91a2a8af6747670d8fde7ccf188539582d03e08441ce0228d057c0ac70",
#   "contract_hash": "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5",
#   "contract_abi_db_id": 362
# }
#
# invoke(event=args, context="")