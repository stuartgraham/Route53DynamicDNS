# Dynamic DNS Update
Dynamically update DNS record of your choice with current public facing IP address

Supported providers:
AWS Route 53

## AWS Route 53
### Environment variables
Pass the following environment vairables to execution environment
```sh
RUNMINS=1                               #RUN EVER X MINUTES
PROVIDER=ROUTE53                        #PROVIDER
AWS_ACCESS_KEY_ID=AKIA3MYACCESSKEY      #IAM CREDENTIALS ACCESS KEY
AWS_SECRET_ACCESS_KEY=MYSECRETKEY       #IAM CREDENTIALS SECRET
ROUTE53_HOSTED_ZONE_ID=ABCD1234         #IAM CREDENTIALS ACCESS KEY
RECORD_NAME=helloworld.test.local       #RECORD TO UPDATE
RECORD_TYPE=A                           #RECORD TYPE
RECORD_TTL=300                          #RECORD TTL
```

### IAM Policy
Attach the following IAM policy to your AWS User
```sh
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Allows Upsert of record",
            "Effect": "Allow",
            "Action": "route53:ChangeResourceRecordSets",
            "Resource": "arn:aws:route53:::hostedzone/*"
        }
    ]
}
