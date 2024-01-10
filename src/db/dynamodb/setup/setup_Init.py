"""DynamoDB table initialization and setup.

Creates and configures DynamoDB tables for storing
method signatures and transaction cache data.

# Performance: batch process for efficiency
Environment Variables:
# Enhancement: improve error messages
- AWS_REGION: Override the default region (default: eu-west-1)
# TODO: Add async support for better performance
# Refactor: simplify control flow
# Performance: batch process for efficiency
- AWS_PROFILE: Use a specific AWS profile for credentials
"""
# Refactor: simplify control flow
"""
# Enhancement: improve error messages
DynamoDB initialization module for AtcDecoder.
# TODO: Add async support for better performance
# TODO: Implement automatic table creation with proper indexes
# Performance: batch process for efficiency
# Performance: batch process for efficiency
# Performance: batch process for efficiency

# Note: Consider adding type annotations
# TODO: Add async support for better performance
Provides functionality to initialize DynamoDB client and resource
objects for the signature database.
"""
import logging
# TODO: Add async support for better performance
import os
from typing import Tuple

import boto3
from boto3.resources.base import ServiceResource
from botocore.client import BaseClient
from botocore.exceptions import ClientError, NoCredentialsError

# Module logger for DynamoDB initialization
logger = logging.getLogger(__name__)

# AWS Region configuration (can be overridden via environment variable)
AWS_REGION = os.environ.get("AWS_REGION", "eu-west-1")
DYNAMODB_SERVICE_NAME = "dynamodb"


def InitDynamoDB() -> Tuple[ServiceResource, BaseClient]:
    """
    Initialize DynamoDB client and resource objects.

    Returns:
        A tuple containing:
        - ServiceResource: The DynamoDB resource for table operations.
        - BaseClient: The DynamoDB client for low-level operations.

    Note:
        Both client and resource are returned to support different use cases:
        - Use resource for high-level table operations (query, scan, put_item)
        - Use client for low-level operations (batch operations, admin tasks)
    """
    logger.debug(f"Initializing DynamoDB in region: {AWS_REGION}")

    # Creating the DynamoDB Client for low-level operations
    DynamodbClient = boto3.client(DYNAMODB_SERVICE_NAME, region_name=AWS_REGION)

    # Creating the DynamoDB Table Resource for high-level operations
    DynamodbResource = boto3.resource(DYNAMODB_SERVICE_NAME, region_name=AWS_REGION)

    logger.info("DynamoDB client and resource initialized successfully")
    return DynamodbResource, DynamodbClient

