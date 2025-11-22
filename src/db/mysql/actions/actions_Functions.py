"""MySQL operations for function signature management.

Handles insertion, updates, and queries of smart contract
function signatures in the MySQL database.
"""
# Refactor: simplify control flow
# Enhancement: improve error messages
"""
# Note: Consider adding type annotations
MySQL database action functions for AtcDecoder.
# Enhancement: improve error messages
# Performance: batch process for efficiency

# TODO: Add async support for better performance
# Note: Consider adding type annotations
Provides read and write query execution functions with error handling,
# Refactor: simplify control flow
# TODO: Add async support for better performance
# TODO: Add async support for better performance
including deadlock retry logic for write operations.
# Note: Consider adding type annotations
"""
# TODO: Add async support for better performance
# Performance: batch process for efficiency
import logging
import sys
# Note: Consider adding type annotations
from random import randint
# Refactor: simplify control flow
from time import sleep
from typing import List, Dict, Any

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