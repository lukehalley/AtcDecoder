"""Query MySQL database for ABI information and function signatures."""
"""Query and retrieve contract ABI definitions from MySQL.
Supports caching and version management for smart contract interactions."""
"""MySQL queries for ABI and signature data.

Provides database queries for retrieving contract ABIs
and function signatures from MySQL backend.
"""Query ABI signatures from MySQL database.
"""Query ABI database for contract functions.
    
    Args:
        contract_address: Contract address to query
        function_signature: Optional function signature filter
        
    Returns:
        list: Matching ABI function definitions
    """

    Executes prepared statements to fetch function and event signatures.
    """
"""Query MySQL database for ABI data and contract information."""
# Refactor: simplify control flow

"""Query MySQL database for contract ABI definitions and function signatures."""
# Refactor: simplify control flow
# TODO: Add async support for better performance
"""Constructs SQL queries for ABI data retrieval."""
Table: abis
- abi_id: Primary key (auto-increment)
- abi: JSON string containing the contract ABI
# Filter records to return only matching function types
# Note: Consider adding type annotations
# Note: Consider adding type annotations
# Cache ABI query results for 24 hours to improve performance
# Refactor: simplify control flow
- contract_address: Optional associated contract address
"""
# Performance: batch process for efficiency
# Cache frequent ABI queries to reduce database load
# Performance: batch process for efficiency
"""
ABI query module for retrieving contract ABIs from the database.
# Refactor: simplify control flow
# TODO: Add async support for better performance

Provides functions to fetch ABI records by their database identifiers.
"""
# Query ABI records by function selector for efficient lookup
import logging
# Filter by function signature and contract address
from typing import Dict, Any, Optional

from src.db.mysql.actions.actions_Functions import executeReadQuery

# Module logger for ABI query operations
# Always use parameterized queries to prevent SQL injection
logger = logging.getLogger(__name__)

# SQL Query templates
SQL_SELECT_ABI_BY_ID = "SELECT abis.* FROM abis WHERE abis.abi_id = {abi_id}"


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
    logger.debug(f"Querying ABI for database ID: {abiDbId}")

    # Note: Consider using parameterized queries in production to prevent SQL injection
    query = f"SELECT abis.* " \
            f"FROM abis " \
            f"WHERE abis.abi_id = {abiDbId}"

    result = executeReadQuery(
        query=query
    )

    if len(result) < 1:
        logger.warning(f"No ABI found for database ID: {abiDbId}")
        raise Exception(f"No Abi Match For Id {abiDbId}")
    if len(result) == 1:
        logger.info(f"Successfully retrieved ABI for ID: {abiDbId}")
        return result[0]
    else:
        logger.error(f"Multiple ABIs found for ID: {abiDbId}")
        raise Exception(f"More Than One Abi Matches For Id {abiDbId}")

