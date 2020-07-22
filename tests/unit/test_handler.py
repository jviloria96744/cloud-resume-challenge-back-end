import json
import pytest


@pytest.fixture
def mock_environment_variables(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-west-2")
    monkeypatch.setenv("TABLE_NAME", "WebsiteVisitCounts")


event_fixed_items = {
    "resource": "/{proxy+}",
    "requestContext": {
        "resourceId": "123456",
        "apiId": "1234567890",
        "resourcePath": "/{proxy+}",
        "httpMethod": "POST",
        "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
        "accountId": "123456789012",
        "identity": {
            "apiKey": "",
            "userArn": "",
            "cognitoAuthenticationType": "",
            "caller": "",
            "userAgent": "Custom User Agent String",
            "user": "",
            "cognitoIdentityPoolId": "",
            "cognitoIdentityId": "",
            "cognitoAuthenticationProvider": "",
            "sourceIp": "127.0.0.1",
            "accountId": "",
        },
        "stage": "prod",
    },
    "queryStringParameters": {"foo": "bar"},
    "headers": {
        "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
        "Accept-Language": "en-US,en;q=0.8",
        "CloudFront-Is-Desktop-Viewer": "true",
        "CloudFront-Is-SmartTV-Viewer": "false",
        "CloudFront-Is-Mobile-Viewer": "false",
        "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
        "CloudFront-Viewer-Country": "US",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "X-Forwarded-Port": "443",
        "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
        "X-Forwarded-Proto": "https",
        "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
        "CloudFront-Is-Tablet-Viewer": "false",
        "Cache-Control": "max-age=0",
        "User-Agent": "Custom User Agent String",
        "CloudFront-Forwarded-Proto": "https",
        "Accept-Encoding": "gzip, deflate, sdch",
    },
    "pathParameters": {"proxy": "/examplepath"},
    "httpMethod": "POST",
    "stageVariables": {"baz": "qux"},
    "path": "/examplepath",
}

test_cases = [
    ('{\"message\": \"test\"}', {'status_code': 400, 'test_key': 'error', 'test_type': str}),
    ('{\"Website\": 1}', {'status_code': 400, 'test_key': 'error', 'test_type': str}),
    ('{\"Website\": \"Pytest\"}', {'status_code': 200, 'test_key': 'count', 'test_type': int})
]
@pytest.mark.parametrize("body, expected", test_cases)
def test_lambda_handler(body, expected, mock_environment_variables):
    """
    Run test cases for ValueError, KeyError and Success Scenario
    """
    from cloud_resume_counter import app
    test_body = {"body": body, **event_fixed_items}
    ret = app.lambda_handler(test_body, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] != expected["status_code"]
    assert isinstance(data[expected["test_key"]], expected["test_type"])