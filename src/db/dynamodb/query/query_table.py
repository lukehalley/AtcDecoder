"""DynamoDB query operations for retrieving transaction data.

Provides efficient queries to DynamoDB tables for method
and event signature lookups.

Table Schema:
- Primary Key: id (auto-generated)
- GSI: hashedSignature-index (for method ID lookups)
"""
"""
DynamoDB query module for signature table lookups.

Provides functions to query the signature database for matching
function signatures based on hashed signatures.
"""
import logging
from typing import List, Dict, Any

# Module logger for DynamoDB query operations
logger = logging.getLogger(__name__)

from boto3.dynamodb.conditions import Key

from src.db.dynamodb.setup.setup_Init import InitDynamoDB

# Table configuration constants
SIGNATURE_TABLE_NAME = "atc_sig_db"
SIGNATURE_INDEX_NAME = "hashedSignature-index"
DEFAULT_QUERY_LIMIT = 100


def QuerySigTable(HashedSignature: str) -> List[Dict[str, Any]]:
    """
    Query the signature table for matching function signatures.

    Args:
        HashedSignature: The hashed signature to search for (e.g., '0x38ed1739').

    Returns:
        A list of matching signature records from the database.
    """
    logger.debug(f"Querying signature table for: {HashedSignature}")

    # Init DynamoDB Client
    DynamodbResource, DynamodbClient = InitDynamoDB()

    # Init Table Object
    DynamodbTable = DynamodbResource.Table(SIGNATURE_TABLE_NAME)

    # Execute Query
    QueryResponse = DynamodbTable.query(
        IndexName=SIGNATURE_INDEX_NAME,
        KeyConditionExpression=Key('hashedSignature').eq(HashedSignature)
    )

    results = QueryResponse["Items"]
    logger.info(f"Found {len(results)} matching signatures for {HashedSignature}")
    return results