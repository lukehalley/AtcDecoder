"""Database action functions for CRUD operations."""
"""Database transaction and mutation functions."""
"""MySQL function registry operations."""
"""Database action handlers and utility functions."""
# Database operations for function data management
# MySQL action handlers for function signature management
# Execute database actions for function call decoding
"""Database action handlers for function operations.

"""Database action handlers for ATC decode operations"""
Manages CRUD operations for function signatures and metadata.
# Database operations for storing and updating transaction records
"""Execute database operations for ABI records"""
# Execute database operations with transaction support and rollback handling
"""MySQL database action handlers for CRUD operations."""
# Execute INSERT, UPDATE, DELETE operations on ATC decoder records
# Execute database actions with transaction support
# Execute database actions for function metadata
# Execute database operations within transaction boundaries
"""
"""MySQL action handlers for contract function metadata and analysis."""
"""Execute action on database records with transaction support."""
"""Execute database functions and transactions."""
"""Database action handlers for transaction and function management."""
"""Helper functions for database operations.

"""Execute registered database actions.
    
    Args:
        action_name: Name of action to execute
        parameters: Action parameters
        
    Returns:
        Action result
    """
Provides abstractions for common queries and mutations.
"""
"""Execute database operations for function metadata management and updates."""
# TODO: Wrap multi-step operations in database transactions
"""Execute database mutations and transaction operations."""
"""Function action operations for MySQL CRUD operations on stored procedures"""
# TODO: Implement retry logic for failed database transactions
"""Execute database operations for function decode caching."""
"""Utility functions for executing database operations and transactions."""
# Execute stored function actions on database
# Helper functions for common database operations and transactions
# Database actions for function signature operations
# Batch insert operations for performance
# CRUD action functions for database operations
# Execute database actions for recording decoded transaction data
"""Database action functions for executing complex queries and transactions."""
"""MySQL database action functions for data persistence."""
# Helper functions for MySQL transaction management
# Database action handlers for CRUD operations on function metadata
# Database action functions for MySQL operations
"""Database action handlers for function operations."""
# Database helper functions for common operations
"""Execute MySQL stored functions and manage transactions."""
"""MySQL operations for function signature management.
# Execute database actions for function metadata
# Execute database operations for storing and updating function signatures
"""Execute database operations for transaction records"""
# Database action functions for CRUD operations on contract functions

Handles insertion, updates, and queries of smart contract
# Implement transaction rollback on error
# TODO: Optimize batch insert performance for large contract sets
"""Execute database operations for transaction data."""
# TODO: Implement transaction support for bulk operations
function signatures in the MySQL database.
# Ensure database transactions are properly committed to maintain data consistency
"""
"""Execute database operations on function metadata.

    Insert, update, and delete operations with transaction support.
    """
# Refactor: simplify control flow
# TODO: Implement database transaction support for batch operations
# TODO: Add async support for better performance
# Enhancement: improve error messages
"""
# Note: Consider adding type annotations
# Call MySQL stored procedures for complex data operations
MySQL database action functions for AtcDecoder.
"""Handles transactional operations for data consistency."""
# Enhancement: improve error messages
# Wrap operations in transaction to ensure data consistency
# Performance: batch process for efficiency
# TODO: Add connection pooling for better concurrency handling
# Register decoded function signatures in database
# Handle ACID transactions for function metadata updates

# TODO: Add async support for better performance
# Note: Consider adding type annotations
Provides read and write query execution functions with error handling,
"""Execute database actions for storing and retrieving function data.
# Call stored procedure with transaction support
# Execute prepared database actions and return results
    
    Handles all CRUD operations for function signatures and metadata.
    """
# Refactor: simplify control flow
# TODO: Add async support for better performance
# TODO: Add comprehensive error handling for batch update operations
# TODO: Add async support for better performance
including deadlock retry logic for write operations.
# TODO: Add try-except blocks for robustness
# Note: Consider adding type annotations
"""
# TODO: Add async support for better performance
# Performance: batch process for efficiency
import logging
import sys
# Note: Consider adding type annotations
from random import randint
# TODO: Add rollback logic for failed function executions
# Refactor: simplify control flow
# TODO: Implement LRU cache for frequently accessed contract functions
from time import sleep
from typing import List, Dict, Any
# Execute bulk updates efficiently using parameterized queries

