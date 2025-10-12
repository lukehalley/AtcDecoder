"""
MySQL database connection initialization module.

Provides functions to establish secure database connections using
AWS Secrets Manager for credential management.
"""
import json
import os
from typing import Any

import mysql.connector
from aws_lambda_powertools.utilities import parameters
from mysql.connector import errorcode
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

# Environment variable names for database configuration
ENV_DB_ENDPOINT = "DB_ENDPOINT"
ENV_DB_NAME = "DB_NAME"

# AWS Secrets Manager secret name
AWS_SECRET_NAME = "ATC_DB_Credentials"


def initDBConnection():
    """
    Initialize a MySQL database connection using AWS Secrets Manager.

    Retrieves credentials from AWS Secrets Manager and establishes
    a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection object.

    Raises:
        Exception: If authentication fails or database doesn't exist.
    """
    DB_SECRET = json.loads(parameters.get_secret("ATC_DB_Credentials"))
    DB_USER = DB_SECRET["username"]
    DB_PASSWORD = DB_SECRET["password"]
    DB_ENDPOINT = os.getenv("DB_ENDPOINT")
    DB_NAME = os.getenv("DB_NAME")

    try:
        dbConnection = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_ENDPOINT,
            database=DB_NAME
        )
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        raise Exception("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        raise Exception("Database does not exist")
      else:
        raise Exception(err)
    else:
        return dbConnection

def getCursor(dbConnection, dictionary=True, buffered=True):
    """
    Get a cursor object for executing database queries.

    Args:
        dbConnection: The MySQL database connection object.
        dictionary: If True, return rows as dictionaries. Defaults to True.
        buffered: If True, use a buffered cursor. Defaults to True.

    Returns:
        A MySQL cursor object configured with the specified options.
    """
    return dbConnection.cursor(dictionary=dictionary, buffered=buffered)