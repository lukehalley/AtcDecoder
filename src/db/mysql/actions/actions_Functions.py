"""MySQL operations for function signature management.

Handles insertion, updates, and queries of smart contract
function signatures in the MySQL database.
"""
"""
MySQL database action functions for AtcDecoder.

Provides read and write query execution functions with error handling,
including deadlock retry logic for write operations.
"""
import logging
import sys
from random import randint
from time import sleep
from typing import List, Dict, Any

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

    Args:
        query: The SQL query string to execute.

    Returns:
        A list of rows returned by the query.
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

    Handles deadlock situations by retrying with random backoff.

    Args:
        query: The SQL query string to execute.

    Returns:
        The ID of the last inserted row.

    Raises:
        Exception: If the query fails for non-deadlock reasons.
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