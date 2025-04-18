"""
MySQL database action functions for AtcDecoder.

Provides read and write query execution functions with error handling,
including deadlock retry logic for write operations.
"""
import sys
from random import randint
from time import sleep

import mysql
from mysql.connector import OperationalError

from src.db.mysql.setup.setup_Init import initDBConnection, getCursor


def executeReadQuery(query):
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

def executeWriteQuery(query):
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
            deadlockResolved = False
            while not deadlockResolved:
                sleep(randint(1, 5))
                try:
                    cursor.execute(query)
                    dbConnection.commit()
                    deadlockResolved = True
                except mysql.connector.errors.InternalError:
                    pass
        else:
            sys.exit(f"Write DB Error: {error}")
    except Exception as e:
        msg = f"Execute Write Query Error: {e}"
        raise Exception(msg)

    lastRowID = cursor.lastrowid

    dbConnection.close()

    return lastRowID