from web3 import Web3

from src.db.querys.querys_Abi import getAbiByDbId
from src.decode.decode_abi import decode_tx
from src.decode.decode_offline import OfflineDecode


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

    # Try Offline Decode
    DecodeSuccessful, DecodeMsg, FunctionName, FunctionParams = OfflineDecode(TransactionDetails["input"])

    # If That Fails Try ABI Decode
    if not DecodeSuccessful:
        DecodeSuccessful, DecodeMsg, FunctionName, FunctionParams = decode_tx(ContractHash, TransactionDetails["input"], Abi)

    # Collect Results
    if DecodeSuccessful:

        DecodeBody = {
            "function": FunctionName,
            "args": FunctionParams
        }

        ReturnBody = {"statusCode": 200, "msg": DecodeMsg, "body": DecodeBody}

    else:

        ReturnBody = {"statusCode": 400, "msg": DecodeMsg, "body": {}}


    return ReturnBody

# GOOD
# args = {
#   "rpc_url": "https://eth.llamarpc.com",
#   "tx_hash": "0xe8f26d91a2a8af6747670d8fde7ccf188539582d03e08441ce0228d057c0ac70",
#   "contract_hash": "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5",
#   "contract_abi_db_id": 362
# }

# BAD
args = {
  "rpc_url": "https://eth.llamarpc.com",
  "tx_hash": "0x28150100bd1a9217b2edd74222fb3cc01ec0134a898601005e78b51d74b9e6b7",
  "contract_hash": "0x84D99Aa569D93a9CA187D83734c8C4a519c4e9b1",
  "contract_abi_db_id": 394
}

invoke(event=args, context="")