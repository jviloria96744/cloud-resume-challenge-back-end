import os
import json
import logging
import boto3
from pythonjsonlogger import jsonlogger


dynamodb = boto3.resource("dynamodb", os.environ["AWS_REGION"])
table = dynamodb.Table(os.environ["TABLE_NAME"])


def setup_logging(log_level):
    logger = logging.getLogger()
 
    # Testing showed lambda sets up one default handler. If there are more,
    # something has changed and we want to fail so an operator can investigate.

    # This line is causing the unit tests to fail
    if os.environ["TABLE_NAME"] != "TEST_TABLE_NAME":
        assert len(logger.handlers) == 1
 
    logger.setLevel(log_level)
    json_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    json_handler.setFormatter(formatter)
    logger.addHandler(json_handler)
    logger.removeHandler(logger.handlers[0])


def increment_visit_count(website):
    """
    Parameters
    ----------
    website: string, required

    Returns
    -------
    Return value from DynamoDB update item operation with new count: dict
    """
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
        setup_logging(logging.INFO)
        logger = logging.getLogger()
        data = json.loads(event["body"])

        if "Website" in data and not isinstance(data["Website"], str):
            raise ValueError

        logger.info(data["Website"])

        update_item = increment_visit_count(data["Website"])

        logger.info(update_item["Attributes"]["Visit_Count"])

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
