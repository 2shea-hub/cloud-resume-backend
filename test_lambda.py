import os
import json
import importlib
import boto3
from moto import mock_aws

@mock_aws
def test_counter_increments_and_returns_json():
    """
    Unit test for the Lambda visitor counter.
    Uses moto to stand up a fake DynamoDB so we don't hit real AWS.
    """

    # Ensure the Lambda code and boto3 default to the same region
    os.environ["AWS_DEFAULT_REGION"] = "eu-north-1"

    # Create the fake DynamoDB table and seed an item
    dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
    table = dynamodb.create_table(
        TableName="VisitorCount",
        KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    table.put_item(Item={"pk": "visitors", "count": 0})

    # Import Lambda AFTER the table exists so its module-level table reference resolves
    import lambda_function
    importlib.reload(lambda_function)

    # Simulate API Gateway event (path can be anything your function accepts)
    event = {"httpMethod": "GET", "path": "/count"}
    result = lambda_function.lambda_handler(event, None)

    # Basic response shape
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert "count" in body and isinstance(body["count"], int)

    # First call: 0 -> 1
    assert body["count"] == 1

    # Second call should increment again: 1 -> 2
    result2 = lambda_function.lambda_handler(event, None)
    body2 = json.loads(result2["body"])
    assert body2["count"] == 2

    # Optional CORS header check (only if your Lambda sets it)
    if "headers" in result:
        assert result["headers"].get("Access-Control-Allow-Origin", "*") == "*"
