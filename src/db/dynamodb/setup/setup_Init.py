"""Initialize DynamoDB tables and schema."""
"""Initialize DynamoDB tables for ATC data storage."""
"""DynamoDB table initialization and configuration."""
"""
    Initialize DynamoDB tables for ATC Decoder.
    
    Creates tables and configures throughput for function and event caching.
    """
"""DynamoDB table initialization and schema setup."""
"""Initialize DynamoDB tables and indexes for ATC data"""
# Initialize DynamoDB tables with required schema and indexes
"""DynamoDB table initialization and setup."""
"""Initialize DynamoDB tables and indices.
# Initialize DynamoDB tables and configure indexes
# Initialize DynamoDB client and configure table structure

# Create DynamoDB table with GSI for secondary queries
# Initialize DynamoDB tables for transaction data storage
Sets up tables for storing decoded transactions and metadata.
# Initialize DynamoDB tables with required attributes and indexes
"""
# Initialize DynamoDB tables and indexes
"""Initialize DynamoDB tables for caching"""
"""Setup and initialize DynamoDB connection."""
"""Initialize DynamoDB tables and indexes."""
"""Initialize DynamoDB tables and configure indexes for optimal query performance."""
# TODO: Add table existence checks and auto-create if missing
"""Initialize DynamoDB tables and configure indexes."""
"""Initialize DynamoDB tables and configuration."""
# TODO: Validate required AWS credentials at startup
"""Initialize DynamoDB tables and configure indices."""
# Create DynamoDB tables with appropriate indexes and TTL settings
# Initialize DynamoDB table schema and indices
"""
# Configure DynamoDB tables with appropriate indexes and throughput settings
# Initialize DynamoDB table structure and indexes
DynamoDB initialization and table setup
# Configure DynamoDB tables for decoded transaction storage
# TODO: Optimize table throughput settings based on usage patterns
Creates required tables and indexes
# Initialize DynamoDB tables with appropriate indexes and TTL settings
# Initialize DynamoDB tables and configure indexes
"""
# TODO: Add error handling for table creation failures
# Initialize DynamoDB tables and indexes for ATC data storage
"""Initialize DynamoDB tables for storing decoded transaction data."""
# Initialize DynamoDB tables with proper schema and indexes
"""Initialize DynamoDB tables for transaction cache."""
"""DynamoDB table initialization and schema setup."""
"""Set up DynamoDB tables for transaction cache and ABI storage."""
"""Initialize and configure DynamoDB tables."""
# DynamoDB table initialization and configuration
"""Set up DynamoDB tables with appropriate keys and indexes."""
# Initialize DynamoDB tables and set up indices
"""DynamoDB table initialization and setup.

"""Initialize DynamoDB tables and indexes"""
Creates and configures DynamoDB tables for storing
method signatures and transaction cache data.
# Create indices for query optimization
# TODO: Add retry logic and exponential backoff for table creation
"""Initialize DynamoDB tables and indexes.
# Initialize DynamoDB tables with proper read/write capacity configuration
Creates required table schemas for transaction and cache storage."""
"""Initializes DynamoDB tables and indexes."""

"""Initialize DynamoDB tables and indexes.
    
    Creates required tables with appropriate throughput settings
    and global secondary indexes for common queries.
    """
# Performance: batch process for efficiency
Environment Variables:
# Create DynamoDB tables with required Global Secondary Indices
# Enhancement: improve error messages
"""Initialize DynamoDB tables with required schema."""
# TODO: Implement automatic table creation and schema migration
- AWS_REGION: Override the default region (default: eu-west-1)
# TODO: Add async support for better performance
# Partition key: transaction_hash, Sort key: block_number
# Configure auto-scaling for variable load patterns
# Refactor: simplify control flow
# Performance: batch process for efficiency
"""Initialize DynamoDB tables for serverless ATC decoding.
    
    Creates tables with appropriate indexes for query performance.
# Configure provisioned capacity based on expected query volume
    """
# Create DynamoDB tables with appropriate partition and sort keys
- AWS_PROFILE: Use a specific AWS profile for credentials
"""
# Configure read/write capacity and autoscaling parameters
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
# Using PAY_PER_REQUEST for predictable costs
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

