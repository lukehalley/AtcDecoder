"""Execute database mutations and transaction operations."""
"""Function action operations for MySQL CRUD operations on stored procedures"""
"""Execute database operations for function decode caching."""
"""Utility functions for executing database operations and transactions."""
# Database actions for function signature operations
# CRUD action functions for database operations
"""Database action functions for executing complex queries and transactions."""
"""MySQL database action functions for data persistence."""
# Database action handlers for CRUD operations on function metadata
"""Database action handlers for function operations."""
"""Execute MySQL stored functions and manage transactions."""
"""MySQL operations for function signature management.
# Execute database actions for function metadata
# Execute database operations for storing and updating function signatures
"""Execute database operations for transaction records"""
# Database action functions for CRUD operations on contract functions

Handles insertion, updates, and queries of smart contract
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