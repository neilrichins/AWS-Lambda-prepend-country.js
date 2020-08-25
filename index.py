import logging
import io
import boto3

logging.root.setLevel("INFO")

S3 = boto3.client("s3")


def handler(event, contex):
    logging.info("Running")
    record = event["Records"][0]["cf"]
    request = record["request"]
    headers = request["headers"]
    origin = request["origin"]["custom"]
    domain_name = origin["domainName"]
    path = origin.get("path", "")
    uri = request["uri"]
    
    s3_bucket = domain_name.split(".")[0]
    s3_key = (path + uri).lstrip("/")
    logging.info({"s3_bucket": s3_bucket, "s3_key": s3_key})
    
    
    try:
        response = S3.get_object(Bucket=s3_bucket, Key=s3_key)
    except:
        return {"status": 404, "statusDescription": "File not found"}
    content = response["Body"].read().decode(errors="ignore")
    
    country = headers.get("cloudfront-viewer-country", [{"value": "??"}])[0]["value"]
    
    body = f'var countryCode = "{country}";\n\n{content}'

    response = {
        "status": '200',
        "statusDescription": 'OK',
        "country": country,
        "headers": {
            'cache-control': [{
                "key": 'Cache-Control',
                "value": 'max-age=86400',
                'access-control-allow-origin': [{ "key": 'Access-Control-Allow-Origin', "value": '*' }],
                'content-type': [{ "key": 'Content-Type', "value": 'text/javascript;charset=UTF-8' }],
            }]
        },
        "body": body,
    }

    return response
