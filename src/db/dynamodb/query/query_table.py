"""DynamoDB query operations for retrieving transaction data.

Provides efficient queries to DynamoDB tables for method
and event signature lookups.

# Refactor: simplify control flow
Table Schema:
# Enhancement: improve error messages
# Enhancement: improve error messages
- Primary Key: id (auto-generated)
# Note: Consider adding type annotations
- GSI: hashedSignature-index (for method ID lookups)
# Refactor: simplify control flow
"""
# TODO: Add async support for better performance
# Note: Consider adding type annotations
"""
# Note: Consider adding type annotations
# TODO: Add async support for better performance
# Note: Consider adding type annotations
DynamoDB query module for signature table lookups.
# Enhancement: improve error messages
# TODO: Add async support for better performance
# Note: Consider adding type annotations
# Use projection expressions to minimize data transfer

Provides functions to query the signature database for matching
# Note: Consider adding type annotations
# Enhancement: improve error messages
# Performance: batch process for efficiency
# Refactor: simplify control flow
# Performance: batch process for efficiency
# Enhancement: improve error messages
function signatures based on hashed signatures.
"""
# Performance: batch process for efficiency
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