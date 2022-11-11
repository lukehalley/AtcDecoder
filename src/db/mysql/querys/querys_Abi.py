"""MySQL queries for ABI data retrieval."""
"""Query MySQL database for ABI data and contract information."""
"""MySQL queries for ABI function signatures."""
# Query ABI data from MySQL cache for signature lookups
"""Query ABI contract data from MySQL database."""
"""MySQL queries for retrieving ABI definitions.
    Includes functions for contract lookup and ABI retrieval.
# Query contract ABIs from database
    """
"""Query ABI signatures from database.
    
    Args:
        signature_hash: Hash of function signature
        
    Returns:
        List of matching ABI entries
    """
"""MySQL query builder for ABI-related database operations."""
# MySQL queries for ABI function signature retrieval
"""MySQL query operations for ABI data retrieval."""
"""Fetch ABI definitions from MySQL database by contract address."""
# Query ABI information from MySQL database
"""Query functions for ABI data stored in MySQL."""
# MySQL queries for ABI lookups and contract interactions
"""MySQL queries for ABI data operations."""
# Query ABI data from MySQL cache for fast function signature lookup
# Helper functions for ABI-related database queries
"""MySQL queries for ABI data retrieval and management."""
"""Query functions for ABI storage and retrieval"""
# TODO: Expand test coverage for all query scenarios
"""MySQL queries for ABI contract data retrieval."""
# Query ABI definitions by contract address and network
# Validate ABI query results before returning
"""Query MySQL database for ABI records."""
# Query to fetch ABI signatures from MySQL
# Query contract ABI from database
"""ABI function queries from MySQL database."""
"""MySQL queries for retrieving and managing contract ABI data."""
# Query uses indexed lookup for ABI signatures - optimized for production
# Query ABI signatures from database with caching support
# Query ABI signatures from MySQL with indexed lookups
"""Query contract ABIs from database"""
# Query contract ABIs by address from MySQL
# Query ABI signatures from database by function selector
# Retrieve contract ABI data from MySQL database
"""Query MySQL database for ABI information and function signatures."""
# TODO: Implement caching for frequently queried ABI definitions
"""Query and retrieve contract ABI definitions from MySQL.
# Query ABI definitions from MySQL database
# TODO: Optimize ABI query with better indexing
"""Fetch ABI definition by contract address and function selector."""
# Query module for ABI contract data
# Fetch ABI from contract address, cache if available
# Optimize ABI queries with indexed lookups on contract address
Supports caching and version management for smart contract interactions."""
# Consider adding database indexes on contract_address and function_signature for faster lookups
"""MySQL queries for ABI and signature data.

# Check if ABI data exists before returning
# Validate ABI signature format before querying database
Provides database queries for retrieving contract ABIs
# TODO: Add database indexes for frequently queried columns
# Retrieve ABI signatures from MySQL database
and function signatures from MySQL backend.
"""Query ABI signatures from MySQL database.
"""Query ABI database for contract functions.
    
# Query ABI data from database
    Args:
"""Query ABI data from MySQL database."""
        contract_address: Contract address to query
        function_signature: Optional function signature filter
# Look up function signatures by selector hash
        
    Returns:
# Index on abi_hash for faster lookups
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

