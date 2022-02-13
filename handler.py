import json
from web3 import Web3
from src.decode import decode_tx


def invoke(event, context):

    # Collect Args
    RPCUrl = event["rpc_url"]
    TxHash = event["tx_hash"]
    ContractHash = event["contract_hash"]
    ContractAbi = json.dumps(event["contract_abi"])

    # Connect To RPC
    web3Instance = Web3(Web3.HTTPProvider(RPCUrl))

    # Get Transaction
    TransactionDetails = web3Instance.eth.get_transaction(TxHash)

    # Load Contract ABI
    LoadedABI = json.loads(ContractAbi)
    MinifiedAbi = json.dumps(LoadedABI, separators=(',', ':'))

    # Invoke Decode
    DecodeSuccessful, DecodeMsg, FunctionName, FunctionParams, TargetSchema = decode_tx(ContractHash, TransactionDetails["input"], MinifiedAbi)

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