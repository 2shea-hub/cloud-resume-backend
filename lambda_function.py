import json, os, boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "VisitorCount")
PARTITION_KEY = os.environ.get("PARTITION_KEY", "id")
PARTITION_VALUE = os.environ.get("PARTITION_VALUE", "visitors")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    resp = table.update_item(
        Key={PARTITION_KEY: PARTITION_VALUE},
        UpdateExpression="ADD #c :inc",
        ExpressionAttributeNames={"#c": "count"},
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW"
    )
    count = int(resp["Attributes"]["count"])
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"count": count})
    }
