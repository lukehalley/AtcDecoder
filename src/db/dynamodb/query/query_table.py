"""
DynamoDB query module for signature table lookups.

Provides functions to query the signature database for matching
function signatures based on hashed signatures.
"""
from typing import List, Dict, Any

from boto3.dynamodb.conditions import Key

from src.db.dynamodb.setup.setup_Init import InitDynamoDB

# Table configuration constants
SIGNATURE_TABLE_NAME = "atc_sig_db"
SIGNATURE_INDEX_NAME = "hashedSignature-index"


def QuerySigTable(HashedSignature: str) -> List[Dict[str, Any]]:
    """
    Query the signature table for matching function signatures.

    Args:
        HashedSignature: The hashed signature to search for (e.g., '0x38ed1739').

    Returns:
        A list of matching signature records from the database.
    """
    # Init DynamoDB Client
    DynamodbResource, DynamodbClient = InitDynamoDB()

    # Init Table Object
    DynamodbTable = DynamodbResource.Table(SIGNATURE_TABLE_NAME)

    # Execute Query
    QueryResponse = DynamodbTable.query(
        IndexName=SIGNATURE_INDEX_NAME,
        KeyConditionExpression=Key('hashedSignature').eq(HashedSignature)
    )

    return QueryResponse["Items"]