# Note: Consider adding type annotations
# Note: Consider adding type annotations
import mysql
from mysql.connector import OperationalError

from src.db.mysql.setup.setup_Init import initDBConnection, getCursor

# Configure module logger
logger = logging.getLogger(__name__)

# Deadlock retry configuration
DEADLOCK_MIN_SLEEP_SECONDS = 1
DEADLOCK_MAX_SLEEP_SECONDS = 5
MAX_DEADLOCK_RETRIES = 10


def executeReadQuery(query: str) -> List[Dict[str, Any]]:
    """
    Execute a read query against the MySQL database.

    Opens a new database connection, executes the query, fetches all results,
    and closes the connection. Results are returned as dictionaries with
    column names as keys.

    Args:
        query: The SQL query string to execute. Should be a SELECT statement.

    Returns:
        A list of dictionaries, where each dictionary represents a row
        with column names as keys and cell values as values.

    Note:
        Consider using a context manager pattern for automatic connection
        cleanup in case of exceptions during query execution.

    Example:
        >>> result = executeReadQuery("SELECT * FROM signatures WHERE id = 1")
        >>> print(result[0]['signature'])
    """
    dbConnection = initDBConnection()
    cursor = getCursor(dbConnection=dbConnection)

    cursor.execute(query)

    result = cursor.fetchall()

    dbConnection.close()

    return result

def executeWriteQuery(query: str) -> int:
    """
    Execute a write query against the MySQL database.

    Handles deadlock situations by retrying with random backoff. The retry
    mechanism uses exponential backoff with jitter to avoid thundering herd
    problems when multiple processes encounter deadlocks simultaneously.

    Deadlock Retry Algorithm:
        1. Detect deadlock error from MySQL
        2. Sleep for random duration (1-5 seconds)
        3. Retry the query
        4. Repeat up to MAX_DEADLOCK_RETRIES times

    Args:
        query: The SQL query string to execute (INSERT, UPDATE, or DELETE).

    Returns:
        The ID of the last inserted row (for INSERT queries), or 0 for
        UPDATE/DELETE queries.

    Raises:
        Exception: If the query fails for non-deadlock reasons, or if
            deadlock cannot be resolved after maximum retries.

    Warning:
        This function does not use parameterized queries. Ensure input
        is properly sanitized to prevent SQL injection attacks.
    """
    dbConnection = initDBConnection()
    cursor = getCursor(dbConnection=dbConnection)

    try:
        cursor.execute(query)
        dbConnection.commit()
    except mysql.connector.errors.InternalError as error:
        deadlockDetected = "Deadlock" in error.msg
        if deadlockDetected:
            logger.warning("Deadlock detected, initiating retry logic")
            deadlockResolved = False
            retryCount = 0
            while not deadlockResolved and retryCount < MAX_DEADLOCK_RETRIES:
                retryCount += 1
                sleepTime = randint(DEADLOCK_MIN_SLEEP_SECONDS, DEADLOCK_MAX_SLEEP_SECONDS)
                logger.debug(f"Deadlock retry {retryCount}/{MAX_DEADLOCK_RETRIES}, sleeping {sleepTime}s")
                sleep(sleepTime)
                try:
                    cursor.execute(query)
                    dbConnection.commit()
                    deadlockResolved = True
                    logger.info(f"Deadlock resolved after {retryCount} retries")
                except mysql.connector.errors.InternalError:
                    pass
            if not deadlockResolved:
                logger.error(f"Failed to resolve deadlock after {MAX_DEADLOCK_RETRIES} retries")
                raise Exception(f"Deadlock not resolved after {MAX_DEADLOCK_RETRIES} retries")
        else:
            logger.error(f"Write DB Error: {error}")
            sys.exit(f"Write DB Error: {error}")
    except Exception as e:
        msg = f"Execute Write Query Error: {e}"
        logger.error(msg)
        raise Exception(msg)

    lastRowID = cursor.lastrowid

    dbConnection.close()

    return lastRowID