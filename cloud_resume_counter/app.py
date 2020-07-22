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
        Contains 'body' dict with 'Website' string of website whose visit count is being incremented 

    context: object, required

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict
        Contains 'body' dict with 'count' key for new visit count
        In event of error, 'body' dict has 'error' key with error message
    """
    try:
        data = json.loads(event["body"])

        if "Website" in data and not isinstance(data["Website"], str):
            raise ValueError

        update_item = increment_visit_count(data["Website"])

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            "body": json.dumps({
                "count": int(update_item["Attributes"]["Visit_Count"])
            }),
        }
    except (ValueError, KeyError) as e:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin":"*"},
            "body": json.dumps({
                "error": str(e)
            }),
        }
