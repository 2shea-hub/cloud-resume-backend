import json
from lambda_function import lambda_handler

def test_lambda_returns_count():
    # Simulate an API Gateway event
    event = {
        "httpMethod": "GET",
        "path": "/count"
    }

    # Context can just be None for unit tests
    result = lambda_handler(event, None)

    # Convert JSON body to dict
    body = json.loads(result["body"])

    # Check basic structure
    assert "count" in body
    assert isinstance(body["count"], int)
