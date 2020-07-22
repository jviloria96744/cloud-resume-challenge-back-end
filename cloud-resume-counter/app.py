import os
import json
import boto3

dynamodb = boto3.resource("dynamodb", os.environ["AWS_REGION"])
table = dynamodb.Table(os.environ["TABLE_NAME"])


def increment_visit_count(website):
    response = table.update_item(
        Key={
            "Website": website,
        },
        UpdateExpression="ADD Visit_Count :inc",
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW"
    )

    return response


def lambda_handler(event, context):
    """
    Parameters
    ----------
    event: dict, required
        {
            "body": {
                "Website": [website name]
            }
        }

    context: object, required

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        {
            "statusCode": [statusCode],
            "body": {
                "count": [count]
            }
        }
    """

    data = json.loads(event["body"])

    update_item = increment_visit_count(data["Website"])

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin":"*"},
        "body": json.dumps({
            "count": int(update_item["Attributes"]["Visit_Count"])
        }),
    }
