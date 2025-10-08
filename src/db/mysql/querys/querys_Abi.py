"""
ABI query module for retrieving contract ABIs from the database.

Provides functions to fetch ABI records by their database identifiers.
"""
import logging
from typing import Dict, Any

from src.db.mysql.actions.actions_Functions import executeReadQuery

# Module logger
logger = logging.getLogger(__name__)


def getAbiByDbId(abiDbId: int) -> Dict[str, Any]:
    """
    Retrieve a contract ABI by its database ID.

    Args:
        abiDbId: The unique database identifier for the ABI record.

    Returns:
        The ABI record dictionary containing the contract ABI data.

    Raises:
        Exception: If no ABI found or multiple ABIs found for the given ID.
    """

    query = f"SELECT abis.* " \
            f"FROM abis " \
            f"WHERE abis.abi_id = {abiDbId}"

    result = executeReadQuery(
        query=query
    )

    if len(result) < 1:
        raise Exception(f"No Abi Match For Id {abiDbId}")
    if len(result) == 1:
        return result[0]
    else:
        raise Exception(f"More Than One Abi Matches For Id {abiDbId}")

