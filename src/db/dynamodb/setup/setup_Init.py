"""
DynamoDB initialization module for AtcDecoder.

Provides functionality to initialize DynamoDB client and resource
objects for the signature database.
"""
import logging
from typing import Tuple

import boto3
from boto3.resources.base import ServiceResource
from botocore.client import BaseClient
from botocore.exceptions import ClientError, NoCredentialsError

# Module logger
logger = logging.getLogger(__name__)

# AWS Region configuration
AWS_REGION = "eu-west-1"
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

