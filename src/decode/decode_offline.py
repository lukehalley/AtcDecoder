"""
Offline transaction input decoder for common DEX swap functions.

This module provides hardcoded function signatures for common DEX operations,
allowing offline decoding without database or API lookups. Supports major
DEX routers like Uniswap, PancakeSwap, and SushiSwap.
"""
from typing import Any, Dict, List, Optional, Tuple

from eth_abi import abi

# Type alias for function parameter definition (type, name)
FunctionParam = Tuple[str, str]
FunctionParams = List[FunctionParam]

SwapFunctions: Dict[str, FunctionParams] = {
    "swapExactTokensForTokens": [
        ('uint', 'amountIn'),
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapTokensForExactTokens": [
        ('uint', 'amountOut'),
        ('uint', 'amountInMax'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapExactETHForTokens": [
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapTokensForExactETH": [
        ('uint', 'amountOut'),
        ('uint', 'amountInMax'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapExactTokensForETH": [
        ('uint', 'amountIn'),
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapETHForExactTokens": [
        ('uint', 'amountOut'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapExactTokensForTokensSupportingFeeOnTransferTokens": [
        ('uint', 'amountIn'),
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapExactETHForTokensSupportingFeeOnTransferTokens": [
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ],
    "swapExactTokensForETHSupportingFeeOnTransferTokens": [
        ('uint', 'amountIn'),
        ('uint', 'amountOutMin'),
        ('address[]', 'path'),
        ('address', 'to'),
        ('uint', 'deadline')
    ]
}

# Method ID slice indices (first 4 bytes as hex with 0x prefix)
METHOD_ID_START = 0
METHOD_ID_END = 10

# Response message constants
MSG_OFFLINE_DECODE_SUCCESS = MSG_OFFLINE_DECODE_SUCCESS
MSG_OFFLINE_DECODE_FAILURE = MSG_OFFLINE_DECODE_FAILURE

# Method ID to function name mapping
SwapMethods: Dict[str, str] = {
    "0x38ed1739": "swapExactTokensForTokens",
    "0x7ff36ab5": "swapExactETHForTokens",
    "0x791ac947": "swapExactTokensForETHSupportingFeeOnTransferTokens",
    "0x4a25d94a": "swapTokensForExactETH",
    "0xfb3bdb41": "swapETHForExactTokens",
    "0xb6f9de95": "swapExactETHForTokensSupportingFeeOnTransferTokens",
    "0x5c11d795": "swapExactTokensForTokensSupportingFeeOnTransferTokens",
    "0x8803dbee": "swapTokensForExactTokens",
    "0x4e71d92d": "claim",
    "0x18cbafe5": "swapExactTokensForETH",
    "0x1d85bf03": "bugNFT",
    "0xded9382a": "removeLiquidityETHWithPermit",
    "0xe0f4e5b2": "swapForBNB",
    "0xa9059cbb": "transfer",
    "0x095ea7b3": "approve",
    "0x6c197ff5": "sell",
    "0x7f8661a1": "exit"
}

def OfflineDecode(InputData: str) -> Tuple[bool, str, Optional[str], Optional[Dict[str, Any]]]:
    """
    Decode transaction input data using hardcoded function signatures.

    Args:
        InputData: Raw transaction input data as hex string.

    Returns:
        Tuple of (success, message, function_name, decoded_params).
    """
    MethodId = InputData[METHOD_ID_START:METHOD_ID_END]
    MethodParams = bytes.fromhex(InputData[METHOD_ID_END:])
    if MethodId in SwapMethods:
        MethodName = SwapMethods[MethodId]
        FunctionArgs = SwapFunctions[MethodName]
        try:
            ArgTypes = [FunctionArg[0] for FunctionArg in FunctionArgs]
            DecodedInput = abi.decode(ArgTypes, MethodParams)
            DecodedMapped = {}
            for FunctionArg in FunctionArgs:
                FunctionName = FunctionArg[1]
                Index = FunctionArgs.index(FunctionArg)
                DecodedMapped[FunctionName] = DecodedInput[Index]
            return True, MSG_OFFLINE_DECODE_SUCCESS, MethodName, DecodedMapped
        except Exception:
            return False, MSG_OFFLINE_DECODE_FAILURE, None, None
    else:
        for SwapFunction in SwapFunctions:
            FunctionArgs = SwapFunctions[SwapFunction]
            try:
                ArgTypes = [FunctionArg[0] for FunctionArg in FunctionArgs]
                DecodedInput = abi.decode(ArgTypes, MethodParams)
                DecodedMapped = {}
                for FunctionArg in FunctionArgs:
                    FunctionName = FunctionArg[1]
                    Index = FunctionArgs.index(FunctionArg)
                    DecodedMapped[FunctionName] = DecodedInput[Index]
                return True, MSG_OFFLINE_DECODE_SUCCESS, SwapFunction, DecodedMapped
            except Exception:
                continue
        return False, MSG_OFFLINE_DECODE_FAILURE, None, None