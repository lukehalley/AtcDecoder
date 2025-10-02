"""
DynamoDB initialization module for AtcDecoder.

Provides functionality to initialize DynamoDB client and resource
objects for the signature database.
"""
from typing import Tuple

import boto3
from boto3.resources.base import ServiceResource
from botocore.client import BaseClient

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
    """
    # Creating the DynamoDB Client
    DynamodbClient = boto3.client('dynamodb', region_name=AWS_REGION)

    # Creating the DynamoDB Table Resource
    DynamodbResource = boto3.resource('dynamodb', region_name=AWS_REGION)

    return DynamodbResource, DynamodbClient

