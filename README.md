# AWS-Lambda-prepend-country.js
AWS lambda script to prepend javascript .js files with the varible countryCode two letter country code identifier.

If the country can't be found, countryCode is set to "??"
```
var countryCode = "??";
```

To use this script, create a python lambda function in an AWS region that supports cloudfront edge lambda scripts. ex: us-east-1 

Be sure to use an execution role that has access to Cloudwatch Logs
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:*:*:*"
            ]
        }
    ]
}
```
Update the contents of index.py in the Lmabda function from this repository

Publish the code 

Copy the aws arn from the published lambda function.  arn:aws:lambda:.......

Create a CloudFront distribution with the source comming from your S3 bucket containing your .js java scripts

In the CloudFront behaviour whitelist the header CloudFront-Viewer-Country 

At the bottom of the CloudFront behaviour page, Lambda Function Associations

  Set CloudFront Event to  Origin Request
  
  Set CloudFront Lambda Function ARN to the ARN you copied from your published lambda function
  
  Check Include Body


Then click Yes,Edit to save

Before testing be sure to invalidate any caching you have in cloudfront and your browser.

All files viewed through the Cloudfront distrobution ending with .js should now be prepended with a var countryCode = and a two letter country code.
